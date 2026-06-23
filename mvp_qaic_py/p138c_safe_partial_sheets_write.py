from __future__ import annotations

import argparse
import csv
import json
import os
import subprocess
import sys
import urllib.error
import urllib.parse
import urllib.request
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


P138C_VERSION = "MVP_QAIC_P138C_SAFE_PARTIAL_SHEETS_WRITE_AFTER_GO_20260623"
DEFAULT_RUN_ID = "P138C-SAFE-PARTIAL-SHEETS-WRITE-AFTER-GO"
EXPLICIT_GO_PHRASE = "GO P138C SAFE PARTIAL WRITE"
SPREADSHEET_ID = "19KY8Y1ozS7ONaJu9_5NQmjO47l-xM798Xm-y1n7fNd0"

CANONICAL_FIELDS: tuple[str, ...] = (
    "migration_id",
    "source_spreadsheet_id",
    "source_tab",
    "source_row",
    "source_hash",
    "prompt_id",
    "base_prompt_id",
    "parent_prompt_id",
    "prompt_family",
    "gem_id",
    "prompt_profile",
    "record_type",
    "status",
    "validation_status",
    "is_reference_locked",
    "raw_prompt_text",
    "prompt_text_field_used",
    "python_simplification_action",
    "p137_correction_status",
    "p133_compatibility_status",
    "target_sheet",
    "target_row_strategy",
    "write_status",
    "human_review_status",
    "blockers",
)

P138C_AUDIT_FIELDS: tuple[str, ...] = (
    "p138c_run_id",
    "p138c_written_at_utc",
    "p138c_write_mode",
    "p138c_source_scope",
    "p138c_explicit_go",
    "migration_status",
)

REQUIRED_TARGET_HEADERS: tuple[str, ...] = (
    "prompt_id",
    "raw_prompt_text",
    "migration_id",
    "source_hash",
    "source_tab",
    "source_row",
    "p138c_run_id",
    "p138c_written_at_utc",
    "migration_status",
)

SAFETY_MARKERS: tuple[str, ...] = (
    "P138C_SAFE_PARTIAL_SHEETS_WRITE_AFTER_EXPLICIT_GO",
    "LIVE_GOOGLE_SHEETS_WRITE",
    "EXPLICIT_GO_REQUIRED",
    "SAFE_PARTIAL_WRITE_READY_SCOPE_ONLY",
    "BLOCKED_ROWS_EXCLUDED_FROM_WRITE",
    "DUPLICATES_REVIEW_EXCLUDED_FROM_WRITE",
    "LOCKED_REFERENCES_PROTECTED",
    "NO_BLIND_OVERWRITE",
    "APPEND_ONLY_OR_SKIP_DUPLICATE",
    "NO_PROMPT_SOURCE_OVERWRITE",
    "NO_BROKER",
    "NO_ORDER",
    "NO_SIZING",
    "NO_AUTO_APPLY_GEM_RESPONSE",
    "HUMAN_REVIEW_REQUIRED",
)


@dataclass(frozen=True)
class P138CRequest:
    p138b3_export_dir: Path
    p138a2_export_dir: Path
    output_dir: Path
    spreadsheet_id: str = SPREADSHEET_ID
    run_id: str = DEFAULT_RUN_ID
    generated_at_utc: str | None = None
    explicit_go: str = ""
    apply: bool = False


def _utc_now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def _ensure_dir(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)


def _read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def _write_json(path: Path, payload: Any) -> None:
    path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=False) + "\n", encoding="utf-8"
    )


def _normalise_blockers(value: Any) -> list[str]:
    if isinstance(value, list):
        return [str(item) for item in value if str(item).strip()]
    text = str(value or "").strip()
    if not text:
        return []
    return [part.strip() for part in text.split("|") if part.strip()]


def _as_bool(value: Any) -> bool:
    if isinstance(value, bool):
        return value
    return str(value or "").strip().lower() in {"true", "1", "yes", "y", "oui"}


def load_scope_and_candidates(
    p138b3_export_dir: Path, p138a2_export_dir: Path
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    safe_path = p138b3_export_dir / "P138B3_SAFE_PARTIAL_WRITE_READY.json"
    candidate_path = p138a2_export_dir / "P138A_MIGRATION_CANDIDATES.json"
    if not safe_path.exists():
        raise FileNotFoundError(f"Missing safe scope JSON: {safe_path}")
    if not candidate_path.exists():
        raise FileNotFoundError(f"Missing P138A candidates JSON: {candidate_path}")
    safe_rows = _read_json(safe_path)
    candidates = _read_json(candidate_path)
    if not isinstance(safe_rows, list):
        raise ValueError("P138B3 safe scope must be a list")
    if not isinstance(candidates, list):
        raise ValueError("P138A candidates must be a list")
    return [dict(row) for row in safe_rows], [dict(row) for row in candidates]


def rehydrate_safe_candidates(
    safe_rows: list[dict[str, Any]], candidates: list[dict[str, Any]]
) -> list[dict[str, Any]]:
    by_migration_id = {str(row.get("migration_id") or ""): dict(row) for row in candidates}
    by_source_hash = {str(row.get("source_hash") or ""): dict(row) for row in candidates}
    hydrated: list[dict[str, Any]] = []

    for safe in safe_rows:
        migration_id = str(safe.get("migration_id") or "")
        source_hash = str(safe.get("source_hash") or "")
        candidate = by_migration_id.get(migration_id) or by_source_hash.get(source_hash)
        if not candidate:
            raise ValueError(f"Could not rehydrate safe candidate: {migration_id} / {source_hash}")

        blockers = _normalise_blockers(candidate.get("blockers")) + _normalise_blockers(
            safe.get("blockers")
        )
        if blockers:
            raise ValueError(f"Safe candidate unexpectedly has blockers: {migration_id} {blockers}")
        if _as_bool(candidate.get("is_reference_locked")) or _as_bool(
            safe.get("protect_locked_reference")
        ):
            raise ValueError(f"Safe candidate unexpectedly locked reference: {migration_id}")
        if not _as_bool(safe.get("p138c_allowed_after_go")):
            raise ValueError(f"Safe candidate not allowed after GO: {migration_id}")
        if not _as_bool(safe.get("p138b_write_ready")):
            raise ValueError(f"Safe candidate not write-ready: {migration_id}")

        merged = dict(candidate)
        merged.update(
            {
                "p138b_decision": safe.get("p138b_decision"),
                "p138b_write_action": safe.get("p138b_write_action"),
                "p138b_write_ready": True,
                "p138c_allowed_after_go": True,
                "p138b3_bucket": safe.get("p138b3_bucket", "SAFE_PARTIAL_WRITE_READY"),
            }
        )
        hydrated.append(merged)

    return hydrated


def required_output_headers(existing_headers: list[str]) -> list[str]:
    headers = [header for header in existing_headers if str(header).strip()]
    for field in CANONICAL_FIELDS + P138C_AUDIT_FIELDS:
        if field not in headers:
            headers.append(field)
    for field in REQUIRED_TARGET_HEADERS:
        if field not in headers:
            headers.append(field)
    return headers


def build_row_for_headers(
    candidate: dict[str, Any],
    headers: list[str],
    *,
    run_id: str,
    written_at_utc: str,
    explicit_go: str,
) -> list[str]:
    row: dict[str, Any] = dict(candidate)
    raw_prompt = str(row.get("raw_prompt_text") or "")
    text_field = str(row.get("prompt_text_field_used") or "")

    # Preserve old cockpit columns when present.
    if text_field and text_field not in row:
        row[text_field] = raw_prompt
    if "prompt_detail" not in row:
        row["prompt_detail"] = raw_prompt
    if "prompt_template_to_copy" not in row:
        row["prompt_template_to_copy"] = raw_prompt
    if "gem_profile" not in row:
        row["gem_profile"] = row.get("gem_id", "")
    if "ai_runtime_name" not in row:
        row["ai_runtime_name"] = row.get("gem_id", "")

    row["write_status"] = "P138C_SAFE_PARTIAL_WRITTEN"
    row["human_review_status"] = "P138C_SAFE_PARTIAL_GO"
    row["p138c_run_id"] = run_id
    row["p138c_written_at_utc"] = written_at_utc
    row["p138c_write_mode"] = "SAFE_PARTIAL_APPEND_ONLY_OR_SKIP_DUPLICATE"
    row["p138c_source_scope"] = "P138B3_SAFE_PARTIAL_WRITE_READY"
    row["p138c_explicit_go"] = explicit_go
    row["migration_status"] = "MIGRATED_BY_P138C_SAFE_PARTIAL"

    if isinstance(row.get("blockers"), list):
        row["blockers"] = " | ".join(str(item) for item in row.get("blockers") or [])

    values = []
    for header in headers:
        value = row.get(header, "")
        if isinstance(value, bool):
            value = "TRUE" if value else "FALSE"
        elif isinstance(value, (list, tuple)):
            value = " | ".join(str(item) for item in value)
        elif value is None:
            value = ""
        else:
            value = str(value)
        values.append(value)
    return values


def quote_sheet_range(sheet_name: str, a1: str) -> str:
    return f"'{sheet_name.replace(chr(39), chr(39) * 2)}'!{a1}"


def col_to_a1(index_1_based: int) -> str:
    if index_1_based < 1:
        raise ValueError("Column index must be >= 1")
    n = index_1_based
    letters = ""
    while n:
        n, rem = divmod(n - 1, 26)
        letters = chr(65 + rem) + letters
    return letters


def get_access_token(repo_root: Path | None = None) -> str:
    diagnostics: list[str] = []

    for env_name in ("MVP_QAIC_GOOGLE_ACCESS_TOKEN", "GOOGLE_OAUTH_ACCESS_TOKEN"):
        token = os.environ.get(env_name)
        if token:
            diagnostics.append(f"{env_name}=FOUND")
            return token.strip()
        diagnostics.append(f"{env_name}=MISSING")

    gcloud_commands = (
        ("gcloud", "auth", "print-access-token"),
        ("gcloud", "auth", "application-default", "print-access-token"),
    )
    for command in gcloud_commands:
        try:
            completed = subprocess.run(
                list(command),
                check=True,
                capture_output=True,
                text=True,
                timeout=30,
            )
            token = completed.stdout.strip()
            if token:
                diagnostics.append(" ".join(command) + "=OK")
                return token
            diagnostics.append(" ".join(command) + "=EMPTY")
        except Exception as exc:
            diagnostics.append(" ".join(command) + f"=FAILED:{type(exc).__name__}")

    candidate_paths: list[Path] = []
    for env_name in ("MVP_QAIC_GOOGLE_TOKEN_JSON", "GOOGLE_TOKEN_JSON"):
        value = os.environ.get(env_name)
        if value:
            candidate_paths.append(Path(value))
            diagnostics.append(f"{env_name}=FOUND:{value}")
        else:
            diagnostics.append(f"{env_name}=MISSING")

    if repo_root:
        candidate_paths.extend(
            [
                repo_root / "token.json",
                repo_root / ".secrets" / "token.json",
                repo_root / "secrets" / "token.json",
                repo_root / "02_AUTH" / "token.json",
            ]
        )
    appdata = os.environ.get("APPDATA")
    userprofile = os.environ.get("USERPROFILE")
    if appdata:
        candidate_paths.append(Path(appdata) / "gcloud" / "application_default_credentials.json")
    if userprofile:
        candidate_paths.extend(
            [
                Path(userprofile) / ".config" / "gcloud" / "application_default_credentials.json",
                Path(userprofile) / ".credentials" / "mvp_qaic_token.json",
            ]
        )

    seen: set[str] = set()
    for path in candidate_paths:
        key = str(path)
        if key in seen:
            continue
        seen.add(key)
        if not path.exists():
            diagnostics.append(f"TOKEN_JSON_MISSING:{path}")
            continue
        try:
            token = _access_token_from_token_json(path)
            if token:
                diagnostics.append(f"TOKEN_JSON_OK:{path}")
                return token
            diagnostics.append(f"TOKEN_JSON_EMPTY:{path}")
        except Exception as exc:
            diagnostics.append(f"TOKEN_JSON_FAILED:{path}:{type(exc).__name__}:{exc}")
            continue

    raise RuntimeError(
        "No valid Google access token found. Diagnostics: "
        + " ; ".join(diagnostics)
        + " ; Fix: run `gcloud auth login --update-adc --scopes=https://www.googleapis.com/auth/spreadsheets,https://www.googleapis.com/auth/drive` "
        + "or set MVP_QAIC_GOOGLE_ACCESS_TOKEN from `gcloud auth print-access-token`."
    )


def _access_token_from_token_json(path: Path) -> str | None:
    payload = _read_json(path)
    access_token = str(payload.get("access_token") or "").strip()
    if access_token and not payload.get("refresh_token"):
        return access_token

    refresh_token = str(payload.get("refresh_token") or "").strip()
    client_id = str(payload.get("client_id") or "").strip()
    client_secret = str(payload.get("client_secret") or "").strip()
    token_uri = str(payload.get("token_uri") or "https://oauth2.googleapis.com/token").strip()
    if not (refresh_token and client_id and client_secret):
        return access_token or None

    data = urllib.parse.urlencode(
        {
            "client_id": client_id,
            "client_secret": client_secret,
            "refresh_token": refresh_token,
            "grant_type": "refresh_token",
        }
    ).encode("utf-8")
    request = urllib.request.Request(
        token_uri,
        data=data,
        headers={"Content-Type": "application/x-www-form-urlencoded"},
        method="POST",
    )
    with urllib.request.urlopen(request, timeout=30) as response:
        result = json.loads(response.read().decode("utf-8"))
    return str(result.get("access_token") or "").strip() or None


def _http_json(
    method: str,
    url: str,
    *,
    token: str,
    payload: dict[str, Any] | None = None,
) -> dict[str, Any]:
    body = None
    headers = {"Authorization": f"Bearer {token}"}
    if payload is not None:
        body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        headers["Content-Type"] = "application/json; charset=utf-8"
    request = urllib.request.Request(url, data=body, headers=headers, method=method)
    try:
        with urllib.request.urlopen(request, timeout=60) as response:
            content = response.read().decode("utf-8")
            return json.loads(content) if content else {}
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"Google Sheets API HTTP {exc.code}: {detail}") from exc


def sheets_api_url(path: str, params: dict[str, str] | None = None) -> str:
    base = f"https://sheets.googleapis.com/v4/spreadsheets/{path}"
    if params:
        base += "?" + urllib.parse.urlencode(params)
    return base


def get_spreadsheet_metadata(spreadsheet_id: str, token: str) -> dict[str, Any]:
    return _http_json(
        "GET",
        sheets_api_url(
            spreadsheet_id,
            {"fields": "sheets(properties(sheetId,title,gridProperties(rowCount,columnCount)))"},
        ),
        token=token,
    )


def find_sheet(metadata: dict[str, Any], title: str) -> dict[str, Any] | None:
    for sheet in metadata.get("sheets", []):
        props = sheet.get("properties", {})
        if props.get("title") == title:
            return sheet
    return None


def values_get(spreadsheet_id: str, token: str, range_a1: str) -> list[list[str]]:
    url = sheets_api_url(
        f"{spreadsheet_id}/values/{urllib.parse.quote(range_a1, safe='')}",
        {"majorDimension": "ROWS", "valueRenderOption": "FORMATTED_VALUE"},
    )
    payload = _http_json("GET", url, token=token)
    return payload.get("values", [])


def values_update(
    spreadsheet_id: str,
    token: str,
    range_a1: str,
    values: list[list[Any]],
    *,
    value_input_option: str = "USER_ENTERED",
) -> dict[str, Any]:
    url = sheets_api_url(
        f"{spreadsheet_id}/values/{urllib.parse.quote(range_a1, safe='')}",
        {"valueInputOption": value_input_option},
    )
    return _http_json(
        "PUT",
        url,
        token=token,
        payload={"range": range_a1, "majorDimension": "ROWS", "values": values},
    )


def batch_update(spreadsheet_id: str, token: str, requests: list[dict[str, Any]]) -> dict[str, Any]:
    return _http_json(
        "POST",
        sheets_api_url(f"{spreadsheet_id}:batchUpdate"),
        token=token,
        payload={"requests": requests},
    )


def ensure_grid_capacity(
    spreadsheet_id: str,
    token: str,
    *,
    sheet_id: int,
    current_rows: int,
    current_cols: int,
    required_rows: int,
    required_cols: int,
) -> None:
    requests: list[dict[str, Any]] = []
    if required_cols > current_cols:
        requests.append(
            {
                "appendDimension": {
                    "sheetId": sheet_id,
                    "dimension": "COLUMNS",
                    "length": required_cols - current_cols,
                }
            }
        )
    if required_rows > current_rows:
        requests.append(
            {
                "appendDimension": {
                    "sheetId": sheet_id,
                    "dimension": "ROWS",
                    "length": required_rows - current_rows,
                }
            }
        )
    if requests:
        batch_update(spreadsheet_id, token, requests)


def detect_header_row(values: list[list[str]]) -> tuple[int, list[str]]:
    for index, row in enumerate(values, start=1):
        normalized = [str(cell).strip() for cell in row]
        if "prompt_id" in normalized:
            return index, normalized
    if values:
        return 1, [str(cell).strip() for cell in values[0]]
    return 1, []


def write_backup_csv(path: Path, values: list[list[str]]) -> None:
    with path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.writer(handle)
        writer.writerows(values)


def make_safe_partial_write_plan(
    request: P138CRequest,
    *,
    written_at_utc: str,
) -> dict[str, Any]:
    safe_rows, candidates = load_scope_and_candidates(
        request.p138b3_export_dir, request.p138a2_export_dir
    )
    hydrated = rehydrate_safe_candidates(safe_rows, candidates)
    grouped: dict[str, list[dict[str, Any]]] = {}
    for candidate in hydrated:
        target_sheet = str(candidate.get("target_sheet") or "📘 PROMPT_LIBRARY")
        grouped.setdefault(target_sheet, []).append(candidate)

    return {
        "step": "P138C_SAFE_PARTIAL_SHEETS_WRITE_AFTER_GO",
        "version": P138C_VERSION,
        "status": "P138C_PREFLIGHT_READY" if not request.apply else "P138C_APPLY_REQUESTED",
        "run_id": request.run_id,
        "generated_at_utc": written_at_utc,
        "spreadsheet_id": request.spreadsheet_id,
        "source_p138b3_export_dir": str(request.p138b3_export_dir),
        "source_p138a2_export_dir": str(request.p138a2_export_dir),
        "safe_candidate_count": len(hydrated),
        "target_sheets": {sheet: len(rows) for sheet, rows in grouped.items()},
        "apply": request.apply,
        "explicit_go_valid": request.explicit_go == EXPLICIT_GO_PHRASE,
        "write_policy": {
            "append_only_or_skip_duplicate": True,
            "no_blind_overwrite": True,
            "blocked_rows_excluded": True,
            "duplicate_rows_excluded": True,
            "locked_references_excluded": True,
        },
        "safety_markers": list(SAFETY_MARKERS),
        "hydrated_candidates": hydrated,
    }


def apply_safe_partial_write(
    request: P138CRequest, *, repo_root: Path | None = None
) -> dict[str, Any]:
    if not request.apply:
        raise ValueError("apply_safe_partial_write requires request.apply=True")
    if request.explicit_go != EXPLICIT_GO_PHRASE:
        raise ValueError(f"Explicit GO mismatch. Expected: {EXPLICIT_GO_PHRASE!r}")

    _ensure_dir(request.output_dir)
    written_at_utc = request.generated_at_utc or _utc_now_iso()
    plan = make_safe_partial_write_plan(request, written_at_utc=written_at_utc)

    token = get_access_token(repo_root=repo_root)
    metadata = get_spreadsheet_metadata(request.spreadsheet_id, token)

    write_results: list[dict[str, Any]] = []
    skipped_duplicates: list[dict[str, Any]] = []
    candidates_by_sheet: dict[str, list[dict[str, Any]]] = {}
    for candidate in plan["hydrated_candidates"]:
        candidates_by_sheet.setdefault(
            str(candidate.get("target_sheet") or "📘 PROMPT_LIBRARY"), []
        ).append(candidate)

    for sheet_name, candidates in candidates_by_sheet.items():
        sheet = find_sheet(metadata, sheet_name)
        if sheet is None:
            raise ValueError(f"Target sheet missing: {sheet_name}")
        props = sheet["properties"]
        sheet_id = int(props["sheetId"])
        grid = props.get("gridProperties", {})
        current_rows = int(grid.get("rowCount") or 1000)
        current_cols = int(grid.get("columnCount") or 26)

        existing_values = values_get(
            request.spreadsheet_id, token, quote_sheet_range(sheet_name, "1:2000")
        )
        backup_name = f"P138C_BACKUP_{_safe_filename(sheet_name)}.csv"
        write_backup_csv(request.output_dir / backup_name, existing_values)

        header_row_idx, existing_headers = detect_header_row(existing_values[:30])
        final_headers = required_output_headers(existing_headers)
        header_map = {header: idx for idx, header in enumerate(final_headers)}
        existing_migration_ids: set[str] = set()
        existing_source_hashes: set[str] = set()

        mig_idx = header_map.get("migration_id")
        hash_idx = header_map.get("source_hash")
        for row in existing_values[header_row_idx:]:
            if mig_idx is not None and mig_idx < len(row) and str(row[mig_idx]).strip():
                existing_migration_ids.add(str(row[mig_idx]).strip())
            if hash_idx is not None and hash_idx < len(row) and str(row[hash_idx]).strip():
                existing_source_hashes.add(str(row[hash_idx]).strip())

        rows_to_append: list[list[str]] = []
        for candidate in candidates:
            migration_id = str(candidate.get("migration_id") or "")
            source_hash = str(candidate.get("source_hash") or "")
            if migration_id in existing_migration_ids or source_hash in existing_source_hashes:
                skipped_duplicates.append(
                    {
                        "target_sheet": sheet_name,
                        "migration_id": migration_id,
                        "source_hash": source_hash,
                        "reason": "ALREADY_WRITTEN_OR_SOURCE_HASH_PRESENT",
                    }
                )
                continue
            rows_to_append.append(
                build_row_for_headers(
                    candidate,
                    final_headers,
                    run_id=request.run_id,
                    written_at_utc=written_at_utc,
                    explicit_go=request.explicit_go,
                )
            )

        required_rows = max(current_rows, len(existing_values) + len(rows_to_append) + 2)
        required_cols = max(current_cols, len(final_headers))
        ensure_grid_capacity(
            request.spreadsheet_id,
            token,
            sheet_id=sheet_id,
            current_rows=current_rows,
            current_cols=current_cols,
            required_rows=required_rows,
            required_cols=required_cols,
        )

        header_end_col = col_to_a1(len(final_headers))
        values_update(
            request.spreadsheet_id,
            token,
            quote_sheet_range(sheet_name, f"A{header_row_idx}:{header_end_col}{header_row_idx}"),
            [final_headers],
        )

        if rows_to_append:
            start_row = max(len(existing_values) + 1, header_row_idx + 1)
            end_row = start_row + len(rows_to_append) - 1
            values_update(
                request.spreadsheet_id,
                token,
                quote_sheet_range(sheet_name, f"A{start_row}:{header_end_col}{end_row}"),
                rows_to_append,
            )

        write_results.append(
            {
                "target_sheet": sheet_name,
                "existing_row_count_before": len(existing_values),
                "header_row": header_row_idx,
                "final_header_count": len(final_headers),
                "rows_requested": len(candidates),
                "rows_written": len(rows_to_append),
                "rows_skipped_duplicates": len(candidates) - len(rows_to_append),
                "backup_file": backup_name,
            }
        )

    report = dict(plan)
    report.pop("hydrated_candidates", None)
    report.update(
        {
            "status": "P138C_SAFE_PARTIAL_WRITE_APPLIED",
            "written_at_utc": written_at_utc,
            "write_results": write_results,
            "skipped_duplicates": skipped_duplicates,
            "total_rows_written": sum(int(item["rows_written"]) for item in write_results),
            "total_rows_skipped_duplicates": len(skipped_duplicates),
        }
    )
    _write_json(request.output_dir / "P138C_LIVE_WRITE_REPORT.json", report)
    return report


def _safe_filename(value: str) -> str:
    return "".join(ch if ch.isalnum() or ch in {"-", "_"} else "_" for ch in value)[:80] or "sheet"


def write_preflight_pack(request: P138CRequest) -> dict[str, Any]:
    _ensure_dir(request.output_dir)
    written_at_utc = request.generated_at_utc or _utc_now_iso()
    plan = make_safe_partial_write_plan(request, written_at_utc=written_at_utc)
    export_plan = dict(plan)
    hydrated = export_plan.pop("hydrated_candidates")
    _write_json(request.output_dir / "P138C_PREFLIGHT_PAYLOAD.json", export_plan)
    _write_json(request.output_dir / "P138C_HYDRATED_SAFE_CANDIDATES.json", hydrated)
    _write_scope_csv(request.output_dir / "P138C_HYDRATED_SAFE_CANDIDATES.csv", hydrated)
    _write_runbook(request.output_dir / "P138C_RUNBOOK.md", export_plan)
    return export_plan


def _write_scope_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    fields = list(CANONICAL_FIELDS) + [
        "p138b_decision",
        "p138b_write_action",
        "p138b3_bucket",
    ]
    with path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        for row in rows:
            out = dict(row)
            if isinstance(out.get("blockers"), list):
                out["blockers"] = " | ".join(str(item) for item in out.get("blockers") or [])
            writer.writerow({field: out.get(field, "") for field in fields})


def _write_runbook(path: Path, payload: dict[str, Any]) -> None:
    lines = [
        "# P138C — Safe Partial Sheets Write",
        "",
        f"Status: `{payload['status']}`",
        f"Safe candidate count: `{payload['safe_candidate_count']}`",
        "",
        "## Target sheets",
        "",
    ]
    for sheet, count in payload["target_sheets"].items():
        lines.append(f"- `{sheet}`: `{count}` rows")
    lines.extend(
        [
            "",
            "## Write rules",
            "",
            "- Explicit GO required.",
            "- Append only or skip duplicate by `migration_id` / `source_hash`.",
            "- No blocked rows.",
            "- No duplicate-review rows.",
            "- No locked-reference overwrite.",
            "- Backup CSV exported before write.",
        ]
    )
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="P138C safe partial Sheets write after explicit GO"
    )
    parser.add_argument("--p138b3-export-dir", type=Path, required=True)
    parser.add_argument("--p138a2-export-dir", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--spreadsheet-id", default=SPREADSHEET_ID)
    parser.add_argument("--run-id", default=DEFAULT_RUN_ID)
    parser.add_argument("--generated-at-utc", default=None)
    parser.add_argument("--explicit-go", default="")
    parser.add_argument("--apply", action="store_true")
    parser.add_argument("--repo-root", type=Path, default=None)
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    request = P138CRequest(
        p138b3_export_dir=args.p138b3_export_dir,
        p138a2_export_dir=args.p138a2_export_dir,
        output_dir=args.output_dir,
        spreadsheet_id=args.spreadsheet_id,
        run_id=args.run_id,
        generated_at_utc=args.generated_at_utc,
        explicit_go=args.explicit_go,
        apply=args.apply,
    )

    preflight = write_preflight_pack(request)
    print(preflight["status"])
    print(f"safe_candidate_count={preflight['safe_candidate_count']}")
    print(
        "target_sheets=" + json.dumps(preflight["target_sheets"], ensure_ascii=True, sort_keys=True)
    )

    if args.apply:
        report = apply_safe_partial_write(request, repo_root=args.repo_root)
        print(report["status"])
        print(f"total_rows_written={report['total_rows_written']}")
        print(f"total_rows_skipped_duplicates={report['total_rows_skipped_duplicates']}")
    else:
        print("apply=false")
    print(f"output_dir={args.output_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
