"""P168F operator export capture gate for MVP_QAIC_PY.

This module prepares a local-only dropzone and manifest for the operator
exports required by the P168B/P168C/P168D/P168E snapshot pipeline.

Safety contract:
- no Google Sheets write
- no live Google API call from Python
- no Apps Script execution
- no CLASP push
- no broker/order/sizing
- no runtime prompt modification
"""

from __future__ import annotations

import argparse
import csv
import json
from dataclasses import dataclass, asdict
from datetime import UTC, datetime
from pathlib import Path
from typing import Iterable

STEP = "P168F_OPERATOR_EXPORT_CAPTURE_OR_WAIT"
EXPORT_PREFIX = "P168F_OPERATOR_EXPORT_CAPTURE_OR_WAIT"
DROPZONE_RELATIVE = Path("00_OPERATOR_EXPORTS") / "P168F_REQUIRED_SNAPSHOTS"


@dataclass(frozen=True)
class RequiredExport:
    snapshot_id: str
    expected_file_name: str
    source_domain: str
    export_format: str
    required: bool
    purpose: str
    minimum_columns_hint: str
    operator_action: str


@dataclass(frozen=True)
class ExportFileStatus:
    snapshot_id: str
    expected_file_name: str
    source_domain: str
    expected_path: str
    found: bool
    file_size_bytes: int
    validation_status: str
    validation_note: str


def utc_stamp() -> str:
    return datetime.now(UTC).strftime("%Y%m%d_%H%M%S")


def required_exports() -> list[RequiredExport]:
    return [
        RequiredExport(
            snapshot_id="CONFIG",
            expected_file_name="MVP_QAIC_CONFIG.csv",
            source_domain="MVP_QAIC_PY",
            export_format="CSV_UTF8",
            required=True,
            purpose="Runtime/project configuration snapshot for local cockpit binding.",
            minimum_columns_hint="key,value OR config_key,config_value",
            operator_action="Export the CONFIG tab/range as CSV and save it with this exact name.",
        ),
        RequiredExport(
            snapshot_id="PROMPT_SOURCE_REGISTRY",
            expected_file_name="MVP_QAIC_PROMPT_SOURCE_REGISTRY.csv",
            source_domain="MVP_QAIC_PY",
            export_format="CSV_UTF8",
            required=True,
            purpose="Prompt/source registry used to bind prompt cockpit references.",
            minimum_columns_hint="source_id,status,source_type,version OR equivalent",
            operator_action="Export the prompt/source registry tab or approved source table.",
        ),
        RequiredExport(
            snapshot_id="DECISION_JOURNAL",
            expected_file_name="MVP_QAIC_DECISION_JOURNAL.csv",
            source_domain="MVP_QAIC_PY",
            export_format="CSV_UTF8",
            required=True,
            purpose="Decision journal snapshot for review history and operator traceability.",
            minimum_columns_hint="journal_id,decision_status,human_final_decision,validation_status",
            operator_action="Export the decision journal tab/range as CSV.",
        ),
        RequiredExport(
            snapshot_id="PROMPT_REVIEW_WORKBENCH",
            expected_file_name="MVP_QAIC_PROMPT_REVIEW_WORKBENCH.csv",
            source_domain="MVP_QAIC_PY",
            export_format="CSV_UTF8",
            required=True,
            purpose="Human review rows for prompt patch/apply decisions.",
            minimum_columns_hint="review_id,item_id,review_status,apply_now,human_note",
            operator_action="Export the current prompt review/workbench table as CSV.",
        ),
        RequiredExport(
            snapshot_id="LEXIQUE_OR_COCKPIT_DATA",
            expected_file_name="MVP_QAIC_LEXIQUE_OR_COCKPIT_DATA.csv",
            source_domain="MVP_QAIC_PY",
            export_format="CSV_UTF8",
            required=True,
            purpose="Useful lexique/cockpit data for local UI binding after cache build.",
            minimum_columns_hint="term,category,definition OR cockpit_key,cockpit_value",
            operator_action="Export the approved lexique or current useful cockpit dataset.",
        ),
    ]


def ensure_dropzone(project_dir: Path) -> Path:
    dropzone = project_dir / DROPZONE_RELATIVE
    dropzone.mkdir(parents=True, exist_ok=True)
    readme = dropzone / "README_P168F_DROPZONE.md"
    readme.write_text(build_dropzone_readme(dropzone), encoding="utf-8")
    return dropzone


def build_dropzone_readme(dropzone: Path) -> str:
    names = "\n".join(f"- `{item.expected_file_name}`" for item in required_exports())
    return f"""# P168F operator export dropzone

Place the required local CSV exports in this folder.

Folder:
`{dropzone}`

Required files:
{names}

Rules:
- CSV UTF-8 preferred.
- Keep exact file names.
- Do not paste secrets.
- Do not export broker/API credentials.
- Do not write back to Google Sheets from Python.
- This folder is local/operator-controlled input for MVP_QAIC_PY only.
"""


def inspect_dropzone(project_dir: Path) -> tuple[Path, list[ExportFileStatus]]:
    dropzone = ensure_dropzone(project_dir)
    statuses: list[ExportFileStatus] = []
    for item in required_exports():
        path = dropzone / item.expected_file_name
        found = path.exists() and path.is_file()
        size = path.stat().st_size if found else 0
        if found and size > 0:
            validation_status = "FOUND_PENDING_SCHEMA_VALIDATION"
            validation_note = "File exists; schema/content validation belongs to P168G."
        elif found and size == 0:
            validation_status = "FOUND_EMPTY_REVIEW_REQUIRED"
            validation_note = "File exists but is empty; replace with a real export."
        else:
            validation_status = "WAITING_OPERATOR_EXPORT"
            validation_note = "Expected export file is not present yet."
        statuses.append(
            ExportFileStatus(
                snapshot_id=item.snapshot_id,
                expected_file_name=item.expected_file_name,
                source_domain=item.source_domain,
                expected_path=str(path),
                found=found,
                file_size_bytes=size,
                validation_status=validation_status,
                validation_note=validation_note,
            )
        )
    return dropzone, statuses


def write_csv(path: Path, rows: Iterable[dict[str, object]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


def latest_export_dir(project_dir: Path, prefix: str) -> Path | None:
    exports_root = project_dir / "05_EXPORTS"
    if not exports_root.exists():
        return None
    matches = [p for p in exports_root.iterdir() if p.is_dir() and p.name.startswith(prefix)]
    if not matches:
        return None
    return sorted(matches, key=lambda p: p.name, reverse=True)[0]


def build_operator_instructions(dropzone: Path) -> str:
    rows = required_exports()
    table = "\n".join(
        f"| {item.snapshot_id} | `{item.expected_file_name}` | {item.operator_action} |"
        for item in rows
    )
    return f"""# P168F — Operator export capture instructions

## Goal

Prepare the five local CSV snapshots required before the local cache can be built.

Current preferred path: `LOCAL_EXPORT_IMPORT_FIRST`.

## Dropzone

`{dropzone}`

## Required exports

| Snapshot | Expected file | Operator action |
|---|---|---|
{table}

## Safety

- No Google Sheets write.
- No live Google API call from Python.
- No Apps Script execution.
- No CLASP push.
- No broker, order, or sizing.
- No runtime prompt modification.

## After placing files

Run the next cache validation/build step:

`P168G_LOCAL_CACHE_BUILD_FROM_OPERATOR_EXPORTS`
"""


def build_report(
    *,
    output_dir: Path,
    dropzone: Path,
    statuses: list[ExportFileStatus],
    p168e_dir: Path | None,
) -> str:
    ready = sum(1 for s in statuses if s.found and s.file_size_bytes > 0)
    waiting = sum(1 for s in statuses if not s.found)
    empty = sum(1 for s in statuses if s.found and s.file_size_bytes == 0)
    p168e_text = str(p168e_dir) if p168e_dir else "NOT_FOUND"
    return f"""# P168F — Operator export capture gate

## Status

`P168F_OPERATOR_EXPORT_CAPTURE_READY_WAIT_OPERATOR_FILES_READONLY`

## Counts

- required_snapshot_count: {len(statuses)}
- files_found_count: {sum(1 for s in statuses if s.found)}
- ready_snapshot_count: {ready}
- waiting_snapshot_count: {waiting}
- empty_file_count: {empty}
- cache_files_created_count: 0
- blocker_count: 0

## Dropzone

`{dropzone}`

## Previous P168E evidence

`{p168e_text}`

## Output directory

`{output_dir}`

## Safety

- runtime_prompt_modified: False
- apply_allowed: False
- google_sheets_write: False
- live_google_api_call_from_python: False
- apps_script_execution: False
- clasp_push: False
- broker: False
- order: False
- sizing: False

## Next

`P168G_LOCAL_CACHE_BUILD_FROM_OPERATOR_EXPORTS_OR_WAIT`
"""


def build_capture(project_dir: Path, *, stamp: str | None = None) -> dict[str, object]:
    project_dir = project_dir.resolve()
    stamp = stamp or utc_stamp()
    output_dir = project_dir / "05_EXPORTS" / f"{EXPORT_PREFIX}_{stamp}"
    output_dir.mkdir(parents=True, exist_ok=True)

    dropzone, statuses = inspect_dropzone(project_dir)
    required = required_exports()
    p168e_dir = latest_export_dir(
        project_dir, "P168E_LOCAL_CACHE_BUILD_FROM_VALIDATED_SNAPSHOTS_OR_WAIT_"
    )

    write_csv(
        output_dir / "P168F_REQUIRED_EXPORTS_MANIFEST.csv",
        [asdict(row) for row in required],
        [
            "snapshot_id",
            "expected_file_name",
            "source_domain",
            "export_format",
            "required",
            "purpose",
            "minimum_columns_hint",
            "operator_action",
        ],
    )
    write_csv(
        output_dir / "P168F_LOCAL_EXPORT_FILE_STATUS.csv",
        [asdict(row) for row in statuses],
        [
            "snapshot_id",
            "expected_file_name",
            "source_domain",
            "expected_path",
            "found",
            "file_size_bytes",
            "validation_status",
            "validation_note",
        ],
    )
    write_csv(
        output_dir / "P168F_OPERATOR_EXPORT_CAPTURE_CHECKLIST.csv",
        [
            {
                "snapshot_id": item.snapshot_id,
                "expected_file_name": item.expected_file_name,
                "done": "NO",
                "operator_note": "",
                "review_status": "PENDING_OPERATOR_EXPORT",
            }
            for item in required
        ],
        ["snapshot_id", "expected_file_name", "done", "operator_note", "review_status"],
    )

    (output_dir / "P168F_OPERATOR_EXPORT_INSTRUCTIONS.md").write_text(
        build_operator_instructions(dropzone),
        encoding="utf-8",
    )
    (output_dir / "P168F_CAPTURE_STATUS_REPORT.md").write_text(
        build_report(
            output_dir=output_dir, dropzone=dropzone, statuses=statuses, p168e_dir=p168e_dir
        ),
        encoding="utf-8",
    )

    ready_snapshot_count = sum(1 for row in statuses if row.found and row.file_size_bytes > 0)
    files_found_count = sum(1 for row in statuses if row.found)
    waiting_snapshot_count = sum(1 for row in statuses if not row.found)
    empty_file_count = sum(1 for row in statuses if row.found and row.file_size_bytes == 0)

    summary: dict[str, object] = {
        "step": STEP,
        "status": "P168F_OPERATOR_EXPORT_CAPTURE_READY_WAIT_OPERATOR_FILES_READONLY",
        "output_dir": str(output_dir),
        "dropzone_dir": str(dropzone),
        "hierarchy_locked": True,
        "required_snapshot_count": len(required),
        "files_found_count": files_found_count,
        "ready_snapshot_count": ready_snapshot_count,
        "waiting_snapshot_count": waiting_snapshot_count,
        "empty_file_count": empty_file_count,
        "cache_files_created_count": 0,
        "preferred_path_now": "LOCAL_EXPORT_IMPORT_FIRST",
        "api_binding_later": "GOOGLE_SHEETS_API_READONLY",
        "runtime_prompt_modified": False,
        "apply_allowed": False,
        "google_sheets_write": False,
        "live_google_api_call_from_python": False,
        "apps_script_execution": False,
        "clasp_push": False,
        "broker": False,
        "order": False,
        "sizing": False,
        "blocker_count": 0,
        "next": "P168G_LOCAL_CACHE_BUILD_FROM_OPERATOR_EXPORTS_OR_WAIT",
    }
    (output_dir / "P168F_SUMMARY.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    return summary


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=STEP)
    parser.add_argument("--project-dir", default=".", help="Repository/project root")
    args = parser.parse_args(argv)

    summary = build_capture(Path(args.project_dir))
    print("P168F_OPERATOR_EXPORT_CAPTURE_READY_WAIT_OPERATOR_FILES_READONLY")
    print(f"hierarchy_locked={summary['hierarchy_locked']}")
    print(f"required_snapshot_count={summary['required_snapshot_count']}")
    print(f"files_found_count={summary['files_found_count']}")
    print(f"ready_snapshot_count={summary['ready_snapshot_count']}")
    print(f"waiting_snapshot_count={summary['waiting_snapshot_count']}")
    print(f"cache_files_created_count={summary['cache_files_created_count']}")
    print(f"runtime_prompt_modified={summary['runtime_prompt_modified']}")
    print(f"apply_allowed={summary['apply_allowed']}")
    print(f"google_sheets_write={summary['google_sheets_write']}")
    print(f"live_google_api_call_from_python={summary['live_google_api_call_from_python']}")
    print(f"blocker_count={summary['blocker_count']}")
    print(f"output_dir={summary['output_dir']}")
    print(f"dropzone_dir={summary['dropzone_dir']}")
    print(f"next={summary['next']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
