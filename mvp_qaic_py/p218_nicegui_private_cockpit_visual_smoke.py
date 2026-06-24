from __future__ import annotations

from html import escape
import json
from pathlib import Path
from typing import Any

from mvp_qaic_py.p217_nicegui_private_cockpit_ui_wiring import (
    build_nicegui_private_cockpit_view_model,
)


def _response_preview_from_view_model(view_model_payload: dict[str, Any]) -> str:
    return str(
        view_model_payload.get("bundle", {})
        .get("response_draft_panel", {})
        .get("response_editor", {})
        .get("preview", "")
        or ""
    )


def build_private_cockpit_static_html(view_model_payload: dict[str, Any]) -> str:
    view = view_model_payload["view_model"]
    header = view["header"]
    cards = view.get("cards", [])
    actions = view.get("actions", [])
    safety = view.get("safety", {})
    response_preview = _response_preview_from_view_model(view_model_payload)

    card_html = "\n".join(
        [
            "<section class='card'>"
            f"<h2>{escape(str(card.get('title', '')))}</h2>"
            f"<p class='status'>{escape(str(card.get('status', '')))}</p>"
            + "".join(f"<p>{escape(str(line))}</p>" for line in card.get("lines", []))
            + "</section>"
            for card in cards
        ]
    )

    response_preview_html = (
        "<section class='card response-preview'>"
        "<h2>Response Preview</h2>"
        f"<pre>{escape(response_preview)}</pre>"
        "</section>"
        if response_preview
        else ""
    )

    action_html = "\n".join(
        [
            "<button "
            f"data-action='{escape(str(action.get('id', '')))}' "
            f"{'' if action.get('enabled') else 'disabled'}>"
            f"{escape(str(action.get('label', '')))}"
            "</button>"
            for action in actions
        ]
    )

    safety_html = "\n".join(
        [
            f"<li>{escape(str(key))}: <strong>{escape(str(value))}</strong></li>"
            for key, value in safety.items()
        ]
    )

    return "\n".join(
        [
            "<!doctype html>",
            "<html lang='fr'>",
            "<head>",
            "<meta charset='utf-8'>",
            "<title>MVP QAIC Private Prompt Cockpit</title>",
            "<style>",
            "body{font-family:Arial,sans-serif;margin:24px;background:#f6f7fb;color:#111827}",
            ".shell{max-width:1180px;margin:auto}",
            ".hero{background:white;border-radius:18px;padding:22px;margin-bottom:18px;box-shadow:0 2px 12px #0001}",
            ".grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(260px,1fr));gap:14px}",
            ".card{background:white;border-radius:16px;padding:16px;box-shadow:0 2px 12px #0001}",
            ".status{font-weight:bold;color:#374151}",
            ".actions{display:flex;flex-wrap:wrap;gap:10px;margin:18px 0}",
            "button{border:0;border-radius:12px;padding:10px 14px;background:#111827;color:white}",
            "button:disabled{background:#9ca3af}",
            ".safety{background:white;border-radius:16px;padding:16px;box-shadow:0 2px 12px #0001}",
            "pre{white-space:pre-wrap;word-break:break-word;background:#f3f4f6;border-radius:12px;padding:12px}",
            "</style>",
            "</head>",
            "<body>",
            "<main class='shell'>",
            "<section class='hero'>",
            f"<h1>{escape(str(header.get('title', '')))}</h1>",
            f"<p>{escape(str(header.get('subtitle', '')))}</p>",
            f"<p class='status'>Status: {escape(str(header.get('status', '')))}</p>",
            "</section>",
            "<section class='grid'>",
            card_html,
            response_preview_html,
            "</section>",
            "<section class='actions'>",
            action_html,
            "</section>",
            "<section class='safety'>",
            "<h2>Safety</h2>",
            f"<ul>{safety_html}</ul>",
            "</section>",
            "</main>",
            "</body>",
            "</html>",
        ]
    )


def build_private_cockpit_visual_smoke_payload(
    project_root: str | Path,
    output_dir: str | Path,
    *,
    gem_response_text: str,
    card_id: str | None = None,
    query: str = "",
    generated_at: str | None = None,
    execute_export: bool = False,
) -> dict[str, Any]:
    view_model = build_nicegui_private_cockpit_view_model(
        project_root,
        output_dir,
        gem_response_text=gem_response_text,
        card_id=card_id,
        query=query,
        generated_at=generated_at,
        execute_export=execute_export,
    )
    html = build_private_cockpit_static_html(view_model)

    status = "OK_P218_NICEGUI_PRIVATE_COCKPIT_VISUAL_SMOKE_READY"
    if view_model["STATUS"].startswith("REVIEW_"):
        status = "REVIEW_P218_NICEGUI_PRIVATE_COCKPIT_VISUAL_SMOKE"
    elif view_model["STATUS"].startswith("BLOCKED_"):
        status = "BLOCKED_P218_NICEGUI_PRIVATE_COCKPIT_VISUAL_SMOKE"

    observation_checklist = [
        {
            "id": "HEADER_VISIBLE",
            "label": "Le titre cockpit privé est visible",
            "expected": True,
        },
        {
            "id": "PROMPT_HISTORY_CARD_VISIBLE",
            "label": "La carte historique prompts est visible",
            "expected": True,
        },
        {
            "id": "RESPONSE_DRAFT_CARD_VISIBLE",
            "label": "La carte brouillon GEM est visible",
            "expected": True,
        },
        {
            "id": "LOCAL_EXPORT_CARD_VISIBLE",
            "label": "La carte export local est visible",
            "expected": True,
        },
        {
            "id": "SAVE_BUTTON_STATE_CLEAR",
            "label": "Le bouton sauvegarde reflète export_allowed",
            "expected": True,
        },
        {
            "id": "SAFETY_BLOCK_VISIBLE",
            "label": "Le bloc safety est visible",
            "expected": True,
        },
    ]

    return {
        "STATUS": status,
        "source_status": view_model["STATUS"],
        "blocker_count": view_model.get("blocker_count", 0),
        "blockers": view_model.get("blockers", []),
        "html_preview": html,
        "html_preview_bytes": len(html.encode("utf-8")),
        "observation_checklist": observation_checklist,
        "observation_required": True,
        "operator_decision_values": ["OK", "UX_POLISH", "BLOCKER"],
        "view_model_payload": view_model,
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
        "recommended_next": "P219_NICEGUI_PRIVATE_COCKPIT_UX_POLISH_FAST_FUSE",
    }


def write_private_cockpit_visual_smoke_files(
    payload: dict[str, Any],
    output_dir: str | Path,
) -> dict[str, Any]:
    output = Path(output_dir)
    output.mkdir(parents=True, exist_ok=True)

    html_path = output / "P218_PRIVATE_COCKPIT_VISUAL_SMOKE.html"
    json_path = output / "P218_PRIVATE_COCKPIT_VISUAL_SMOKE.json"

    html_path.write_text(payload["html_preview"], encoding="utf-8")
    json_path.write_text(
        json.dumps(
            {key: value for key, value in payload.items() if key != "html_preview"},
            ensure_ascii=False,
            indent=2,
            sort_keys=True,
        ),
        encoding="utf-8",
    )

    return {
        **payload,
        "files_written": True,
        "html_path": str(html_path),
        "json_path": str(json_path),
    }


def main() -> None:
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--project-root", default=".")
    parser.add_argument("--output-dir", required=True)
    parser.add_argument("--gem-response-text", required=True)
    parser.add_argument("--card-id", default=None)
    parser.add_argument("--query", default="")
    parser.add_argument("--generated-at", default=None)
    parser.add_argument("--execute-export", action="store_true")
    parser.add_argument("--write-preview", action="store_true")
    args = parser.parse_args()

    payload = build_private_cockpit_visual_smoke_payload(
        args.project_root,
        args.output_dir,
        gem_response_text=args.gem_response_text,
        card_id=args.card_id,
        query=args.query,
        generated_at=args.generated_at,
        execute_export=args.execute_export,
    )
    if args.write_preview:
        payload = write_private_cockpit_visual_smoke_files(payload, args.output_dir)

    print(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
