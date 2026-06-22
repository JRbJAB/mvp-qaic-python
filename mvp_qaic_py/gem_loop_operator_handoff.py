from __future__ import annotations

import argparse
import csv
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Mapping, Sequence

VERSION = "MVP_QAIC_P122_GEM_LOOP_OPERATOR_HANDOFF_STOP_PACK_0_1_0_SAFE"

SAFETY_MARKERS = (
    "MVP_PUBLIC_SCOPE",
    "HUMAN_REVIEW_ONLY",
    "LOCAL_ONLY",
    "OPERATOR_HANDOFF_ONLY",
    "STOP_AFTER_HANDOFF",
    "NO_AUTO_APPLY_GEM_RESPONSE",
    "NO_INDEX_EDIT",
    "NO_CLASP",
    "NO_APPS_SCRIPT_EXECUTION",
    "NO_SHEET_WRITE",
    "NO_PUBLIC_DEPLOY",
    "NO_BROKER",
    "NO_ORDER",
    "NO_CANCEL",
    "NO_REPLACE_ORDER",
    "NO_AUTO_SIZING",
    "NO_REVOLUTX_REAL_ACCESS_FROM_MVP",
)

CHECKLIST_FIELDS = (
    "check_id",
    "priority",
    "check_name",
    "expected_state",
    "operator_action",
    "safety_marker",
)


@dataclass(frozen=True)
class OperatorHandoffRequest:
    output_dir: str | Path
    exports_dir: str | Path | None = None
    latest_smoke_dir: str | Path | None = None
    generated_at_utc: str | None = None
    notes: str | None = None


def discover_latest_smoke_dir(exports_dir: str | Path) -> Path | None:
    root = Path(exports_dir)
    if not root.exists():
        return None
    candidates = [
        path for path in root.glob("P121_DAILY_GEM_LOOP_E2E_LOCAL_SMOKE_*") if path.is_dir()
    ]
    if not candidates:
        return None
    return sorted(candidates, key=lambda path: path.stat().st_mtime, reverse=True)[0]


def build_handoff_contract() -> dict[str, Any]:
    return {
        "contract": "P122_GEM_LOOP_OPERATOR_HANDOFF_AND_STOP_PACK",
        "version": VERSION,
        "status": "HANDOFF_READY_LOCAL_ONLY",
        "purpose": "Give the operator a practical handoff for the local GEM loop P118 -> P119 -> P120, after P121 e2e smoke.",
        "validated_chain": [
            "P118_DAILY_OPERATOR_SHORTCUT",
            "P119_GEM_RESPONSE_CAPTURE_REVIEW_QUEUE",
            "P120_DECISION_JOURNAL_BRIDGE_LOCAL_ONLY",
            "P121_DAILY_GEM_LOOP_E2E_LOCAL_SMOKE",
        ],
        "operator_boundary": "Manual copy/paste with human review only. No live apply.",
        "forbidden": [
            "auto_apply_gem_response",
            "apps_script_execution",
            "sheet_write",
            "clasp_push",
            "public_deploy",
            "broker_execution",
            "order_execution",
            "cancel_order",
            "replace_order",
            "auto_sizing",
            "revolutx_real_access_from_mvp",
            "secret_logging",
        ],
        "safety_markers": list(SAFETY_MARKERS),
    }


def build_ready_checklist_rows() -> list[dict[str, str]]:
    return [
        {
            "check_id": "P122-CHECK-001",
            "priority": "P0",
            "check_name": "Use local files only",
            "expected_state": "No Google Sheet write, no Apps Script execution.",
            "operator_action": "Run only Python local commands from P122_DAILY_OPERATOR_COMMANDS.md.",
            "safety_marker": "LOCAL_ONLY",
        },
        {
            "check_id": "P122-CHECK-002",
            "priority": "P0",
            "check_name": "Copy prompt to GEM manually",
            "expected_state": "Prompt file exists under P118/P121 runtime pack.",
            "operator_action": "Open P116_GEM_PROMPT_COPY_PASTE.md and paste manually into GEM.",
            "safety_marker": "HUMAN_REVIEW_ONLY",
        },
        {
            "check_id": "P122-CHECK-003",
            "priority": "P0",
            "check_name": "Capture GEM response locally",
            "expected_state": "Response is pasted into local text or JSON file.",
            "operator_action": "Use P119 command to create P119_REVIEW_QUEUE.csv.",
            "safety_marker": "NO_AUTO_APPLY_GEM_RESPONSE",
        },
        {
            "check_id": "P122-CHECK-004",
            "priority": "P0",
            "check_name": "Bridge to local journal candidate only",
            "expected_state": "P120 creates CSV/JSON candidate but does not write Sheets.",
            "operator_action": "Review P120_DECISION_JOURNAL_ENTRY.csv manually.",
            "safety_marker": "NO_SHEET_WRITE",
        },
        {
            "check_id": "P122-CHECK-005",
            "priority": "P0",
            "check_name": "No execution action",
            "expected_state": "No broker, no order, no sizing, no Revolut X real access from MVP.",
            "operator_action": "Keep all trading decisions human-only and outside MVP automation.",
            "safety_marker": "NO_BROKER_NO_ORDER_NO_SIZING",
        },
        {
            "check_id": "P122-CHECK-006",
            "priority": "P1",
            "check_name": "Stop after handoff",
            "expected_state": "Do not add UI/live layer until user validates first manual GEM test.",
            "operator_action": "Either stop or explicitly launch P123 UI input helper.",
            "safety_marker": "STOP_AFTER_HANDOFF",
        },
    ]


def _write_json(path: Path, payload: Mapping[str, Any]) -> None:
    path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )


def _write_checklist_csv(path: Path, rows: list[Mapping[str, str]]) -> None:
    with path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(CHECKLIST_FIELDS))
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field, "") for field in CHECKLIST_FIELDS})


def _daily_commands_markdown() -> str:
    return "\n".join(
        [
            "# P122 Daily Operator Commands",
            "",
            "## 1. Create daily prompt from portfolio text",
            "",
            "```powershell",
            'python -m mvp_qaic_py.gem_prompt_daily_shortcut --output-dir "05_EXPORTS/DAILY_GEM_RUN" --pasted-text-file "portfolio_input.txt" --run-id "DAILY-GEM-RUN"',
            "```",
            "",
            "## 2. Paste the generated prompt into GEM manually",
            "",
            "Open:",
            "",
            "`05_EXPORTS/DAILY_GEM_RUN/P118_RUNTIME_PACK/P116_GEM_PROMPT_COPY_PASTE.md`",
            "",
            "## 3. Capture GEM response locally",
            "",
            "```powershell",
            'python -m mvp_qaic_py.gem_response_review_queue --output-dir "05_EXPORTS/DAILY_GEM_RESPONSE_CAPTURE" --response-text-file "gem_response.txt" --source-prompt-run-id "DAILY-GEM-RUN" --response-run-id "DAILY-GEM-RESPONSE"',
            "```",
            "",
            "## 4. Bridge to local decision journal candidate",
            "",
            "```powershell",
            'python -m mvp_qaic_py.gem_response_decision_journal_bridge --output-dir "05_EXPORTS/DAILY_GEM_JOURNAL_CANDIDATE" --response-capture-json-file "05_EXPORTS/DAILY_GEM_RESPONSE_CAPTURE/P119_RESPONSE_CAPTURE.json" --journal-entry-id "DAILY-GEM-JOURNAL-CANDIDATE"',
            "```",
            "",
            "## 5. Optional smoke check",
            "",
            "```powershell",
            'python -m mvp_qaic_py.gem_daily_loop_smoke --output-dir "05_EXPORTS/DAILY_GEM_E2E_SMOKE" --run-id "DAILY-GEM-E2E-SMOKE"',
            "```",
            "",
            "## Hard stop",
            "",
            "Do not write to Sheets. Do not run Apps Script. Do not create orders. Do not auto-apply GEM output.",
            "",
        ]
    )


def _handoff_markdown(latest_smoke_dir: Path | None, notes: str | None) -> str:
    latest_line = str(latest_smoke_dir) if latest_smoke_dir else "NOT_PROVIDED"
    return "\n".join(
        [
            "# P122 GEM Loop Operator Handoff And Stop",
            "",
            "## Status",
            "",
            "The local MVP QAIC GEM loop is ready for manual operator testing.",
            "",
            "Validated local chain:",
            "",
            "- P118: daily prompt/runtime pack.",
            "- P119: GEM response capture and review queue.",
            "- P120: local decision journal bridge.",
            "- P121: end-to-end local smoke.",
            "",
            "## Latest P121 smoke directory",
            "",
            f"`{latest_line}`",
            "",
            "## Operating rule",
            "",
            "Manual copy/paste only. Human review only. No live apply.",
            "",
            "## Hard boundaries",
            "",
            "- NO_SHEET_WRITE.",
            "- NO_APPS_SCRIPT_EXECUTION.",
            "- NO_CLASP.",
            "- NO_PUBLIC_DEPLOY.",
            "- NO_BROKER / NO_ORDER / NO_SIZING.",
            "- NO_REVOLUTX_REAL_ACCESS_FROM_MVP.",
            "",
            "## Stop condition",
            "",
            "After this handoff, stop development unless the operator explicitly requests a real manual GEM test or a P123 UI/input helper.",
            "",
            "## Notes",
            "",
            notes or "No extra notes.",
            "",
        ]
    )


def _runbook_markdown() -> str:
    return "\n".join(
        [
            "# P122 Daily GEM Loop Runbook",
            "",
            "## Daily manual flow",
            "",
            "1. Prepare `portfolio_input.txt` locally.",
            "2. Generate P118 daily prompt pack.",
            "3. Copy the prompt manually into GEM.",
            "4. Paste GEM response into `gem_response.txt`.",
            "5. Run P119 capture to create review queue.",
            "6. Run P120 bridge to create local journal candidate.",
            "7. Read blockers and missing data before any decision.",
            "",
            "## Interpretation",
            "",
            "- `BLOCKED`: do not continue until blockers are resolved manually.",
            "- `REVIEW_REQUIRED`: missing data or manual verification still needed.",
            "- `READY_FOR_HUMAN_DECISION`: still human-only; no automatic order or sizing.",
            "",
            "## Future step",
            "",
            "P123 may add a local input helper, but not a live UI/deployment layer.",
            "",
        ]
    )


def _discover_latest_manifest(latest_smoke_dir: Path | None) -> dict[str, Any] | None:
    if latest_smoke_dir is None:
        return None
    manifest = latest_smoke_dir / "P121_E2E_SMOKE_MANIFEST.json"
    if not manifest.exists():
        return None
    payload = json.loads(manifest.read_text(encoding="utf-8-sig"))
    if not isinstance(payload, dict):
        return None
    return payload


def write_operator_handoff_pack(request: OperatorHandoffRequest) -> dict[str, Any]:
    out = Path(request.output_dir)
    out.mkdir(parents=True, exist_ok=True)

    latest_smoke_dir: Path | None = None
    if request.latest_smoke_dir:
        latest_smoke_dir = Path(request.latest_smoke_dir)
    elif request.exports_dir:
        latest_smoke_dir = discover_latest_smoke_dir(request.exports_dir)

    latest_manifest = _discover_latest_manifest(latest_smoke_dir)

    contract_path = out / "P122_OPERATOR_HANDOFF_CONTRACT.json"
    handoff_path = out / "P122_OPERATOR_HANDOFF.md"
    commands_path = out / "P122_DAILY_OPERATOR_COMMANDS.md"
    runbook_path = out / "P122_DAILY_GEM_LOOP_RUNBOOK.md"
    checklist_path = out / "P122_READY_CHECKLIST.csv"
    manifest_path = out / "P122_HANDOFF_MANIFEST.json"
    stop_report_path = out / "P122_STOP_REPORT.md"

    contract = build_handoff_contract()
    checklist_rows = build_ready_checklist_rows()

    _write_json(contract_path, contract)
    handoff_path.write_text(_handoff_markdown(latest_smoke_dir, request.notes), encoding="utf-8")
    commands_path.write_text(_daily_commands_markdown(), encoding="utf-8")
    runbook_path.write_text(_runbook_markdown(), encoding="utf-8")
    _write_checklist_csv(checklist_path, checklist_rows)

    manifest = {
        "status": "HANDOFF_READY",
        "step": "P122_GEM_LOOP_OPERATOR_HANDOFF_AND_STOP_PACK",
        "version": VERSION,
        "output_dir": str(out),
        "generated_at_utc": request.generated_at_utc,
        "latest_smoke_dir": str(latest_smoke_dir) if latest_smoke_dir else None,
        "latest_smoke_status": latest_manifest.get("status") if latest_manifest else None,
        "latest_smoke_chain_verified": bool(
            latest_manifest and latest_manifest.get("status") == "PASS"
        ),
        "ready_check_count": len(checklist_rows),
        "stop_after_handoff": True,
        "next": "WAIT_OPERATOR_REAL_GEM_TEST_OR_P123_UI_INPUT_HELPER",
        "safety_markers": list(SAFETY_MARKERS),
        "files": [
            str(contract_path),
            str(handoff_path),
            str(commands_path),
            str(runbook_path),
            str(checklist_path),
            str(stop_report_path),
        ],
    }
    _write_json(manifest_path, manifest)

    stop_report_path.write_text(
        "\n".join(
            [
                "# P122 Stop Report",
                "",
                "- status: HANDOFF_READY",
                "- stop_after_handoff: true",
                "- next: WAIT_OPERATOR_REAL_GEM_TEST_OR_P123_UI_INPUT_HELPER",
                "- safety: LOCAL_ONLY / HUMAN_REVIEW_ONLY / NO_SHEET_WRITE / NO_BROKER / NO_ORDER / NO_SIZING",
                "",
            ]
        ),
        encoding="utf-8",
    )

    manifest["files"].append(str(manifest_path))
    return manifest


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        prog="python -m mvp_qaic_py.gem_loop_operator_handoff",
        description="Generate P122 operator handoff and stop pack for local GEM loop.",
    )
    parser.add_argument("--output-dir", required=True)
    parser.add_argument("--exports-dir")
    parser.add_argument("--latest-smoke-dir")
    parser.add_argument("--generated-at-utc")
    parser.add_argument("--notes")
    return parser.parse_args(argv)


def main(argv: Sequence[str] | None = None) -> int:
    args = parse_args(argv)
    result = write_operator_handoff_pack(
        OperatorHandoffRequest(
            output_dir=args.output_dir,
            exports_dir=args.exports_dir,
            latest_smoke_dir=args.latest_smoke_dir,
            generated_at_utc=args.generated_at_utc,
            notes=args.notes,
        )
    )
    print(result["status"])
    print(result["ready_check_count"])
    print(result["stop_after_handoff"])
    print(result["output_dir"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
