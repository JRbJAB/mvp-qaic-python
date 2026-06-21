"""Offline CLI for the P59C AI trade benchmark."""

from __future__ import annotations

from collections.abc import Mapping

from qaic_core.benchmark.ai_trade_benchmark_export import (
    build_benchmark_export_bundle,
    build_benchmark_export_payload,
)

import argparse
import csv
import json
from dataclasses import asdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Sequence

from .ai_trade_benchmark_model import BenchmarkRun, SafetyContract
from .ai_trade_benchmark_seed import baseline_tools
from .ai_trade_benchmark_sheets import (
    ALLOWED_TAB,
    build_google_sheets_apply_plan,
    build_sheets_dry_run_plan,
)


def create_run(run_id: str | None = None) -> BenchmarkRun:
    resolved = run_id or datetime.now(timezone.utc).strftime("P59C-%Y%m%dT%H%M%SZ")
    return BenchmarkRun(resolved, baseline_tools())


def write_local_outputs(output_dir: str | Path, run: BenchmarkRun) -> tuple[Path, Path, Path]:
    output = Path(output_dir)
    output.mkdir(parents=True, exist_ok=True)
    csv_path = output / "BENCHMARK_AI_TRADE.csv"
    json_path = output / "P59C_BENCHMARK_AI_TRADE.json"
    audit_path = output / "P59C_BENCHMARK_AI_TRADE_AUDIT.json"
    safety = asdict(run.safety)
    with csv_path.open("w", newline="", encoding="utf-8") as handle:
        fields = [
            "tool_id",
            "tool_name",
            "category",
            "overall_score",
            "source_url",
            "decision",
            "notes",
            "human_review_only",
            "no_broker",
            "no_order",
            "no_sizing",
            "missing_data",
            "no_auto_signal_copy",
        ]
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        for tool in run.tools:
            row = tool.to_dict()
            row["missing_data"] = ";".join(row["missing_data"])
            row["no_auto_signal_copy"] = safety["no_auto_signal_copy"]
            writer.writerow(row)
    json_path.write_text(
        json.dumps(run.to_dict(), indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    decisions = {tool.tool_name: tool.decision.value for tool in run.tools}
    audit = {
        "run_id": run.run_id,
        "generated_at": run.generated_at,
        "status": "HUMAN_REVIEW_ONLY",
        "candidate_count": len(run.tools),
        "decisions": decisions,
        "safety": safety,
        "google_live_call": False,
        "broker_order_sizing": False,
    }
    audit.update(
        {
            key: safety[key]
            for key in (
                "human_review_only",
                "no_broker",
                "no_order",
                "no_sizing",
                "no_auto_signal_copy",
            )
        }
    )
    audit_path.write_text(json.dumps(audit, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return csv_path, json_path, audit_path


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="benchmark-ai-trade")
    commands = parser.add_subparsers(dest="command", required=True)
    build = commands.add_parser("build")
    build.add_argument("--output-dir", required=True)
    build.add_argument("--run-id")
    dry = commands.add_parser("sheets-dry-run")
    dry.add_argument("--spreadsheet-id", required=True)
    dry.add_argument("--run-id", required=True)
    dry.add_argument("--output")
    apply_cmd = commands.add_parser("sheets-apply")
    apply_cmd.add_argument("--spreadsheet-id", required=True)
    apply_cmd.add_argument("--run-id", required=True)
    apply_cmd.add_argument("--tab", default=ALLOWED_TAB)
    apply_cmd.add_argument("--apply", action="store_true", default=False)
    apply_cmd.add_argument("--human-go", action="store_true", default=False)
    apply_cmd.add_argument("--backup-confirmed", action="store_true", default=False)
    credentials = apply_cmd.add_mutually_exclusive_group()
    credentials.add_argument("--credentials-path")
    credentials.add_argument("--credentials-ref")
    apply_cmd.add_argument("--output")
    return parser


def _emit(payload: object, destination: str | None) -> None:
    rendered = json.dumps(payload, indent=2, ensure_ascii=False) + "\n"
    if destination:
        Path(destination).write_text(rendered, encoding="utf-8")
    else:
        print(rendered, end="")


def main(argv: Sequence[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    if args.command == "build":
        paths = write_local_outputs(args.output_dir, create_run(args.run_id))
        _emit(
            {
                "status": "OK",
                "files": [str(path) for path in paths],
                "safety": asdict(SafetyContract()),
            },
            None,
        )
        return 0
    run = create_run(args.run_id)
    if args.command == "sheets-dry-run":
        _emit(build_sheets_dry_run_plan(args.spreadsheet_id, run), args.output)
        return 0
    payload = build_google_sheets_apply_plan(
        spreadsheet_id=args.spreadsheet_id,
        run=run,
        allowed_tab_name=args.tab,
        run_id=args.run_id,
        backup_confirmed=args.backup_confirmed,
        apply=args.apply,
        human_go=args.human_go,
        dry_run=not args.apply,
        credentials_path=args.credentials_path,
        credentials_ref=args.credentials_ref,
    )
    _emit(payload, args.output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())


def _coerce_cli_export_records(records: object) -> list[object]:
    if isinstance(records, Mapping):
        return [records]
    if isinstance(records, (str, bytes, bytearray)):
        return [records]
    try:
        return list(records)  # type: ignore[arg-type]
    except TypeError:
        return [records]


def build_cli_benchmark_export_payload(
    records: object,
    *,
    run_id: str = "CLI_BENCHMARK_EXPORT",
    generated_at: str = "CLI_EXPORT_UNSPECIFIED_TIME",
    source: str = "cli",
) -> dict[str, object]:
    """Build a local-only benchmark export payload for CLI-facing flows.

    This helper is deliberately data-only:
    - no file write
    - no Google live write
    - no broker/order/sizing
    """

    return build_benchmark_export_payload(
        _coerce_cli_export_records(records),
        run_id=run_id,
        generated_at=generated_at,
        source=source,
    )


def build_cli_benchmark_export_bundle(
    records: object,
    *,
    run_id: str = "CLI_BENCHMARK_EXPORT",
    generated_at: str = "CLI_EXPORT_UNSPECIFIED_TIME",
    source: str = "cli",
) -> dict[str, str]:
    """Build JSON/CSV/Markdown strings for CLI-facing local benchmark export."""

    return build_benchmark_export_bundle(
        _coerce_cli_export_records(records),
        run_id=run_id,
        generated_at=generated_at,
        source=source,
    )
