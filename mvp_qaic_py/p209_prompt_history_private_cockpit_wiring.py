from __future__ import annotations

from pathlib import Path
from typing import Any

from mvp_qaic_py.p208_prompt_history_ui_binding import (
    build_prompt_history_ui_binding,
    build_prompt_history_ui_markdown,
)


def build_prompt_history_private_cockpit_panel(
    project_root: str | Path,
    *,
    query: str = "",
    generated_at: str | None = None,
    max_cards: int = 50,
) -> dict[str, Any]:
    binding = build_prompt_history_ui_binding(
        project_root,
        query=query,
        generated_at=generated_at,
        max_cards=max_cards,
    )

    ui = binding.get("ui", {})
    cards = list(binding.get("cards", []))

    panel_status = "OK_P209_PROMPT_HISTORY_PRIVATE_COCKPIT_PANEL_READY"
    if binding["STATUS"].startswith("REVIEW_"):
        panel_status = "REVIEW_P209_PROMPT_HISTORY_PRIVATE_COCKPIT_PANEL"

    return {
        "STATUS": panel_status,
        "source_status": binding["STATUS"],
        "generated_at": binding.get("generated_at"),
        "project_root": binding.get("project_root"),
        "panel": {
            "panel_id": "prompt_history_library",
            "title": ui.get("title", "Prompt History Library"),
            "subtitle": ui.get(
                "subtitle",
                "Historique local des prompts, captures et réponses GEM",
            ),
            "route_hint": "/prompt-history",
            "search_placeholder": ui.get(
                "search_placeholder",
                "Rechercher prompt, GEM, capture, session...",
            ),
            "tabs": ui.get("tabs", []),
            "primary_actions": ui.get("primary_actions", []),
        },
        "decision_header": {
            "main_status": panel_status,
            "library_entry_count": binding.get("library_entry_count", 0),
            "filtered_entry_count": binding.get("filtered_entry_count", 0),
            "card_count": binding.get("card_count", 0),
            "query": binding.get("query", query),
            "next_action": "P210_PROMPT_HISTORY_OPERATOR_WORKFLOW_FAST_FUSE",
        },
        "counters": binding.get("counters", {}),
        "cards": cards,
        "markdown_preview": build_prompt_history_ui_markdown(binding),
        "local_only": True,
        "review_only": True,
        "server_started": False,
        "browser_started": False,
        "gem_call_executed": False,
        "auto_apply_gem_response": False,
        "google_sheets_write": False,
        "apps_script_execution": False,
        "broker": False,
        "order": False,
        "sizing": False,
        "recommended_next": "P210_PROMPT_HISTORY_OPERATOR_WORKFLOW_FAST_FUSE",
    }


def build_private_cockpit_prompt_history_sections(
    project_root: str | Path,
    *,
    queries: tuple[str, ...] = ("", "gem", "session"),
    generated_at: str | None = None,
) -> dict[str, Any]:
    panels = [
        build_prompt_history_private_cockpit_panel(
            project_root,
            query=query,
            generated_at=generated_at,
        )
        for query in queries
    ]

    blocked = [panel for panel in panels if panel["STATUS"].startswith("BLOCKED_")]
    review = [panel for panel in panels if panel["STATUS"].startswith("REVIEW_")]

    status = "OK_P209_PROMPT_HISTORY_PRIVATE_COCKPIT_SECTIONS_READY"
    if blocked:
        status = "BLOCKED_P209_PROMPT_HISTORY_PRIVATE_COCKPIT_SECTIONS"
    elif review:
        status = "REVIEW_P209_PROMPT_HISTORY_PRIVATE_COCKPIT_SECTIONS"

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
        "auto_apply_gem_response": False,
        "google_sheets_write": False,
        "apps_script_execution": False,
        "broker": False,
        "order": False,
        "sizing": False,
        "recommended_next": "P210_PROMPT_HISTORY_OPERATOR_WORKFLOW_FAST_FUSE",
    }


def main() -> None:
    import argparse
    import json

    parser = argparse.ArgumentParser()
    parser.add_argument("--project-root", default=".")
    parser.add_argument("--query", default="")
    parser.add_argument("--generated-at", default=None)
    args = parser.parse_args()

    payload = build_prompt_history_private_cockpit_panel(
        args.project_root,
        query=args.query,
        generated_at=args.generated_at,
    )
    print(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
