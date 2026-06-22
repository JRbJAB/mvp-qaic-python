from __future__ import annotations

import argparse
import csv
import hashlib
import json
import re
import sys
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


P138A_VERSION = "MVP_QAIC_P138A_SHEETS_PROMPT_BASE_MIGRATION_CANDIDATE_20260622"
DEFAULT_RUN_ID = "P138A-SHEETS-PROMPT-BASE-MIGRATION-CANDIDATE"

SHEETS_DEV_SPREADSHEET_ID = "19KY8Y1ozS7ONaJu9_5NQmjO47l-xM798Xm-y1n7fNd0"

SOURCE_TABS: tuple[str, ...] = (
    "📘 PROMPT_LIBRARY",
    "🎛️ PROMPT_VARIANT_CONTROL_CENTER",
    "🚀 PROMPT_RUN_QUEUE",
    "🧩 PROMPT_READY_TO_COPY",
    "🧠 PROMPT_CONTEXT_PACKS",
    "🔗 PROMPT_LEXIQUE_BRIDGE",
    "GPT_PROMPT_RUNTIME_SPEC",
    "OUTPUT_TEMPLATES",
    "DATA_REQUIREMENTS",
    "QAIC_OUTPUT_CONTRACT",
    "🤖 AI_RUNTIME_REFERENCE",
)

TARGET_WRITE_TABS_AFTER_VALIDATION: tuple[str, ...] = (
    "📘 PROMPT_LIBRARY",
    "🧩 PROMPT_READY_TO_COPY",
    "🎛️ PROMPT_VARIANT_CONTROL_CENTER",
    "GPT_PROMPT_RUNTIME_SPEC",
    "QAIC_OUTPUT_CONTRACT",
)

PROMPT_TEXT_FIELDS: tuple[str, ...] = (
    "prompt_template_to_copy",
    "prompt_detail",
    "original_prompt_template",
    "ultimate_reference_prompt",
    "future_output_format",
    "notes",
)

SAFETY_MARKERS: tuple[str, ...] = (
    "P138A_SHEETS_PROMPT_BASE_MIGRATION_CANDIDATE",
    "READ_OLD_SHEETS_BASE_FIRST",
    "PYTHON_ULTIMATE_PROCESS_SIMPLIFICATION",
    "PYTHON_OPTIMIZES_ORIGIN_SHEETS_PROCESS",
    "ONE_CANONICAL_PROMPT_REGISTRY",
    "ONE_VALIDATION_GATE",
    "ONE_SHEETS_WRITE_PLAN_AFTER_VALIDATION",
    "NO_SHEETS_WRITE_IN_P138A",
    "WRITE_IN_SHEETS_ONLY_AFTER_VALIDATION_GO",
    "NO_PROMPT_SOURCE_OVERWRITE",
    "NO_BROKER",
    "NO_ORDER",
    "NO_SIZING",
    "NO_AUTO_APPLY_GEM_RESPONSE",
    "HUMAN_REVIEW_REQUIRED",
)


@dataclass(frozen=True)
class P138ARequest:
    output_dir: Path = Path("05_EXPORTS/P138A_SHEETS_PROMPT_BASE_MIGRATION_CANDIDATE")
    csv_dir: Path | None = None
    spreadsheet_id: str = SHEETS_DEV_SPREADSHEET_ID
    run_id: str = DEFAULT_RUN_ID
    generated_at_utc: str | None = None


@dataclass(frozen=True)
class PromptMigrationCandidate:
    migration_id: str
    source_spreadsheet_id: str
    source_tab: str
    source_row: int
    source_hash: str
    prompt_id: str
    base_prompt_id: str | None
    parent_prompt_id: str | None
    prompt_family: str | None
    gem_id: str
    prompt_profile: str | None
    record_type: str | None
    status: str | None
    validation_status: str | None
    is_reference_locked: bool
    raw_prompt_text: str
    prompt_text_field_used: str | None
    python_simplification_action: str
    p137_correction_status: str
    p133_compatibility_status: str
    target_sheet: str
    target_row_strategy: str
    write_status: str
    human_review_status: str
    blockers: tuple[str, ...]


def _utc_now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def _ensure_dir(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)


def _sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def _slug(value: str) -> str:
    value = value.strip().lower()
    value = re.sub(r"[^a-z0-9]+", "_", value)
    value = re.sub(r"_+", "_", value).strip("_")
    return value or "unknown"


def _safe_cell(row: dict[str, Any], key: str) -> str:
    value = row.get(key)
    if value is None:
        return ""
    return str(value).strip()


def _truthy(value: str | None) -> bool:
    return str(value or "").strip().upper() in {"YES", "TRUE", "1", "Y", "OUI", "LOCKED"}


def canonical_prompt_registry_fields() -> list[str]:
    return [
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
    ]


def build_process_simplification_spec() -> dict[str, Any]:
    return {
        "status": "PYTHON_ULTIMATE_PROCESS_SIMPLIFICATION_READY",
        "objective": "Remplacer le process Sheets fragmenté par une migration Python canonique, validée, puis écrite dans Sheets après GO.",
        "origin_process_problems": [
            "prompts répartis dans plusieurs onglets",
            "variantes, queues, runtime specs et output contracts séparés",
            "risque de corriger le mauvais prompt",
            "historique utile mais difficile à exploiter directement",
            "write Sheets dangereux sans provenance, hash, validation et plan ligne par ligne",
        ],
        "python_target_process": [
            "read old Sheets base once",
            "normalize all source tabs into one canonical registry",
            "hash every source row and prompt body",
            "deduplicate references and variants",
            "preserve locked reference prompts",
            "apply P137 corrections as local candidate, not as blind overwrite",
            "build a deterministic Sheets write plan",
            "block write until validation GO",
            "write to Sheets with run_id/source_hash/migration_status only after approval",
        ],
        "ultimate_simplification_rules": {
            "single_registry": "one canonical PromptMigrationCandidate table",
            "single_gate": "P138B validates blockers before any write",
            "single_write_plan": "P138C writes only approved rows",
            "single_traceability": "source_tab + source_row + source_hash + run_id on every migrated row",
            "single_safety_contract": "no broker/order/sizing/auto apply for all prompts",
        },
        "sheets_write_policy": {
            "p138a": "NO_SHEETS_WRITE",
            "p138b": "NO_SHEETS_WRITE_VALIDATE_ONLY",
            "p138c": "SHEETS_WRITE_AFTER_EXPLICIT_GO_ONLY",
        },
    }


def build_source_tab_contract() -> dict[str, Any]:
    return {
        "spreadsheet_id": SHEETS_DEV_SPREADSHEET_ID,
        "source_tabs": list(SOURCE_TABS),
        "target_write_tabs_after_validation": list(TARGET_WRITE_TABS_AFTER_VALIDATION),
        "primary_source_tab": "📘 PROMPT_LIBRARY",
        "primary_prompt_fields": list(PROMPT_TEXT_FIELDS),
        "known_primary_columns": [
            "contract_id",
            "ai_runtime_name",
            "prompt_id",
            "prompt_detail",
            "used_by_ai_runtime_names",
            "record_type",
            "prompt_version_role",
            "status",
            "validation_status",
            "cleanup_action",
            "cleanup_reason",
            "ai_runtime_id",
            "gem_profile",
            "target_runtime",
            "variant_id",
            "variant_version",
            "variant_scope",
            "is_reference_locked",
            "base_prompt_id",
            "parent_prompt_id",
            "prompt_family",
            "prompt_template_to_copy",
            "original_prompt_template",
            "ultimate_reference_prompt",
            "required_inputs",
            "required_outputs",
            "mandatory_fields",
            "blocked_if_missing",
            "review_if_missing",
            "safety_rules",
            "output_format",
            "fallback_behavior",
            "priority",
            "owner",
            "source_queue_refs",
            "run_id",
            "generated_at",
            "version",
            "notes",
        ],
    }


def _pick_prompt_text(row: dict[str, Any]) -> tuple[str, str | None]:
    for field in PROMPT_TEXT_FIELDS:
        text = _safe_cell(row, field)
        if text:
            return text, field
    return "", None


def normalize_prompt_library_row(
    row: dict[str, Any],
    *,
    source_tab: str,
    source_row: int,
    spreadsheet_id: str = SHEETS_DEV_SPREADSHEET_ID,
) -> PromptMigrationCandidate:
    prompt_text, text_field = _pick_prompt_text(row)
    prompt_id = _safe_cell(row, "prompt_id") or _safe_cell(row, "contract_id")
    if not prompt_id:
        prompt_id = f"{_slug(source_tab)}_row_{source_row}"

    base_prompt_id = _safe_cell(row, "base_prompt_id") or None
    parent_prompt_id = _safe_cell(row, "parent_prompt_id") or None
    prompt_family = _safe_cell(row, "prompt_family") or None
    gem_id = _safe_cell(row, "gem_profile") or _safe_cell(row, "ai_runtime_name") or "UNKNOWN_GEM"
    prompt_profile = (
        _safe_cell(row, "target_runtime") or _safe_cell(row, "prompt_version_role") or None
    )
    record_type = _safe_cell(row, "record_type") or None
    status = _safe_cell(row, "status") or None
    validation_status = _safe_cell(row, "validation_status") or None
    prompt_version_role = _safe_cell(row, "prompt_version_role")

    row_fingerprint = json.dumps(row, ensure_ascii=False, sort_keys=True)
    source_hash = _sha256_text(f"{source_tab}|{source_row}|{row_fingerprint}")
    migration_id = f"MIG-{_slug(prompt_id)}-{source_hash[:12]}"

    is_reference_locked = (
        _truthy(_safe_cell(row, "is_reference_locked"))
        or "LOCKED" in prompt_version_role.upper()
        or "REFERENCE" in prompt_version_role.upper()
    )

    blockers: list[str] = []
    if not prompt_text:
        blockers.append("PROMPT_TEXT_MISSING")
    if gem_id == "UNKNOWN_GEM":
        blockers.append("GEM_ID_MISSING")
    if is_reference_locked and record_type == "PROMPT_CONTRACT":
        target_row_strategy = "CREATE_VARIANT_ROW_DO_NOT_OVERWRITE_REFERENCE"
        action = "PRESERVE_LOCKED_REFERENCE_AND_CREATE_VALIDATED_VARIANT"
    else:
        target_row_strategy = "UPSERT_BY_PROMPT_ID_AFTER_VALIDATION"
        action = "NORMALIZE_AND_PREPARE_VALIDATED_UPSERT"

    p137_correction_status = "REQUIRED" if prompt_text else "BLOCKED_NO_PROMPT_TEXT"
    p133_compatibility_status = (
        "READY_FOR_VALIDATION" if prompt_text and not blockers else "BLOCKED"
    )

    return PromptMigrationCandidate(
        migration_id=migration_id,
        source_spreadsheet_id=spreadsheet_id,
        source_tab=source_tab,
        source_row=source_row,
        source_hash=source_hash,
        prompt_id=prompt_id,
        base_prompt_id=base_prompt_id,
        parent_prompt_id=parent_prompt_id,
        prompt_family=prompt_family,
        gem_id=gem_id,
        prompt_profile=prompt_profile,
        record_type=record_type,
        status=status,
        validation_status=validation_status,
        is_reference_locked=is_reference_locked,
        raw_prompt_text=prompt_text,
        prompt_text_field_used=text_field,
        python_simplification_action=action,
        p137_correction_status=p137_correction_status,
        p133_compatibility_status=p133_compatibility_status,
        target_sheet="📘 PROMPT_LIBRARY",
        target_row_strategy=target_row_strategy,
        write_status="PLANNED_ONLY_NO_WRITE_BEFORE_VALIDATION",
        human_review_status="REQUIRED",
        blockers=tuple(blockers),
    )


def _detect_header_row(rows: list[list[str]]) -> tuple[int, list[str]]:
    for idx, row in enumerate(rows):
        normalized = [str(cell).strip() for cell in row]
        if "prompt_id" in normalized and (
            "prompt_detail" in normalized or "prompt_template_to_copy" in normalized
        ):
            return idx, normalized
    if rows:
        return 0, [str(cell).strip() for cell in rows[0]]
    return 0, []


def candidates_from_tab_values(
    values: list[list[str]],
    *,
    source_tab: str,
    spreadsheet_id: str = SHEETS_DEV_SPREADSHEET_ID,
) -> list[PromptMigrationCandidate]:
    if not values:
        return []

    header_idx, headers = _detect_header_row(values)
    candidates: list[PromptMigrationCandidate] = []
    for row_idx, values_row in enumerate(values[header_idx + 1 :], start=header_idx + 2):
        row = {
            header: values_row[col] if col < len(values_row) else ""
            for col, header in enumerate(headers)
        }
        if not any(str(value).strip() for value in row.values()):
            continue
        if not (
            _safe_cell(row, "prompt_id")
            or _safe_cell(row, "contract_id")
            or _pick_prompt_text(row)[0]
        ):
            continue
        candidates.append(
            normalize_prompt_library_row(
                row,
                source_tab=source_tab,
                source_row=row_idx,
                spreadsheet_id=spreadsheet_id,
            )
        )
    return candidates


def load_csv_directory(csv_dir: Path | None) -> dict[str, list[list[str]]]:
    if csv_dir is None or not csv_dir.exists():
        return {}

    loaded: dict[str, list[list[str]]] = {}
    for file in sorted(csv_dir.glob("*.csv")):
        tab_name = file.stem
        with file.open("r", encoding="utf-8-sig", newline="") as handle:
            loaded[tab_name] = [row for row in csv.reader(handle)]
    return loaded


def build_migration_payload(request: P138ARequest) -> dict[str, Any]:
    generated_at = request.generated_at_utc or _utc_now_iso()
    csv_tabs = load_csv_directory(request.csv_dir)

    candidates: list[PromptMigrationCandidate] = []
    for source_tab, values in csv_tabs.items():
        candidates.extend(
            candidates_from_tab_values(
                values,
                source_tab=source_tab,
                spreadsheet_id=request.spreadsheet_id,
            )
        )

    candidate_dicts = [asdict(candidate) for candidate in candidates]
    blocker_count = sum(1 for candidate in candidates if candidate.blockers)
    locked_reference_count = sum(1 for candidate in candidates if candidate.is_reference_locked)
    variant_candidate_count = sum(
        1
        for candidate in candidates
        if "VARIANT" in (candidate.record_type or "").upper()
        or "VARIANT" in (candidate.prompt_profile or "").upper()
    )

    status = "P138A_MIGRATION_CANDIDATE_READY"
    if not csv_tabs:
        status = "P138A_SOURCE_SHEETS_EXPORT_REQUIRED_FOR_FULL_CANDIDATE"

    return {
        "step": "P138A_SHEETS_PROMPT_BASE_MIGRATION_CANDIDATE",
        "version": P138A_VERSION,
        "status": status,
        "generated_at_utc": generated_at,
        "run_id": request.run_id,
        "spreadsheet_id": request.spreadsheet_id,
        "csv_dir": str(request.csv_dir) if request.csv_dir else None,
        "source_tab_contract": build_source_tab_contract(),
        "process_simplification_spec": build_process_simplification_spec(),
        "candidate_count": len(candidates),
        "blocker_count": blocker_count,
        "locked_reference_count": locked_reference_count,
        "variant_candidate_count": variant_candidate_count,
        "write_policy": {
            "sheets_write_in_p138a": False,
            "future_sheets_write_allowed_after_validation_go": True,
            "write_gate": "P138C_EXPLICIT_GO_REQUIRED",
        },
        "validation_gate": {
            "next_step": "P138B_VALIDATE_MIGRATION_CANDIDATES_BEFORE_SHEETS_WRITE",
            "requires_human_review": True,
            "blocks_if_candidate_has_blockers": True,
            "blocks_if_source_export_missing": not bool(csv_tabs),
        },
        "safety_markers": list(SAFETY_MARKERS),
        "canonical_fields": canonical_prompt_registry_fields(),
        "migration_candidates": candidate_dicts,
    }


def _write_json(path: Path, payload: Any) -> None:
    path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=False) + "\n", encoding="utf-8"
    )


def _write_candidates_csv(path: Path, candidates: list[dict[str, Any]]) -> None:
    fields = canonical_prompt_registry_fields()
    with path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        for row in candidates:
            csv_row = dict(row)
            csv_row["blockers"] = " | ".join(csv_row.get("blockers") or [])
            writer.writerow({field: csv_row.get(field, "") for field in fields})


def _write_simplification_md(path: Path, payload: dict[str, Any]) -> None:
    spec = payload["process_simplification_spec"]
    lines = [
        "# P138A — Python Ultimate Process Simplification",
        "",
        f"Status: `{spec['status']}`",
        "",
        "## Objectif",
        "",
        spec["objective"],
        "",
        "## Problèmes du process Sheets d'origine",
        "",
    ]
    lines.extend(f"- {item}" for item in spec["origin_process_problems"])
    lines.extend(["", "## Process cible Python", ""])
    lines.extend(f"- {item}" for item in spec["python_target_process"])
    lines.extend(["", "## Règles de simplification ultime", ""])
    for key, value in spec["ultimate_simplification_rules"].items():
        lines.append(f"- `{key}`: {value}")
    lines.extend(["", "## Politique write Sheets", ""])
    for key, value in spec["sheets_write_policy"].items():
        lines.append(f"- `{key}`: `{value}`")
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def _write_validation_plan_md(path: Path, payload: dict[str, Any]) -> None:
    lines = [
        "# P138A — Migration Validation Plan",
        "",
        f"Status: `{payload['status']}`",
        f"Candidate count: `{payload['candidate_count']}`",
        f"Blocker count: `{payload['blocker_count']}`",
        f"Locked reference count: `{payload['locked_reference_count']}`",
        f"Variant candidate count: `{payload['variant_candidate_count']}`",
        "",
        "## Règles",
        "",
        "- P138A ne fait aucun write Sheets.",
        "- P138B valide les candidats, les doublons et les blockers.",
        "- P138C écrira dans Sheets uniquement après GO explicite.",
        "- Les prompts originaux verrouillés restent préservés.",
        "- Les corrections P137 créent ou mettent à jour des variantes validées, pas les références verrouillées.",
        "",
        "## Write cible après validation",
        "",
    ]
    lines.extend(f"- `{tab}`" for tab in TARGET_WRITE_TABS_AFTER_VALIDATION)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def _write_runbook(path: Path, payload: dict[str, Any]) -> None:
    text = f"""# P138A — Sheets Prompt Base Migration Candidate

## Objectif

Préparer la migration définitive depuis l'ancienne base Sheets vers un process Python simplifié, puis un write Sheets après validation.

## Statut

- Status: `{payload["status"]}`
- Candidates: `{payload["candidate_count"]}`
- Blockers: `{payload["blocker_count"]}`
- Spreadsheet ID: `{payload["spreadsheet_id"]}`

## Source tabs

{chr(10).join(f"- `{tab}`" for tab in SOURCE_TABS)}

## Process cible

Python devient le moteur de simplification:
1. lecture ancienne base Sheets ;
2. normalisation registry unique ;
3. hash/provenance ;
4. déduplication ;
5. corrections P137 ;
6. validation P138B ;
7. write Sheets P138C après GO.

## Sécurité

- Aucun write Sheets en P138A.
- Aucun broker/order/sizing/auto apply.
- Human review obligatoire.
"""
    path.write_text(text, encoding="utf-8")


def write_p138a_pack(request: P138ARequest) -> dict[str, Any]:
    _ensure_dir(request.output_dir)
    payload = build_migration_payload(request)
    candidates = payload["migration_candidates"]

    _write_json(request.output_dir / "P138A_MIGRATION_PAYLOAD.json", payload)
    _write_json(
        request.output_dir / "P138A_SOURCE_TAB_CONTRACT.json", payload["source_tab_contract"]
    )
    _write_json(
        request.output_dir / "P138A_PROCESS_SIMPLIFICATION_SPEC.json",
        payload["process_simplification_spec"],
    )
    _write_candidates_csv(request.output_dir / "P138A_MIGRATION_CANDIDATES.csv", candidates)
    _write_json(request.output_dir / "P138A_MIGRATION_CANDIDATES.json", candidates)
    _write_simplification_md(request.output_dir / "P138A_PROCESS_SIMPLIFICATION_SPEC.md", payload)
    _write_validation_plan_md(request.output_dir / "P138A_VALIDATION_PLAN.md", payload)
    _write_runbook(request.output_dir / "P138A_RUNBOOK.md", payload)

    return payload


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="P138A Sheets prompt base migration candidate")
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("05_EXPORTS/P138A_SHEETS_PROMPT_BASE_MIGRATION_CANDIDATE"),
    )
    parser.add_argument("--csv-dir", type=Path, default=None)
    parser.add_argument("--spreadsheet-id", default=SHEETS_DEV_SPREADSHEET_ID)
    parser.add_argument("--run-id", default=DEFAULT_RUN_ID)
    parser.add_argument("--generated-at-utc", default=None)
    parser.add_argument("--dry-run-export", action="store_true")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    request = P138ARequest(
        output_dir=args.output_dir,
        csv_dir=args.csv_dir,
        spreadsheet_id=args.spreadsheet_id,
        run_id=args.run_id,
        generated_at_utc=args.generated_at_utc,
    )
    payload = write_p138a_pack(request)
    print(payload["status"])
    print(f"candidate_count={payload['candidate_count']}")
    print(f"blocker_count={payload['blocker_count']}")
    print(f"output_dir={request.output_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
