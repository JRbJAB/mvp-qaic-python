from __future__ import annotations

from dataclasses import asdict, dataclass, field, is_dataclass
from pathlib import Path
from typing import Any, Mapping, Sequence

from qaic_core.decision_journal import (
    build_decision_journal_entry,
    decision_journal_entry_to_dict,
    journal_write_result_to_dict,
    write_decision_journal_jsonl,
)
from qaic_core.live.providers.public_market import (
    Transport,
    fetch_public_market_snapshot,
    market_snapshot_to_dict,
)
from qaic_core.trade_plan.runtime_contract import evaluate_trade_plan_request

RUNTIME_TO_JOURNAL_PIPELINE_VERSION = "mvp_qaic.runtime_to_journal_pipeline.v1"

PIPELINE_SAFETY_MARKERS: tuple[str, ...] = (
    "LOCAL_PIPELINE_ONLY",
    "LIVE_READONLY",
    "PUBLIC_MARKET_DATA_ONLY",
    "HUMAN_REVIEW_ONLY",
    "NO_GOOGLE_LIVE_WRITE",
    "NO_SHEET_WRITE",
    "NO_BROKER",
    "NO_ORDER",
    "NO_SIZING",
    "NO_SECRET",
    "JOURNAL_WRITE_EXPLICIT_PATH_ONLY",
)


@dataclass(frozen=True)
class RuntimeToJournalPipelineResult:
    pipeline_version: str
    run_id: str
    status: str
    asset: str
    market_snapshot: Mapping[str, Any]
    trade_plan_request: Mapping[str, Any]
    runtime_result: Mapping[str, Any]
    journal_entry: Mapping[str, Any]
    journal_write: Mapping[str, Any] | None = None
    missing_data: tuple[str, ...] = field(default_factory=tuple)
    blockers: tuple[str, ...] = field(default_factory=tuple)
    live_readonly: bool = True
    network_called: bool = False
    journal_written: bool = False
    broker_called: bool = False
    order_created: bool = False
    sizing_created: bool = False
    safety_markers: tuple[str, ...] = PIPELINE_SAFETY_MARKERS


def _as_tuple(value: object) -> tuple[str, ...]:
    if value is None:
        return ()
    if isinstance(value, str):
        return (value,) if value.strip() else ()
    if isinstance(value, Sequence) and not isinstance(value, (bytes, bytearray)):
        return tuple(str(item) for item in value if str(item).strip())
    return (str(value),)


def _unique(values: Sequence[str]) -> tuple[str, ...]:
    ordered: list[str] = []
    seen: set[str] = set()
    for value in values:
        if value not in seen:
            ordered.append(value)
            seen.add(value)
    return tuple(ordered)


def _has_missing_current_price(record: Mapping[str, Any]) -> bool:
    value = record.get("current_price")
    if value is None:
        return True
    if isinstance(value, str) and value.strip() == "":
        return True
    return False


def _result_to_mapping(value: object) -> dict[str, Any]:
    if isinstance(value, Mapping):
        return dict(value)
    if is_dataclass(value) and not isinstance(value, type):
        return asdict(value)
    if hasattr(value, "__dict__"):
        return dict(vars(value))
    raise TypeError("runtime_result must be mapping-like or dataclass-like")


def _pipeline_status(runtime_result: Mapping[str, Any], blockers: Sequence[str]) -> str:
    if runtime_result.get("decision_status") == "BLOCKED":
        return "BLOCKED"
    if "FORBIDDEN_AUTO_ORDER_REQUEST" in blockers or "FORBIDDEN_SIZING_REQUEST" in blockers:
        return "BLOCKED"
    return "REVIEW_REQUIRED"


def run_runtime_to_journal_pipeline(
    *,
    trade_plan: Mapping[str, Any],
    run_id: str,
    quote_currency: str = "USD",
    allow_network: bool = False,
    transport: Transport | None = None,
    write_journal: bool = False,
    journal_dir: str | Path | None = None,
    journal_file_name: str = "decision_journal.jsonl",
    journal_timestamp: str | None = None,
    journal_notes: Sequence[str] | None = None,
) -> RuntimeToJournalPipelineResult:
    """Run the local read-only runtime-to-journal path.

    The default path performs no real network call and writes no journal file.
    A fake transport can be injected for deterministic tests. JSONL journal
    writing requires write_journal=True and an explicit journal_dir.
    """

    if not isinstance(trade_plan, Mapping):
        raise TypeError("trade_plan must be a mapping")

    trade_plan_request: dict[str, Any] = dict(trade_plan)
    asset = str(trade_plan_request.get("asset", "")).strip().upper()

    market_snapshot = fetch_public_market_snapshot(
        asset=asset,
        quote_currency=quote_currency,
        allow_network=allow_network,
        transport=transport,
    )
    market_payload = market_snapshot_to_dict(market_snapshot)

    if (
        _has_missing_current_price(trade_plan_request)
        and market_payload.get("current_price") is not None
    ):
        trade_plan_request["current_price"] = market_payload["current_price"]

    runtime_result = evaluate_trade_plan_request(trade_plan_request)
    runtime_payload = _result_to_mapping(runtime_result)

    runtime_blockers = _as_tuple(runtime_payload.get("blockers"))
    runtime_missing = _as_tuple(runtime_payload.get("missing_data"))
    market_blockers = _as_tuple(market_payload.get("blockers"))
    market_missing = _as_tuple(market_payload.get("missing_data"))

    blockers = list(market_blockers) + list(runtime_blockers)
    missing_data = list(market_missing) + list(runtime_missing)

    journal_record = {
        "signal_id": trade_plan_request.get("signal_id", ""),
        "asset": asset,
        "decision_status": runtime_payload.get("decision_status", "REVIEW_REQUIRED"),
        "human_decision_only": runtime_payload.get("human_decision_only", True),
        "no_order_no_sizing": runtime_payload.get("no_order_no_sizing", True),
        "risk_guard": trade_plan_request.get("risk_guard", ""),
        "missing_data": list(runtime_missing),
        "blockers": list(runtime_blockers),
        "notes": list(journal_notes or ()),
    }
    journal_entry = build_decision_journal_entry(
        journal_record,
        run_id=run_id,
        timestamp=journal_timestamp,
        notes=journal_notes,
    )
    journal_payload = decision_journal_entry_to_dict(journal_entry)

    journal_write_payload: dict[str, object] | None = None
    journal_written = False

    if write_journal:
        if journal_dir is None:
            blockers.append("JOURNAL_PATH_REQUIRED")
        else:
            write_result = write_decision_journal_jsonl(
                entries=[journal_entry],
                journal_dir=journal_dir,
                file_name=journal_file_name,
            )
            journal_write_payload = journal_write_result_to_dict(write_result)
            journal_written = bool(write_result.wrote_file)

    unique_blockers = _unique(blockers)
    unique_missing = _unique(missing_data)
    status = _pipeline_status(runtime_payload, unique_blockers)

    return RuntimeToJournalPipelineResult(
        pipeline_version=RUNTIME_TO_JOURNAL_PIPELINE_VERSION,
        run_id=run_id,
        status=status,
        asset=asset,
        market_snapshot=market_payload,
        trade_plan_request=trade_plan_request,
        runtime_result=runtime_payload,
        journal_entry=journal_payload,
        journal_write=journal_write_payload,
        missing_data=unique_missing,
        blockers=unique_blockers,
        live_readonly=True,
        network_called=bool(market_payload.get("network_called", False)),
        journal_written=journal_written,
        broker_called=False,
        order_created=False,
        sizing_created=False,
    )


def pipeline_result_to_dict(
    result: RuntimeToJournalPipelineResult,
) -> dict[str, object]:
    return {
        "pipeline_version": result.pipeline_version,
        "run_id": result.run_id,
        "status": result.status,
        "asset": result.asset,
        "market_snapshot": dict(result.market_snapshot),
        "trade_plan_request": dict(result.trade_plan_request),
        "runtime_result": dict(result.runtime_result),
        "journal_entry": dict(result.journal_entry),
        "journal_write": dict(result.journal_write) if result.journal_write is not None else None,
        "missing_data": list(result.missing_data),
        "blockers": list(result.blockers),
        "live_readonly": result.live_readonly,
        "network_called": result.network_called,
        "journal_written": result.journal_written,
        "broker_called": result.broker_called,
        "order_created": result.order_created,
        "sizing_created": result.sizing_created,
        "safety_markers": list(result.safety_markers),
    }
