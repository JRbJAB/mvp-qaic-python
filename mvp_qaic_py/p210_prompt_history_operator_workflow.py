from __future__ import annotations

from pathlib import Path
from typing import Any

from mvp_qaic_py.p209_prompt_history_private_cockpit_wiring import (
    build_prompt_history_private_cockpit_panel,
)

ALLOWED_ACTIONS = (
    "copy_prompt",
    "save_gem_response_local",
    "create_review_session",
)


def _find_card(cards: list[dict[str, Any]], card_id: str | None) -> dict[str, Any] | None:
    if not cards:
        return None
    if not card_id:
        return cards[0]
    for card in cards:
        if card.get("card_id") == card_id or card.get("path") == card_id:
            return card
    return None


def build_prompt_history_operator_workflow(
    project_root: str | Path,
    *,
    card_id: str | None = None,
    action: str = "copy_prompt",
    query: str = "",
    gem_response_text: str = "",
    generated_at: str | None = None,
) -> dict[str, Any]:
    panel_payload = build_prompt_history_private_cockpit_panel(
        project_root,
        query=query,
        generated_at=generated_at,
    )

    cards = list(panel_payload.get("cards", []))
    selected_card = _find_card(cards, card_id)

    blockers: list[str] = []
    if action not in ALLOWED_ACTIONS:
        blockers.append(f"UNSUPPORTED_ACTION:{action}")
    if selected_card is None:
        blockers.append("NO_PROMPT_CARD_SELECTED")
    if action == "save_gem_response_local" and not gem_response_text.strip():
        blockers.append("EMPTY_GEM_RESPONSE_TEXT")

    status = "OK_P210_PROMPT_HISTORY_OPERATOR_WORKFLOW_READY"
    if blockers:
        status = "REVIEW_P210_PROMPT_HISTORY_OPERATOR_WORKFLOW"

    workflow = {
        "action": action,
        "selected_card_id": selected_card.get("card_id") if selected_card else None,
        "selected_path": selected_card.get("path") if selected_card else None,
        "selected_title": selected_card.get("title") if selected_card else None,
        "copy_payload": {
            "copy_mode": "MANUAL_COPY_ONLY",
            "prompt_text_preview": selected_card.get("preview", "") if selected_card else "",
            "clipboard_access": False,
        },
        "save_response_payload": {
            "write_mode": "LOCAL_OPERATOR_REVIEW_ONLY",
            "gem_response_text_present": bool(gem_response_text.strip()),
            "auto_apply_gem_response": False,
        },
        "review_session_payload": {
            "session_mode": "REVIEW_ONLY",
            "source_path": selected_card.get("path") if selected_card else None,
            "requires_human_review": True,
        },
    }

    return {
        "STATUS": status,
        "blocker_count": len(blockers),
        "blockers": blockers,
        "generated_at": panel_payload.get("generated_at"),
        "project_root": panel_payload.get("project_root"),
        "panel_status": panel_payload.get("STATUS"),
        "query": query,
        "available_action_count": len(ALLOWED_ACTIONS),
        "allowed_actions": list(ALLOWED_ACTIONS),
        "selected_card_found": selected_card is not None,
        "workflow": workflow,
        "local_only": True,
        "review_only": True,
        "clipboard_access": False,
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
        "recommended_next": "P211_PROMPT_HISTORY_RESPONSE_SAVE_DRAFT_FAST_FUSE",
    }


def build_prompt_history_operator_action_menu() -> dict[str, Any]:
    return {
        "STATUS": "OK_P210_PROMPT_HISTORY_OPERATOR_ACTION_MENU_READY",
        "actions": [
            {
                "action": "copy_prompt",
                "label": "Copier le prompt",
                "mode": "MANUAL_COPY_ONLY",
            },
            {
                "action": "save_gem_response_local",
                "label": "Sauver réponse GEM localement",
                "mode": "LOCAL_OPERATOR_REVIEW_ONLY",
            },
            {
                "action": "create_review_session",
                "label": "Créer session review-only",
                "mode": "REVIEW_ONLY",
            },
        ],
        "local_only": True,
        "review_only": True,
        "clipboard_access": False,
        "server_started": False,
        "browser_started": False,
        "gem_call_executed": False,
        "broker": False,
        "order": False,
        "sizing": False,
    }


def main() -> None:
    import argparse
    import json

    parser = argparse.ArgumentParser()
    parser.add_argument("--project-root", default=".")
    parser.add_argument("--card-id", default=None)
    parser.add_argument("--action", default="copy_prompt")
    parser.add_argument("--query", default="")
    parser.add_argument("--gem-response-text", default="")
    parser.add_argument("--generated-at", default=None)
    args = parser.parse_args()

    payload = build_prompt_history_operator_workflow(
        args.project_root,
        card_id=args.card_id,
        action=args.action,
        query=args.query,
        gem_response_text=args.gem_response_text,
        generated_at=args.generated_at,
    )
    print(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
