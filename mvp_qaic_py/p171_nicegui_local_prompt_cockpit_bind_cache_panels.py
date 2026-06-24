from __future__ import annotations

import argparse
import csv
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from mvp_qaic_py.p170_nicegui_local_cache_read_binding import build_local_cache_binding_payload


SAFETY_FLAGS: dict[str, bool] = {
    "google_sheets_write": False,
    "live_google_api_call_from_python": False,
    "apps_script_execution": False,
    "clasp_push": False,
    "public_serve": False,
    "broker": False,
    "order": False,
    "sizing": False,
    "raw_operator_exports_committed": False,
}


def _utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def build_cockpit_panel_model(
    project_root: str | Path,
    *,
    preview_limit: int = 5,
    generated_at: str | None = None,
) -> dict[str, Any]:
    root = Path(project_root)
    p170_payload = build_local_cache_binding_payload(root, preview_limit=preview_limit)
    generated = generated_at or _utc_now()

    panels: list[dict[str, Any]] = []
    blockers: list[str] = list(p170_payload.get("blockers", []))

    for panel in p170_payload.get("panels", []):
        panel_id = f"p171_{panel['ui_slot']}"
        panels.append(
            {
                "panel_id": panel_id,
                "ui_slot": panel["ui_slot"],
                "panel_title": panel["panel_title"],
                "source_id": panel["source_id"],
                "file_name": panel["file_name"],
                "row_count": panel["row_count"],
                "component_type": "nicegui_local_cache_panel",
                "binding_mode": "LOCAL_CACHE_READ_ONLY",
                "visible_in_private_cockpit": True,
                "write_allowed": False,
                "live_api_allowed": False,
                "human_review_required": True,
                "operator_action": "READ_REVIEW_ONLY",
            }
        )

    ready_panel_count = len(panels)
    cockpit_ready = (
        bool(p170_payload.get("binding_ready")) and ready_panel_count == 5 and not blockers
    )

    return {
        "STATUS": "OK_P171_NICEGUI_LOCAL_PROMPT_COCKPIT_PANELS_READY_REVIEW_ONLY"
        if cockpit_ready
        else "BLOCKED_P171_NICEGUI_LOCAL_PROMPT_COCKPIT_PANELS",
        "generated_at": generated,
        "project_root": str(root),
        "source_step": "P170_NICEGUI_LOCAL_CACHE_READ_BINDING",
        "cache_dir": p170_payload.get("cache_dir"),
        "panel_count": len(panels),
        "ready_panel_count": ready_panel_count,
        "cockpit_ready": cockpit_ready,
        "blocker_count": len(blockers),
        "blockers": blockers,
        "panels": panels,
        "private_routes": [
            {
                "route": "/",
                "route_id": "local_prompt_cockpit_home",
                "purpose": "Private local cockpit home",
                "public_access_allowed": False,
            },
            {
                "route": "/cache",
                "route_id": "local_cache_panels",
                "purpose": "Read-only cache panels",
                "public_access_allowed": False,
            },
            {
                "route": "/review",
                "route_id": "human_review_workbench",
                "purpose": "Prompt review workbench",
                "public_access_allowed": False,
            },
        ],
        "recommended_launch_host": "127.0.0.1",
        "recommended_launch_port": 8088,
        **SAFETY_FLAGS,
        "recommended_next": "P172_NICEGUI_PRIVATE_COCKPIT_RENDER_LOCAL_CACHE_PANELS",
    }


def export_cockpit_panel_model(
    project_root: str | Path,
    *,
    export_dir: str | Path | None = None,
    preview_limit: int = 5,
) -> dict[str, Any]:
    root = Path(project_root)
    if export_dir is None:
        stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        export_path = (
            root / "05_EXPORTS" / f"P171_NICEGUI_LOCAL_PROMPT_COCKPIT_CACHE_PANELS_{stamp}"
        )
    else:
        export_path = Path(export_dir)

    export_path.mkdir(parents=True, exist_ok=True)
    payload = build_cockpit_panel_model(root, preview_limit=preview_limit)
    payload["export_dir"] = str(export_path)

    (export_path / "P171_COCKPIT_PANEL_MODEL.json").write_text(
        json.dumps(payload, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )

    summary_keys = [
        "STATUS",
        "generated_at",
        "project_root",
        "source_step",
        "cache_dir",
        "export_dir",
        "panel_count",
        "ready_panel_count",
        "cockpit_ready",
        "blocker_count",
        "blockers",
        "recommended_launch_host",
        "recommended_launch_port",
        "google_sheets_write",
        "live_google_api_call_from_python",
        "apps_script_execution",
        "clasp_push",
        "public_serve",
        "broker",
        "order",
        "sizing",
        "raw_operator_exports_committed",
        "recommended_next",
    ]
    (export_path / "P171_SUMMARY.json").write_text(
        json.dumps({key: payload[key] for key in summary_keys}, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )

    with (export_path / "P171_NICEGUI_PANEL_MODEL.csv").open(
        "w", encoding="utf-8", newline=""
    ) as file_obj:
        fieldnames = [
            "panel_id",
            "ui_slot",
            "panel_title",
            "source_id",
            "file_name",
            "row_count",
            "component_type",
            "binding_mode",
            "visible_in_private_cockpit",
            "write_allowed",
            "live_api_allowed",
            "human_review_required",
            "operator_action",
        ]
        writer = csv.DictWriter(file_obj, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(payload["panels"])

    report_lines = [
        "# P171 NiceGUI Local Prompt Cockpit Cache Panels",
        "",
        f"- STATUS: {payload['STATUS']}",
        f"- panel_count: {payload['panel_count']}",
        f"- ready_panel_count: {payload['ready_panel_count']}",
        f"- cockpit_ready: {payload['cockpit_ready']}",
        f"- blocker_count: {payload['blocker_count']}",
        "",
        "Decision:",
        "- Prepare five private NiceGUI cache panels from P170.",
        "- Keep launch private on 127.0.0.1 only.",
        "- Do not use Google Sheets live API yet.",
        "- Do not write Sheets.",
        "- Do not expose public route.",
        "",
        "Safety:",
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
        "- P172_NICEGUI_PRIVATE_COCKPIT_RENDER_LOCAL_CACHE_PANELS",
    ]
    (export_path / "P171_COCKPIT_PANEL_MODEL_REPORT.md").write_text(
        "\n".join(report_lines) + "\n",
        encoding="utf-8",
    )

    return payload


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Build P171 NiceGUI local cockpit panel model.")
    parser.add_argument("--project-root", default=".")
    parser.add_argument("--export-dir", default=None)
    parser.add_argument("--preview-limit", type=int, default=5)
    parser.add_argument("--write-export", action="store_true")
    parser.add_argument("--json", action="store_true")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = _build_parser().parse_args(argv)
    if args.write_export:
        payload = export_cockpit_panel_model(
            args.project_root,
            export_dir=args.export_dir,
            preview_limit=args.preview_limit,
        )
    else:
        payload = build_cockpit_panel_model(args.project_root, preview_limit=args.preview_limit)

    if args.json:
        print(json.dumps(payload, indent=2, ensure_ascii=False))
    else:
        print(payload["STATUS"])
        print(f"PANEL_COUNT={payload['panel_count']}")
        print(f"READY_PANEL_COUNT={payload['ready_panel_count']}")
        print(f"COCKPIT_READY={payload['cockpit_ready']}")
        print(f"BLOCKER_COUNT={payload['blocker_count']}")

    return 0 if payload["cockpit_ready"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
