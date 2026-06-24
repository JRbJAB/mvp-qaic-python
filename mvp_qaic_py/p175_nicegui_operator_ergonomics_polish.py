from __future__ import annotations

import argparse
import csv
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from mvp_qaic_py.p172_nicegui_private_cockpit_render_local_cache_panels import (
    build_private_cockpit_render_model,
)


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
    "auto_apply_gem_response": False,
}


def _utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def build_operator_ergonomics_model(
    project_root: str | Path,
    *,
    preview_limit: int = 5,
    generated_at: str | None = None,
) -> dict[str, Any]:
    root = Path(project_root)
    render_payload = build_private_cockpit_render_model(root, preview_limit=preview_limit)
    blockers: list[str] = list(render_payload.get("blockers", []))
    generated = generated_at or _utc_now()

    tabs: list[dict[str, Any]] = [
        {
            "tab_id": "dashboard",
            "label": "Dashboard",
            "purpose": "Vue rapide état cache, prompts, review, journal.",
            "default_visible": True,
            "route": "/",
            "component_hint": "ui.tabs + status cards",
        },
        {
            "tab_id": "prompt",
            "label": "Prompt GEM",
            "purpose": "Préparer/copier le prompt opérateur image/portfolio.",
            "default_visible": True,
            "route": "/prompt",
            "component_hint": "ui.textarea + copy button + prompt source selector",
        },
        {
            "tab_id": "cache",
            "label": "Cache local",
            "purpose": "Voir les 5 sources locales read-only.",
            "default_visible": True,
            "route": "/cache",
            "component_hint": "ui.table + filters",
        },
        {
            "tab_id": "review",
            "label": "Review",
            "purpose": "Traiter les lignes PENDING en review-only.",
            "default_visible": True,
            "route": "/review",
            "component_hint": "ui.table + status chips",
        },
        {
            "tab_id": "journal",
            "label": "Journal",
            "purpose": "Consulter les décisions et smoke runs.",
            "default_visible": True,
            "route": "/journal",
            "component_hint": "ui.timeline + ui.table",
        },
        {
            "tab_id": "lexique",
            "label": "Lexique",
            "purpose": "Explorer les éléments lexique/cockpit disponibles.",
            "default_visible": True,
            "route": "/lexique",
            "component_hint": "search input + ui.table",
        },
    ]

    actions: list[dict[str, Any]] = [
        {
            "action_id": "copy_prompt",
            "label": "Copier prompt",
            "mode": "LOCAL_UI_ONLY",
            "allowed": True,
            "requires_human": True,
            "writes_data": False,
        },
        {
            "action_id": "save_gem_response_local_file",
            "label": "Sauver réponse GEM localement",
            "mode": "LOCAL_FILE_REVIEW_ONLY",
            "allowed": True,
            "requires_human": True,
            "writes_data": False,
        },
        {
            "action_id": "mark_review_decision_local_preview",
            "label": "Prévisualiser décision review",
            "mode": "PREVIEW_ONLY",
            "allowed": True,
            "requires_human": True,
            "writes_data": False,
        },
        {
            "action_id": "refresh_google_sheets_live",
            "label": "Refresh Google Sheets live",
            "mode": "BLOCKED_FOR_NOW",
            "allowed": False,
            "requires_human": True,
            "writes_data": False,
        },
        {
            "action_id": "apply_prompt_patch",
            "label": "Apply prompt patch",
            "mode": "BLOCKED_UNTIL_EXPLICIT_GATE",
            "allowed": False,
            "requires_human": True,
            "writes_data": False,
        },
    ]

    panels = render_payload.get("render_panels", [])
    ready_panel_count = len(panels)
    ergonomics_ready = (
        bool(render_payload.get("render_ready")) and ready_panel_count == 5 and not blockers
    )

    return {
        "STATUS": "OK_P175_NICEGUI_OPERATOR_ERGONOMICS_POLISH_READY_REVIEW_ONLY"
        if ergonomics_ready
        else "BLOCKED_P175_NICEGUI_OPERATOR_ERGONOMICS_POLISH",
        "generated_at": generated,
        "project_root": str(root),
        "source_step": "P174_NICEGUI_PRIVATE_LOCAL_LAUNCH_OPERATOR_SMOKE",
        "tab_count": len(tabs),
        "action_count": len(actions),
        "panel_count": ready_panel_count,
        "ergonomics_ready": ergonomics_ready,
        "blocker_count": len(blockers),
        "blockers": blockers,
        "tabs": tabs,
        "actions": actions,
        "panels": [
            {
                "panel_id": panel["panel_id"],
                "panel_title": panel["panel_title"],
                "source_id": panel["source_id"],
                "row_count": panel["row_count"],
                "default_tab": _default_tab_for_panel(panel["ui_slot"]),
                "filterable": True,
                "copyable": True,
                "read_only": True,
            }
            for panel in panels
        ],
        "navigation_model": {
            "host": "127.0.0.1",
            "port": 8088,
            "default_route": "/",
            "public_access_allowed": False,
        },
        **SAFETY_FLAGS,
        "recommended_next": "P176_NICEGUI_REVIEW_ONLY_ACTIONS_AND_PROMPT_WORKFLOW",
    }


def _default_tab_for_panel(ui_slot: str) -> str:
    mapping = {
        "cockpit_bootstrap": "dashboard",
        "prompt_source_selector": "prompt",
        "decision_history_panel": "journal",
        "human_review_workbench_panel": "review",
        "lexique_context_panel": "lexique",
    }
    return mapping.get(ui_slot, "cache")


def export_operator_ergonomics_model(
    project_root: str | Path,
    *,
    export_dir: str | Path | None = None,
    preview_limit: int = 5,
) -> dict[str, Any]:
    root = Path(project_root)
    if export_dir is None:
        stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        export_path = root / "05_EXPORTS" / f"P175_NICEGUI_OPERATOR_ERGONOMICS_POLISH_{stamp}"
    else:
        export_path = Path(export_dir)

    export_path.mkdir(parents=True, exist_ok=True)
    payload = build_operator_ergonomics_model(root, preview_limit=preview_limit)
    payload["export_dir"] = str(export_path)

    (export_path / "P175_OPERATOR_ERGONOMICS_MODEL.json").write_text(
        json.dumps(payload, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )

    summary_keys = [
        "STATUS",
        "generated_at",
        "project_root",
        "source_step",
        "export_dir",
        "tab_count",
        "action_count",
        "panel_count",
        "ergonomics_ready",
        "blocker_count",
        "blockers",
        "google_sheets_write",
        "live_google_api_call_from_python",
        "apps_script_execution",
        "clasp_push",
        "public_serve",
        "broker",
        "order",
        "sizing",
        "raw_operator_exports_committed",
        "auto_apply_gem_response",
        "recommended_next",
    ]
    (export_path / "P175_SUMMARY.json").write_text(
        json.dumps({key: payload[key] for key in summary_keys}, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )

    with (export_path / "P175_UI_TABS.csv").open("w", encoding="utf-8", newline="") as file_obj:
        writer = csv.DictWriter(
            file_obj,
            fieldnames=["tab_id", "label", "purpose", "default_visible", "route", "component_hint"],
        )
        writer.writeheader()
        writer.writerows(payload["tabs"])

    with (export_path / "P175_UI_ACTIONS.csv").open("w", encoding="utf-8", newline="") as file_obj:
        writer = csv.DictWriter(
            file_obj,
            fieldnames=["action_id", "label", "mode", "allowed", "requires_human", "writes_data"],
        )
        writer.writeheader()
        writer.writerows(payload["actions"])

    report = [
        "# P175 NiceGUI Operator Ergonomics Polish",
        "",
        f"- STATUS: {payload['STATUS']}",
        f"- tab_count: {payload['tab_count']}",
        f"- action_count: {payload['action_count']}",
        f"- panel_count: {payload['panel_count']}",
        f"- ergonomics_ready: {payload['ergonomics_ready']}",
        f"- blocker_count: {payload['blocker_count']}",
        "",
        "UI cible:",
        "- Dashboard",
        "- Prompt GEM",
        "- Cache local",
        "- Review",
        "- Journal",
        "- Lexique",
        "",
        "Actions opérateur:",
        "- Copier prompt: allowed",
        "- Sauver réponse GEM localement: allowed review-only",
        "- Prévisualiser décision review: allowed preview-only",
        "- Refresh Google Sheets live: blocked",
        "- Apply prompt patch: blocked until explicit gate",
        "",
        "Safety:",
        "- PUBLIC_SERVE=False",
        "- GOOGLE_SHEETS_WRITE=False",
        "- LIVE_GOOGLE_API_CALL_FROM_PYTHON=False",
        "- APPS_SCRIPT_EXECUTION=False",
        "- CLASP_PUSH=False",
        "- BROKER=False",
        "- ORDER=False",
        "- SIZING=False",
        "- AUTO_APPLY_GEM_RESPONSE=False",
        "",
        "Next:",
        "- P176_NICEGUI_REVIEW_ONLY_ACTIONS_AND_PROMPT_WORKFLOW",
    ]
    (export_path / "P175_OPERATOR_ERGONOMICS_REPORT.md").write_text(
        "\n".join(report) + "\n",
        encoding="utf-8",
    )

    return payload


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="P175 NiceGUI operator ergonomics polish.")
    parser.add_argument("--project-root", default=".")
    parser.add_argument("--export-dir", default=None)
    parser.add_argument("--preview-limit", type=int, default=5)
    parser.add_argument("--write-export", action="store_true")
    parser.add_argument("--json", action="store_true")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = _build_parser().parse_args(argv)
    if args.write_export:
        payload = export_operator_ergonomics_model(
            args.project_root,
            export_dir=args.export_dir,
            preview_limit=args.preview_limit,
        )
    else:
        payload = build_operator_ergonomics_model(
            args.project_root, preview_limit=args.preview_limit
        )

    if args.json:
        print(json.dumps(payload, indent=2, ensure_ascii=False))
    else:
        print(payload["STATUS"])
        print(f"TAB_COUNT={payload['tab_count']}")
        print(f"ACTION_COUNT={payload['action_count']}")
        print(f"ERGONOMICS_READY={payload['ergonomics_ready']}")
        print(f"BLOCKER_COUNT={payload['blocker_count']}")

    return 0 if payload["ergonomics_ready"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
