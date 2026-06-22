from __future__ import annotations

import argparse
import csv
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Mapping, Sequence

VERSION = "MVP_QAIC_P124_LOCAL_INPUT_HELPER_REAL_GEM_TEST_0_1_1_SAFE"

SAFETY_MARKERS = (
    "LOCAL_ONLY",
    "HUMAN_REVIEW_ONLY",
    "REAL_GEM_MANUAL_TEST_PREP_ONLY",
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
    "NO_AUTO_APPLY_GEM_RESPONSE",
    "NO_REVOLUTX_REAL_ACCESS_FROM_MVP",
)

DEFAULT_PORTFOLIO_TEMPLATE = """# Portfolio input for MVP QAIC GEM manual test

Paste or type the portfolio snapshot here.

Required minimum:
- assets/tickers
- quantity or exposure
- current value if known
- source date/time
- notes on uncertainty

Example:
BTC: quantity=0.10; value_eur=6500; price_source=manual; confidence=REVIEW
ETH: quantity=1.20; value_eur=4200; price_source=manual; confidence=REVIEW

Safety:
HUMAN_REVIEW_ONLY
NO_BROKER
NO_ORDER
NO_SIZING
NO_REVOLUTX_REAL_ACCESS_FROM_MVP
"""

DEFAULT_GEM_RESPONSE_TEMPLATE = """# GEM response paste area

Paste the GEM response here after running the prompt manually.

Accepted formats:
1. Plain text
2. JSON object
3. Markdown fenced JSON

Do not paste secrets.
Do not paste broker credentials.
Do not ask GEM to execute orders.

Safety:
HUMAN_REVIEW_ONLY
NO_AUTO_APPLY_GEM_RESPONSE
NO_BROKER
NO_ORDER
NO_SIZING
"""


@dataclass(frozen=True)
class InputHelperRequest:
    output_dir: str | Path
    run_id: str = "P124-REAL-GEM-TEST"
    portfolio_text: str | None = None
    portfolio_text_file: str | Path | None = None
    generated_at_utc: str | None = None
    notes: str | None = None


def _read_optional_text(path: str | Path | None) -> str | None:
    if not path:
        return None
    return Path(path).read_text(encoding="utf-8-sig")


def _write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text.rstrip() + "\n", encoding="utf-8")


def _write_json(path: Path, payload: Mapping[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )


def build_input_helper_contract() -> dict[str, Any]:
    return {
        "contract": "P124_LOCAL_INPUT_HELPER_REAL_GEM_TEST",
        "version": VERSION,
        "status": "LOCAL_INPUT_HELPER_READY",
        "purpose": "Prepare a local run folder for the first real manual GEM test after P123 final docs.",
        "creates": [
            "portfolio_input.txt",
            "gem_response.txt",
            "run_notes.md",
            "P124_OPERATOR_COMMANDS.md",
            "P124_REAL_GEM_TEST_CHECKLIST.csv",
            "P124_INPUT_HELPER_CONTRACT.json",
            "P124_INPUT_HELPER_MANIFEST.json",
            "P124_README.md",
        ],
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


def build_checklist_rows() -> list[dict[str, str]]:
    return [
        {
            "check_id": "P124-CHECK-001",
            "priority": "P0",
            "check_name": "Portfolio input completed",
            "expected_state": "portfolio_input.txt contains assets, values and uncertainty notes.",
            "operator_action": "Fill or paste the real portfolio snapshot manually.",
            "safety_marker": "HUMAN_REVIEW_ONLY",
        },
        {
            "check_id": "P124-CHECK-002",
            "priority": "P0",
            "check_name": "Prompt generated locally",
            "expected_state": "P118 creates P116_GEM_PROMPT_COPY_PASTE.md.",
            "operator_action": "Run the P118 command from P124_OPERATOR_COMMANDS.md.",
            "safety_marker": "LOCAL_ONLY",
        },
        {
            "check_id": "P124-CHECK-003",
            "priority": "P0",
            "check_name": "GEM used manually",
            "expected_state": "Operator manually pastes prompt into GEM.",
            "operator_action": "No API, no hidden automation, no browser control.",
            "safety_marker": "REAL_GEM_MANUAL_TEST_PREP_ONLY",
        },
        {
            "check_id": "P124-CHECK-004",
            "priority": "P0",
            "check_name": "GEM response captured locally",
            "expected_state": "gem_response.txt contains the GEM answer.",
            "operator_action": "Paste GEM answer manually, then run P119.",
            "safety_marker": "NO_AUTO_APPLY_GEM_RESPONSE",
        },
        {
            "check_id": "P124-CHECK-005",
            "priority": "P0",
            "check_name": "Decision journal candidate local only",
            "expected_state": "P120 creates local CSV/JSON only.",
            "operator_action": "Review manually; do not write Sheets.",
            "safety_marker": "NO_SHEET_WRITE",
        },
        {
            "check_id": "P124-CHECK-006",
            "priority": "P0",
            "check_name": "No trading execution",
            "expected_state": "No broker, no order, no sizing.",
            "operator_action": "Keep all decisions human-only.",
            "safety_marker": "NO_BROKER_NO_ORDER_NO_SIZING",
        },
    ]


def _write_checklist_csv(path: Path) -> None:
    fields = [
        "check_id",
        "priority",
        "check_name",
        "expected_state",
        "operator_action",
        "safety_marker",
    ]
    with path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        for row in build_checklist_rows():
            writer.writerow(row)


def _commands_markdown(run_id: str, run_root: Path) -> str:
    portfolio_path = run_root / "portfolio_input.txt"
    gem_response_path = run_root / "gem_response.txt"
    p118_dir = run_root / "P118_DAILY_PROMPT_PACK"
    p119_dir = run_root / "P119_GEM_RESPONSE_CAPTURE"
    p120_dir = run_root / "P120_DECISION_JOURNAL_CANDIDATE"
    p121_dir = run_root / "P121_E2E_SMOKE_OPTIONAL"
    capture_json = p119_dir / "P119_RESPONSE_CAPTURE.json"
    prompt_file = p118_dir / "P118_RUNTIME_PACK" / "P116_GEM_PROMPT_COPY_PASTE.md"

    return "\n".join(
        [
            "# P124 Operator Commands",
            "",
            "## Step 1 - Generate daily GEM prompt",
            "",
            "```powershell",
            f'python -m mvp_qaic_py.gem_prompt_daily_shortcut --output-dir "{p118_dir}" --pasted-text-file "{portfolio_path}" --run-id "{run_id}-P118"',
            "```",
            "",
            "## Step 2 - Paste prompt manually into GEM",
            "",
            "Open:",
            "",
            f"`{prompt_file}`",
            "",
            "## Step 3 - Paste GEM response into local file",
            "",
            f"`{gem_response_path}`",
            "",
            "## Step 4 - Capture GEM response and review queue",
            "",
            "```powershell",
            f'python -m mvp_qaic_py.gem_response_review_queue --output-dir "{p119_dir}" --response-text-file "{gem_response_path}" --source-prompt-run-id "{run_id}-P118" --response-run-id "{run_id}-P119"',
            "```",
            "",
            "## Step 5 - Bridge to local decision journal candidate",
            "",
            "```powershell",
            f'python -m mvp_qaic_py.gem_response_decision_journal_bridge --output-dir "{p120_dir}" --response-capture-json-file "{capture_json}" --journal-entry-id "{run_id}-P120-JOURNAL"',
            "```",
            "",
            "## Optional - local smoke only",
            "",
            "```powershell",
            f'python -m mvp_qaic_py.gem_daily_loop_smoke --output-dir "{p121_dir}" --run-id "{run_id}-P121-SMOKE"',
            "```",
            "",
            "## Hard stop",
            "",
            "No Sheet write. No Apps Script. No broker. No order. No sizing. No Revolut X real access from MVP.",
            "`NO_REVOLUTX_REAL_ACCESS_FROM_MVP`.",
            "",
        ]
    )


def _readme_markdown(run_id: str) -> str:
    return "\n".join(
        [
            "# P124 Local Input Helper",
            "",
            f"Run ID: `{run_id}`",
            "",
            "This folder prepares the first real manual GEM test.",
            "",
            "## Files",
            "",
            "- `portfolio_input.txt` - paste the real portfolio snapshot.",
            "- `gem_response.txt` - paste GEM answer after manual GEM run.",
            "- `run_notes.md` - notes, uncertainty, operator context.",
            "- `P124_OPERATOR_COMMANDS.md` - exact commands for P118/P119/P120/P121.",
            "- `P124_REAL_GEM_TEST_CHECKLIST.csv` - manual readiness checklist.",
            "",
            "## Safety",
            "",
            "- HUMAN_REVIEW_ONLY",
            "- NO_AUTO_APPLY_GEM_RESPONSE",
            "- NO_SHEET_WRITE",
            "- NO_BROKER",
            "- NO_ORDER",
            "- NO_AUTO_SIZING",
            "- NO_REVOLUTX_REAL_ACCESS_FROM_MVP",
            "",
        ]
    )


def write_input_helper_pack(request: InputHelperRequest) -> dict[str, Any]:
    out = Path(request.output_dir)
    out.mkdir(parents=True, exist_ok=True)

    if request.portfolio_text and request.portfolio_text_file:
        raise ValueError("Use either portfolio_text or portfolio_text_file, not both.")

    portfolio_text = (
        request.portfolio_text
        or _read_optional_text(request.portfolio_text_file)
        or DEFAULT_PORTFOLIO_TEMPLATE
    )

    portfolio_path = out / "portfolio_input.txt"
    gem_response_path = out / "gem_response.txt"
    notes_path = out / "run_notes.md"
    commands_path = out / "P124_OPERATOR_COMMANDS.md"
    checklist_path = out / "P124_REAL_GEM_TEST_CHECKLIST.csv"
    contract_path = out / "P124_INPUT_HELPER_CONTRACT.json"
    manifest_path = out / "P124_INPUT_HELPER_MANIFEST.json"
    readme_path = out / "P124_README.md"

    _write(portfolio_path, portfolio_text)
    _write(gem_response_path, DEFAULT_GEM_RESPONSE_TEMPLATE)
    _write(
        notes_path,
        "\n".join(
            [
                "# P124 Run Notes",
                "",
                f"- run_id: {request.run_id}",
                f"- generated_at_utc: {request.generated_at_utc or 'UNSPECIFIED'}",
                f"- notes: {request.notes or 'UNSPECIFIED'}",
                "",
                "Add operator notes here before/after the GEM test.",
            ]
        ),
    )
    _write(commands_path, _commands_markdown(request.run_id, out))
    _write_checklist_csv(checklist_path)
    _write_json(contract_path, build_input_helper_contract())
    _write(readme_path, _readme_markdown(request.run_id))

    manifest = {
        "status": "INPUT_HELPER_READY",
        "step": "P124_LOCAL_INPUT_HELPER_REAL_GEM_TEST",
        "version": VERSION,
        "run_id": request.run_id,
        "output_dir": str(out),
        "generated_at_utc": request.generated_at_utc,
        "portfolio_input_file": str(portfolio_path),
        "gem_response_file": str(gem_response_path),
        "operator_commands_file": str(commands_path),
        "checklist_file": str(checklist_path),
        "ready_for_real_gem_manual_test": True,
        "human_review_only": True,
        "no_sheet_write": True,
        "no_auto_apply_gem_response": True,
        "no_order_no_sizing": True,
        "safety_markers": list(SAFETY_MARKERS),
        "files": [
            str(portfolio_path),
            str(gem_response_path),
            str(notes_path),
            str(commands_path),
            str(checklist_path),
            str(contract_path),
            str(readme_path),
        ],
        "next": "P125_REAL_GEM_MANUAL_TEST_CAPTURE_PACK_OR_OPERATOR_REVIEW_UX",
    }
    _write_json(manifest_path, manifest)
    manifest["files"].append(str(manifest_path))
    return manifest


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        prog="python -m mvp_qaic_py.gem_loop_input_helper",
        description="Create a local input helper folder for a real manual GEM test.",
    )
    parser.add_argument("--output-dir", required=True)
    parser.add_argument("--run-id", default="P124-REAL-GEM-TEST")
    parser.add_argument("--portfolio-text")
    parser.add_argument("--portfolio-text-file")
    parser.add_argument("--generated-at-utc")
    parser.add_argument("--notes")
    return parser.parse_args(argv)


def main(argv: Sequence[str] | None = None) -> int:
    args = parse_args(argv)
    result = write_input_helper_pack(
        InputHelperRequest(
            output_dir=args.output_dir,
            run_id=args.run_id,
            portfolio_text=args.portfolio_text,
            portfolio_text_file=args.portfolio_text_file,
            generated_at_utc=args.generated_at_utc,
            notes=args.notes,
        )
    )
    print(result["status"])
    print(result["run_id"])
    print(result["ready_for_real_gem_manual_test"])
    print(result["output_dir"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
