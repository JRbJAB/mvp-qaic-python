from __future__ import annotations

import argparse
import csv
import json
import sys
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

VERSION = "MVP_QAIC_P146_CORRECTION_QUEUE_UI_1.0.0_SAFE"
STATUS_RENDERED = "P146_CORRECTION_QUEUE_UI_RENDERED_LOCAL_REVIEW_ONLY"

SAFETY_MARKERS = {
    "source": "P145_LOCAL_GEM_REVIEW_AND_P144_WORKFLOW",
    "live_google_sheets_read": False,
    "google_sheets_write": False,
    "apps_script_execution": False,
    "clasp_push": False,
    "broker": False,
    "order": False,
    "sizing": False,
    "auto_apply_gem_response": False,
    "public_deploy": False,
    "human_review_required": True,
    "apply_requires_explicit_future_go": True,
}


@dataclass(frozen=True)
class CorrectionRequest:
    p145_payload_path: Path
    p144_model_path: Path
    output_dir: Path
    run_id: str
    generated_at_utc: str


def utc_now_iso() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def validate_sources(p145_payload: dict[str, Any], p144_model: dict[str, Any]) -> None:
    if p145_payload.get("status") != "P145_GEM_RESPONSE_IMPORT_E2E_VALIDATED_LOCAL_REVIEW":
        raise ValueError(f"Invalid P145 status: {p145_payload.get('status')}")
    if p144_model.get("status") != "P144_PROMPT_COCKPIT_WORKFLOWS_RENDERED_LOCAL_READONLY":
        raise ValueError(f"Invalid P144 status: {p144_model.get('status')}")
    validation = p145_payload.get("validation", {})
    if validation.get("human_review_required") is not True:
        raise ValueError("P145 validation must require human review")
    if validation.get("no_auto_apply") is not True:
        raise ValueError("P145 validation must block auto-apply")


def priority_for_issue(issue_type: str) -> str:
    if issue_type in {"BLOCKER", "SAFETY"}:
        return "P0"
    if issue_type in {"WARNING", "MISSING_DATA"}:
        return "P1"
    return "P2"


def build_queue_items(
    p145_payload: dict[str, Any], p144_model: dict[str, Any]
) -> list[dict[str, Any]]:
    validation = p145_payload.get("validation", {})
    response_payload = p145_payload.get("response_payload") or {}
    items: list[dict[str, Any]] = []

    for blocker in validation.get("blockers", []):
        items.append(
            {
                "queue_id": f"P146-BLOCKER-{len(items) + 1:03d}",
                "issue_type": "BLOCKER",
                "priority": priority_for_issue("BLOCKER"),
                "title": blocker,
                "source": "P145_VALIDATION",
                "suggested_action": "Corriger le prompt ou la réponse GEM puis réimporter.",
                "human_review_required": True,
                "apply_now": False,
                "blocked_actions": ["SHEET_WRITE", "AUTO_APPLY", "ORDER", "SIZING"],
            }
        )

    for warning in validation.get("warnings", []):
        items.append(
            {
                "queue_id": f"P146-WARNING-{len(items) + 1:03d}",
                "issue_type": "WARNING",
                "priority": priority_for_issue("WARNING"),
                "title": warning,
                "source": "P145_VALIDATION",
                "suggested_action": "Revoir le prompt et décider si le warning doit devenir règle stricte.",
                "human_review_required": True,
                "apply_now": False,
                "blocked_actions": ["SHEET_WRITE", "AUTO_APPLY", "ORDER", "SIZING"],
            }
        )

    if not items:
        items.append(
            {
                "queue_id": "P146-REVIEW-001",
                "issue_type": "REVIEW",
                "priority": "P1",
                "title": "GEM response accepted for human review",
                "source": "P145_REVIEW_QUEUE",
                "suggested_action": "Lire la réponse, valider l'extraction, puis préparer le prochain test réel.",
                "human_review_required": True,
                "apply_now": False,
                "blocked_actions": ["SHEET_WRITE", "AUTO_APPLY", "ORDER", "SIZING"],
            }
        )

    if response_payload and "NO_AUTO_APPLY" not in json.dumps(response_payload, ensure_ascii=False):
        items.append(
            {
                "queue_id": f"P146-SAFETY-{len(items) + 1:03d}",
                "issue_type": "SAFETY",
                "priority": "P0",
                "title": "NO_AUTO_APPLY marker not explicit in payload",
                "source": "P145_RESPONSE_PAYLOAD",
                "suggested_action": "Renforcer le prompt ou le schéma pour rendre NO_AUTO_APPLY explicite.",
                "human_review_required": True,
                "apply_now": False,
                "blocked_actions": ["SHEET_WRITE", "AUTO_APPLY", "ORDER", "SIZING"],
            }
        )

    workflow_steps = p144_model.get("steps", [])
    if workflow_steps:
        first_prompt_step = next(
            (step for step in workflow_steps if step.get("workflow_type") == "prompt_library"),
            workflow_steps[0],
        )
        items.append(
            {
                "queue_id": f"P146-PROMPT-{len(items) + 1:03d}",
                "issue_type": "PROMPT_NEXT_TEST",
                "priority": "P2",
                "title": f"Next prompt workflow: {first_prompt_step.get('title')}",
                "source": "P144_WORKFLOW",
                "suggested_action": first_prompt_step.get(
                    "operator_goal", "Préparer le prochain test prompt."
                ),
                "human_review_required": True,
                "apply_now": False,
                "blocked_actions": ["SHEET_WRITE", "AUTO_APPLY", "ORDER", "SIZING"],
            }
        )

    return items


def build_queue_model(p145_payload: dict[str, Any], p144_model: dict[str, Any]) -> dict[str, Any]:
    validate_sources(p145_payload, p144_model)
    items = build_queue_items(p145_payload, p144_model)
    priority_counts: dict[str, int] = {}
    type_counts: dict[str, int] = {}
    for item in items:
        priority_counts[item["priority"]] = priority_counts.get(item["priority"], 0) + 1
        type_counts[item["issue_type"]] = type_counts.get(item["issue_type"], 0) + 1

    return {
        "status": STATUS_RENDERED,
        "version": VERSION,
        "source_p145_status": p145_payload.get("status"),
        "source_p144_status": p144_model.get("status"),
        "queue_item_count": len(items),
        "priority_counts": priority_counts,
        "issue_type_counts": type_counts,
        "items": items,
        "ui_policy": {
            "review_only": True,
            "apply_button_enabled": False,
            "export_changeset_enabled": True,
            "sheet_write_enabled": False,
            "auto_apply_enabled": False,
        },
        "safety": dict(SAFETY_MARKERS),
        "next": "P147_OPERATOR_POLISH",
    }


def render_queue_app(model: dict[str, Any]) -> str:
    model_repr = repr(json.dumps(model, ensure_ascii=False, indent=2, sort_keys=True))
    return "\n".join(
        [
            "from __future__ import annotations",
            "import json",
            "from nicegui import ui",
            "",
            f"MODEL = json.loads({model_repr})",
            "",
            "@ui.page('/')",
            "def index():",
            "    ui.label('MVP QAIC — Correction Queue').classes('text-h4')",
            "    ui.label('Review only — no Sheet write / no auto apply / no broker').classes('text-caption')",
            "    with ui.row().classes('q-gutter-sm q-mt-md'):",
            "        ui.badge(f\"items {MODEL['queue_item_count']}\")",
            "        ui.badge('review only')",
            "        ui.badge('apply disabled')",
            "    for item in MODEL['items']:",
            "        with ui.card().classes('q-mt-md'):",
            "            ui.label(item['title']).classes('text-subtitle1')",
            "            ui.label(item['suggested_action']).classes('text-body2')",
            "            with ui.row().classes('q-gutter-xs q-mt-sm'):",
            "                ui.badge(item['priority'])",
            "                ui.badge(item['issue_type'])",
            "                ui.badge(item['source'])",
            "            ui.label('Blocked: ' + ', '.join(item['blocked_actions'])).classes('text-caption q-mt-sm')",
            "",
            "if __name__ in {'__main__', '__mp_main__'}:",
            "    ui.run(host='127.0.0.1', port=8088, reload=False, show=True)",
            "",
        ]
    )


def write_outputs(model: dict[str, Any], output_dir: Path) -> dict[str, str]:
    output_dir.mkdir(parents=True, exist_ok=True)
    model_path = output_dir / "P146_CORRECTION_QUEUE_MODEL.json"
    app_path = output_dir / "P146_NICEGUI_CORRECTION_QUEUE_APP.py"
    actions_path = output_dir / "P146_CORRECTION_ACTIONS.csv"
    md_path = output_dir / "P146_CORRECTION_QUEUE_UI.md"
    summary_path = output_dir / "P146_SUMMARY.json"

    model_path.write_text(
        json.dumps(model, ensure_ascii=False, indent=2, sort_keys=True), encoding="utf-8"
    )
    app_path.write_text(render_queue_app(model), encoding="utf-8")

    with actions_path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=[
                "queue_id",
                "priority",
                "issue_type",
                "title",
                "source",
                "suggested_action",
                "human_review_required",
                "apply_now",
            ],
        )
        writer.writeheader()
        for item in model["items"]:
            writer.writerow({field: item.get(field, "") for field in writer.fieldnames})

    md_path.write_text(
        "\n".join(
            [
                "# P146 — Correction Queue UI",
                "",
                f"- Status: `{model['status']}`",
                f"- Queue items: `{model['queue_item_count']}`",
                "",
                "## Safety",
                "",
                "- Review only",
                "- Apply disabled",
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
        "queue_item_count": model["queue_item_count"],
        "priority_counts": model["priority_counts"],
        "review_only": True,
        "apply_button_enabled": False,
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
        "queue_model_json": str(model_path),
        "queue_app_py": str(app_path),
        "actions_csv": str(actions_path),
        "markdown": str(md_path),
        "summary_json": str(summary_path),
    }


def run_queue(request: CorrectionRequest) -> dict[str, Any]:
    p145_payload = load_json(request.p145_payload_path)
    p144_model = load_json(request.p144_model_path)
    model = build_queue_model(p145_payload, p144_model)
    model["run_id"] = request.run_id
    model["generated_at_utc"] = request.generated_at_utc
    model["source_p145_payload_path"] = str(request.p145_payload_path)
    model["source_p144_model_path"] = str(request.p144_model_path)
    outputs = write_outputs(model, request.output_dir)
    model["output_files"] = outputs
    (request.output_dir / "P146_CORRECTION_QUEUE_MODEL.json").write_text(
        json.dumps(model, ensure_ascii=False, indent=2, sort_keys=True),
        encoding="utf-8",
    )
    return model


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="P146 correction queue UI.")
    parser.add_argument("--p145-payload", required=True)
    parser.add_argument("--p144-model", required=True)
    parser.add_argument("--output-dir", required=True)
    parser.add_argument("--run-id", default="P146-CORRECTION-QUEUE-UI")
    parser.add_argument("--generated-at-utc", default=utc_now_iso())
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    model = run_queue(
        CorrectionRequest(
            p145_payload_path=Path(args.p145_payload),
            p144_model_path=Path(args.p144_model),
            output_dir=Path(args.output_dir),
            run_id=args.run_id,
            generated_at_utc=args.generated_at_utc,
        )
    )
    print(model["status"])
    print(f"queue_item_count={model['queue_item_count']}")
    print("review_only=true")
    print("apply_button_enabled=false")
    print("google_sheets_write=false")
    print("auto_apply_gem_response=false")
    print("broker=false")
    print(f"output_dir={args.output_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
