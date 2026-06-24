from __future__ import annotations

import argparse
import csv
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


REQUIRED_CACHE_SOURCES: tuple[dict[str, str], ...] = (
    {
        "source_id": "config",
        "file_name": "MVP_QAIC_CONFIG.csv",
        "ui_slot": "cockpit_bootstrap",
        "panel_title": "Config cockpit",
    },
    {
        "source_id": "prompt_registry",
        "file_name": "MVP_QAIC_PROMPT_SOURCE_REGISTRY.csv",
        "ui_slot": "prompt_source_selector",
        "panel_title": "Prompt source registry",
    },
    {
        "source_id": "decision_journal",
        "file_name": "MVP_QAIC_DECISION_JOURNAL.csv",
        "ui_slot": "decision_history_panel",
        "panel_title": "Decision journal",
    },
    {
        "source_id": "prompt_review",
        "file_name": "MVP_QAIC_PROMPT_REVIEW_WORKBENCH.csv",
        "ui_slot": "human_review_workbench_panel",
        "panel_title": "Prompt review workbench",
    },
    {
        "source_id": "lexique_or_cockpit",
        "file_name": "MVP_QAIC_LEXIQUE_OR_COCKPIT_DATA.csv",
        "ui_slot": "lexique_context_panel",
        "panel_title": "Lexique or cockpit data",
    },
)

SAFETY_FLAGS: dict[str, bool] = {
    "google_sheets_write": False,
    "live_google_api_call_from_python": False,
    "apps_script_execution": False,
    "clasp_push": False,
    "broker": False,
    "order": False,
    "sizing": False,
    "raw_operator_exports_committed": False,
}


def _utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def _sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as file_obj:
        for chunk in iter(lambda: file_obj.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _read_csv_preview(
    path: Path, preview_limit: int
) -> tuple[list[str], list[dict[str, str]], int]:
    with path.open("r", encoding="utf-8-sig", newline="", errors="replace") as file_obj:
        rows = list(csv.reader(file_obj))

    if not rows:
        return [], [], 0

    header = [str(item) for item in rows[0]]
    preview: list[dict[str, str]] = []
    for raw_row in rows[1 : preview_limit + 1]:
        item = {}
        for index, column in enumerate(header):
            item[column] = str(raw_row[index]) if index < len(raw_row) else ""
        preview.append(item)

    return header, preview, max(len(rows) - 1, 0)


def build_local_cache_binding_payload(
    project_root: str | Path,
    *,
    preview_limit: int = 5,
    generated_at: str | None = None,
) -> dict[str, Any]:
    root = Path(project_root)
    cache_dir = root / "00_OPERATOR_EXPORTS" / "P168G_LOCAL_CACHE"
    generated = generated_at or _utc_now()

    sources: list[dict[str, Any]] = []
    panels: list[dict[str, Any]] = []
    blockers: list[str] = []

    for spec in REQUIRED_CACHE_SOURCES:
        path = cache_dir / spec["file_name"]
        if not path.exists():
            blockers.append(f"MISSING_CACHE_FILE:{spec['file_name']}")
            sources.append(
                {
                    **spec,
                    "exists": False,
                    "bytes": 0,
                    "sha256": "",
                    "header_count": 0,
                    "row_count": 0,
                    "preview_rows": [],
                    "binding_status": "BLOCKED_MISSING_CACHE",
                }
            )
            continue

        header, preview_rows, row_count = _read_csv_preview(path, preview_limit)
        source = {
            **spec,
            "exists": True,
            "bytes": path.stat().st_size,
            "sha256": _sha256_file(path),
            "header_count": len(header),
            "row_count": row_count,
            "preview_rows": preview_rows,
            "binding_status": "READY_FOR_NICEGUI_LOCAL_READ",
        }
        sources.append(source)
        panels.append(
            {
                "ui_slot": spec["ui_slot"],
                "panel_title": spec["panel_title"],
                "source_id": spec["source_id"],
                "file_name": spec["file_name"],
                "binding_mode": "LOCAL_CACHE_READ_ONLY",
                "preview_limit": preview_limit,
                "row_count": row_count,
                "write_allowed": False,
                "live_api_allowed": False,
                "human_review_required": True,
            }
        )

    ready_source_count = sum(
        1 for source in sources if source["binding_status"] == "READY_FOR_NICEGUI_LOCAL_READ"
    )
    binding_ready = ready_source_count == len(REQUIRED_CACHE_SOURCES) and not blockers

    return {
        "STATUS": "OK_P170_NICEGUI_LOCAL_CACHE_READ_BINDING_READY_REVIEW_ONLY"
        if binding_ready
        else "BLOCKED_P170_NICEGUI_LOCAL_CACHE_READ_BINDING",
        "generated_at": generated,
        "project_root": str(root),
        "cache_dir": str(cache_dir),
        "preview_limit": preview_limit,
        "cache_source_count": len(sources),
        "ready_source_count": ready_source_count,
        "panel_count": len(panels),
        "binding_ready": binding_ready,
        "blocker_count": len(blockers),
        "blockers": blockers,
        "sources": sources,
        "panels": panels,
        **SAFETY_FLAGS,
        "recommended_next": "P171_NICEGUI_LOCAL_PROMPT_COCKPIT_BIND_CACHE_PANELS",
    }


def export_local_cache_binding(
    project_root: str | Path,
    *,
    export_dir: str | Path | None = None,
    preview_limit: int = 5,
) -> dict[str, Any]:
    root = Path(project_root)
    if export_dir is None:
        stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        export_path = root / "05_EXPORTS" / f"P170_NICEGUI_LOCAL_CACHE_READ_BINDING_{stamp}"
    else:
        export_path = Path(export_dir)

    export_path.mkdir(parents=True, exist_ok=True)
    payload = build_local_cache_binding_payload(root, preview_limit=preview_limit)
    payload["export_dir"] = str(export_path)

    (export_path / "P170_NICEGUI_LOCAL_CACHE_BINDING_PAYLOAD.json").write_text(
        json.dumps(payload, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )
    (export_path / "P170_SUMMARY.json").write_text(
        json.dumps(
            {
                key: payload[key]
                for key in (
                    "STATUS",
                    "generated_at",
                    "project_root",
                    "cache_dir",
                    "export_dir",
                    "cache_source_count",
                    "ready_source_count",
                    "panel_count",
                    "binding_ready",
                    "blocker_count",
                    "blockers",
                    "google_sheets_write",
                    "live_google_api_call_from_python",
                    "apps_script_execution",
                    "clasp_push",
                    "broker",
                    "order",
                    "sizing",
                    "raw_operator_exports_committed",
                    "recommended_next",
                )
            },
            indent=2,
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )

    panel_csv = export_path / "P170_NICEGUI_PANEL_BINDING_MAP.csv"
    with panel_csv.open("w", encoding="utf-8", newline="") as file_obj:
        fieldnames = [
            "ui_slot",
            "panel_title",
            "source_id",
            "file_name",
            "binding_mode",
            "preview_limit",
            "row_count",
            "write_allowed",
            "live_api_allowed",
            "human_review_required",
        ]
        writer = csv.DictWriter(file_obj, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(payload["panels"])

    report_lines = [
        "# P170 NiceGUI Local Cache Read Binding",
        "",
        f"- STATUS: {payload['STATUS']}",
        f"- cache_source_count: {payload['cache_source_count']}",
        f"- ready_source_count: {payload['ready_source_count']}",
        f"- panel_count: {payload['panel_count']}",
        f"- binding_ready: {payload['binding_ready']}",
        f"- blocker_count: {payload['blocker_count']}",
        "",
        "Decision:",
        "- Bind the private NiceGUI cockpit to the local P168G cache.",
        "- Keep Google Sheets API read-only binding for a later phase.",
        "- Do not write Sheets.",
        "- Do not commit raw operator CSV files.",
        "",
        "Safety:",
        "- GOOGLE_SHEETS_WRITE=False",
        "- LIVE_GOOGLE_API_CALL_FROM_PYTHON=False",
        "- APPS_SCRIPT_EXECUTION=False",
        "- CLASP_PUSH=False",
        "- BROKER=False",
        "- ORDER=False",
        "- SIZING=False",
        "",
        "Next:",
        "- P171_NICEGUI_LOCAL_PROMPT_COCKPIT_BIND_CACHE_PANELS",
    ]
    (export_path / "P170_NICEGUI_LOCAL_CACHE_READ_BINDING_REPORT.md").write_text(
        "\n".join(report_lines) + "\n",
        encoding="utf-8",
    )

    return payload


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Build P170 NiceGUI local cache read binding payload."
    )
    parser.add_argument("--project-root", default=".", help="MVP_QAIC_PY project root")
    parser.add_argument("--export-dir", default=None, help="Optional export directory")
    parser.add_argument("--preview-limit", type=int, default=5)
    parser.add_argument("--write-export", action="store_true")
    parser.add_argument("--json", action="store_true")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = _build_parser().parse_args(argv)
    if args.write_export:
        payload = export_local_cache_binding(
            args.project_root,
            export_dir=args.export_dir,
            preview_limit=args.preview_limit,
        )
    else:
        payload = build_local_cache_binding_payload(
            args.project_root,
            preview_limit=args.preview_limit,
        )

    if args.json:
        print(json.dumps(payload, indent=2, ensure_ascii=False))
    else:
        print(payload["STATUS"])
        print(f"READY_SOURCE_COUNT={payload['ready_source_count']}")
        print(f"PANEL_COUNT={payload['panel_count']}")
        print(f"BINDING_READY={payload['binding_ready']}")
        print(f"BLOCKER_COUNT={payload['blocker_count']}")

    return 0 if payload["binding_ready"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
