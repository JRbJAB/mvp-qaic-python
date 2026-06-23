from __future__ import annotations

import argparse
import csv
import json
import re
import sys
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

VERSION = "MVP_QAIC_P144_PROMPT_COCKPIT_WORKFLOWS_1.0.0_SAFE"
STATUS_RENDERED = "P144_PROMPT_COCKPIT_WORKFLOWS_RENDERED_LOCAL_READONLY"

SAFETY_MARKERS = {
    "source": "P143B_LOCAL_PREVIEW_BINDING",
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
}


@dataclass(frozen=True)
class WorkflowRequest:
    p143b_binding_path: Path
    output_dir: Path
    run_id: str
    generated_at_utc: str


def utc_now_iso() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def normalize(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", "_", value.lower()).strip("_")


def classify_workflow(binding_item: dict[str, Any]) -> str:
    title = str(binding_item.get("title", "")).upper()
    route = str(binding_item.get("route", "")).upper()
    text = title + " " + route
    if "PROMPT_LIBRARY" in text:
        return "prompt_library"
    if "VARIANT" in text or "CONTROL" in text:
        return "variant_control"
    if "READY" in text or "COPY" in text:
        return "ready_to_copy"
    if "RUN_QUEUE" in text or "QUEUE" in text:
        return "run_queue"
    if "CONTEXT" in text:
        return "context_pack"
    if "LEXIQUE" in text or "BRIDGE" in text:
        return "lexique_bridge"
    if "RUNTIME" in text or "CONTRACT" in text or "TEMPLATE" in text or "REQUIREMENT" in text:
        return "contract_reference"
    return "support"


def build_step(workflow_type: str, binding_item: dict[str, Any]) -> dict[str, Any]:
    base = {
        "workflow_type": workflow_type,
        "title": binding_item.get("title"),
        "route": binding_item.get("route"),
        "source_filename": binding_item.get("source_filename", ""),
        "preview_row_count": binding_item.get("preview_row_count", 0),
        "binding_mode": binding_item.get("binding_mode"),
        "human_review_required": True,
        "no_auto_apply": True,
    }
    if workflow_type == "prompt_library":
        base["operator_goal"] = "Choisir un prompt validé et consulter son contenu source."
        base["next_action"] = "select_prompt"
        base["primary_fields"] = ["prompt_id", "prompt_title", "raw_prompt_text", "status"]
    elif workflow_type == "variant_control":
        base["operator_goal"] = (
            "Comparer les variantes actives et sélectionner la variante utile au test."
        )
        base["next_action"] = "select_variant"
        base["primary_fields"] = ["variant_id", "prompt_id", "status", "priority"]
    elif workflow_type == "context_pack":
        base["operator_goal"] = "Attacher un contexte métier au prompt avant copie."
        base["next_action"] = "attach_context"
        base["primary_fields"] = ["context_pack_id", "scope", "status"]
    elif workflow_type == "lexique_bridge":
        base["operator_goal"] = "Relier le prompt aux termes/méthodes du lexique."
        base["next_action"] = "review_bridge"
        base["primary_fields"] = ["term", "category", "prompt_id"]
    elif workflow_type == "ready_to_copy":
        base["operator_goal"] = "Préparer le prompt final copiable dans GEM/ChatGPT."
        base["next_action"] = "copy_prompt"
        base["primary_fields"] = ["ready_prompt_id", "compiled_prompt", "safety"]
    elif workflow_type == "run_queue":
        base["operator_goal"] = "Voir les prompts à tester et leur statut opérateur."
        base["next_action"] = "queue_review"
        base["primary_fields"] = ["queue_id", "prompt_id", "run_status"]
    else:
        base["operator_goal"] = "Consulter les contrats/références nécessaires au workflow."
        base["next_action"] = "review_reference"
        base["primary_fields"] = ["id", "status", "notes"]
    return base


def build_workflow_model(binding: dict[str, Any]) -> dict[str, Any]:
    if binding.get("status") != "P143B_DATA_PREVIEW_SOURCE_EXPANSION_RENDERED_LOCAL_READONLY":
        raise ValueError(f"Invalid P143B status: {binding.get('status')}")

    steps: list[dict[str, Any]] = []
    for item in binding.get("bindings", []):
        workflow_type = classify_workflow(item)
        steps.append(build_step(workflow_type, item))

    order = [
        "prompt_library",
        "variant_control",
        "context_pack",
        "lexique_bridge",
        "ready_to_copy",
        "run_queue",
        "contract_reference",
        "support",
    ]
    type_rank = {name: index for index, name in enumerate(order)}
    steps.sort(
        key=lambda step: (type_rank.get(step["workflow_type"], 999), str(step.get("title", "")))
    )

    workflow_counts: dict[str, int] = {}
    for step in steps:
        workflow_counts[step["workflow_type"]] = workflow_counts.get(step["workflow_type"], 0) + 1

    return {
        "status": STATUS_RENDERED,
        "version": VERSION,
        "source_p143b_status": binding.get("status"),
        "source_csv_count": binding.get("source_csv_count"),
        "cockpit_page_count": binding.get("cockpit_page_count"),
        "workflow_step_count": len(steps),
        "workflow_counts": workflow_counts,
        "steps": steps,
        "operator_flow": [
            "select_prompt",
            "select_variant",
            "attach_context",
            "review_lexique_bridge",
            "copy_prompt",
            "queue_review",
            "import_gem_response_in_p145",
        ],
        "gates": {
            "p145_gem_response_import_ready": True,
            "requires_human_review": True,
            "allows_auto_apply": False,
            "allows_broker": False,
            "allows_sizing": False,
        },
        "safety": dict(SAFETY_MARKERS),
        "next": "P145_GEM_RESPONSE_IMPORT_E2E",
    }


def render_workflow_app(model: dict[str, Any]) -> str:
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
            "    ui.label('MVP QAIC — Prompt Cockpit Workflows').classes('text-h4')",
            "    ui.label('Local workflow shell — no Sheet write / no broker / human review only').classes('text-caption')",
            "    with ui.row().classes('q-gutter-sm q-mt-md'):",
            "        _badge(f\"steps {MODEL['workflow_step_count']}\")",
            "        _badge('human review')",
            "        _badge('no auto apply')",
            "    for step in MODEL['steps']:",
            "        with ui.card().classes('q-mt-md'):",
            "            ui.label(step['title']).classes('text-subtitle1')",
            "            ui.label(step['operator_goal']).classes('text-body2')",
            "            with ui.row().classes('q-gutter-xs q-mt-sm'):",
            "                _badge(step['workflow_type'])",
            "                _badge(step['next_action'])",
            "                _badge(step['binding_mode'])",
            "            ui.label('Fields: ' + ', '.join(step.get('primary_fields', []))).classes('text-caption q-mt-sm')",
            "",
            "if __name__ in {'__main__', '__mp_main__'}:",
            "    ui.run(host='127.0.0.1', port=8088, reload=False, show=True)",
            "",
        ]
    )


def write_outputs(model: dict[str, Any], output_dir: Path) -> dict[str, str]:
    output_dir.mkdir(parents=True, exist_ok=True)
    model_path = output_dir / "P144_PROMPT_WORKFLOW_MODEL.json"
    app_path = output_dir / "P144_NICEGUI_PROMPT_WORKFLOW_APP.py"
    actions_csv_path = output_dir / "P144_OPERATOR_ACTIONS.csv"
    md_path = output_dir / "P144_PROMPT_COCKPIT_WORKFLOWS.md"
    summary_path = output_dir / "P144_SUMMARY.json"

    model_path.write_text(
        json.dumps(model, ensure_ascii=False, indent=2, sort_keys=True), encoding="utf-8"
    )
    app_path.write_text(render_workflow_app(model), encoding="utf-8")

    with actions_csv_path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=[
                "workflow_type",
                "title",
                "route",
                "next_action",
                "human_review_required",
                "no_auto_apply",
                "binding_mode",
                "preview_row_count",
            ],
        )
        writer.writeheader()
        for step in model["steps"]:
            writer.writerow({field: step.get(field, "") for field in writer.fieldnames})

    flow_lines = "\n".join(
        f"{index + 1}. `{step}`" for index, step in enumerate(model["operator_flow"])
    )
    md_path.write_text(
        "\n".join(
            [
                "# P144 — Prompt Cockpit Workflows",
                "",
                f"- Status: `{model['status']}`",
                f"- Workflow steps: `{model['workflow_step_count']}`",
                f"- Source CSV count: `{model.get('source_csv_count')}`",
                "",
                "## Operator flow",
                "",
                flow_lines,
                "",
                "## Safety",
                "",
                "- Human review required",
                "- No auto apply GEM response",
                "- No Sheet write",
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
        "workflow_step_count": model["workflow_step_count"],
        "workflow_counts": model["workflow_counts"],
        "p145_gem_response_import_ready": model["gates"]["p145_gem_response_import_ready"],
        "human_review_required": True,
        "google_sheets_write": False,
        "live_google_sheets_read": False,
        "public_deploy": False,
        "broker": False,
        "order": False,
        "sizing": False,
        "output_dir": str(output_dir),
        "next": model["next"],
    }
    summary_path.write_text(
        json.dumps(summary, ensure_ascii=False, indent=2, sort_keys=True), encoding="utf-8"
    )
    return {
        "workflow_model_json": str(model_path),
        "workflow_app_py": str(app_path),
        "operator_actions_csv": str(actions_csv_path),
        "workflow_md": str(md_path),
        "summary_json": str(summary_path),
    }


def run_workflows(request: WorkflowRequest) -> dict[str, Any]:
    binding = load_json(request.p143b_binding_path)
    model = build_workflow_model(binding)
    model["run_id"] = request.run_id
    model["generated_at_utc"] = request.generated_at_utc
    model["source_p143b_binding_path"] = str(request.p143b_binding_path)
    outputs = write_outputs(model, request.output_dir)
    model["output_files"] = outputs
    (request.output_dir / "P144_PROMPT_WORKFLOW_MODEL.json").write_text(
        json.dumps(model, ensure_ascii=False, indent=2, sort_keys=True),
        encoding="utf-8",
    )
    return model


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="P144 prompt cockpit workflows.")
    parser.add_argument("--p143b-binding", required=True)
    parser.add_argument("--output-dir", required=True)
    parser.add_argument("--run-id", default="P144-PROMPT-COCKPIT-WORKFLOWS")
    parser.add_argument("--generated-at-utc", default=utc_now_iso())
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    model = run_workflows(
        WorkflowRequest(
            p143b_binding_path=Path(args.p143b_binding),
            output_dir=Path(args.output_dir),
            run_id=args.run_id,
            generated_at_utc=args.generated_at_utc,
        )
    )
    print(model["status"])
    print(f"workflow_step_count={model['workflow_step_count']}")
    print("p145_gem_response_import_ready=true")
    print("human_review_required=true")
    print("google_sheets_write=false")
    print("broker=false")
    print(f"output_dir={args.output_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
