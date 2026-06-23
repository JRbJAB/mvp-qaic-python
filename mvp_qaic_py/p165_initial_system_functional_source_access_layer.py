"""P165-R3 initial MVP QAIC system functional source access layer.

Purpose:
- Recover the initial Google Sheet / Apps Script functional map into Python-friendly
  registries.
- Create a durable local source access layer from CLASP import CSV + known live seeds.
- Do not modify the runtime prompt, Google Sheets, Apps Script, broker, order, or sizing.

This module is read-only and local-output only.
"""

from __future__ import annotations

import argparse
import csv
import json
from collections import Counter, defaultdict
from dataclasses import asdict, dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Iterable

STATUS = "OK_P165_R3_INITIAL_SHEET_APPS_SCRIPT_FUNCTIONAL_LAYER_READY_TO_SEAL"
P165_R3_STATUS = "P165_R3_PYTHON_INITIAL_FUNCTIONAL_SOURCE_ACCESS_LAYER_READY_REVIEW_ONLY"
PROMPT_SOURCE_ID = "P132_P133_PORTFOLIO_MULTIMODAL_REVIEW"

LIVE_SOURCE_SEEDS = [
    {
        "source_id": "LIVE_SHEET_MVP_QAIC_DEV",
        "source_type": "GOOGLE_SHEET",
        "source_title": "MVP QAIC - Crypto Signal OS - DEV",
        "source_ref": "19KY8Y1ozS7ONaJu9_5NQmjO47l-xM798Xm-y1n7fNd0",
        "access_mode": "READ_ONLY_SEED",
        "migration_use": "initial MVP sheet data/tabs/config/journal/prompt queues",
    },
    {
        "source_id": "LIVE_SHEET_QAIC_CRYPTO_V25_DEV",
        "source_type": "GOOGLE_SHEET",
        "source_title": "QAIC Crypto - V25 DEV",
        "source_ref": "1vBwQ6GMfqBOfesIIpzBVGieTm-GcY9y_dXink_VY1Vg",
        "access_mode": "READ_ONLY_SEED",
        "migration_use": "upstream QAIC/V25 functional context and possible historical prompt material",
    },
    {
        "source_id": "LIVE_DOC_MVP_QAIC_INSTRUCTIONS_0_6_2",
        "source_type": "GOOGLE_DRIVE_MD_OR_DOC",
        "source_title": "INSTRUCTIONS_PROJET_MVP_QAIC_0.6.2_REAL_FUSION_REPAIR",
        "source_ref": "13MS0do4ho0uUJfDVKRe3z0i4HbieFG2N",
        "access_mode": "READ_ONLY_SEED",
        "migration_use": "historical project requirements / lexique-first / prompt design source",
    },
    {
        "source_id": "LOCAL_CLASP_IMPORTS_ALL",
        "source_type": "LOCAL_CSV_EXPORT",
        "source_title": "MVPQAIC_CLASP_IMPORTS_ALL.csv",
        "source_ref": "MVPQAIC_CLASP_IMPORTS_ALL.csv",
        "access_mode": "LOCAL_READ_ONLY",
        "migration_use": "Apps Script module/function/risk/flags recovery",
    },
]

PROMPT_KEYWORDS = (
    "prompt",
    "gpt",
    "gem",
    "quality",
    "response",
    "intake",
    "journal",
    "decision",
    "human",
    "review",
    "portfolio",
    "image",
    "json",
)

FUNCTIONAL_FAMILY_TARGETS = {
    "PROMPT_ENGINE": "mvp_qaic_py.prompt_engine",
    "JOURNAL": "mvp_qaic_py.journal",
    "KNOWLEDGE_SEARCH": "mvp_qaic_py.knowledge",
    "IMPORT_SEEDS": "mvp_qaic_py.ingestion",
    "AUDIT_INVENTORY": "mvp_qaic_py.audit",
    "SCRIPT_REGISTRY": "mvp_qaic_py.registry",
    "FORMATTING": "mvp_qaic_py.formatting",
    "SETUP_FOUNDATION": "mvp_qaic_py.setup",
    "QAIC_BRIDGE": "mvp_qaic_py.bridge",
    "MANIFEST": "mvp_qaic_py.manifest",
}

SHEET_PLAN_ROWS = [
    {
        "sheet_or_domain": "CONFIG",
        "purpose": "runtime/config key-value source",
        "python_target": "settings/config loader",
        "migration_status": "NEEDS_LIVE_READ_EXPORT_OR_LOCAL_CACHE",
        "priority": "P0",
    },
    {
        "sheet_or_domain": "LEXIQUE / KNOWLEDGE",
        "purpose": "lexique, methods, signals, risk playbook",
        "python_target": "knowledge index + search service",
        "migration_status": "NEEDS_LIVE_READ_EXPORT_OR_LOCAL_CACHE",
        "priority": "P0",
    },
    {
        "sheet_or_domain": "PROMPT_QUALITY / PROMPT_IMPROVEMENT",
        "purpose": "prompt corrections, prompt quality dashboard, queue",
        "python_target": "prompt improvement queue + source selector",
        "migration_status": "NEEDS_LIVE_READ_EXPORT_OR_LOCAL_CACHE",
        "priority": "P0",
    },
    {
        "sheet_or_domain": "DECISION_JOURNAL",
        "purpose": "human review journal and decision evidence",
        "python_target": "decision journal local store",
        "migration_status": "NEEDS_LIVE_READ_EXPORT_OR_LOCAL_CACHE",
        "priority": "P0",
    },
    {
        "sheet_or_domain": "WEBAPP / FRONTEND",
        "purpose": "MVP web app visible data and sync candidates",
        "python_target": "local UI/NiceGUI source tables",
        "migration_status": "NEEDS_LIVE_READ_EXPORT_OR_LOCAL_CACHE",
        "priority": "P1",
    },
]


@dataclass(frozen=True)
class Summary:
    STATUS: str
    P165_R3_STATUS: str
    PYTHON_SOURCE_ACCESS_LAYER_CREATED: bool
    INITIAL_SHEET_APPS_SCRIPT_RECOVERY_READY: bool
    LIVE_SOURCE_SEED_COUNT: int
    CLASP_CSV_FOUND: bool
    APPS_SCRIPT_MODULE_COUNT: int
    APPS_SCRIPT_FUNCTION_COUNT: int
    PUBLIC_FUNCTION_COUNT: int
    PROMPT_ENGINE_FUNCTION_COUNT: int
    FUNCTIONAL_MIGRATION_MAP_COUNT: int
    SHEETS_DATA_ACCESS_PLAN_COUNT: int
    P132_P133_DEMOTED_TO_RUNTIME_CONTRACT_ONLY: bool
    RUNTIME_PROMPT_MODIFIED: bool
    GOOGLE_SHEETS_WRITE: bool
    LIVE_GOOGLE_SHEETS_READ: bool
    APPS_SCRIPT_EXECUTION: bool
    CLASP_PUSH: bool
    PUBLIC_DEPLOY: bool
    BROKER: bool
    ORDER: bool
    SIZING: bool
    APPLY_ALLOWED: bool
    BLOCKER_COUNT: int
    EXPORT_DIR: str
    NEXT: str
    created_at_utc: str


def utc_now() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def read_csv_dicts(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="", errors="replace") as f:
        return [{k: (v or "") for k, v in row.items()} for row in csv.DictReader(f)]


def write_csv(
    path: Path, rows: Iterable[dict[str, object]], fieldnames: list[str] | None = None
) -> None:
    rows = list(rows)
    if fieldnames is None:
        keys: list[str] = []
        for row in rows:
            for key in row:
                if key not in keys:
                    keys.append(key)
        fieldnames = keys
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def write_json(path: Path, payload: dict[str, object]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def normalize_bool(value: str) -> bool:
    return str(value).strip().upper() in {"YES", "TRUE", "1", "Y"}


def find_clasp_csv(repo_root: Path, explicit: str | None = None) -> Path | None:
    candidates: list[Path] = []
    if explicit:
        candidates.append(Path(explicit))
    candidates.extend(
        [
            repo_root / "MVPQAIC_CLASP_IMPORTS_ALL.csv",
            repo_root / "05_EXPORTS" / "MVPQAIC_CLASP_IMPORTS_ALL.csv",
            Path.home() / "Downloads" / "MVPQAIC_CLASP_IMPORTS_ALL.csv",
        ]
    )
    candidates.extend(repo_root.glob("**/MVPQAIC_CLASP_IMPORTS_ALL.csv"))
    for candidate in candidates:
        if candidate.exists() and candidate.is_file():
            return candidate
    return None


def classify_function(row: dict[str, str]) -> str:
    function = row.get("function_name", "")
    script = row.get("script_file_name", "")
    family = row.get("module_family", "")
    text = f"{family} {script} {function}".lower()
    if "prompt" in text or "gpt" in text or "gem" in text:
        return "PROMPT_OR_AI"
    if "journal" in text or "decision" in text:
        return "DECISION_JOURNAL"
    if "lexique" in text or "knowledge" in text or "search" in text:
        return "KNOWLEDGE_SEARCH"
    if "webapp" in text or "frontend" in text:
        return "WEBAPP_FRONTEND"
    if "registry" in text or "inventory" in text or "audit" in text:
        return "AUDIT_REGISTRY"
    if "import" in text or "intake" in text:
        return "INGESTION_INTAKE"
    return "OTHER"


def migration_priority(row: dict[str, str]) -> str:
    role = classify_function(row)
    if role in {"PROMPT_OR_AI", "DECISION_JOURNAL", "KNOWLEDGE_SEARCH"}:
        return "P0"
    if role in {"INGESTION_INTAKE", "AUDIT_REGISTRY", "WEBAPP_FRONTEND"}:
        return "P1"
    return "P2"


def is_prompt_related(row: dict[str, str]) -> bool:
    text = " ".join(
        [
            row.get("module_family", ""),
            row.get("script_file_name", ""),
            row.get("function_name", ""),
            row.get("raw_key", ""),
            row.get("raw_value", ""),
            row.get("notes", ""),
        ]
    ).lower()
    return any(keyword in text for keyword in PROMPT_KEYWORDS)


def build_source_registry(clasp_csv: Path | None) -> list[dict[str, object]]:
    rows = [dict(seed) for seed in LIVE_SOURCE_SEEDS]
    if clasp_csv:
        rows.append(
            {
                "source_id": "LOCAL_CLASP_IMPORTS_ALL_RESOLVED",
                "source_type": "LOCAL_CSV_EXPORT",
                "source_title": clasp_csv.name,
                "source_ref": str(clasp_csv),
                "access_mode": "LOCAL_READ_ONLY_RESOLVED",
                "migration_use": "resolved CLASP import CSV used for P165-R3 functional recovery",
            }
        )
    return rows


def build_module_inventory(records: list[dict[str, str]]) -> list[dict[str, object]]:
    rows = []
    for r in records:
        if r.get("record_type") != "SCRIPT_INVENTORY":
            continue
        rows.append(
            {
                "script_file_name": r.get("script_file_name", ""),
                "module_family": r.get("module_family", ""),
                "detected_version": r.get("detected_version", ""),
                "file_size_bytes": r.get("file_size_bytes", ""),
                "line_count": r.get("line_count", ""),
                "char_count": r.get("char_count", ""),
                "public_function_count": r.get("public_function_count", ""),
                "internal_function_count": r.get("internal_function_count", ""),
                "total_function_count": r.get("total_function_count", ""),
                "risk_hit_count": r.get("risk_hit_count", ""),
                "calls_spreadsheet": r.get("calls_spreadsheet", ""),
                "writes_sheet_likely": r.get("writes_sheet_likely", ""),
                "calls_drive": r.get("calls_drive", ""),
                "calls_trigger": r.get("calls_trigger", ""),
                "calls_properties": r.get("calls_properties", ""),
                "python_target_package": FUNCTIONAL_FAMILY_TARGETS.get(
                    r.get("module_family", ""), "mvp_qaic_py.legacy"
                ),
                "migration_action": "RECOVER_TO_PYTHON_READONLY_FIRST",
            }
        )
    return rows


def build_function_index(records: list[dict[str, str]]) -> list[dict[str, object]]:
    rows = []
    for r in records:
        if r.get("record_type") != "FUNCTION_INDEX":
            continue
        rows.append(
            {
                "function_name": r.get("function_name", ""),
                "script_file_name": r.get("script_file_name", ""),
                "module_family": r.get("module_family", ""),
                "function_visibility": r.get("function_visibility", ""),
                "line_number": r.get("line_number", ""),
                "functional_role": classify_function(r),
                "migration_priority": migration_priority(r),
                "python_target_package": FUNCTIONAL_FAMILY_TARGETS.get(
                    r.get("module_family", ""), "mvp_qaic_py.legacy"
                ),
                "safe_migration_mode": "READONLY_PORT_FIRST",
            }
        )
    return rows


def build_prompt_engine_recovery(records: list[dict[str, str]]) -> list[dict[str, object]]:
    rows = []
    for r in records:
        if r.get("record_type") not in {"FUNCTION_INDEX", "SCRIPT_INVENTORY", "RISK_HIT"}:
            continue
        if not is_prompt_related(r):
            continue
        rows.append(
            {
                "record_type": r.get("record_type", ""),
                "script_file_name": r.get("script_file_name", ""),
                "module_family": r.get("module_family", ""),
                "function_name": r.get("function_name", ""),
                "function_visibility": r.get("function_visibility", ""),
                "functional_role": classify_function(r),
                "migration_priority": migration_priority(r),
                "evidence_text": " ".join(
                    x
                    for x in [
                        r.get("module_family", ""),
                        r.get("script_file_name", ""),
                        r.get("function_name", ""),
                        r.get("raw_key", ""),
                        r.get("raw_value", ""),
                        r.get("notes", ""),
                    ]
                    if x
                )[:500],
            }
        )
    return rows


def build_migration_map(
    module_rows: list[dict[str, object]], function_rows: list[dict[str, object]]
) -> list[dict[str, object]]:
    by_script: dict[str, list[dict[str, object]]] = defaultdict(list)
    for f in function_rows:
        by_script[str(f.get("script_file_name", ""))].append(f)

    rows = []
    for m in module_rows:
        script = str(m.get("script_file_name", ""))
        functions = by_script.get(script, [])
        roles = Counter(str(f.get("functional_role", "OTHER")) for f in functions)
        priorities = Counter(str(f.get("migration_priority", "P2")) for f in functions)
        rows.append(
            {
                "script_file_name": script,
                "module_family": m.get("module_family", ""),
                "detected_version": m.get("detected_version", ""),
                "function_count": len(functions),
                "top_functional_roles": ";".join(f"{k}:{v}" for k, v in roles.most_common(5)),
                "top_priority": priorities.most_common(1)[0][0] if priorities else "P2",
                "writes_sheet_likely": m.get("writes_sheet_likely", ""),
                "calls_spreadsheet": m.get("calls_spreadsheet", ""),
                "python_target_package": m.get("python_target_package", ""),
                "migration_action": "PORT_READONLY_PYTHON_LAYER_BEFORE_ANY_WRITE",
            }
        )
    return rows


def markdown_report(summary: Summary, top_prompt_rows: list[dict[str, object]]) -> str:
    top_lines = []
    for row in top_prompt_rows[:25]:
        top_lines.append(
            f"- `{row.get('script_file_name', '')}` / `{row.get('function_name', '')}` "
            f"family=`{row.get('module_family', '')}` role=`{row.get('functional_role', '')}`"
        )
    return "\n".join(
        [
            "# P165-R3 — Initial Sheet & Apps Script Functional Source Access Layer",
            "",
            "## Decision",
            "",
            "- This is the correction layer for the Python migration.",
            "- P132/P133 remains a runtime contract only, not the final business reference prompt.",
            "- The initial Google Sheet / Apps Script system is recovered into Python-friendly registries.",
            "- No runtime prompt modification, no Sheet write, no Apps Script execution, no CLASP push.",
            "",
            "## Summary",
            "",
            f"- `APPS_SCRIPT_MODULE_COUNT`: `{summary.APPS_SCRIPT_MODULE_COUNT}`",
            f"- `APPS_SCRIPT_FUNCTION_COUNT`: `{summary.APPS_SCRIPT_FUNCTION_COUNT}`",
            f"- `PROMPT_ENGINE_FUNCTION_COUNT`: `{summary.PROMPT_ENGINE_FUNCTION_COUNT}`",
            f"- `FUNCTIONAL_MIGRATION_MAP_COUNT`: `{summary.FUNCTIONAL_MIGRATION_MAP_COUNT}`",
            "",
            "## Top prompt/AI recovery candidates",
            "",
            *(top_lines or ["- No prompt/AI candidates found."]),
            "",
            "## Next",
            "",
            "`P166_REFERENCE_PROMPT_REBUILD_FROM_SOURCE_INDEX_OR_LIVE_EXPORT`",
            "",
        ]
    )


def build_and_write_export(repo_root: Path, clasp_csv_arg: str | None = None) -> Summary:
    export_dir = (
        repo_root
        / "05_EXPORTS"
        / f"P165_R3_INITIAL_SHEET_APPS_SCRIPT_FUNCTIONAL_LAYER_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    )
    export_dir.mkdir(parents=True, exist_ok=True)

    clasp_csv = find_clasp_csv(repo_root, clasp_csv_arg)
    records = read_csv_dicts(clasp_csv) if clasp_csv else []

    source_registry = build_source_registry(clasp_csv)
    module_rows = build_module_inventory(records)
    function_rows = build_function_index(records)
    prompt_rows = build_prompt_engine_recovery(records)
    migration_rows = build_migration_map(module_rows, function_rows)

    write_csv(export_dir / "P165_R3_SOURCE_REGISTRY.csv", source_registry)
    write_csv(export_dir / "P165_R3_APPS_SCRIPT_MODULE_INVENTORY.csv", module_rows)
    write_csv(export_dir / "P165_R3_APPS_SCRIPT_FUNCTION_INDEX.csv", function_rows)
    write_csv(export_dir / "P165_R3_PROMPT_ENGINE_RECOVERY.csv", prompt_rows)
    write_csv(export_dir / "P165_R3_FUNCTIONAL_MIGRATION_MAP.csv", migration_rows)
    write_csv(export_dir / "P165_R3_SHEETS_DATA_ACCESS_PLAN.csv", SHEET_PLAN_ROWS)

    public_count = sum(
        1 for r in function_rows if str(r.get("function_visibility", "")).upper() == "PUBLIC"
    )
    blockers: list[str] = []
    if not clasp_csv:
        blockers.append("CLASP_IMPORT_CSV_NOT_FOUND")
    if not module_rows:
        blockers.append("NO_APPS_SCRIPT_MODULES_RECOVERED")
    if not function_rows:
        blockers.append("NO_APPS_SCRIPT_FUNCTIONS_RECOVERED")

    summary = Summary(
        STATUS=STATUS,
        P165_R3_STATUS=P165_R3_STATUS,
        PYTHON_SOURCE_ACCESS_LAYER_CREATED=True,
        INITIAL_SHEET_APPS_SCRIPT_RECOVERY_READY=not blockers,
        LIVE_SOURCE_SEED_COUNT=len(LIVE_SOURCE_SEEDS),
        CLASP_CSV_FOUND=clasp_csv is not None,
        APPS_SCRIPT_MODULE_COUNT=len(module_rows),
        APPS_SCRIPT_FUNCTION_COUNT=len(function_rows),
        PUBLIC_FUNCTION_COUNT=public_count,
        PROMPT_ENGINE_FUNCTION_COUNT=len(prompt_rows),
        FUNCTIONAL_MIGRATION_MAP_COUNT=len(migration_rows),
        SHEETS_DATA_ACCESS_PLAN_COUNT=len(SHEET_PLAN_ROWS),
        P132_P133_DEMOTED_TO_RUNTIME_CONTRACT_ONLY=True,
        RUNTIME_PROMPT_MODIFIED=False,
        GOOGLE_SHEETS_WRITE=False,
        LIVE_GOOGLE_SHEETS_READ=False,
        APPS_SCRIPT_EXECUTION=False,
        CLASP_PUSH=False,
        PUBLIC_DEPLOY=False,
        BROKER=False,
        ORDER=False,
        SIZING=False,
        APPLY_ALLOWED=False,
        BLOCKER_COUNT=len(blockers),
        EXPORT_DIR=str(export_dir),
        NEXT="P166_REFERENCE_PROMPT_REBUILD_FROM_SOURCE_INDEX_OR_LIVE_EXPORT"
        if not blockers
        else "P165_R3_REPAIR_INPUTS_OR_STOP",
        created_at_utc=utc_now(),
    )

    write_json(export_dir / "P165_R3_SUMMARY.json", asdict(summary))
    (export_dir / "P165_R3_FUNCTIONAL_SOURCE_ACCESS_REPORT.md").write_text(
        markdown_report(summary, prompt_rows), encoding="utf-8"
    )

    print(summary.P165_R3_STATUS)
    print(
        f"python_source_access_layer_created={str(summary.PYTHON_SOURCE_ACCESS_LAYER_CREATED).lower()}"
    )
    print(f"clasp_csv_found={str(summary.CLASP_CSV_FOUND).lower()}")
    print(f"apps_script_module_count={summary.APPS_SCRIPT_MODULE_COUNT}")
    print(f"apps_script_function_count={summary.APPS_SCRIPT_FUNCTION_COUNT}")
    print(f"prompt_engine_function_count={summary.PROMPT_ENGINE_FUNCTION_COUNT}")
    print(f"functional_migration_map_count={summary.FUNCTIONAL_MIGRATION_MAP_COUNT}")
    print(f"blocker_count={summary.BLOCKER_COUNT}")
    print(f"output_dir={summary.EXPORT_DIR}")
    print(f"next={summary.NEXT}")

    if blockers:
        raise RuntimeError(";".join(blockers))
    return summary


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", default=".")
    parser.add_argument("--clasp-csv", default=None)
    args = parser.parse_args(argv)
    build_and_write_export(Path(args.repo_root).resolve(), args.clasp_csv)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
