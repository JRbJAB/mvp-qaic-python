from __future__ import annotations

from pathlib import Path
from typing import Any

from mvp_qaic_py.p211_prompt_history_response_save_draft import (
    build_response_draft_markdown,
    build_response_draft_payload,
)


def build_response_draft_ui_payload(
    project_root: str | Path,
    *,
    gem_response_text: str,
    card_id: str | None = None,
    query: str = "",
    generated_at: str | None = None,
) -> dict[str, Any]:
    draft = build_response_draft_payload(
        project_root,
        card_id=card_id,
        query=query,
        gem_response_text=gem_response_text,
        generated_at=generated_at,
    )

    status = "OK_P212_PROMPT_HISTORY_RESPONSE_DRAFT_UI_READY"
    if draft["STATUS"].startswith("REVIEW_"):
        status = "REVIEW_P212_PROMPT_HISTORY_RESPONSE_DRAFT_UI"

    write_plan = draft.get("write_plan", {})
    source_path = draft.get("source_prompt_path")
    source_title = draft.get("source_prompt_title")

    ui_payload = {
        "header": {
            "title": "GEM Response Draft",
            "subtitle": "Préparer, relire et sauvegarder une réponse GEM locale",
            "status": status,
        },
        "source_prompt_card": {
            "title": source_title or "Prompt non sélectionné",
            "path": source_path,
            "selection_status": "SELECTED" if source_path else "MISSING",
        },
        "response_editor": {
            "label": "Réponse GEM",
            "text_present": draft.get("response_text_present", False),
            "preview": draft.get("response_preview", ""),
            "max_preview_chars": 1200,
            "placeholder": "Coller ici la réponse GEM à sauvegarder localement.",
        },
        "save_plan_card": {
            "mode": write_plan.get("mode", "LOCAL_OPERATOR_REVIEW_ONLY"),
            "json_filename": write_plan.get("json_filename"),
            "md_filename": write_plan.get("md_filename"),
            "requires_human_review": True,
            "auto_apply_gem_response": False,
        },
        "actions": [
            {
                "action": "preview_response_draft",
                "label": "Prévisualiser brouillon",
                "enabled": True,
            },
            {
                "action": "save_response_draft_local",
                "label": "Sauver localement",
                "enabled": draft.get("response_text_present", False) and bool(source_path),
            },
            {
                "action": "mark_review_only",
                "label": "Marquer review-only",
                "enabled": True,
            },
        ],
    }

    return {
        "STATUS": status,
        "source_status": draft["STATUS"],
        "draft_id": draft["draft_id"],
        "blocker_count": draft.get("blocker_count", 0),
        "blockers": draft.get("blockers", []),
        "generated_at": draft.get("generated_at"),
        "project_root": draft.get("project_root"),
        "ui": ui_payload,
        "markdown_preview": build_response_draft_markdown(draft),
        "draft_payload": draft,
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
        "recommended_next": "P213_RESPONSE_DRAFT_PRIVATE_COCKPIT_WIRING_FAST_FUSE",
    }


def build_response_draft_ui_summary(payload: dict[str, Any]) -> dict[str, Any]:
    ui = payload.get("ui", {})
    save_plan = ui.get("save_plan_card", {})
    editor = ui.get("response_editor", {})
    source = ui.get("source_prompt_card", {})

    return {
        "STATUS": "OK_P212_RESPONSE_DRAFT_UI_SUMMARY_READY",
        "draft_id": payload.get("draft_id"),
        "source_selected": source.get("selection_status") == "SELECTED",
        "response_text_present": editor.get("text_present", False),
        "save_enabled": any(
            action.get("action") == "save_response_draft_local" and action.get("enabled") is True
            for action in ui.get("actions", [])
        ),
        "json_filename": save_plan.get("json_filename"),
        "md_filename": save_plan.get("md_filename"),
        "review_only": True,
        "auto_apply_gem_response": False,
        "server_started": False,
        "browser_started": False,
        "broker": False,
        "order": False,
        "sizing": False,
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

    payload = build_response_draft_ui_payload(
        args.project_root,
        gem_response_text=args.gem_response_text,
        card_id=args.card_id,
        query=args.query,
        generated_at=args.generated_at,
    )
    print(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
