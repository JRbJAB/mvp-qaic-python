from __future__ import annotations

import argparse
import csv
import json
import sys
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

VERSION = "MVP_QAIC_P147_OPERATOR_POLISH_1.0.0_SAFE"
STATUS_RENDERED = "P147_OPERATOR_POLISH_RENDERED_LOCAL_PRIVATE"

SAFETY_MARKERS = {
    "source": "P146_CORRECTION_QUEUE_AND_P144_WORKFLOW",
    "live_google_sheets_read": False,
    "google_sheets_write": False,
    "apps_script_execution": False,
    "clasp_push": False,
    "broker": False,
    "order": False,
    "sizing": False,
    "auto_apply_gem_response": False,
    "public_deploy": False,
    "local_private_only": True,
    "human_review_required": True,
}


@dataclass(frozen=True)
class PolishRequest:
    p146_queue_path: Path
    p144_model_path: Path
    output_dir: Path
    run_id: str
    generated_at_utc: str


def utc_now_iso() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def validate_sources(queue: dict[str, Any], workflow: dict[str, Any]) -> None:
    if queue.get("status") != "P146_CORRECTION_QUEUE_UI_RENDERED_LOCAL_REVIEW_ONLY":
        raise ValueError(f"Invalid P146 status: {queue.get('status')}")
    if workflow.get("status") != "P144_PROMPT_COCKPIT_WORKFLOWS_RENDERED_LOCAL_READONLY":
        raise ValueError(f"Invalid P144 status: {workflow.get('status')}")
    policy = queue.get("ui_policy", {})
    if policy.get("apply_button_enabled") is not False:
        raise ValueError("P146 apply button must remain disabled")
    if policy.get("sheet_write_enabled") is not False:
        raise ValueError("P146 sheet write must remain disabled")


def build_navigation(workflow: dict[str, Any], queue: dict[str, Any]) -> list[dict[str, Any]]:
    nav: list[dict[str, Any]] = [
        {"label": "Dashboard", "route": "/", "icon": "dashboard", "priority": "P0"},
        {"label": "Prompt Workflow", "route": "/workflow", "icon": "route", "priority": "P0"},
        {"label": "Correction Queue", "route": "/queue", "icon": "rule", "priority": "P0"},
        {"label": "GEM Review", "route": "/gem-review", "icon": "psychology", "priority": "P1"},
        {"label": "Safety", "route": "/safety", "icon": "lock", "priority": "P0"},
    ]
    for step in workflow.get("steps", [])[:6]:
        route = "/workflow/" + str(step.get("workflow_type", "step")).replace("_", "-")
        nav.append(
            {
                "label": str(step.get("workflow_type", "workflow")).replace("_", " ").title(),
                "route": route,
                "icon": "article",
                "priority": step.get("priority", "P1"),
            }
        )
    if int(queue.get("queue_item_count", 0) or 0) > 0:
        nav.append(
            {
                "label": "Review Items",
                "route": "/queue/items",
                "icon": "checklist",
                "priority": "P0",
            }
        )
    return nav


def build_shortcuts() -> list[dict[str, str]]:
    return [
        {"keys": "Ctrl+1", "action": "open_dashboard", "description": "Retour dashboard"},
        {
            "keys": "Ctrl+2",
            "action": "open_prompt_workflow",
            "description": "Ouvrir workflow prompt",
        },
        {
            "keys": "Ctrl+3",
            "action": "open_correction_queue",
            "description": "Ouvrir correction queue",
        },
        {
            "keys": "Ctrl+C",
            "action": "copy_selected_prompt",
            "description": "Copie manuelle uniquement",
        },
        {
            "keys": "Ctrl+S",
            "action": "save_local_review",
            "description": "Sauvegarde locale review-only",
        },
        {"keys": "Esc", "action": "clear_selection", "description": "Annuler sélection"},
    ]


def build_operator_cards(queue: dict[str, Any], workflow: dict[str, Any]) -> list[dict[str, Any]]:
    cards = [
        {
            "card_id": "workflow_status",
            "title": "Workflow prompt",
            "value": str(workflow.get("workflow_step_count", 0)),
            "subtitle": "étapes opérateur",
            "severity": "info",
        },
        {
            "card_id": "queue_status",
            "title": "Correction queue",
            "value": str(queue.get("queue_item_count", 0)),
            "subtitle": "items review-only",
            "severity": "review",
        },
        {
            "card_id": "safety_status",
            "title": "Safety",
            "value": "LOCKED",
            "subtitle": "no write / no broker / no auto apply",
            "severity": "safe",
        },
    ]
    return cards


def build_polish_model(queue: dict[str, Any], workflow: dict[str, Any]) -> dict[str, Any]:
    validate_sources(queue, workflow)
    return {
        "status": STATUS_RENDERED,
        "version": VERSION,
        "source_p146_status": queue.get("status"),
        "source_p144_status": workflow.get("status"),
        "operator_shell": {
            "title": "MVP QAIC — Prompt Operator Cockpit",
            "mode": "local_private_review_only",
            "layout": "left_nav_top_status_main_cards",
            "default_route": "/",
            "density": "compact",
            "theme": "clean_light",
        },
        "navigation": build_navigation(workflow, queue),
        "shortcuts": build_shortcuts(),
        "operator_cards": build_operator_cards(queue, workflow),
        "review_policy": {
            "copy_prompt_enabled": True,
            "save_local_review_enabled": True,
            "export_changeset_enabled": True,
            "apply_to_sheet_enabled": False,
            "auto_apply_gem_response_enabled": False,
            "broker_actions_enabled": False,
            "order_actions_enabled": False,
            "sizing_enabled": False,
        },
        "queue_item_count": queue.get("queue_item_count", 0),
        "workflow_step_count": workflow.get("workflow_step_count", 0),
        "launch": {
            "host": "127.0.0.1",
            "port": 8088,
            "public_deploy": False,
            "command": "python P147_NICEGUI_OPERATOR_POLISH_APP.py",
        },
        "safety": dict(SAFETY_MARKERS),
        "next": "P148_SYNC_STRATEGY_READONLY",
    }


def render_app(model: dict[str, Any]) -> str:
    model_repr = repr(json.dumps(model, ensure_ascii=False, indent=2, sort_keys=True))
    return "\n".join(
        [
            "from __future__ import annotations",
            "import json",
            "from nicegui import ui",
            "",
            f"MODEL = json.loads({model_repr})",
            "",
            "def _badge(text: str):",
            "    ui.badge(text).classes('q-mr-xs')",
            "",
            "@ui.page('/')",
            "def index():",
            "    ui.label(MODEL['operator_shell']['title']).classes('text-h4')",
            "    ui.label('Local private / review-only / no Sheet write / no broker').classes('text-caption')",
            "    with ui.row().classes('q-gutter-md q-mt-md'):",
            "        for card in MODEL['operator_cards']:",
            "            with ui.card().classes('w-72'):",
            "                ui.label(card['title']).classes('text-subtitle1')",
            "                ui.label(card['value']).classes('text-h5')",
            "                ui.label(card['subtitle']).classes('text-caption')",
            "    ui.separator().classes('q-my-md')",
            "    ui.label('Navigation').classes('text-h6')",
            "    with ui.row().classes('q-gutter-sm'):",
            "        for item in MODEL['navigation']:",
            "            ui.link(item['label'], item['route']).classes('q-pa-sm')",
            "    ui.separator().classes('q-my-md')",
            "    ui.label('Shortcuts').classes('text-h6')",
            "    for shortcut in MODEL['shortcuts']:",
            "        ui.label(shortcut['keys'] + ' — ' + shortcut['description']).classes('text-body2')",
            "",
            "@ui.page('/safety')",
            "def safety():",
            "    ui.label('Safety Locks').classes('text-h5')",
            "    for key, value in MODEL['safety'].items():",
            "        ui.label(f'{key}: {value}')",
            "",
            "@ui.page('/queue')",
            "def queue():",
            "    ui.label('Correction Queue').classes('text-h5')",
            "    ui.label('Apply disabled. Export/review only.').classes('text-caption')",
            "",
            "@ui.page('/workflow')",
            "def workflow():",
            "    ui.label('Prompt Workflow').classes('text-h5')",
            "    ui.label('Prompt workflow shell; data stays local/read-only.').classes('text-caption')",
            "",
            "if __name__ in {'__main__', '__mp_main__'}:",
            "    ui.run(host='127.0.0.1', port=8088, reload=False, show=True)",
            "",
        ]
    )


def write_outputs(model: dict[str, Any], output_dir: Path) -> dict[str, str]:
    output_dir.mkdir(parents=True, exist_ok=True)
    model_path = output_dir / "P147_OPERATOR_POLISH_MODEL.json"
    app_path = output_dir / "P147_NICEGUI_OPERATOR_POLISH_APP.py"
    shortcuts_path = output_dir / "P147_OPERATOR_SHORTCUTS.csv"
    md_path = output_dir / "P147_OPERATOR_POLISH.md"
    summary_path = output_dir / "P147_SUMMARY.json"

    model_path.write_text(
        json.dumps(model, ensure_ascii=False, indent=2, sort_keys=True), encoding="utf-8"
    )
    app_path.write_text(render_app(model), encoding="utf-8")

    with shortcuts_path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=["keys", "action", "description"])
        writer.writeheader()
        for row in model["shortcuts"]:
            writer.writerow(row)

    md_path.write_text(
        "\n".join(
            [
                "# P147 — Operator Polish",
                "",
                f"- Status: `{model['status']}`",
                f"- Navigation items: `{len(model['navigation'])}`",
                f"- Shortcuts: `{len(model['shortcuts'])}`",
                f"- Queue items: `{model['queue_item_count']}`",
                "",
                "## Safety",
                "",
                "- Local private only",
                "- No Sheet write",
                "- No auto apply GEM response",
                "- No broker/order/sizing",
                "- No public deploy",
                "",
                f"Next: `{model['next']}`",
                "",
            ]
        ),
        encoding="utf-8",
    )

    summary = {
        "status": model["status"],
        "navigation_item_count": len(model["navigation"]),
        "shortcut_count": len(model["shortcuts"]),
        "queue_item_count": model["queue_item_count"],
        "workflow_step_count": model["workflow_step_count"],
        "copy_prompt_enabled": model["review_policy"]["copy_prompt_enabled"],
        "save_local_review_enabled": model["review_policy"]["save_local_review_enabled"],
        "apply_to_sheet_enabled": False,
        "google_sheets_write": False,
        "auto_apply_gem_response": False,
        "broker": False,
        "order": False,
        "sizing": False,
        "public_deploy": False,
        "output_dir": str(output_dir),
        "next": model["next"],
    }
    summary_path.write_text(
        json.dumps(summary, ensure_ascii=False, indent=2, sort_keys=True), encoding="utf-8"
    )
    return {
        "model_json": str(model_path),
        "app_py": str(app_path),
        "shortcuts_csv": str(shortcuts_path),
        "markdown": str(md_path),
        "summary_json": str(summary_path),
    }


def run_polish(request: PolishRequest) -> dict[str, Any]:
    queue = load_json(request.p146_queue_path)
    workflow = load_json(request.p144_model_path)
    model = build_polish_model(queue, workflow)
    model["run_id"] = request.run_id
    model["generated_at_utc"] = request.generated_at_utc
    model["source_p146_queue_path"] = str(request.p146_queue_path)
    model["source_p144_model_path"] = str(request.p144_model_path)
    outputs = write_outputs(model, request.output_dir)
    model["output_files"] = outputs
    (request.output_dir / "P147_OPERATOR_POLISH_MODEL.json").write_text(
        json.dumps(model, ensure_ascii=False, indent=2, sort_keys=True),
        encoding="utf-8",
    )
    return model


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="P147 operator polish.")
    parser.add_argument("--p146-queue", required=True)
    parser.add_argument("--p144-model", required=True)
    parser.add_argument("--output-dir", required=True)
    parser.add_argument("--run-id", default="P147-OPERATOR-POLISH")
    parser.add_argument("--generated-at-utc", default=utc_now_iso())
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    model = run_polish(
        PolishRequest(
            p146_queue_path=Path(args.p146_queue),
            p144_model_path=Path(args.p144_model),
            output_dir=Path(args.output_dir),
            run_id=args.run_id,
            generated_at_utc=args.generated_at_utc,
        )
    )
    print(model["status"])
    print(f"navigation_item_count={len(model['navigation'])}")
    print(f"shortcut_count={len(model['shortcuts'])}")
    print("local_private_only=true")
    print("apply_to_sheet_enabled=false")
    print("google_sheets_write=false")
    print("broker=false")
    print(f"output_dir={args.output_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
