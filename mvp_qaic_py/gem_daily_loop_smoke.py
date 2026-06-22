from __future__ import annotations

import argparse
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Mapping, Sequence

from .gem_prompt_daily_shortcut import DailyShortcutRequest, write_daily_shortcut_pack
from .gem_response_decision_journal_bridge import (
    DecisionJournalBridgeRequest,
    write_decision_journal_bridge_pack,
)
from .gem_response_review_queue import GemResponseCaptureRequest, write_response_review_pack

VERSION = "MVP_QAIC_P121_DAILY_GEM_LOOP_E2E_LOCAL_SMOKE_0_1_0_SAFE"

SAFETY_MARKERS = (
    "MVP_PUBLIC_SCOPE",
    "HUMAN_REVIEW_ONLY",
    "LOCAL_ONLY",
    "E2E_LOCAL_SMOKE_ONLY",
    "PROMPT_TO_GEM_TO_CAPTURE_TO_JOURNAL_LOCAL_LOOP",
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

DEFAULT_PORTFOLIO_TEXT = (
    "BTC 0.10 value EUR 6500; ETH 1.20 value EUR 4200; "
    "USDC 1000 value EUR 920; source=P121 local smoke sample; "
    "human_review_required=true; prices_not_verified=true."
)

DEFAULT_GEM_RESPONSE = {
    "decision_status": "REVIEW_REQUIRED",
    "missing_data": [
        "human_confirmed_asset_symbols",
        "current_prices",
        "portfolio_total_value_eur",
    ],
    "blockers": [],
    "summary": "P121 sample GEM response. Manual review required before any journal acceptance.",
    "human_decision_only": True,
    "no_order_no_sizing": True,
}


@dataclass(frozen=True)
class DailyGemLoopSmokeRequest:
    output_dir: str | Path
    run_id: str = "P121-LOCAL-SMOKE"
    portfolio_text: str = DEFAULT_PORTFOLIO_TEXT
    gem_response: Mapping[str, Any] | None = None
    generated_at_utc: str | None = None
    notes: str | None = None


def build_smoke_contract() -> dict[str, Any]:
    return {
        "contract": "P121_DAILY_GEM_LOOP_END_TO_END_LOCAL_SMOKE",
        "version": VERSION,
        "status": "LOCAL_ONLY_E2E_SMOKE",
        "purpose": "Verify P118 -> P119 -> P120 local GEM loop in one reproducible smoke run.",
        "steps": [
            "P118_DAILY_OPERATOR_SHORTCUT",
            "P119_GEM_RESPONSE_CAPTURE_REVIEW_QUEUE",
            "P120_DECISION_JOURNAL_BRIDGE_LOCAL_ONLY",
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


def _write_json(path: Path, payload: Mapping[str, Any]) -> None:
    path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )


def _report_markdown(result: Mapping[str, Any]) -> str:
    return "\n".join(
        [
            "# P121 Daily GEM Loop End-to-End Local Smoke Report",
            "",
            f"- status: {result['status']}",
            f"- version: {VERSION}",
            f"- output_dir: {result['output_dir']}",
            f"- run_id: {result['run_id']}",
            f"- p118_status: {result['p118']['status']}",
            f"- p119_decision_status: {result['p119']['decision_status']}",
            f"- p119_queue_rows: {result['p119']['queue_rows']}",
            f"- p120_journal_status: {result['p120']['journal_status']}",
            f"- p120_decision_status: {result['p120']['decision_status']}",
            "- safety: LOCAL_ONLY / HUMAN_REVIEW_ONLY / NO_SHEET_WRITE / NO_BROKER / NO_ORDER / NO_SIZING",
            "",
            "## Result",
            "",
            "The local loop is operational: daily prompt pack, GEM response capture queue, and local decision journal entry candidate.",
            "",
            "## Next",
            "",
            "P122_GEM_LOOP_OPERATOR_HANDOFF_AND_STOP_OR_UI_INPUT_HELPER",
            "",
        ]
    )


def write_daily_gem_loop_smoke_pack(request: DailyGemLoopSmokeRequest) -> dict[str, Any]:
    out = Path(request.output_dir)
    out.mkdir(parents=True, exist_ok=True)

    run_id = request.run_id
    generated_at = request.generated_at_utc

    p118_dir = out / "P121_STEP_P118_DAILY_SHORTCUT"
    p119_dir = out / "P121_STEP_P119_RESPONSE_CAPTURE_QUEUE"
    p120_dir = out / "P121_STEP_P120_DECISION_JOURNAL_BRIDGE"

    p118 = write_daily_shortcut_pack(
        DailyShortcutRequest(
            output_dir=p118_dir,
            pasted_text=request.portfolio_text,
            notes=request.notes or "P121 local smoke: P118 prompt generation.",
            run_id=f"{run_id}-P118",
            generated_at_utc=generated_at,
        )
    )

    gem_response = dict(request.gem_response or DEFAULT_GEM_RESPONSE)
    raw_gem_response = json.dumps(gem_response, ensure_ascii=False, indent=2, sort_keys=True)

    p119 = write_response_review_pack(
        GemResponseCaptureRequest(
            output_dir=p119_dir,
            raw_response=raw_gem_response,
            source_prompt_run_id=f"{run_id}-P118",
            response_run_id=f"{run_id}-P119",
            generated_at_utc=generated_at,
            notes=request.notes or "P121 local smoke: P119 response capture.",
        )
    )

    p119_capture = p119_dir / "P119_RESPONSE_CAPTURE.json"

    p120 = write_decision_journal_bridge_pack(
        DecisionJournalBridgeRequest(
            output_dir=p120_dir,
            response_capture_json_file=p119_capture,
            journal_entry_id=f"{run_id}-P120-JOURNAL",
            generated_at_utc=generated_at,
            notes=request.notes or "P121 local smoke: P120 local journal bridge.",
        )
    )

    result: dict[str, Any] = {
        "status": "PASS",
        "step": "P121_DAILY_GEM_LOOP_END_TO_END_LOCAL_SMOKE",
        "version": VERSION,
        "output_dir": str(out),
        "run_id": run_id,
        "p118": {
            "status": p118["status"],
            "runtime_prompt": p118.get("runtime_prompt"),
            "output_dir": p118["output_dir"],
        },
        "p119": {
            "status": p119["status"],
            "decision_status": p119["decision_status"],
            "missing_data_count": p119["missing_data_count"],
            "blocker_count": p119["blocker_count"],
            "queue_rows": p119["queue_rows"],
            "output_dir": p119["output_dir"],
        },
        "p120": {
            "status": p120["status"],
            "journal_status": p120["journal_status"],
            "decision_status": p120["decision_status"],
            "missing_data_count": p120["missing_data_count"],
            "blocker_count": p120["blocker_count"],
            "output_dir": p120["output_dir"],
        },
        "contract": build_smoke_contract(),
        "safety_markers": list(SAFETY_MARKERS),
        "human_review_only": True,
        "no_sheet_write": True,
        "no_order_no_sizing": True,
        "no_auto_apply_gem_response": True,
    }

    manifest_path = out / "P121_E2E_SMOKE_MANIFEST.json"
    contract_path = out / "P121_E2E_SMOKE_CONTRACT.json"
    report_path = out / "P121_E2E_SMOKE_REPORT.md"

    _write_json(manifest_path, result)
    _write_json(contract_path, build_smoke_contract())
    report_path.write_text(_report_markdown(result), encoding="utf-8")

    result["files"] = [
        str(manifest_path),
        str(contract_path),
        str(report_path),
        *p118["files"],
        *p119["files"],
        *p120["files"],
    ]
    return result


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        prog="python -m mvp_qaic_py.gem_daily_loop_smoke",
        description="Run local P118 -> P119 -> P120 GEM loop smoke.",
    )
    parser.add_argument("--output-dir", required=True)
    parser.add_argument("--run-id", default="P121-LOCAL-SMOKE")
    parser.add_argument("--portfolio-text")
    parser.add_argument("--portfolio-text-file")
    parser.add_argument("--gem-response-json-file")
    parser.add_argument("--generated-at-utc")
    parser.add_argument("--notes")
    return parser.parse_args(argv)


def _read_optional_text(path: str | None) -> str | None:
    if not path:
        return None
    return Path(path).read_text(encoding="utf-8-sig")


def _read_optional_json(path: str | None) -> Mapping[str, Any] | None:
    if not path:
        return None
    payload = json.loads(Path(path).read_text(encoding="utf-8-sig"))
    if not isinstance(payload, dict):
        raise ValueError("gem-response-json-file must contain a JSON object.")
    return payload


def main(argv: Sequence[str] | None = None) -> int:
    args = parse_args(argv)

    if args.portfolio_text and args.portfolio_text_file:
        raise ValueError("Use either --portfolio-text or --portfolio-text-file, not both.")

    portfolio_text = (
        args.portfolio_text
        or _read_optional_text(args.portfolio_text_file)
        or DEFAULT_PORTFOLIO_TEXT
    )
    gem_response = _read_optional_json(args.gem_response_json_file)

    result = write_daily_gem_loop_smoke_pack(
        DailyGemLoopSmokeRequest(
            output_dir=args.output_dir,
            run_id=args.run_id,
            portfolio_text=portfolio_text,
            gem_response=gem_response,
            generated_at_utc=args.generated_at_utc,
            notes=args.notes,
        )
    )

    print(result["status"])
    print(result["run_id"])
    print(result["p119"]["queue_rows"])
    print(result["p120"]["journal_status"])
    print(result["output_dir"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
