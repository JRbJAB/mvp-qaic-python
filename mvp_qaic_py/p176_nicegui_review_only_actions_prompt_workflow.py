from __future__ import annotations

import argparse
import csv
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from mvp_qaic_py.p175_nicegui_operator_ergonomics_polish import build_operator_ergonomics_model


SAFETY_FLAGS: dict[str, bool] = {
    "google_sheets_write": False,
    "live_google_api_call_from_python": False,
    "apps_script_execution": False,
    "clasp_push": False,
    "public_serve": False,
    "broker": False,
    "order": False,
    "sizing": False,
    "raw_operator_exports_committed": False,
    "auto_apply_gem_response": False,
    "source_prompt_modified": False,
}


def _utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def build_review_only_prompt_workflow(
    project_root: str | Path,
    *,
    generated_at: str | None = None,
) -> dict[str, Any]:
    root = Path(project_root)
    ergonomics = build_operator_ergonomics_model(root)
    generated = generated_at or _utc_now()

    blockers: list[str] = list(ergonomics.get("blockers", []))
    if not ergonomics.get("ergonomics_ready"):
        blockers.append("P175_ERGONOMICS_NOT_READY")

    steps: list[dict[str, Any]] = [
        {
            "step_id": "select_prompt_source",
            "label": "Sélectionner source prompt",
            "tab": "prompt",
            "mode": "READ_ONLY",
            "allowed": True,
            "writes_data": False,
        },
        {
            "step_id": "copy_prompt_to_gem",
            "label": "Copier prompt vers GEM",
            "tab": "prompt",
            "mode": "LOCAL_UI_ONLY",
            "allowed": True,
            "writes_data": False,
        },
        {
            "step_id": "save_gem_response_local_review_file",
            "label": "Sauver réponse GEM fichier local review-only",
            "tab": "review",
            "mode": "LOCAL_FILE_REVIEW_ONLY",
            "allowed": True,
            "writes_data": False,
        },
        {
            "step_id": "preview_review_decision",
            "label": "Prévisualiser décision humaine",
            "tab": "review",
            "mode": "PREVIEW_ONLY",
            "allowed": True,
            "writes_data": False,
        },
        {
            "step_id": "apply_review_decision",
            "label": "Appliquer décision review",
            "tab": "review",
            "mode": "BLOCKED_UNTIL_EXPLICIT_GATE",
            "allowed": False,
            "writes_data": False,
        },
        {
            "step_id": "apply_prompt_patch",
            "label": "Appliquer patch prompt runtime",
            "tab": "prompt",
            "mode": "BLOCKED_UNTIL_EXPLICIT_GATE",
            "allowed": False,
            "writes_data": False,
        },
    ]

    allowed_steps = sum(1 for step in steps if step["allowed"])
    blocked_steps = sum(1 for step in steps if not step["allowed"])
    workflow_ready = not blockers and allowed_steps == 4 and blocked_steps == 2

    return {
        "STATUS": "OK_P176_NICEGUI_REVIEW_ONLY_ACTIONS_PROMPT_WORKFLOW_READY"
        if workflow_ready
        else "BLOCKED_P176_NICEGUI_REVIEW_ONLY_ACTIONS_PROMPT_WORKFLOW",
        "generated_at": generated,
        "project_root": str(root),
        "source_step": "P175_NICEGUI_OPERATOR_ERGONOMICS_POLISH",
        "workflow_ready": workflow_ready,
        "step_count": len(steps),
        "allowed_step_count": allowed_steps,
        "blocked_step_count": blocked_steps,
        "blocker_count": len(blockers),
        "blockers": blockers,
        "steps": steps,
        "workflow_rules": {
            "copy_prompt_allowed": True,
            "save_gem_response_local_allowed": True,
            "review_preview_allowed": True,
            "apply_decision_allowed": False,
            "apply_prompt_patch_allowed": False,
            "auto_apply_gem_response_allowed": False,
        },
        **SAFETY_FLAGS,
        "recommended_next": "P177_GEM_PORTFOLIO_PROMPT_WORKFLOW_USABLE_SMOKE",
    }


def export_review_only_prompt_workflow(
    project_root: str | Path,
    *,
    export_dir: str | Path | None = None,
) -> dict[str, Any]:
    root = Path(project_root)
    if export_dir is None:
        stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        export_path = (
            root / "05_EXPORTS" / f"P176_NICEGUI_REVIEW_ONLY_ACTIONS_PROMPT_WORKFLOW_{stamp}"
        )
    else:
        export_path = Path(export_dir)

    export_path.mkdir(parents=True, exist_ok=True)
    payload = build_review_only_prompt_workflow(root)
    payload["export_dir"] = str(export_path)

    (export_path / "P176_REVIEW_ONLY_PROMPT_WORKFLOW_MODEL.json").write_text(
        json.dumps(payload, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )

    summary_keys = [
        "STATUS",
        "generated_at",
        "project_root",
        "source_step",
        "export_dir",
        "workflow_ready",
        "step_count",
        "allowed_step_count",
        "blocked_step_count",
        "blocker_count",
        "blockers",
        "google_sheets_write",
        "live_google_api_call_from_python",
        "apps_script_execution",
        "clasp_push",
        "public_serve",
        "broker",
        "order",
        "sizing",
        "raw_operator_exports_committed",
        "auto_apply_gem_response",
        "source_prompt_modified",
        "recommended_next",
    ]
    (export_path / "P176_SUMMARY.json").write_text(
        json.dumps({key: payload[key] for key in summary_keys}, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )

    with (export_path / "P176_WORKFLOW_STEPS.csv").open(
        "w", encoding="utf-8", newline=""
    ) as file_obj:
        writer = csv.DictWriter(
            file_obj,
            fieldnames=["step_id", "label", "tab", "mode", "allowed", "writes_data"],
        )
        writer.writeheader()
        writer.writerows(payload["steps"])

    report = [
        "# P176 NiceGUI Review-Only Actions And Prompt Workflow",
        "",
        f"- STATUS: {payload['STATUS']}",
        f"- workflow_ready: {payload['workflow_ready']}",
        f"- step_count: {payload['step_count']}",
        f"- allowed_step_count: {payload['allowed_step_count']}",
        f"- blocked_step_count: {payload['blocked_step_count']}",
        f"- blocker_count: {payload['blocker_count']}",
        "",
        "Allowed:",
        "- select_prompt_source",
        "- copy_prompt_to_gem",
        "- save_gem_response_local_review_file",
        "- preview_review_decision",
        "",
        "Blocked:",
        "- apply_review_decision",
        "- apply_prompt_patch",
        "",
        "Safety:",
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
        "- P177_GEM_PORTFOLIO_PROMPT_WORKFLOW_USABLE_SMOKE",
    ]
    (export_path / "P176_REVIEW_ONLY_PROMPT_WORKFLOW_REPORT.md").write_text(
        "\n".join(report) + "\n",
        encoding="utf-8",
    )

    return payload


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="P176 review-only prompt workflow.")
    parser.add_argument("--project-root", default=".")
    parser.add_argument("--export-dir", default=None)
    parser.add_argument("--write-export", action="store_true")
    parser.add_argument("--json", action="store_true")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = _build_parser().parse_args(argv)
    if args.write_export:
        payload = export_review_only_prompt_workflow(args.project_root, export_dir=args.export_dir)
    else:
        payload = build_review_only_prompt_workflow(args.project_root)

    if args.json:
        print(json.dumps(payload, indent=2, ensure_ascii=False))
    else:
        print(payload["STATUS"])
        print(f"WORKFLOW_READY={payload['workflow_ready']}")
        print(f"ALLOWED_STEP_COUNT={payload['allowed_step_count']}")
        print(f"BLOCKED_STEP_COUNT={payload['blocked_step_count']}")
        print(f"BLOCKER_COUNT={payload['blocker_count']}")

    return 0 if payload["workflow_ready"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
