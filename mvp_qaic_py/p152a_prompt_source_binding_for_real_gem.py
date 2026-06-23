from __future__ import annotations

import argparse
import csv
import json
import sys
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

VERSION = "MVP_QAIC_P152A_PROMPT_SOURCE_BINDING_FOR_REAL_GEM_1.0.0_SAFE"
STATUS_READY = "P152A_PROMPT_SOURCE_BINDING_READY_FOR_REAL_GEM"

ACTIVE_PROMPT_SOURCE_ID = "P132_P133_PORTFOLIO_MULTIMODAL_REVIEW"

SAFETY_MARKERS = {
    "prompt_binding_only": True,
    "real_gem_import_executed": False,
    "fixture_allowed": False,
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
class BindingRequest:
    p152_summary_path: Path
    p144_model_path: Path
    output_dir: Path
    prompt_source_id: str
    run_id: str
    generated_at_utc: str


def utc_now_iso() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def validate_p152(summary: dict[str, Any]) -> list[str]:
    blockers: list[str] = []
    if summary.get("status") not in {
        "P152_STOP_WAIT_REAL_GEM_RESPONSE_FILE_READY",
        "P152_REAL_GEM_RESPONSE_IMPORTED_LOCAL_REVIEW",
    }:
        blockers.append("P152_STATUS_NOT_COMPATIBLE")
    if summary.get("google_sheets_write") is not False:
        blockers.append("GOOGLE_SHEETS_WRITE_NOT_FALSE")
    if summary.get("public_deploy") is not False:
        blockers.append("PUBLIC_DEPLOY_NOT_FALSE")
    if summary.get("auto_apply_gem_response") is not False:
        blockers.append("AUTO_APPLY_GEM_RESPONSE_NOT_FALSE")
    return blockers


def validate_p144(model: dict[str, Any]) -> list[str]:
    blockers: list[str] = []
    if model.get("status") != "P144_PROMPT_COCKPIT_WORKFLOWS_RENDERED_LOCAL_READONLY":
        blockers.append("P144_STATUS_NOT_READY")
    return blockers


def build_prompt_sources(p144_model: dict[str, Any]) -> list[dict[str, Any]]:
    sources: list[dict[str, Any]] = [
        {
            "prompt_source_id": ACTIVE_PROMPT_SOURCE_ID,
            "label": "P132/P133 — Portfolio multimodal Revolut X",
            "source_family": "MVP_QAIC_PY_ACTIVE",
            "source_origin": "P132_P133_MULTIMODAL_PROMPT",
            "runtime_profile": "GEM_MULTIMODAL_PORTFOLIO_REVIEW",
            "status": "ACTIVE_FOR_P152_REAL_GEM",
            "allowed_for_p152": True,
            "expected_input": "Capture écran portefeuille crypto/Revolut X + texte optionnel",
            "expected_output": "JSON review-only avec extraction portfolio",
            "required_markers": "REVIEW_REQUIRED,human_review_required,no_order_no_sizing,NO_AUTO_APPLY",
            "notes": "Référence prioritaire pour le prochain import réel P152.",
        }
    ]

    for idx, step in enumerate(p144_model.get("steps", []), start=1):
        workflow_type = str(step.get("workflow_type", "workflow"))
        title = str(step.get("title", workflow_type))
        sources.append(
            {
                "prompt_source_id": f"HIST_SHEETS_{idx:03d}_{workflow_type.upper()}",
                "label": title,
                "source_family": "SHEETS_HISTORICAL_REFERENCE",
                "source_origin": "P144_WORKFLOW_MODEL_FROM_SHEETS_MIGRATION",
                "runtime_profile": workflow_type,
                "status": "HISTORICAL_REFERENCE_ONLY",
                "allowed_for_p152": False,
                "expected_input": step.get("operator_goal", ""),
                "expected_output": "À contractualiser avant import P152",
                "required_markers": "À définir",
                "notes": "Ne pas utiliser pour P152 tant que le contrat JSON/safety n'est pas validé.",
            }
        )
    return sources


def choose_source(
    sources: list[dict[str, Any]], prompt_source_id: str
) -> tuple[dict[str, Any] | None, list[str]]:
    blockers: list[str] = []
    selected = next(
        (source for source in sources if source["prompt_source_id"] == prompt_source_id), None
    )
    if selected is None:
        blockers.append(f"PROMPT_SOURCE_ID_NOT_FOUND:{prompt_source_id}")
        return None, blockers
    if selected.get("allowed_for_p152") is not True:
        blockers.append(f"PROMPT_SOURCE_NOT_ALLOWED_FOR_P152:{prompt_source_id}")
    return selected, blockers


def build_binding(
    p152_summary: dict[str, Any], p144_model: dict[str, Any], prompt_source_id: str
) -> dict[str, Any]:
    p152_blockers = validate_p152(p152_summary)
    p144_blockers = validate_p144(p144_model)
    sources = build_prompt_sources(p144_model)
    selected, source_blockers = choose_source(sources, prompt_source_id)
    blockers = p152_blockers + p144_blockers + source_blockers

    binding = {
        "status": STATUS_READY if not blockers else "P152A_PROMPT_SOURCE_BINDING_BLOCKED",
        "version": VERSION,
        "source_p152_status": p152_summary.get("status"),
        "source_p144_status": p144_model.get("status"),
        "prompt_source_id": prompt_source_id,
        "selected_prompt_source": selected,
        "prompt_source_count": len(sources),
        "historical_reference_count": sum(
            1 for source in sources if source["source_family"] == "SHEETS_HISTORICAL_REFERENCE"
        ),
        "allowed_for_p152_count": sum(
            1 for source in sources if source["allowed_for_p152"] is True
        ),
        "prompt_sources": sources,
        "binding_contract": {
            "gem_response_file_required_next": True,
            "gem_response_must_reference_prompt_source_id": True,
            "accepted_prompt_source_for_next_real_run": ACTIVE_PROMPT_SOURCE_ID,
            "required_response_markers": [
                "status=REVIEW_REQUIRED|OK|BLOCKED",
                "human_review_required=true",
                "no_order_no_sizing=true",
                "NO_AUTO_APPLY explicit",
                "French notes allowed",
                "JSON detectable",
            ],
            "historical_sheets_prompts_policy": "REFERENCE_ONLY_UNTIL_CONTRACTUALIZED",
        },
        "real_gem_binding_template": {
            "prompt_source_id": prompt_source_id,
            "prompt_source_label": selected.get("label") if selected else "",
            "gem_response_file": "C:\\Users\\Julie\\Documents\\JRb-Secrets\\QAIC\\MVP QAIC\\GEM_RESPONSES\\gem_response_real.json",
            "input_evidence_type": "portfolio_screenshot",
            "expected_runtime_profile": selected.get("runtime_profile") if selected else "",
            "human_review_required": True,
            "no_order_no_sizing": True,
            "NO_AUTO_APPLY": True,
        },
        "blocker_count": len(blockers),
        "blockers": blockers,
        "safety": dict(SAFETY_MARKERS),
        "next": "P152_REAL_GEM_RESPONSE_IMPORT_WITH_BOUND_PROMPT_OR_STOP",
    }
    return binding


def write_outputs(binding: dict[str, Any], output_dir: Path) -> dict[str, str]:
    output_dir.mkdir(parents=True, exist_ok=True)

    binding_path = output_dir / "P152A_PROMPT_SOURCE_BINDING.json"
    options_csv = output_dir / "P152A_PROMPT_SOURCE_OPTIONS.csv"
    template_path = output_dir / "P152A_REAL_GEM_BINDING_TEMPLATE.json"
    md_path = output_dir / "P152A_PROMPT_SOURCE_BINDING_FOR_REAL_GEM.md"
    summary_path = output_dir / "P152A_SUMMARY.json"

    binding_path.write_text(
        json.dumps(binding, ensure_ascii=False, indent=2, sort_keys=True), encoding="utf-8"
    )
    template_path.write_text(
        json.dumps(
            binding["real_gem_binding_template"], ensure_ascii=False, indent=2, sort_keys=True
        ),
        encoding="utf-8",
    )

    with options_csv.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=[
                "prompt_source_id",
                "label",
                "source_family",
                "source_origin",
                "runtime_profile",
                "status",
                "allowed_for_p152",
                "expected_input",
                "expected_output",
                "required_markers",
                "notes",
            ],
        )
        writer.writeheader()
        for row in binding["prompt_sources"]:
            writer.writerow(row)

    md_path.write_text(
        "\n".join(
            [
                "# P152A — Prompt Source Binding for Real GEM",
                "",
                f"- Status: `{binding['status']}`",
                f"- Prompt source selected: `{binding['prompt_source_id']}`",
                f"- Historical references: `{binding['historical_reference_count']}`",
                f"- Allowed for P152: `{binding['allowed_for_p152_count']}`",
                f"- Blockers: `{binding['blocker_count']}`",
                "",
                "## Décision",
                "",
                "Pour le prochain P152 réel, utiliser le prompt actif `P132_P133_PORTFOLIO_MULTIMODAL_REVIEW`.",
                "",
                "Les prompts historiques Sheets restent référence/matière première, mais ne sont pas runtime P152 tant qu'ils ne sont pas contractualisés.",
                "",
                "## Safety",
                "",
                "- Binding only",
                "- No real import executed",
                "- No Sheet write",
                "- No public deploy",
                "- No broker/order/sizing",
                "- No auto apply GEM response",
                "",
                f"Next: `{binding['next']}`",
                "",
            ]
        ),
        encoding="utf-8",
    )

    summary = {
        "status": binding["status"],
        "prompt_source_id": binding["prompt_source_id"],
        "selected_prompt_source_status": binding["selected_prompt_source"].get("status")
        if binding["selected_prompt_source"]
        else "",
        "prompt_source_count": binding["prompt_source_count"],
        "historical_reference_count": binding["historical_reference_count"],
        "allowed_for_p152_count": binding["allowed_for_p152_count"],
        "blocker_count": binding["blocker_count"],
        "google_sheets_write": False,
        "live_google_sheets_read": False,
        "public_deploy": False,
        "real_gem_import_executed": False,
        "broker": False,
        "order": False,
        "sizing": False,
        "auto_apply_gem_response": False,
        "output_dir": str(output_dir),
        "next": binding["next"],
    }
    summary_path.write_text(
        json.dumps(summary, ensure_ascii=False, indent=2, sort_keys=True), encoding="utf-8"
    )

    return {
        "binding_json": str(binding_path),
        "options_csv": str(options_csv),
        "template_json": str(template_path),
        "markdown": str(md_path),
        "summary_json": str(summary_path),
    }


def run_binding(request: BindingRequest) -> dict[str, Any]:
    p152_summary = load_json(request.p152_summary_path)
    p144_model = load_json(request.p144_model_path)
    binding = build_binding(p152_summary, p144_model, request.prompt_source_id)
    binding["run_id"] = request.run_id
    binding["generated_at_utc"] = request.generated_at_utc
    binding["source_p152_summary_path"] = str(request.p152_summary_path)
    binding["source_p144_model_path"] = str(request.p144_model_path)
    outputs = write_outputs(binding, request.output_dir)
    binding["output_files"] = outputs
    (request.output_dir / "P152A_PROMPT_SOURCE_BINDING.json").write_text(
        json.dumps(binding, ensure_ascii=False, indent=2, sort_keys=True),
        encoding="utf-8",
    )
    return binding


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="P152A prompt source binding for real GEM.")
    parser.add_argument("--p152-summary", required=True)
    parser.add_argument("--p144-model", required=True)
    parser.add_argument("--output-dir", required=True)
    parser.add_argument("--prompt-source-id", default=ACTIVE_PROMPT_SOURCE_ID)
    parser.add_argument("--run-id", default="P152A-PROMPT-SOURCE-BINDING-FOR-REAL-GEM")
    parser.add_argument("--generated-at-utc", default=utc_now_iso())
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    binding = run_binding(
        BindingRequest(
            p152_summary_path=Path(args.p152_summary),
            p144_model_path=Path(args.p144_model),
            output_dir=Path(args.output_dir),
            prompt_source_id=args.prompt_source_id,
            run_id=args.run_id,
            generated_at_utc=args.generated_at_utc,
        )
    )
    print(binding["status"])
    print(f"prompt_source_id={binding['prompt_source_id']}")
    print(
        f"selected_prompt_source_status={binding['selected_prompt_source'].get('status') if binding['selected_prompt_source'] else ''}"
    )
    print(f"prompt_source_count={binding['prompt_source_count']}")
    print(f"historical_reference_count={binding['historical_reference_count']}")
    print(f"allowed_for_p152_count={binding['allowed_for_p152_count']}")
    print(f"blocker_count={binding['blocker_count']}")
    print("google_sheets_write=false")
    print("public_deploy=false")
    print("real_gem_import_executed=false")
    print(f"output_dir={args.output_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
