from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Sequence

from qaic_core.runner import local_mvp_run_result_to_dict, run_local_mvp_review

LOCAL_MVP_CLI_VERSION = "mvp_qaic.local_mvp_cli.v1"

LOCAL_MVP_CLI_SAFETY_MARKERS: tuple[str, ...] = (
    "LOCAL_MVP_CLI_ONLY",
    "EXPLICIT_INPUT_JSON_REQUIRED",
    "LIVE_READONLY",
    "HUMAN_REVIEW_ONLY",
    "NO_GOOGLE_LIVE_WRITE",
    "NO_SHEET_WRITE",
    "NO_BROKER",
    "NO_ORDER",
    "NO_SIZING",
    "NO_SECRET",
    "NO_REAL_NETWORK_BY_DEFAULT",
    "EXPLICIT_OUTPUT_DIR_REQUIRED_FOR_WRITE",
)


def _load_json_mapping(path: str | Path) -> dict[str, Any]:
    payload = json.loads(Path(path).read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise TypeError("input JSON must contain an object")
    return payload


def _mock_price_transport(asset: str, quote_currency: str, price: float):
    coin_id = {
        "BTC": "bitcoin",
        "XBT": "bitcoin",
        "ETH": "ethereum",
        "SOL": "solana",
        "LINK": "chainlink",
        "NEAR": "near",
    }.get(asset.strip().upper(), asset.strip().lower())

    quote = quote_currency.strip().lower()

    def transport(url: str, timeout_sec: float) -> dict[str, object]:
        return {coin_id: {quote: price}}

    return transport


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="python -m qaic_core.runner.cli",
        description="Run MVP QAIC local MVP review from an explicit JSON input.",
    )
    parser.add_argument("--input-json", required=True, help="Explicit trade plan JSON path.")
    parser.add_argument("--run-id", required=True, help="Deterministic run id.")
    parser.add_argument("--quote-currency", default="USD")
    parser.add_argument("--mock-current-price", type=float, default=None)
    parser.add_argument("--write-outputs", action="store_true")
    parser.add_argument("--output-dir", default=None)
    parser.add_argument("--journal-timestamp", default=None)
    parser.add_argument("--review-generated-at", default=None)
    parser.add_argument(
        "--pretty",
        action="store_true",
        help="Pretty print JSON stdout.",
    )
    return parser


def run_cli(argv: Sequence[str] | None = None) -> tuple[int, dict[str, object]]:
    parser = build_parser()
    args = parser.parse_args(argv)

    trade_plan = _load_json_mapping(args.input_json)
    asset = str(trade_plan.get("asset", ""))
    transport = None
    if args.mock_current_price is not None:
        transport = _mock_price_transport(asset, args.quote_currency, args.mock_current_price)

    result = run_local_mvp_review(
        trade_plan=trade_plan,
        run_id=args.run_id,
        quote_currency=args.quote_currency,
        allow_network=False,
        transport=transport,
        write_outputs=bool(args.write_outputs),
        output_dir=args.output_dir,
        journal_timestamp=args.journal_timestamp,
        review_generated_at=args.review_generated_at,
    )
    payload = local_mvp_run_result_to_dict(result)
    payload["cli_version"] = LOCAL_MVP_CLI_VERSION
    payload["cli_safety_markers"] = list(LOCAL_MVP_CLI_SAFETY_MARKERS)

    return 0, payload


def main(argv: Sequence[str] | None = None) -> int:
    try:
        exit_code, payload = run_cli(argv)
    except Exception as exc:  # noqa: BLE001
        error_payload = {
            "cli_version": LOCAL_MVP_CLI_VERSION,
            "status": "ERROR",
            "error": type(exc).__name__,
            "message": str(exc),
            "human_decision_only": True,
            "no_order_no_sizing": True,
            "broker_called": False,
            "order_created": False,
            "sizing_created": False,
            "safety_markers": list(LOCAL_MVP_CLI_SAFETY_MARKERS),
        }
        print(json.dumps(error_payload, sort_keys=True), file=sys.stderr)
        return 2

    parser = build_parser()
    parsed = parser.parse_args(argv)
    if parsed.pretty:
        print(json.dumps(payload, indent=2, sort_keys=True, ensure_ascii=False))
    else:
        print(json.dumps(payload, sort_keys=True, ensure_ascii=False))
    return exit_code


if __name__ == "__main__":
    raise SystemExit(main())
