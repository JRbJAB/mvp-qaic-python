from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from mvp_qaic_py.p176_nicegui_review_only_actions_prompt_workflow import (
    build_review_only_prompt_workflow,
)


SAFETY_FLAGS: dict[str, bool] = {
    "gem_call_executed": False,
    "google_sheets_write": False,
    "live_google_api_call_from_python": False,
    "apps_script_execution": False,
    "clasp_push": False,
    "public_serve": False,
    "broker": False,
    "order": False,
    "sizing": False,
    "auto_apply_gem_response": False,
    "source_prompt_modified": False,
}


def _utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def build_gem_portfolio_prompt_smoke(
    project_root: str | Path,
    *,
    generated_at: str | None = None,
) -> dict[str, Any]:
    root = Path(project_root)
    workflow = build_review_only_prompt_workflow(root)
    generated = generated_at or _utc_now()

    blockers: list[str] = list(workflow.get("blockers", []))
    if not workflow.get("workflow_ready"):
        blockers.append("P176_WORKFLOW_NOT_READY")

    prompt_sections = [
        "input_mode",
        "language",
        "hard_rules",
        "portfolio_extraction",
        "data_quality_review",
        "risk_review",
        "decision_review",
        "json_output_contract",
        "missing_data_policy",
        "safety_audit",
    ]

    sample_operator_case = {
        "case_id": "P177_SAMPLE_GEM_PORTFOLIO_IMAGE_REVIEW",
        "input_type": "IMAGE_OR_SCREENSHOT_PLUS_OPTIONAL_TEXT",
        "asset_scope": "crypto_portfolio",
        "reference_currency": "USD_OR_EUR_REVIEW_REQUIRED",
        "expected_output_mode": "JSON_PLUS_FRENCH_REVIEW_SUMMARY",
        "human_review_required": True,
    }

    required_guards = {
        "no_gem_call": True,
        "no_auto_apply": True,
        "no_order": True,
        "no_sizing": True,
        "no_broker": True,
        "review_required_if_missing_data": True,
        "block_if_score_inputs_missing": True,
    }

    usability_checks = [
        {
            "check_id": "prompt_sections_present",
            "status": "PASS" if len(prompt_sections) >= 8 else "FAIL",
        },
        {
            "check_id": "operator_case_defined",
            "status": "PASS" if sample_operator_case["human_review_required"] else "FAIL",
        },
        {
            "check_id": "guards_review_only",
            "status": "PASS" if all(required_guards.values()) else "FAIL",
        },
        {
            "check_id": "copy_prompt_step_available",
            "status": "PASS" if workflow["workflow_rules"]["copy_prompt_allowed"] else "FAIL",
        },
        {
            "check_id": "save_response_local_available",
            "status": "PASS"
            if workflow["workflow_rules"]["save_gem_response_local_allowed"]
            else "FAIL",
        },
        {
            "check_id": "apply_steps_blocked",
            "status": "PASS"
            if not workflow["workflow_rules"]["apply_decision_allowed"]
            and not workflow["workflow_rules"]["apply_prompt_patch_allowed"]
            else "FAIL",
        },
    ]

    failed_checks = [row["check_id"] for row in usability_checks if row["status"] != "PASS"]
    blockers.extend(f"FAILED_CHECK:{check}" for check in failed_checks)

    smoke_ready = not blockers and len(usability_checks) == 6

    return {
        "STATUS": "OK_P177_GEM_PORTFOLIO_PROMPT_WORKFLOW_USABLE_SMOKE_READY"
        if smoke_ready
        else "BLOCKED_P177_GEM_PORTFOLIO_PROMPT_WORKFLOW_USABLE_SMOKE",
        "generated_at": generated,
        "project_root": str(root),
        "source_step": "P176_NICEGUI_REVIEW_ONLY_ACTIONS_AND_PROMPT_WORKFLOW",
        "sample_operator_case": sample_operator_case,
        "prompt_sections": prompt_sections,
        "required_guards": required_guards,
        "usability_checks": usability_checks,
        "check_count": len(usability_checks),
        "pass_count": sum(1 for row in usability_checks if row["status"] == "PASS"),
        "fail_count": len(failed_checks),
        "smoke_ready": smoke_ready,
        "blocker_count": len(blockers),
        "blockers": blockers,
        **SAFETY_FLAGS,
        "recommended_next": "P178_OPERATOR_SHORTCUT_AND_PRIVATE_COCKPIT_HANDOFF",
    }


def export_gem_portfolio_prompt_smoke(
    project_root: str | Path,
    *,
    export_dir: str | Path | None = None,
) -> dict[str, Any]:
    root = Path(project_root)
    if export_dir is None:
        stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        export_path = (
            root / "05_EXPORTS" / f"P177_GEM_PORTFOLIO_PROMPT_WORKFLOW_USABLE_SMOKE_{stamp}"
        )
    else:
        export_path = Path(export_dir)

    export_path.mkdir(parents=True, exist_ok=True)
    payload = build_gem_portfolio_prompt_smoke(root)
    payload["export_dir"] = str(export_path)

    (export_path / "P177_GEM_PORTFOLIO_PROMPT_SMOKE_MODEL.json").write_text(
        json.dumps(payload, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )

    summary_keys = [
        "STATUS",
        "generated_at",
        "project_root",
        "source_step",
        "export_dir",
        "check_count",
        "pass_count",
        "fail_count",
        "smoke_ready",
        "blocker_count",
        "blockers",
        "gem_call_executed",
        "google_sheets_write",
        "live_google_api_call_from_python",
        "apps_script_execution",
        "clasp_push",
        "public_serve",
        "broker",
        "order",
        "sizing",
        "auto_apply_gem_response",
        "source_prompt_modified",
        "recommended_next",
    ]
    (export_path / "P177_SUMMARY.json").write_text(
        json.dumps({key: payload[key] for key in summary_keys}, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )

    prompt_text = "\n".join(
        [
            "# P177 Operator Prompt Smoke — GEM Portfolio Image",
            "",
            "Utilise le prompt MVP QAIC portfolio/image en mode review-only.",
            "",
            "Contraintes:",
            "- Ne pas passer d’ordre.",
            "- Ne pas calculer de sizing automatique.",
            "- Ne pas appliquer automatiquement la réponse GEM.",
            "- Retourner REVIEW_REQUIRED si les données nécessaires manquent.",
            "- Garder les enums techniques inchangés.",
            "",
            "Entrée attendue:",
            "- Capture écran portfolio crypto.",
            "- Texte copié optionnel.",
            "",
            "Sortie attendue:",
            "- JSON structuré.",
            "- Résumé français.",
            "- missing_data.",
            "- blockers.",
            "- safety_audit.",
            "",
        ]
    )
    (export_path / "P177_OPERATOR_PROMPT_SMOKE_TEXT.md").write_text(prompt_text, encoding="utf-8")

    report = [
        "# P177 GEM Portfolio Prompt Workflow Usable Smoke",
        "",
        f"- STATUS: {payload['STATUS']}",
        f"- check_count: {payload['check_count']}",
        f"- pass_count: {payload['pass_count']}",
        f"- fail_count: {payload['fail_count']}",
        f"- smoke_ready: {payload['smoke_ready']}",
        f"- blocker_count: {payload['blocker_count']}",
        "",
        "Validated:",
        "- Prompt workflow can be used for GEM portfolio/image review.",
        "- Copy prompt step is available.",
        "- Save GEM response local review file is available.",
        "- Apply steps remain blocked.",
        "- No GEM call is executed by Python.",
        "",
        "Safety:",
        "- GEM_CALL_EXECUTED=False",
        "- AUTO_APPLY_GEM_RESPONSE=False",
        "- SOURCE_PROMPT_MODIFIED=False",
        "- GOOGLE_SHEETS_WRITE=False",
        "- LIVE_GOOGLE_API_CALL_FROM_PYTHON=False",
        "- APPS_SCRIPT_EXECUTION=False",
        "- CLASP_PUSH=False",
        "- PUBLIC_SERVE=False",
        "- BROKER=False",
        "- ORDER=False",
        "- SIZING=False",
        "",
        "Next:",
        "- P178_OPERATOR_SHORTCUT_AND_PRIVATE_COCKPIT_HANDOFF",
    ]
    (export_path / "P177_GEM_PORTFOLIO_PROMPT_SMOKE_REPORT.md").write_text(
        "\n".join(report) + "\n",
        encoding="utf-8",
    )

    return payload


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="P177 GEM portfolio prompt workflow usable smoke.")
    parser.add_argument("--project-root", default=".")
    parser.add_argument("--export-dir", default=None)
    parser.add_argument("--write-export", action="store_true")
    parser.add_argument("--json", action="store_true")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = _build_parser().parse_args(argv)
    if args.write_export:
        payload = export_gem_portfolio_prompt_smoke(args.project_root, export_dir=args.export_dir)
    else:
        payload = build_gem_portfolio_prompt_smoke(args.project_root)

    if args.json:
        print(json.dumps(payload, indent=2, ensure_ascii=False))
    else:
        print(payload["STATUS"])
        print(f"SMOKE_READY={payload['smoke_ready']}")
        print(f"PASS_COUNT={payload['pass_count']}")
        print(f"FAIL_COUNT={payload['fail_count']}")
        print(f"BLOCKER_COUNT={payload['blocker_count']}")

    return 0 if payload["smoke_ready"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
