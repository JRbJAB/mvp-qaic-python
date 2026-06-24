from __future__ import annotations

from pathlib import Path
from typing import Any

from mvp_qaic_py.p212_prompt_history_response_draft_ui import (
    build_response_draft_ui_payload,
    build_response_draft_ui_summary,
)


def build_response_draft_private_cockpit_panel(
    project_root: str | Path,
    *,
    gem_response_text: str,
    card_id: str | None = None,
    query: str = "",
    generated_at: str | None = None,
) -> dict[str, Any]:
    ui_payload = build_response_draft_ui_payload(
        project_root,
        gem_response_text=gem_response_text,
        card_id=card_id,
        query=query,
        generated_at=generated_at,
    )
    summary = build_response_draft_ui_summary(ui_payload)

    status = "OK_P213_RESPONSE_DRAFT_PRIVATE_COCKPIT_PANEL_READY"
    if ui_payload["STATUS"].startswith("REVIEW_"):
        status = "REVIEW_P213_RESPONSE_DRAFT_PRIVATE_COCKPIT_PANEL"
    elif ui_payload["STATUS"].startswith("BLOCKED_"):
        status = "BLOCKED_P213_RESPONSE_DRAFT_PRIVATE_COCKPIT_PANEL"

    ui = ui_payload.get("ui", {})
    source = ui.get("source_prompt_card", {})
    editor = ui.get("response_editor", {})
    save_plan = ui.get("save_plan_card", {})

    return {
        "STATUS": status,
        "source_status": ui_payload["STATUS"],
        "draft_id": ui_payload["draft_id"],
        "blocker_count": ui_payload.get("blocker_count", 0),
        "blockers": ui_payload.get("blockers", []),
        "generated_at": ui_payload.get("generated_at"),
        "project_root": ui_payload.get("project_root"),
        "panel": {
            "panel_id": "response_draft_review",
            "title": "GEM Response Draft Review",
            "subtitle": "Relire, préparer et sauvegarder un brouillon GEM local",
            "route_hint": "/response-draft",
            "main_status": status,
        },
        "decision_header": {
            "draft_id": ui_payload["draft_id"],
            "source_selected": source.get("selection_status") == "SELECTED",
            "response_text_present": editor.get("text_present", False),
            "save_enabled": summary.get("save_enabled", False),
            "next_action": "P214_RESPONSE_DRAFT_LOCAL_WRITE_GATE_FAST_FUSE",
        },
        "source_prompt_card": source,
        "response_editor": editor,
        "save_plan_card": save_plan,
        "actions": ui.get("actions", []),
        "summary": summary,
        "markdown_preview": ui_payload.get("markdown_preview", ""),
        "draft_ui_payload": ui_payload,
        "local_only": True,
        "review_only": True,
        "server_started": False,
        "browser_started": False,
        "gem_call_executed": False,
        "provider_call_executed": False,
        "auto_apply_gem_response": False,
        "google_sheets_write": False,
        "apps_script_execution": False,
        "broker": False,
        "order": False,
        "sizing": False,
        "recommended_next": "P214_RESPONSE_DRAFT_LOCAL_WRITE_GATE_FAST_FUSE",
    }


def build_response_draft_private_cockpit_sections(
    project_root: str | Path,
    *,
    gem_response_text: str,
    generated_at: str | None = None,
) -> dict[str, Any]:
    panels = [
        build_response_draft_private_cockpit_panel(
            project_root,
            gem_response_text=gem_response_text,
            query=query,
            generated_at=generated_at,
        )
        for query in ("", "gem", "session")
    ]

    blocked = [panel for panel in panels if panel["STATUS"].startswith("BLOCKED_")]
    review = [panel for panel in panels if panel["STATUS"].startswith("REVIEW_")]

    status = "OK_P213_RESPONSE_DRAFT_PRIVATE_COCKPIT_SECTIONS_READY"
    if blocked:
        status = "BLOCKED_P213_RESPONSE_DRAFT_PRIVATE_COCKPIT_SECTIONS"
    elif review:
        status = "REVIEW_P213_RESPONSE_DRAFT_PRIVATE_COCKPIT_SECTIONS"

    return {
        "STATUS": status,
        "panel_count": len(panels),
        "review_panel_count": len(review),
        "blocked_panel_count": len(blocked),
        "panels": panels,
        "local_only": True,
        "review_only": True,
        "server_started": False,
        "browser_started": False,
        "gem_call_executed": False,
        "provider_call_executed": False,
        "auto_apply_gem_response": False,
        "google_sheets_write": False,
        "apps_script_execution": False,
        "broker": False,
        "order": False,
        "sizing": False,
        "recommended_next": "P214_RESPONSE_DRAFT_LOCAL_WRITE_GATE_FAST_FUSE",
    }


def main() -> None:
    import argparse
    import json

    parser = argparse.ArgumentParser()
    parser.add_argument("--project-root", default=".")
    parser.add_argument("--gem-response-text", required=True)
    parser.add_argument("--card-id", default=None)
    parser.add_argument("--query", default="")
    parser.add_argument("--generated-at", default=None)
    args = parser.parse_args()

    payload = build_response_draft_private_cockpit_panel(
        args.project_root,
        gem_response_text=args.gem_response_text,
        card_id=args.card_id,
        query=args.query,
        generated_at=args.generated_at,
    )
    print(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
