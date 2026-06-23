from __future__ import annotations

import argparse
import csv
import json
import sys
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

VERSION = "MVP_QAIC_P154_PROMPT_CORRECTION_APPLY_PLAN_OR_STOP_1.0.0_SAFE"
STATUS_READY = "P154_PROMPT_CORRECTION_APPLY_PLAN_READY_REVIEW_ONLY"

SAFETY_MARKERS = {
    "apply_plan_only": True,
    "review_only": True,
    "prompt_source_modified": False,
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
class ApplyPlanRequest:
    p153_report_path: Path
    output_dir: Path
    run_id: str
    generated_at_utc: str


def utc_now_iso() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def validate_p153(report: dict[str, Any]) -> list[str]:
    blockers: list[str] = []
    if report.get("status") != "P153_CORRECTION_LOOP_REAL_CASE_READY_REVIEW_ONLY":
        blockers.append("P153_STATUS_NOT_READY")
    if int(report.get("blocker_count", 0) or 0) != 0:
        blockers.append("P153_BLOCKERS_NOT_ZERO")
    if report.get("apply_allowed") is not False:
        blockers.append("P153_APPLY_ALLOWED_NOT_FALSE")
    safety = report.get("safety", {})
    if safety.get("google_sheets_write") is not False:
        blockers.append("GOOGLE_SHEETS_WRITE_NOT_FALSE")
    if safety.get("public_deploy") is not False:
        blockers.append("PUBLIC_DEPLOY_NOT_FALSE")
    if safety.get("auto_apply_gem_response") is not False:
        blockers.append("AUTO_APPLY_GEM_RESPONSE_NOT_FALSE")
    return blockers


def build_apply_plan_rows(p153_report: dict[str, Any]) -> list[dict[str, Any]]:
    actions = p153_report.get("actions") or []
    rows: list[dict[str, Any]] = []
    for idx, action in enumerate(actions, start=1):
        action_type = str(action.get("action_type", "REVIEW"))
        priority = str(action.get("priority", "P2"))
        source = str(action.get("source", ""))
        description = str(action.get("description", ""))
        recommended_change = str(action.get("recommended_change", ""))

        if action_type == "FINAL_HUMAN_REVIEW":
            correction_type = "NO_PROMPT_EDIT_REVIEW_CHECK"
            proposed_edit = "Valider manuellement la réponse GEM avant toute correction."
        elif action_type == "PROMPT_IMPROVEMENT_PROPOSAL":
            correction_type = "PROMPT_EDIT_CANDIDATE"
            proposed_edit = (
                "Renforcer P132/P133 pour demander explicitement : image evidence, devise, "
                "réconciliation totale, missing_data, no_order_no_sizing, NO_AUTO_APPLY."
            )
        elif action_type == "PAYLOAD_FIELD_REVIEW":
            correction_type = "PROMPT_FIELD_CLARIFICATION"
            proposed_edit = "Ajouter/renforcer la consigne de sortie pour ce champ dans P132/P133."
        else:
            correction_type = "REVIEW_ONLY"
            proposed_edit = recommended_change

        rows.append(
            {
                "plan_id": f"P154-PLAN-{idx:03d}",
                "source_action_id": str(action.get("action_id", f"P153-ACTION-{idx:03d}")),
                "priority": priority,
                "source": source,
                "action_type": action_type,
                "correction_type": correction_type,
                "description": description,
                "proposed_edit": proposed_edit,
                "apply_allowed": False,
                "apply_now": "NO",
                "human_review_required": True,
                "status": "READY_FOR_HUMAN_REVIEW",
            }
        )

    if not rows:
        rows.append(
            {
                "plan_id": "P154-PLAN-001",
                "source_action_id": "P153-NO-ACTION",
                "priority": "P2",
                "source": "P153",
                "action_type": "NO_ACTION",
                "correction_type": "NO_PROMPT_EDIT_REQUIRED",
                "description": "Aucune correction explicite remontée par P153.",
                "proposed_edit": "Conserver P132/P133 tel quel après revue humaine.",
                "apply_allowed": False,
                "apply_now": "NO",
                "human_review_required": True,
                "status": "READY_FOR_HUMAN_REVIEW",
            }
        )
    return rows


def build_report(p153_report: dict[str, Any]) -> dict[str, Any]:
    blockers = validate_p153(p153_report)
    plan_rows = build_apply_plan_rows(p153_report)

    prompt_edit_candidate_count = sum(
        1 for row in plan_rows if row["correction_type"] == "PROMPT_EDIT_CANDIDATE"
    )
    field_clarification_count = sum(
        1 for row in plan_rows if row["correction_type"] == "PROMPT_FIELD_CLARIFICATION"
    )
    no_apply_count = sum(1 for row in plan_rows if row["apply_now"] == "NO")

    return {
        "status": STATUS_READY if not blockers else "P154_PROMPT_CORRECTION_APPLY_PLAN_BLOCKED",
        "version": VERSION,
        "source_p153_status": p153_report.get("status"),
        "prompt_source_id": p153_report.get("prompt_source_id"),
        "source_p152_status": p153_report.get("source_p152_status"),
        "source_p152_validation_status": p153_report.get("source_p152_validation_status"),
        "plan_row_count": len(plan_rows),
        "prompt_edit_candidate_count": prompt_edit_candidate_count,
        "field_clarification_count": field_clarification_count,
        "no_apply_count": no_apply_count,
        "apply_allowed": False,
        "apply_now_yes_count": 0,
        "human_review_required": True,
        "plan_rows": plan_rows,
        "blocker_count": len(blockers),
        "blockers": blockers,
        "safety": dict(SAFETY_MARKERS),
        "next": "P155_PROMPT_CORRECTION_WORKBENCH_OR_STOP",
    }


def write_outputs(report: dict[str, Any], output_dir: Path) -> dict[str, str]:
    output_dir.mkdir(parents=True, exist_ok=True)

    report_path = output_dir / "P154_PROMPT_CORRECTION_APPLY_PLAN_REPORT.json"
    plan_csv = output_dir / "P154_PROMPT_CORRECTION_APPLY_PLAN.csv"
    patch_md = output_dir / "P154_P132_P133_PATCH_PLAN.md"
    review_md = output_dir / "P154_HUMAN_REVIEW_DECISION.md"
    summary_path = output_dir / "P154_SUMMARY.json"

    report_path.write_text(
        json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True), encoding="utf-8"
    )

    with plan_csv.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=[
                "plan_id",
                "source_action_id",
                "priority",
                "source",
                "action_type",
                "correction_type",
                "description",
                "proposed_edit",
                "apply_allowed",
                "apply_now",
                "human_review_required",
                "status",
            ],
        )
        writer.writeheader()
        for row in report["plan_rows"]:
            writer.writerow(row)

    patch_md.write_text(
        "\n".join(
            [
                "# P154 — P132/P133 Patch Plan",
                "",
                f"- Status: `{report['status']}`",
                f"- Prompt source: `{report['prompt_source_id']}`",
                f"- Plan rows: `{report['plan_row_count']}`",
                f"- Apply allowed: `{report['apply_allowed']}`",
                "",
                "## Plan proposé",
                "",
                "Ce batch ne modifie pas le prompt. Il prépare seulement les corrections candidates.",
                "",
                "### Correction candidate principale",
                "",
                "- Renforcer P132/P133 sur la preuve d'utilisation image.",
                "- Renforcer la devise de référence.",
                "- Renforcer la réconciliation arithmétique.",
                "- Maintenir `human_review_required=true`.",
                "- Maintenir `no_order_no_sizing=true`.",
                "- Maintenir `NO_AUTO_APPLY=true`.",
                "",
                "## Interdits",
                "",
                "- Pas d'apply automatique.",
                "- Pas d'écriture Sheets.",
                "- Pas de public deploy.",
                "- Pas de broker/order/sizing.",
                "",
            ]
        ),
        encoding="utf-8",
    )

    review_md.write_text(
        "\n".join(
            [
                "# P154 — Human Review Decision",
                "",
                "Décision requise avant P155 :",
                "",
                "- [ ] ACCEPT_AS_IS — aucune correction prompt",
                "- [ ] EDIT_P132_P133 — préparer une version corrigée review-only",
                "- [ ] NEEDS_MORE_GEM_CASES — importer d'autres réponses GEM avant correction",
                "- [ ] STOP — pause",
                "",
                "Valeur par défaut recommandée : `EDIT_P132_P133` uniquement si le vrai cas GEM a montré un manque clair.",
                "",
            ]
        ),
        encoding="utf-8",
    )

    summary = {
        "status": report["status"],
        "prompt_source_id": report["prompt_source_id"],
        "source_p153_status": report["source_p153_status"],
        "plan_row_count": report["plan_row_count"],
        "prompt_edit_candidate_count": report["prompt_edit_candidate_count"],
        "field_clarification_count": report["field_clarification_count"],
        "apply_allowed": False,
        "apply_now_yes_count": 0,
        "blocker_count": report["blocker_count"],
        "human_review_required": True,
        "google_sheets_write": False,
        "live_google_sheets_read": False,
        "public_deploy": False,
        "broker": False,
        "order": False,
        "sizing": False,
        "auto_apply_gem_response": False,
        "prompt_source_modified": False,
        "output_dir": str(output_dir),
        "next": report["next"],
    }
    summary_path.write_text(
        json.dumps(summary, ensure_ascii=False, indent=2, sort_keys=True), encoding="utf-8"
    )

    return {
        "report_json": str(report_path),
        "plan_csv": str(plan_csv),
        "patch_plan_md": str(patch_md),
        "human_review_md": str(review_md),
        "summary_json": str(summary_path),
    }


def run_apply_plan(request: ApplyPlanRequest) -> dict[str, Any]:
    p153_report = load_json(request.p153_report_path)
    report = build_report(p153_report)
    report["run_id"] = request.run_id
    report["generated_at_utc"] = request.generated_at_utc
    report["source_p153_report_path"] = str(request.p153_report_path)
    outputs = write_outputs(report, request.output_dir)
    report["output_files"] = outputs
    (request.output_dir / "P154_PROMPT_CORRECTION_APPLY_PLAN_REPORT.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True),
        encoding="utf-8",
    )
    return report


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="P154 prompt correction apply plan or stop.")
    parser.add_argument("--p153-report", required=True)
    parser.add_argument("--output-dir", required=True)
    parser.add_argument("--run-id", default="P154-PROMPT-CORRECTION-APPLY-PLAN-OR-STOP")
    parser.add_argument("--generated-at-utc", default=utc_now_iso())
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    report = run_apply_plan(
        ApplyPlanRequest(
            p153_report_path=Path(args.p153_report),
            output_dir=Path(args.output_dir),
            run_id=args.run_id,
            generated_at_utc=args.generated_at_utc,
        )
    )
    print(report["status"])
    print(f"prompt_source_id={report['prompt_source_id']}")
    print(f"source_p153_status={report['source_p153_status']}")
    print(f"plan_row_count={report['plan_row_count']}")
    print(f"prompt_edit_candidate_count={report['prompt_edit_candidate_count']}")
    print(f"apply_allowed={str(report['apply_allowed']).lower()}")
    print(f"apply_now_yes_count={report['apply_now_yes_count']}")
    print(f"blocker_count={report['blocker_count']}")
    print("google_sheets_write=false")
    print("public_deploy=false")
    print("prompt_source_modified=false")
    print(f"output_dir={args.output_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
