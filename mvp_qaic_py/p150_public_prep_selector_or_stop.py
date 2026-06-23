from __future__ import annotations

import argparse
import csv
import json
import sys
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

VERSION = "MVP_QAIC_P150_PUBLIC_PREP_SELECTOR_OR_STOP_1.0.0_SAFE"
STATUS_READY = "P150_PUBLIC_PREP_SELECTOR_OR_STOP_READY_READONLY"

SAFETY_MARKERS = {
    "selector_only": True,
    "live_google_sheets_read": False,
    "google_sheets_write": False,
    "apps_script_execution": False,
    "clasp_push": False,
    "broker": False,
    "order": False,
    "sizing": False,
    "auto_apply_gem_response": False,
    "public_deploy": False,
    "public_prep_only": True,
    "future_public_deploy_requires_explicit_go": True,
    "future_sheet_write_requires_explicit_go": True,
}


@dataclass(frozen=True)
class SelectorRequest:
    p149_report_path: Path
    output_dir: Path
    run_id: str
    generated_at_utc: str


def utc_now_iso() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def validate_p149(report: dict[str, Any]) -> list[str]:
    blockers: list[str] = []
    if report.get("status") != "P149_MIGRATION_CLOSE_GATE_READY_LOCAL_PRIVATE":
        blockers.append("P149_STATUS_NOT_READY")
    if report.get("migration_close_ready") is not True:
        blockers.append("MIGRATION_CLOSE_READY_NOT_TRUE")
    if report.get("mvp_prompt_cockpit_local_private_ready") is not True:
        blockers.append("MVP_LOCAL_PRIVATE_READY_NOT_TRUE")
    if report.get("blocker_count", 0) != 0:
        blockers.append("P149_BLOCKERS_NOT_ZERO")
    if report.get("safety", {}).get("google_sheets_write") is not False:
        blockers.append("GOOGLE_SHEETS_WRITE_NOT_FALSE")
    if report.get("safety", {}).get("public_deploy") is not False:
        blockers.append("PUBLIC_DEPLOY_NOT_FALSE")
    return blockers


def build_options(report: dict[str, Any]) -> list[dict[str, Any]]:
    return [
        {
            "option_id": "STOP_AFTER_P149",
            "label": "Stop / validation opérateur",
            "priority": "P0",
            "recommended": False,
            "why": "La migration locale/private est close ; pause possible pour validation visuelle par l'opérateur.",
            "writes": False,
            "public_deploy": False,
            "risk": "LOW",
            "next_batch": "STOP_WAIT_HUMAN_DECISION",
        },
        {
            "option_id": "P150B_LOCAL_PRIVATE_RELEASE_PACK",
            "label": "Release pack local privé",
            "priority": "P0",
            "recommended": True,
            "why": "Meilleur choix immédiat : empaqueter les preuves P140-P149, runbook, commandes launch et état safety avant tout public.",
            "writes": False,
            "public_deploy": False,
            "risk": "LOW",
            "next_batch": "P150B_LOCAL_PRIVATE_RELEASE_PACK",
        },
        {
            "option_id": "P150A_REAL_GEM_RESPONSE_IMPORT",
            "label": "Importer une vraie réponse GEM",
            "priority": "P1",
            "recommended": False,
            "why": "Utile pour remplacer la fixture P145, mais mieux après release pack local.",
            "writes": False,
            "public_deploy": False,
            "risk": "LOW",
            "next_batch": "P150A_REAL_GEM_RESPONSE_IMPORT",
        },
        {
            "option_id": "P150_PUBLIC_PREP_NO_DEPLOY",
            "label": "Préparation public sans déploiement",
            "priority": "P1",
            "recommended": False,
            "why": "Préparer la séparation contenu public / backend privé, sans tunnel ni déploiement.",
            "writes": False,
            "public_deploy": False,
            "risk": "MEDIUM",
            "next_batch": "P150_PUBLIC_PREP_NO_DEPLOY",
        },
        {
            "option_id": "P150C_SHEETS_WRITE_GATE_AFTER_EXPLICIT_GO",
            "label": "Future Sheet write gate",
            "priority": "P2",
            "recommended": False,
            "why": "Réservé à un GO explicite séparé ; pas nécessaire pour le cockpit local privé.",
            "writes": True,
            "public_deploy": False,
            "risk": "HIGH",
            "next_batch": "P150C_SHEETS_WRITE_GATE_AFTER_EXPLICIT_GO",
        },
    ]


def build_selector(report: dict[str, Any]) -> dict[str, Any]:
    blockers = validate_p149(report)
    options = build_options(report)
    recommended = next(option for option in options if option["recommended"])
    return {
        "status": STATUS_READY if not blockers else "P150_PUBLIC_PREP_SELECTOR_BLOCKED",
        "version": VERSION,
        "source_p149_status": report.get("status"),
        "source_p149_headline": {
            "migration_close_ready": report.get("migration_close_ready"),
            "mvp_prompt_cockpit_local_private_ready": report.get(
                "mvp_prompt_cockpit_local_private_ready"
            ),
            "evidence_ok_count": report.get("evidence_ok_count"),
            "required_export_count": report.get("required_export_count"),
            "blocker_count": report.get("blocker_count"),
        },
        "blocker_count": len(blockers),
        "blockers": blockers,
        "option_count": len(options),
        "options": options,
        "recommended_next": recommended["next_batch"] if not blockers else "BLOCKED_REVIEW_P149",
        "recommended_option_id": recommended["option_id"] if not blockers else "",
        "decision_required": "HUMAN_DECISION_BEFORE_PUBLIC_OR_SHEET_WRITE",
        "selector_scope": "READONLY_DECISION_PACK_NO_DEPLOY_NO_WRITE",
        "safety": dict(SAFETY_MARKERS),
        "next": recommended["next_batch"] if not blockers else "FIX_P149_BLOCKERS",
    }


def write_outputs(selector: dict[str, Any], output_dir: Path) -> dict[str, str]:
    output_dir.mkdir(parents=True, exist_ok=True)
    selector_path = output_dir / "P150_PUBLIC_PREP_SELECTOR.json"
    options_csv = output_dir / "P150_NEXT_OPTIONS.csv"
    md_path = output_dir / "P150_PUBLIC_PREP_SELECTOR.md"
    summary_path = output_dir / "P150_SUMMARY.json"
    handoff_path = output_dir / "P150_OPERATOR_HANDOFF.md"

    selector_path.write_text(
        json.dumps(selector, ensure_ascii=False, indent=2, sort_keys=True), encoding="utf-8"
    )

    with options_csv.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=[
                "option_id",
                "label",
                "priority",
                "recommended",
                "why",
                "writes",
                "public_deploy",
                "risk",
                "next_batch",
            ],
        )
        writer.writeheader()
        for option in selector["options"]:
            writer.writerow(option)

    options_lines = "\n".join(
        f"- `{option['option_id']}` — {option['label']} — rec={option['recommended']} — next `{option['next_batch']}`"
        for option in selector["options"]
    )
    md_path.write_text(
        "\n".join(
            [
                "# P150 — Public Prep Selector or Stop",
                "",
                f"- Status: `{selector['status']}`",
                f"- Recommended next: `{selector['recommended_next']}`",
                f"- Decision required: `{selector['decision_required']}`",
                "",
                "## Options",
                "",
                options_lines,
                "",
                "## Safety",
                "",
                "- Selector only",
                "- No Sheet write",
                "- No public deploy",
                "- No Apps Script / CLASP",
                "- No broker/order/sizing",
                "- Future Sheet write requires explicit GO",
                "- Future public deploy requires explicit GO",
                "",
            ]
        ),
        encoding="utf-8",
    )

    handoff_path.write_text(
        "\n".join(
            [
                "# P150 — Operator Handoff",
                "",
                "Recommandation opérationnelle : lancer `P150B_LOCAL_PRIVATE_RELEASE_PACK`.",
                "",
                "Raison : P149 a fermé la migration locale/private ; avant public prep ou vrais imports GEM, il faut figer un release pack local privé contenant preuves, exports, runbook et commandes launch.",
                "",
                "Ne pas lancer de Sheet write, public deploy, tunnel, broker, order ou sizing sans GO explicite séparé.",
                "",
            ]
        ),
        encoding="utf-8",
    )

    summary = {
        "status": selector["status"],
        "source_p149_status": selector["source_p149_status"],
        "recommended_next": selector["recommended_next"],
        "recommended_option_id": selector["recommended_option_id"],
        "option_count": selector["option_count"],
        "blocker_count": selector["blocker_count"],
        "decision_required": selector["decision_required"],
        "google_sheets_write": False,
        "live_google_sheets_read": False,
        "public_deploy": False,
        "broker": False,
        "order": False,
        "sizing": False,
        "auto_apply_gem_response": False,
        "output_dir": str(output_dir),
        "next": selector["next"],
    }
    summary_path.write_text(
        json.dumps(summary, ensure_ascii=False, indent=2, sort_keys=True), encoding="utf-8"
    )
    return {
        "selector_json": str(selector_path),
        "options_csv": str(options_csv),
        "markdown": str(md_path),
        "operator_handoff_md": str(handoff_path),
        "summary_json": str(summary_path),
    }


def run_selector(request: SelectorRequest) -> dict[str, Any]:
    report = load_json(request.p149_report_path)
    selector = build_selector(report)
    selector["run_id"] = request.run_id
    selector["generated_at_utc"] = request.generated_at_utc
    selector["source_p149_report_path"] = str(request.p149_report_path)
    outputs = write_outputs(selector, request.output_dir)
    selector["output_files"] = outputs
    (request.output_dir / "P150_PUBLIC_PREP_SELECTOR.json").write_text(
        json.dumps(selector, ensure_ascii=False, indent=2, sort_keys=True),
        encoding="utf-8",
    )
    return selector


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="P150 public prep selector or stop.")
    parser.add_argument("--p149-report", required=True)
    parser.add_argument("--output-dir", required=True)
    parser.add_argument("--run-id", default="P150-PUBLIC-PREP-SELECTOR-OR-STOP")
    parser.add_argument("--generated-at-utc", default=utc_now_iso())
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    selector = run_selector(
        SelectorRequest(
            p149_report_path=Path(args.p149_report),
            output_dir=Path(args.output_dir),
            run_id=args.run_id,
            generated_at_utc=args.generated_at_utc,
        )
    )
    print(selector["status"])
    print(f"recommended_next={selector['recommended_next']}")
    print(f"option_count={selector['option_count']}")
    print(f"blocker_count={selector['blocker_count']}")
    print("google_sheets_write=false")
    print("public_deploy=false")
    print("future_sheet_write_requires_explicit_go=true")
    print(f"output_dir={args.output_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
