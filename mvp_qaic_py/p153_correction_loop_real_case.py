from __future__ import annotations

import argparse
import csv
import json
import sys
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

VERSION = "MVP_QAIC_P153_CORRECTION_LOOP_REAL_CASE_1.0.0_SAFE"
STATUS_READY = "P153_CORRECTION_LOOP_REAL_CASE_READY_REVIEW_ONLY"

SAFETY_MARKERS = {
    "correction_loop_only": True,
    "review_only": True,
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
class CorrectionLoopRequest:
    p152_report_path: Path
    p152a_binding_path: Path
    output_dir: Path
    run_id: str
    generated_at_utc: str


def utc_now_iso() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def validate_p152_report(report: dict[str, Any]) -> list[str]:
    blockers: list[str] = []
    if report.get("status") != "P152_REAL_GEM_RESPONSE_IMPORTED_LOCAL_REVIEW":
        blockers.append("P152_REAL_IMPORT_STATUS_NOT_READY")
    if report.get("mode") != "REAL_GEM_RESPONSE_FILE_IMPORT":
        blockers.append("P152_MODE_NOT_REAL_IMPORT")
    if report.get("validation_status") != "VALIDATED_FOR_HUMAN_REVIEW":
        blockers.append("P152_VALIDATION_NOT_READY")
    if int(report.get("blocker_count", 0) or 0) != 0:
        blockers.append("P152_BLOCKERS_NOT_ZERO")
    safety = report.get("safety", {})
    if safety.get("google_sheets_write") is not False:
        blockers.append("GOOGLE_SHEETS_WRITE_NOT_FALSE")
    if safety.get("public_deploy") is not False:
        blockers.append("PUBLIC_DEPLOY_NOT_FALSE")
    if safety.get("auto_apply_gem_response") is not False:
        blockers.append("AUTO_APPLY_GEM_RESPONSE_NOT_FALSE")
    return blockers


def validate_p152a_binding(binding: dict[str, Any]) -> list[str]:
    blockers: list[str] = []
    if binding.get("status") != "P152A_PROMPT_SOURCE_BINDING_READY_FOR_REAL_GEM":
        blockers.append("P152A_BINDING_STATUS_NOT_READY")
    if binding.get("prompt_source_id") != "P132_P133_PORTFOLIO_MULTIMODAL_REVIEW":
        blockers.append("P152A_PROMPT_SOURCE_NOT_P132_P133")
    selected = binding.get("selected_prompt_source") or {}
    if selected.get("status") != "ACTIVE_FOR_P152_REAL_GEM":
        blockers.append("P152A_SELECTED_SOURCE_NOT_ACTIVE")
    if binding.get("safety", {}).get("google_sheets_write") is not False:
        blockers.append("P152A_GOOGLE_SHEETS_WRITE_NOT_FALSE")
    return blockers


def _payload_from_report(report: dict[str, Any]) -> dict[str, Any]:
    payload = report.get("response_payload")
    return payload if isinstance(payload, dict) else {}


def _collect_payload_checks(payload: dict[str, Any]) -> list[dict[str, str]]:
    checks: list[dict[str, str]] = []
    required = [
        ("status", "status", "REVIEW_REQUIRED|OK|BLOCKED"),
        ("human_review_required", "human_review_required", "true"),
        ("no_order_no_sizing", "no_order_no_sizing", "true"),
        ("NO_AUTO_APPLY", "NO_AUTO_APPLY", "true"),
        ("image_used", "image_used", "true when source_type=image"),
        ("reference_currency", "reference_currency", "USD or explicit"),
    ]
    for check_id, key, expected in required:
        value = payload.get(key)
        ok = "REVIEW" if key in {"image_used", "reference_currency"} else "OK"
        if key == "human_review_required" and value is not True:
            ok = "FAIL"
        if key == "no_order_no_sizing" and value is not True:
            ok = "FAIL"
        if key == "NO_AUTO_APPLY" and value is not True:
            ok = "FAIL"
        checks.append(
            {
                "check_id": check_id,
                "field": key,
                "observed": json.dumps(value, ensure_ascii=False),
                "expected": expected,
                "status": ok,
            }
        )
    return checks


def build_actions(report: dict[str, Any], binding: dict[str, Any]) -> list[dict[str, Any]]:
    payload = _payload_from_report(report)
    actions: list[dict[str, Any]] = []

    warnings = report.get("warnings") or []
    blockers = report.get("blockers") or []
    validation = report.get("validation") or {}

    if blockers:
        for idx, blocker in enumerate(blockers, start=1):
            actions.append(
                {
                    "action_id": f"P153-BLOCKER-{idx:03d}",
                    "action_type": "BLOCKER_REVIEW",
                    "priority": "P0",
                    "source": "P152_IMPORT",
                    "description": blocker,
                    "recommended_change": "Corriger le fichier GEM ou le prompt avant tout import.",
                    "apply_allowed": False,
                    "human_review_required": True,
                }
            )

    if warnings or validation.get("warnings"):
        for idx, warning in enumerate(
            list(warnings) + list(validation.get("warnings", [])), start=1
        ):
            actions.append(
                {
                    "action_id": f"P153-WARNING-{idx:03d}",
                    "action_type": "WARNING_REVIEW",
                    "priority": "P1",
                    "source": "P152_VALIDATION",
                    "description": warning,
                    "recommended_change": "Renforcer le prompt P132/P133 ou compléter la réponse GEM.",
                    "apply_allowed": False,
                    "human_review_required": True,
                }
            )

    for check in _collect_payload_checks(payload):
        if check["status"] in {"FAIL", "REVIEW"}:
            actions.append(
                {
                    "action_id": f"P153-CHECK-{check['check_id'].upper()}",
                    "action_type": "PAYLOAD_FIELD_REVIEW",
                    "priority": "P1" if check["status"] == "FAIL" else "P2",
                    "source": "P152_PAYLOAD",
                    "description": f"{check['field']} observed={check['observed']} expected={check['expected']}",
                    "recommended_change": "Valider manuellement la cohérence ou renforcer le prompt source.",
                    "apply_allowed": False,
                    "human_review_required": True,
                }
            )

    # Always keep an explicit final human review action even when validation is clean.
    actions.append(
        {
            "action_id": "P153-HUMAN-REVIEW-001",
            "action_type": "FINAL_HUMAN_REVIEW",
            "priority": "P0",
            "source": "P152_REAL_GEM_RESPONSE",
            "description": "Relire la réponse GEM réelle avant toute correction de prompt.",
            "recommended_change": "Confirmer les chiffres, la devise, l'image_used, et la présence des garde-fous no order/no sizing/no auto apply.",
            "apply_allowed": False,
            "human_review_required": True,
        }
    )

    actions.append(
        {
            "action_id": "P153-PROMPT-IMPROVEMENT-001",
            "action_type": "PROMPT_IMPROVEMENT_PROPOSAL",
            "priority": "P1",
            "source": binding.get("prompt_source_id", ""),
            "description": "Préparer une itération P132/P133 si la réponse GEM manque de précision ou de structure.",
            "recommended_change": "Ajouter seulement des corrections review-only, sans ordre, sans sizing, sans Sheet write.",
            "apply_allowed": False,
            "human_review_required": True,
        }
    )

    return actions


def build_report(p152_report: dict[str, Any], p152a_binding: dict[str, Any]) -> dict[str, Any]:
    blockers = validate_p152_report(p152_report) + validate_p152a_binding(p152a_binding)
    actions = build_actions(p152_report, p152a_binding)
    payload = _payload_from_report(p152_report)

    return {
        "status": STATUS_READY if not blockers else "P153_CORRECTION_LOOP_REAL_CASE_BLOCKED",
        "version": VERSION,
        "source_p152_status": p152_report.get("status"),
        "source_p152_validation_status": p152_report.get("validation_status"),
        "source_p152a_status": p152a_binding.get("status"),
        "prompt_source_id": p152a_binding.get("prompt_source_id"),
        "payload_status": payload.get("status"),
        "payload_reference_currency": payload.get("reference_currency"),
        "payload_image_used": payload.get("image_used"),
        "payload_human_review_required": payload.get("human_review_required"),
        "payload_no_order_no_sizing": payload.get("no_order_no_sizing"),
        "payload_no_auto_apply": payload.get("NO_AUTO_APPLY"),
        "action_count": len(actions),
        "actions": actions,
        "blocker_count": len(blockers),
        "blockers": blockers,
        "review_gate": "HUMAN_REVIEW_REQUIRED",
        "apply_allowed": False,
        "safety": dict(SAFETY_MARKERS),
        "next": "P154_PROMPT_CORRECTION_APPLY_PLAN_OR_STOP",
    }


def write_outputs(report: dict[str, Any], output_dir: Path) -> dict[str, str]:
    output_dir.mkdir(parents=True, exist_ok=True)

    report_path = output_dir / "P153_CORRECTION_LOOP_REAL_CASE_REPORT.json"
    actions_csv = output_dir / "P153_CORRECTION_ACTIONS.csv"
    suggestions_md = output_dir / "P153_PROMPT_IMPROVEMENT_SUGGESTIONS.md"
    checklist_md = output_dir / "P153_OPERATOR_REVIEW_CHECKLIST.md"
    summary_path = output_dir / "P153_SUMMARY.json"

    report_path.write_text(
        json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True), encoding="utf-8"
    )

    with actions_csv.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=[
                "action_id",
                "action_type",
                "priority",
                "source",
                "description",
                "recommended_change",
                "apply_allowed",
                "human_review_required",
            ],
        )
        writer.writeheader()
        for action in report["actions"]:
            writer.writerow(action)

    suggestions_md.write_text(
        "\n".join(
            [
                "# P153 — Prompt Improvement Suggestions",
                "",
                f"- Prompt source: `{report['prompt_source_id']}`",
                f"- Payload status: `{report['payload_status']}`",
                f"- Action count: `{report['action_count']}`",
                "",
                "## Règles",
                "",
                "- Toute correction reste review-only.",
                "- Aucun ordre, aucun sizing, aucun auto-apply.",
                "- Ne pas écrire dans Sheets.",
                "- Ne pas déployer publiquement.",
                "",
                "## Suggestions prioritaires",
                "",
                "- Confirmer que la réponse GEM a bien exploité l'image.",
                "- Confirmer la devise de référence.",
                "- Confirmer les reconciliations arithmétiques.",
                "- Renforcer P132/P133 uniquement si un manque est observé.",
                "",
            ]
        ),
        encoding="utf-8",
    )

    checklist_md.write_text(
        "\n".join(
            [
                "# P153 — Operator Review Checklist",
                "",
                "- [ ] Image utilisée correctement",
                "- [ ] Devise correcte",
                "- [ ] Total portefeuille cohérent",
                "- [ ] Somme des positions cohérente",
                "- [ ] PnL cohérent",
                "- [ ] `human_review_required=true`",
                "- [ ] `no_order_no_sizing=true`",
                "- [ ] `NO_AUTO_APPLY=true`",
                "- [ ] Aucun ordre",
                "- [ ] Aucun sizing",
                "- [ ] Aucune action Sheet/public",
                "",
            ]
        ),
        encoding="utf-8",
    )

    summary = {
        "status": report["status"],
        "prompt_source_id": report["prompt_source_id"],
        "source_p152_status": report["source_p152_status"],
        "source_p152_validation_status": report["source_p152_validation_status"],
        "action_count": report["action_count"],
        "blocker_count": report["blocker_count"],
        "review_gate": report["review_gate"],
        "apply_allowed": False,
        "google_sheets_write": False,
        "live_google_sheets_read": False,
        "public_deploy": False,
        "broker": False,
        "order": False,
        "sizing": False,
        "auto_apply_gem_response": False,
        "output_dir": str(output_dir),
        "next": report["next"],
    }
    summary_path.write_text(
        json.dumps(summary, ensure_ascii=False, indent=2, sort_keys=True), encoding="utf-8"
    )

    return {
        "report_json": str(report_path),
        "actions_csv": str(actions_csv),
        "suggestions_md": str(suggestions_md),
        "checklist_md": str(checklist_md),
        "summary_json": str(summary_path),
    }


def run_correction_loop(request: CorrectionLoopRequest) -> dict[str, Any]:
    p152_report = load_json(request.p152_report_path)
    p152a_binding = load_json(request.p152a_binding_path)
    report = build_report(p152_report, p152a_binding)
    report["run_id"] = request.run_id
    report["generated_at_utc"] = request.generated_at_utc
    report["source_p152_report_path"] = str(request.p152_report_path)
    report["source_p152a_binding_path"] = str(request.p152a_binding_path)
    outputs = write_outputs(report, request.output_dir)
    report["output_files"] = outputs
    (request.output_dir / "P153_CORRECTION_LOOP_REAL_CASE_REPORT.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True),
        encoding="utf-8",
    )
    return report


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="P153 correction loop real case.")
    parser.add_argument("--p152-report", required=True)
    parser.add_argument("--p152a-binding", required=True)
    parser.add_argument("--output-dir", required=True)
    parser.add_argument("--run-id", default="P153-CORRECTION-LOOP-REAL-CASE")
    parser.add_argument("--generated-at-utc", default=utc_now_iso())
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    report = run_correction_loop(
        CorrectionLoopRequest(
            p152_report_path=Path(args.p152_report),
            p152a_binding_path=Path(args.p152a_binding),
            output_dir=Path(args.output_dir),
            run_id=args.run_id,
            generated_at_utc=args.generated_at_utc,
        )
    )
    print(report["status"])
    print(f"prompt_source_id={report['prompt_source_id']}")
    print(f"source_p152_status={report['source_p152_status']}")
    print(f"source_p152_validation_status={report['source_p152_validation_status']}")
    print(f"action_count={report['action_count']}")
    print(f"blocker_count={report['blocker_count']}")
    print("apply_allowed=false")
    print("google_sheets_write=false")
    print("public_deploy=false")
    print("auto_apply_gem_response=false")
    print(f"output_dir={args.output_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
