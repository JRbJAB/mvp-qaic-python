from __future__ import annotations

import argparse
import csv
import json
import sys
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

VERSION = "MVP_QAIC_P149_MIGRATION_CLOSE_GATE_1.0.0_SAFE"
STATUS_READY = "P149_MIGRATION_CLOSE_GATE_READY_LOCAL_PRIVATE"

REQUIRED_EXPORT_PREFIXES = [
    "P140_NICEGUI_COCKPIT_REPLICA_RENDERER_",
    "P141_NICEGUI_COCKPIT_REPLICA_LOCAL_LAUNCH_",
    "P142_UI_FIDELITY_SHELL_",
    "P143B_DATA_PREVIEW_SOURCE_EXPANSION_",
    "P144_PROMPT_COCKPIT_WORKFLOWS_",
    "P145_GEM_RESPONSE_IMPORT_E2E_",
    "P146_CORRECTION_QUEUE_UI_",
    "P147_OPERATOR_POLISH_",
    "P148_SYNC_STRATEGY_READONLY_",
]

SAFETY_MARKERS = {
    "close_gate_only": True,
    "live_google_sheets_read": False,
    "google_sheets_write": False,
    "apps_script_execution": False,
    "clasp_push": False,
    "broker": False,
    "order": False,
    "sizing": False,
    "auto_apply_gem_response": False,
    "public_deploy": False,
    "future_sheet_write_requires_explicit_go": True,
    "future_public_deploy_requires_explicit_go": True,
}


@dataclass(frozen=True)
class CloseGateRequest:
    p148_strategy_path: Path
    exports_root: Path
    output_dir: Path
    run_id: str
    generated_at_utc: str


def utc_now_iso() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def latest_export_for_prefix(exports_root: Path, prefix: str) -> Path | None:
    matches = [
        path for path in exports_root.iterdir() if path.is_dir() and path.name.startswith(prefix)
    ]
    if not matches:
        return None
    return sorted(matches, key=lambda path: path.stat().st_mtime, reverse=True)[0]


def collect_evidence(exports_root: Path) -> list[dict[str, Any]]:
    if not exports_root.exists():
        raise FileNotFoundError(f"exports_root not found: {exports_root}")

    evidence: list[dict[str, Any]] = []
    for prefix in REQUIRED_EXPORT_PREFIXES:
        path = latest_export_for_prefix(exports_root, prefix)
        exists = path is not None
        files = []
        if path:
            files = sorted([item.name for item in path.iterdir() if item.is_file()])
        evidence.append(
            {
                "prefix": prefix,
                "found": exists,
                "export_dir": str(path) if path else "",
                "file_count": len(files),
                "files": files,
                "gate": "OK" if exists and len(files) > 0 else "MISSING",
            }
        )
    return evidence


def validate_p148_strategy(strategy: dict[str, Any]) -> list[str]:
    blockers: list[str] = []
    if strategy.get("status") != "P148_SYNC_STRATEGY_READONLY_RENDERED":
        blockers.append("P148_STATUS_NOT_RENDERED")
    if strategy.get("p149_readiness", {}).get("migration_close_gate_ready") is not True:
        blockers.append("P149_READINESS_NOT_TRUE")
    if strategy.get("policy", {}).get("future_sheet_write_requires_explicit_go") is not True:
        blockers.append("FUTURE_SHEET_WRITE_EXPLICIT_GO_MISSING")
    if strategy.get("policy", {}).get("write_back_allowed_now") is not False:
        blockers.append("WRITE_BACK_NOT_DISABLED")
    if strategy.get("safety", {}).get("google_sheets_write") is not False:
        blockers.append("GOOGLE_SHEETS_WRITE_NOT_FALSE")
    return blockers


def build_timeline(evidence: list[dict[str, Any]]) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for index, item in enumerate(evidence, start=1):
        phase = item["prefix"].rstrip("_")
        rows.append(
            {
                "rank": str(index),
                "phase": phase,
                "gate": str(item["gate"]),
                "export_dir": str(item["export_dir"]),
                "file_count": str(item["file_count"]),
            }
        )
    return rows


def build_close_report(strategy: dict[str, Any], evidence: list[dict[str, Any]]) -> dict[str, Any]:
    blockers = validate_p148_strategy(strategy)
    missing = [item["prefix"] for item in evidence if item["gate"] != "OK"]
    if missing:
        blockers.append("MISSING_REQUIRED_EXPORTS:" + ",".join(missing))

    ready = not blockers
    return {
        "status": STATUS_READY if ready else "P149_MIGRATION_CLOSE_GATE_BLOCKED",
        "version": VERSION,
        "source_p148_status": strategy.get("status"),
        "required_export_count": len(REQUIRED_EXPORT_PREFIXES),
        "evidence_ok_count": sum(1 for item in evidence if item["gate"] == "OK"),
        "evidence_missing_count": sum(1 for item in evidence if item["gate"] != "OK"),
        "blocker_count": len(blockers),
        "blockers": blockers,
        "migration_close_ready": ready,
        "mvp_prompt_cockpit_local_private_ready": ready,
        "migration_scope_closed": ready,
        "evidence": evidence,
        "timeline": build_timeline(evidence),
        "final_state": {
            "nicegui_local_cockpit_ready": ready,
            "prompt_workflow_ready": ready,
            "gem_response_import_review_ready": ready,
            "correction_queue_review_only_ready": ready,
            "sync_strategy_readonly_ready": ready,
            "no_more_migration_dev_batches_required": ready,
        },
        "future_options": [
            "P150_PUBLIC_PREP_SELECTOR",
            "P150A_REAL_GEM_RESPONSE_IMPORT",
            "P150B_LOCAL_PRIVATE_RELEASE_PACK",
            "P150C_SHEETS_WRITE_GATE_AFTER_EXPLICIT_GO",
        ],
        "safety": dict(SAFETY_MARKERS),
        "next": "P150_PUBLIC_PREP_SELECTOR_OR_STOP",
    }


def write_outputs(report: dict[str, Any], output_dir: Path) -> dict[str, str]:
    output_dir.mkdir(parents=True, exist_ok=True)

    report_path = output_dir / "P149_MIGRATION_CLOSE_GATE_REPORT.json"
    timeline_path = output_dir / "P149_MIGRATION_TIMELINE.csv"
    runbook_path = output_dir / "P149_POST_MIGRATION_RUNBOOK.md"
    md_path = output_dir / "P149_MIGRATION_CLOSE_GATE.md"
    summary_path = output_dir / "P149_SUMMARY.json"

    report_path.write_text(
        json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True), encoding="utf-8"
    )

    with timeline_path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(
            handle, fieldnames=["rank", "phase", "gate", "export_dir", "file_count"]
        )
        writer.writeheader()
        for row in report["timeline"]:
            writer.writerow(row)

    runbook_path.write_text(
        "\n".join(
            [
                "# P149 — Post Migration Runbook",
                "",
                "## État final",
                "",
                "- Cockpit NiceGUI local privé prêt",
                "- Workflow prompt prêt",
                "- Import GEM en review locale prêt",
                "- Correction queue review-only prête",
                "- Sync strategy read-only prête",
                "",
                "## Garde-fous permanents",
                "",
                "- No Sheet write sans GO explicite futur",
                "- No public deploy sans GO explicite futur",
                "- No broker/order/sizing dans MVP",
                "- No auto apply GEM response",
                "",
                "## Prochain choix",
                "",
                "- Stop / validation opérateur",
                "- P150 public prep selector",
                "- P150A importer une vraie réponse GEM",
                "- P150B release pack local privé",
                "",
            ]
        ),
        encoding="utf-8",
    )

    md_path.write_text(
        "\n".join(
            [
                "# P149 — Migration Close Gate",
                "",
                f"- Status: `{report['status']}`",
                f"- Evidence OK: `{report['evidence_ok_count']}/{report['required_export_count']}`",
                f"- Blockers: `{report['blocker_count']}`",
                f"- Migration close ready: `{report['migration_close_ready']}`",
                "",
                "## Safety",
                "",
                "- No live Sheets read",
                "- No Sheet write",
                "- No Apps Script / CLASP",
                "- No broker/order/sizing",
                "- No public deploy",
                "- Future writes require explicit GO",
                "",
                f"Next: `{report['next']}`",
                "",
            ]
        ),
        encoding="utf-8",
    )

    summary = {
        "status": report["status"],
        "migration_close_ready": report["migration_close_ready"],
        "mvp_prompt_cockpit_local_private_ready": report["mvp_prompt_cockpit_local_private_ready"],
        "migration_scope_closed": report["migration_scope_closed"],
        "evidence_ok_count": report["evidence_ok_count"],
        "required_export_count": report["required_export_count"],
        "blocker_count": report["blocker_count"],
        "google_sheets_write": False,
        "live_google_sheets_read": False,
        "future_sheet_write_requires_explicit_go": True,
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
        "timeline_csv": str(timeline_path),
        "runbook_md": str(runbook_path),
        "close_gate_md": str(md_path),
        "summary_json": str(summary_path),
    }


def run_close_gate(request: CloseGateRequest) -> dict[str, Any]:
    strategy = load_json(request.p148_strategy_path)
    evidence = collect_evidence(request.exports_root)
    report = build_close_report(strategy, evidence)
    report["run_id"] = request.run_id
    report["generated_at_utc"] = request.generated_at_utc
    report["source_p148_strategy_path"] = str(request.p148_strategy_path)
    report["exports_root"] = str(request.exports_root)
    outputs = write_outputs(report, request.output_dir)
    report["output_files"] = outputs
    (request.output_dir / "P149_MIGRATION_CLOSE_GATE_REPORT.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True),
        encoding="utf-8",
    )
    return report


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="P149 migration close gate.")
    parser.add_argument("--p148-strategy", required=True)
    parser.add_argument("--exports-root", required=True)
    parser.add_argument("--output-dir", required=True)
    parser.add_argument("--run-id", default="P149-MIGRATION-CLOSE-GATE")
    parser.add_argument("--generated-at-utc", default=utc_now_iso())
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    report = run_close_gate(
        CloseGateRequest(
            p148_strategy_path=Path(args.p148_strategy),
            exports_root=Path(args.exports_root),
            output_dir=Path(args.output_dir),
            run_id=args.run_id,
            generated_at_utc=args.generated_at_utc,
        )
    )
    print(report["status"])
    print(f"migration_close_ready={str(report['migration_close_ready']).lower()}")
    print(
        f"mvp_prompt_cockpit_local_private_ready={str(report['mvp_prompt_cockpit_local_private_ready']).lower()}"
    )
    print(f"evidence_ok_count={report['evidence_ok_count']}")
    print(f"required_export_count={report['required_export_count']}")
    print(f"blocker_count={report['blocker_count']}")
    print("google_sheets_write=false")
    print("future_sheet_write_requires_explicit_go=true")
    print(f"output_dir={args.output_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
