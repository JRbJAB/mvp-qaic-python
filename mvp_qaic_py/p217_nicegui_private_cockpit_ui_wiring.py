from __future__ import annotations

from pathlib import Path
from typing import Any

from mvp_qaic_py.p216_private_cockpit_runtime_bundle import (
    build_private_cockpit_runtime_bundle,
    build_private_cockpit_runtime_summary,
)


def build_nicegui_private_cockpit_view_model(
    project_root: str | Path,
    output_dir: str | Path,
    *,
    gem_response_text: str,
    card_id: str | None = None,
    query: str = "",
    generated_at: str | None = None,
    execute_export: bool = False,
) -> dict[str, Any]:
    bundle = build_private_cockpit_runtime_bundle(
        project_root,
        output_dir,
        gem_response_text=gem_response_text,
        card_id=card_id,
        query=query,
        generated_at=generated_at,
        execute_export=execute_export,
    )
    summary = build_private_cockpit_runtime_summary(bundle)

    decision = bundle.get("decision_header", {})
    cockpit = bundle.get("cockpit", {})
    response_panel = bundle.get("response_draft_panel", {})
    export_runtime = bundle.get("export_runtime", {})

    status = "OK_P217_NICEGUI_PRIVATE_COCKPIT_VIEW_MODEL_READY"
    if str(bundle["STATUS"]).startswith("REVIEW_"):
        status = "REVIEW_P217_NICEGUI_PRIVATE_COCKPIT_VIEW_MODEL"
    elif str(bundle["STATUS"]).startswith("BLOCKED_"):
        status = "BLOCKED_P217_NICEGUI_PRIVATE_COCKPIT_VIEW_MODEL"

    view_model = {
        "header": {
            "title": cockpit.get("title", "MVP QAIC Private Prompt Cockpit"),
            "subtitle": cockpit.get(
                "subtitle",
                "Historique prompts, réponse GEM, brouillon local review-only",
            ),
            "status": status,
            "bundle_status": bundle["STATUS"],
        },
        "tabs": [
            {"id": "prompt_history", "label": "Historique prompts"},
            {"id": "response_draft", "label": "Brouillon GEM"},
            {"id": "local_export", "label": "Export local"},
            {"id": "safety", "label": "Safety"},
        ],
        "cards": [
            {
                "id": "prompt_history",
                "title": "Prompt History",
                "status": decision.get("prompt_history_status"),
                "lines": [
                    f"Status: {decision.get('prompt_history_status')}",
                    "Mode: local private review-only",
                ],
            },
            {
                "id": "response_draft",
                "title": "Response Draft",
                "status": decision.get("response_draft_status"),
                "lines": [
                    f"Status: {decision.get('response_draft_status')}",
                    f"Draft: {response_panel.get('draft_id')}",
                    f"Save enabled: {response_panel.get('decision_header', {}).get('save_enabled')}",
                ],
            },
            {
                "id": "local_export",
                "title": "Local Export",
                "status": decision.get("export_status"),
                "lines": [
                    f"Status: {decision.get('export_status')}",
                    f"Export allowed: {decision.get('export_allowed')}",
                    f"Files written: {decision.get('files_written')}",
                    f"JSON: {export_runtime.get('json_path')}",
                    f"MD: {export_runtime.get('md_path')}",
                ],
            },
        ],
        "actions": [
            {
                "id": "select_prompt",
                "label": "Sélectionner prompt",
                "enabled": True,
            },
            {
                "id": "preview_response_draft",
                "label": "Prévisualiser brouillon",
                "enabled": True,
            },
            {
                "id": "save_response_draft_local",
                "label": "Sauver brouillon local",
                "enabled": bool(decision.get("export_allowed")),
            },
            {
                "id": "review_only_mark",
                "label": "Review-only",
                "enabled": True,
            },
        ],
        "safety": {
            "local_only": True,
            "review_only": True,
            "server_started": False,
            "browser_started": False,
            "gem_call_executed": False,
            "provider_call_executed": False,
            "auto_apply_gem_response": False,
            "broker": False,
            "order": False,
            "sizing": False,
        },
    }

    return {
        "STATUS": status,
        "bundle_status": bundle["STATUS"],
        "blocker_count": bundle.get("blocker_count", 0),
        "blockers": bundle.get("blockers", []),
        "view_model": view_model,
        "summary": summary,
        "bundle": bundle,
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
        "recommended_next": "P218_NICEGUI_PRIVATE_COCKPIT_VISUAL_SMOKE_FAST_FUSE",
    }


def render_nicegui_private_cockpit(ui: Any, view_model_payload: dict[str, Any]) -> dict[str, Any]:
    view = view_model_payload["view_model"]
    rendered: list[dict[str, Any]] = []

    header = view["header"]
    ui.label(header["title"])
    rendered.append({"type": "label", "text": header["title"]})
    ui.label(header["subtitle"])
    rendered.append({"type": "label", "text": header["subtitle"]})
    ui.label(f"Status: {header['status']}")
    rendered.append({"type": "label", "text": f"Status: {header['status']}"})

    for card in view["cards"]:
        ui.label(card["title"])
        rendered.append({"type": "card_title", "text": card["title"]})
        for line in card["lines"]:
            ui.label(line)
            rendered.append({"type": "card_line", "text": line})

    for action in view["actions"]:
        ui.button(action["label"])
        rendered.append(
            {
                "type": "button",
                "id": action["id"],
                "label": action["label"],
                "enabled": action["enabled"],
            }
        )

    return {
        "STATUS": "OK_P217_NICEGUI_PRIVATE_COCKPIT_RENDERED_WITH_UI_ADAPTER",
        "rendered_count": len(rendered),
        "rendered": rendered,
        "server_started": False,
        "browser_started": False,
        "gem_call_executed": False,
        "provider_call_executed": False,
        "broker": False,
        "order": False,
        "sizing": False,
    }


def main() -> None:
    import argparse
    import json

    parser = argparse.ArgumentParser()
    parser.add_argument("--project-root", default=".")
    parser.add_argument("--output-dir", required=True)
    parser.add_argument("--gem-response-text", required=True)
    parser.add_argument("--card-id", default=None)
    parser.add_argument("--query", default="")
    parser.add_argument("--generated-at", default=None)
    parser.add_argument("--execute-export", action="store_true")
    args = parser.parse_args()

    payload = build_nicegui_private_cockpit_view_model(
        args.project_root,
        args.output_dir,
        gem_response_text=args.gem_response_text,
        card_id=args.card_id,
        query=args.query,
        generated_at=args.generated_at,
        execute_export=args.execute_export,
    )
    print(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
