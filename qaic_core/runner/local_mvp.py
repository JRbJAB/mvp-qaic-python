from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Mapping, Sequence

from qaic_core.live.providers.public_market import Transport
from qaic_core.pipelines import pipeline_result_to_dict, run_runtime_to_journal_pipeline
from qaic_core.review_pack import (
    build_operator_review_pack,
    operator_review_pack_to_dict,
    write_operator_review_pack,
    write_result_to_dict,
)

LOCAL_MVP_RUNNER_VERSION = "mvp_qaic.local_mvp_runner.v1"

LOCAL_MVP_RUNNER_SAFETY_MARKERS: tuple[str, ...] = (
    "LOCAL_MVP_RUNNER_ONLY",
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


@dataclass(frozen=True)
class LocalMvpRunResult:
    runner_version: str
    run_id: str
    status: str
    asset: str
    pipeline_result: Mapping[str, Any]
    review_pack: Mapping[str, Any]
    review_write: Mapping[str, Any] | None = None
    output_dir: str | None = None
    missing_data: tuple[str, ...] = field(default_factory=tuple)
    blockers: tuple[str, ...] = field(default_factory=tuple)
    live_readonly: bool = True
    human_decision_only: bool = True
    no_order_no_sizing: bool = True
    network_called: bool = False
    journal_written: bool = False
    review_pack_written: bool = False
    broker_called: bool = False
    order_created: bool = False
    sizing_created: bool = False
    safety_markers: tuple[str, ...] = LOCAL_MVP_RUNNER_SAFETY_MARKERS


def _as_tuple(value: object) -> tuple[str, ...]:
    if value is None:
        return ()
    if isinstance(value, str):
        return (value,) if value.strip() else ()
    if isinstance(value, Sequence) and not isinstance(value, (bytes, bytearray)):
        return tuple(str(item) for item in value if str(item).strip())
    return (str(value),)


def _unique(values: Sequence[str]) -> tuple[str, ...]:
    seen: set[str] = set()
    ordered: list[str] = []
    for value in values:
        if value not in seen:
            ordered.append(value)
            seen.add(value)
    return tuple(ordered)


def _runner_status(
    pipeline_result: Mapping[str, Any],
    review_pack: Mapping[str, Any],
    blockers: Sequence[str],
) -> str:
    if pipeline_result.get("status") == "BLOCKED" or review_pack.get("status") == "BLOCKED":
        return "BLOCKED"
    if "FORBIDDEN_AUTO_ORDER_REQUEST" in blockers or "FORBIDDEN_SIZING_REQUEST" in blockers:
        return "BLOCKED"
    return "REVIEW_REQUIRED"


def run_local_mvp_review(
    *,
    trade_plan: Mapping[str, Any],
    run_id: str,
    quote_currency: str = "USD",
    allow_network: bool = False,
    transport: Transport | None = None,
    write_outputs: bool = False,
    output_dir: str | Path | None = None,
    journal_timestamp: str | None = None,
    review_generated_at: str | None = None,
) -> LocalMvpRunResult:
    """Run the local MVP review path.

    Default behavior is read-only and fileless: no real network by default and
    no local files written. File writes require write_outputs=True and an
    explicit output_dir.
    """

    if not isinstance(trade_plan, Mapping):
        raise TypeError("trade_plan must be a mapping")

    output_path = Path(output_dir) if output_dir is not None else None
    write_requested_without_path = write_outputs and output_path is None

    pipeline = run_runtime_to_journal_pipeline(
        trade_plan=trade_plan,
        run_id=run_id,
        quote_currency=quote_currency,
        allow_network=allow_network,
        transport=transport,
        write_journal=write_outputs and output_path is not None,
        journal_dir=(output_path / "journal") if output_path is not None else None,
        journal_timestamp=journal_timestamp,
    )
    pipeline_payload = pipeline_result_to_dict(pipeline)

    review_pack = build_operator_review_pack(
        pipeline_payload,
        generated_at=review_generated_at,
    )
    review_payload = operator_review_pack_to_dict(review_pack)

    review_write_payload: dict[str, object] | None = None
    review_pack_written = False
    blockers = list(_as_tuple(pipeline_payload.get("blockers")))
    missing_data = list(_as_tuple(pipeline_payload.get("missing_data")))

    if write_requested_without_path:
        blockers.append("OUTPUT_DIR_REQUIRED")
    elif write_outputs and output_path is not None:
        write_result = write_operator_review_pack(
            review_pack,
            output_dir=output_path / "review_pack",
        )
        review_write_payload = write_result_to_dict(write_result)
        review_pack_written = bool(write_result.wrote_files)

    unique_blockers = _unique(blockers)
    unique_missing = _unique(missing_data)
    status = _runner_status(pipeline_payload, review_payload, unique_blockers)

    return LocalMvpRunResult(
        runner_version=LOCAL_MVP_RUNNER_VERSION,
        run_id=run_id,
        status=status,
        asset=str(pipeline_payload.get("asset", "")).upper(),
        pipeline_result=pipeline_payload,
        review_pack=review_payload,
        review_write=review_write_payload,
        output_dir=str(output_path) if output_path is not None else None,
        missing_data=unique_missing,
        blockers=unique_blockers,
        live_readonly=True,
        human_decision_only=True,
        no_order_no_sizing=True,
        network_called=bool(pipeline_payload.get("network_called", False)),
        journal_written=bool(pipeline_payload.get("journal_written", False)),
        review_pack_written=review_pack_written,
        broker_called=False,
        order_created=False,
        sizing_created=False,
    )


def local_mvp_run_result_to_dict(result: LocalMvpRunResult) -> dict[str, object]:
    return {
        "runner_version": result.runner_version,
        "run_id": result.run_id,
        "status": result.status,
        "asset": result.asset,
        "pipeline_result": dict(result.pipeline_result),
        "review_pack": dict(result.review_pack),
        "review_write": dict(result.review_write) if result.review_write is not None else None,
        "output_dir": result.output_dir,
        "missing_data": list(result.missing_data),
        "blockers": list(result.blockers),
        "live_readonly": result.live_readonly,
        "human_decision_only": result.human_decision_only,
        "no_order_no_sizing": result.no_order_no_sizing,
        "network_called": result.network_called,
        "journal_written": result.journal_written,
        "review_pack_written": result.review_pack_written,
        "broker_called": result.broker_called,
        "order_created": result.order_created,
        "sizing_created": result.sizing_created,
        "safety_markers": list(result.safety_markers),
    }
