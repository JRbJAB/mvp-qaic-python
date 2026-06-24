from __future__ import annotations

import argparse
import csv
import json
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


SAFETY_FLAGS: dict[str, bool] = {
    "gem_call_executed": False,
    "google_sheets_write": False,
    "live_google_api_call_from_python": False,
    "apps_script_execution": False,
    "clasp_push": False,
    "public_serve": False,
    "broker": False,
    "order": False,
    "sizing": False,
    "auto_apply_gem_response": False,
    "source_prompt_modified": False,
}


def _utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def _stamp() -> str:
    return datetime.now().strftime("%Y%m%d_%H%M%S")


def _extract_json_candidate(text: str) -> tuple[dict[str, Any] | None, str]:
    stripped = text.strip()
    if stripped.startswith("{") and stripped.endswith("}"):
        try:
            parsed = json.loads(stripped)
            return parsed if isinstance(parsed, dict) else None, "FULL_JSON"
        except json.JSONDecodeError:
            pass

    fenced = re.search(r"```(?:json)?\s*(\{.*?\})\s*```", text, flags=re.DOTALL | re.IGNORECASE)
    if fenced:
        try:
            parsed = json.loads(fenced.group(1))
            return parsed if isinstance(parsed, dict) else None, "FENCED_JSON"
        except json.JSONDecodeError:
            pass

    first = text.find("{")
    last = text.rfind("}")
    if first >= 0 and last > first:
        try:
            parsed = json.loads(text[first : last + 1])
            return parsed if isinstance(parsed, dict) else None, "EMBEDDED_JSON"
        except json.JSONDecodeError:
            pass

    return None, "NO_VALID_JSON"


def _flatten_keys(payload: Any, prefix: str = "") -> set[str]:
    keys: set[str] = set()
    if isinstance(payload, dict):
        for key, value in payload.items():
            name = f"{prefix}.{key}" if prefix else str(key)
            keys.add(name)
            keys.update(_flatten_keys(value, name))
    elif isinstance(payload, list):
        for index, value in enumerate(payload[:20]):
            keys.update(_flatten_keys(value, f"{prefix}[{index}]"))
    return keys


def parse_gem_response_text(text: str, *, source_name: str = "inline") -> dict[str, Any]:
    json_payload, extraction_mode = _extract_json_candidate(text)
    lower = text.lower()
    keys = _flatten_keys(json_payload) if json_payload else set()

    has_review_required = "review_required" in lower
    has_image_used = (
        "image_used" in lower or "image_used" in keys or "image_usage_evidence" in lower
    )
    has_no_order = "no_order" in lower or "aucun ordre" in lower or '"order": false' in lower
    has_no_sizing = "no_sizing" in lower or "aucun sizing" in lower or '"sizing": false' in lower
    has_auto_apply_block = "auto_apply" in lower or "no_auto_apply" in lower
    has_reference_currency = "reference_currency" in keys or "reference_currency" in lower
    has_missing_data = any("missing_data" in key for key in keys) or "missing_data" in lower
    has_blockers = any("blocker" in key.lower() for key in keys) or "blockers" in lower

    blockers: list[str] = []
    warnings: list[str] = []

    if extraction_mode == "NO_VALID_JSON":
        warnings.append("NO_VALID_JSON_FOUND")
    if not has_review_required:
        warnings.append("REVIEW_REQUIRED_NOT_EXPLICIT")
    if not has_image_used:
        warnings.append("IMAGE_USED_NOT_EXPLICIT")
    if not has_no_order:
        blockers.append("NO_ORDER_SAFETY_MARKER_MISSING")
    if not has_no_sizing:
        blockers.append("NO_SIZING_SAFETY_MARKER_MISSING")
    if not has_auto_apply_block:
        warnings.append("AUTO_APPLY_BLOCK_NOT_EXPLICIT")
    if not has_reference_currency:
        warnings.append("REFERENCE_CURRENCY_NOT_EXPLICIT")
    if not has_missing_data:
        warnings.append("MISSING_DATA_FIELD_NOT_EXPLICIT")
    if not has_blockers:
        warnings.append("BLOCKERS_FIELD_NOT_EXPLICIT")

    review_status = "VALIDATED_FOR_HUMAN_REVIEW" if not blockers else "REVIEW_REQUIRED"

    return {
        "source_name": source_name,
        "extraction_mode": extraction_mode,
        "json_found": json_payload is not None,
        "json_payload": json_payload,
        "json_key_count": len(keys),
        "has_review_required": has_review_required,
        "has_image_used": has_image_used,
        "has_no_order": has_no_order,
        "has_no_sizing": has_no_sizing,
        "has_auto_apply_block": has_auto_apply_block,
        "has_reference_currency": has_reference_currency,
        "has_missing_data": has_missing_data,
        "has_blockers": has_blockers,
        "review_status": review_status,
        "human_review_required": True,
        "apply_allowed": False,
        "blocker_count": len(blockers),
        "warning_count": len(warnings),
        "blockers": blockers,
        "warnings": warnings,
        **SAFETY_FLAGS,
    }


def _response_dir(root: Path) -> Path:
    folder = root / "00_OPERATOR_EXPORTS" / "P181_GEM_RESPONSES"
    folder.mkdir(parents=True, exist_ok=True)
    return folder


def _session_dir(root: Path) -> Path:
    folder = root / "00_OPERATOR_EXPORTS" / "P181_SESSION_LOG"
    folder.mkdir(parents=True, exist_ok=True)
    return folder


def _latest_response_files(root: Path, limit: int = 30) -> list[Path]:
    allowed = {".json", ".md", ".txt"}
    files: list[Path] = []
    for path in _response_dir(root).glob("*"):
        if not path.is_file():
            continue
        if path.name.lower() == "desktop.ini":
            continue
        if path.suffix.lower() not in allowed:
            continue
        files.append(path)
    return sorted(files, key=lambda item: item.stat().st_mtime, reverse=True)[:limit]


def build_real_gem_session_review(
    project_root: str | Path,
    *,
    generated_at: str | None = None,
) -> dict[str, Any]:
    root = Path(project_root)
    responses = _latest_response_files(root)

    parsed = [
        parse_gem_response_text(
            path.read_text(encoding="utf-8", errors="replace"),
            source_name=path.name,
        )
        for path in responses
    ]

    return {
        "STATUS": "OK_P184_REAL_GEM_SESSION_REVIEW_RESPONSE_PARSER_READY",
        "generated_at": generated_at or _utc_now(),
        "project_root": str(root),
        "response_dir": str(_response_dir(root)),
        "session_dir": str(_session_dir(root)),
        "parser_ready": True,
        "response_file_count": len(responses),
        "parsed_response_count": len(parsed),
        "blocking_count": sum(row["blocker_count"] for row in parsed),
        "warning_count": sum(row["warning_count"] for row in parsed),
        "has_real_response_ready": len(parsed) > 0,
        "review_status": "WAITING_REAL_GEM_RESPONSE" if not parsed else "REVIEW_REQUIRED",
        "parsed_responses": parsed,
        "blocker_count": 0,
        "blockers": [],
        **SAFETY_FLAGS,
        "recommended_next": "P185_REAL_OPERATOR_CAPTURE_RESPONSE_UI_ROUNDTRIP",
    }


def export_real_gem_session_review(
    project_root: str | Path,
    *,
    export_dir: str | Path | None = None,
) -> dict[str, Any]:
    root = Path(project_root)
    export_path = (
        Path(export_dir)
        if export_dir is not None
        else root / "05_EXPORTS" / f"P184_REAL_GEM_SESSION_REVIEW_RESPONSE_PARSER_{_stamp()}"
    )
    export_path.mkdir(parents=True, exist_ok=True)

    payload = build_real_gem_session_review(root)
    payload["export_dir"] = str(export_path)

    (export_path / "P184_REAL_GEM_SESSION_REVIEW.json").write_text(
        json.dumps(payload, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )

    summary_keys = [
        "STATUS",
        "generated_at",
        "project_root",
        "export_dir",
        "parser_ready",
        "response_file_count",
        "parsed_response_count",
        "blocking_count",
        "warning_count",
        "has_real_response_ready",
        "review_status",
        "blocker_count",
        "blockers",
        "gem_call_executed",
        "google_sheets_write",
        "live_google_api_call_from_python",
        "apps_script_execution",
        "clasp_push",
        "public_serve",
        "broker",
        "order",
        "sizing",
        "auto_apply_gem_response",
        "source_prompt_modified",
        "recommended_next",
    ]
    summary = {key: payload[key] for key in summary_keys}
    (export_path / "P184_SUMMARY.json").write_text(
        json.dumps(summary, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )

    csv_path = export_path / "P184_PARSED_RESPONSES.csv"
    with csv_path.open("w", encoding="utf-8", newline="") as file_obj:
        writer = csv.DictWriter(
            file_obj,
            fieldnames=[
                "source_name",
                "extraction_mode",
                "json_found",
                "review_status",
                "blocker_count",
                "warning_count",
                "has_review_required",
                "has_image_used",
                "has_no_order",
                "has_no_sizing",
                "has_auto_apply_block",
            ],
        )
        writer.writeheader()
        for row in payload["parsed_responses"]:
            writer.writerow(
                {
                    "source_name": row["source_name"],
                    "extraction_mode": row["extraction_mode"],
                    "json_found": row["json_found"],
                    "review_status": row["review_status"],
                    "blocker_count": row["blocker_count"],
                    "warning_count": row["warning_count"],
                    "has_review_required": row["has_review_required"],
                    "has_image_used": row["has_image_used"],
                    "has_no_order": row["has_no_order"],
                    "has_no_sizing": row["has_no_sizing"],
                    "has_auto_apply_block": row["has_auto_apply_block"],
                }
            )

    report = [
        "# P184 Real GEM Session Review And Response Parser",
        "",
        f"- STATUS: {payload['STATUS']}",
        f"- parser_ready: {payload['parser_ready']}",
        f"- response_file_count: {payload['response_file_count']}",
        f"- parsed_response_count: {payload['parsed_response_count']}",
        f"- has_real_response_ready: {payload['has_real_response_ready']}",
        f"- review_status: {payload['review_status']}",
        "",
        "Safety:",
        "- GEM_CALL_EXECUTED=False",
        "- AUTO_APPLY_GEM_RESPONSE=False",
        "- SOURCE_PROMPT_MODIFIED=False",
        "- GOOGLE_SHEETS_WRITE=False",
        "- LIVE_GOOGLE_API_CALL_FROM_PYTHON=False",
        "- APPS_SCRIPT_EXECUTION=False",
        "- CLASP_PUSH=False",
        "- PUBLIC_SERVE=False",
        "- BROKER=False",
        "- ORDER=False",
        "- SIZING=False",
        "",
        "Next:",
        "- P185_REAL_OPERATOR_CAPTURE_RESPONSE_UI_ROUNDTRIP",
    ]
    (export_path / "P184_REAL_GEM_SESSION_REVIEW_REPORT.md").write_text(
        "\n".join(report) + "\n",
        encoding="utf-8",
    )
    return payload


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="P184 real GEM session review parser.")
    parser.add_argument("--project-root", default=".")
    parser.add_argument("--export-dir", default=None)
    parser.add_argument("--write-export", action="store_true")
    parser.add_argument("--json", action="store_true")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = _build_parser().parse_args(argv)
    payload = (
        export_real_gem_session_review(args.project_root, export_dir=args.export_dir)
        if args.write_export
        else build_real_gem_session_review(args.project_root)
    )

    if args.json:
        print(json.dumps(payload, indent=2, ensure_ascii=False))
    else:
        print(payload["STATUS"])
        print(f"PARSER_READY={payload['parser_ready']}")
        print(f"PARSED_RESPONSE_COUNT={payload['parsed_response_count']}")
        print(f"REVIEW_STATUS={payload['review_status']}")

    return 0 if payload["parser_ready"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
