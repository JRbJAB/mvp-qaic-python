from __future__ import annotations

import json

import pytest

from qaic_core.pipelines import (
    PIPELINE_SAFETY_MARKERS,
    pipeline_result_to_dict,
    run_runtime_to_journal_pipeline,
)


def complete_trade_plan_without_price() -> dict[str, object]:
    return {
        "signal_id": "SIG-BTC-PIPE-001",
        "risk_guard": "HUMAN_REVIEW_ONLY,NO_BROKER,NO_ORDER,NO_SIZING",
        "asset": "BTC",
        "entry_price": 67200,
        "tp1": 70000,
        "tp2": 73500,
        "tp3": 78000,
        "stop_loss": 65000,
        "invalidation_level": 65000,
    }


def fake_btc_transport(url: str, timeout_sec: float) -> dict[str, object]:
    return {"bitcoin": {"usd": 68123.45}}


def test_pipeline_enriches_current_price_and_builds_journal_entry() -> None:
    result = run_runtime_to_journal_pipeline(
        trade_plan=complete_trade_plan_without_price(),
        run_id="RUN-P68-001",
        transport=fake_btc_transport,
        journal_timestamp="2026-06-21T00:00:00+00:00",
    )
    payload = pipeline_result_to_dict(result)

    assert payload["status"] == "REVIEW_REQUIRED"
    assert payload["asset"] == "BTC"
    assert payload["market_snapshot"]["current_price"] == 68123.45
    assert payload["trade_plan_request"]["current_price"] == 68123.45
    assert payload["runtime_result"]["decision_status"] == "REVIEW_REQUIRED"
    assert payload["journal_entry"]["run_id"] == "RUN-P68-001"
    assert payload["journal_entry"]["asset"] == "BTC"
    assert payload["journal_written"] is False
    assert payload["broker_called"] is False
    assert payload["order_created"] is False
    assert payload["sizing_created"] is False


def test_pipeline_without_transport_keeps_network_disabled_by_default() -> None:
    trade_plan = complete_trade_plan_without_price()
    trade_plan["current_price"] = 68000

    result = run_runtime_to_journal_pipeline(
        trade_plan=trade_plan,
        run_id="RUN-P68-NETWORK-OFF",
        journal_timestamp="2026-06-21T00:00:00+00:00",
    )
    payload = pipeline_result_to_dict(result)

    assert payload["status"] == "REVIEW_REQUIRED"
    assert "NETWORK_DISABLED_BY_DEFAULT" in payload["blockers"]
    assert payload["network_called"] is False
    assert payload["journal_written"] is False


def test_pipeline_propagates_forbidden_auto_order_blocker() -> None:
    trade_plan = complete_trade_plan_without_price()
    trade_plan["requested_action"] = "Place an automatic trailing stop order after TP1"

    result = run_runtime_to_journal_pipeline(
        trade_plan=trade_plan,
        run_id="RUN-P68-BLOCKED",
        transport=fake_btc_transport,
        journal_timestamp="2026-06-21T00:00:00+00:00",
    )
    payload = pipeline_result_to_dict(result)

    assert payload["status"] == "BLOCKED"
    assert "FORBIDDEN_AUTO_ORDER_REQUEST" in payload["blockers"]
    assert payload["journal_entry"]["decision_status"] == "BLOCKED"
    assert payload["order_created"] is False
    assert payload["sizing_created"] is False


def test_pipeline_journal_write_requires_explicit_path() -> None:
    result = run_runtime_to_journal_pipeline(
        trade_plan=complete_trade_plan_without_price(),
        run_id="RUN-P68-NO-PATH",
        transport=fake_btc_transport,
        write_journal=True,
        journal_timestamp="2026-06-21T00:00:00+00:00",
    )
    payload = pipeline_result_to_dict(result)

    assert payload["status"] == "REVIEW_REQUIRED"
    assert "JOURNAL_PATH_REQUIRED" in payload["blockers"]
    assert payload["journal_write"] is None
    assert payload["journal_written"] is False


def test_pipeline_writes_journal_only_to_explicit_tmp_path(tmp_path) -> None:
    result = run_runtime_to_journal_pipeline(
        trade_plan=complete_trade_plan_without_price(),
        run_id="RUN-P68-WRITE",
        transport=fake_btc_transport,
        write_journal=True,
        journal_dir=tmp_path,
        journal_file_name="pipeline_journal.jsonl",
        journal_timestamp="2026-06-21T00:00:00+00:00",
    )
    payload = pipeline_result_to_dict(result)

    assert payload["journal_written"] is True
    assert payload["journal_write"] is not None
    assert payload["journal_write"]["line_count"] == 1

    written = tmp_path / "pipeline_journal.jsonl"
    assert written.exists()
    line = written.read_text(encoding="utf-8").splitlines()[0]
    loaded = json.loads(line)
    assert loaded["entry"]["run_id"] == "RUN-P68-WRITE"
    assert loaded["validation"]["status"] == "PASS"


def test_pipeline_rejects_non_mapping_trade_plan() -> None:
    with pytest.raises(TypeError, match="trade_plan must be a mapping"):
        run_runtime_to_journal_pipeline(  # type: ignore[arg-type]
            trade_plan=[("asset", "BTC")],
            run_id="RUN-BAD",
        )


def test_pipeline_output_is_deterministic_with_fixed_timestamp() -> None:
    first = pipeline_result_to_dict(
        run_runtime_to_journal_pipeline(
            trade_plan=complete_trade_plan_without_price(),
            run_id="RUN-P68-DETERMINISTIC",
            transport=fake_btc_transport,
            journal_timestamp="2026-06-21T00:00:00+00:00",
        )
    )
    second = pipeline_result_to_dict(
        run_runtime_to_journal_pipeline(
            trade_plan=complete_trade_plan_without_price(),
            run_id="RUN-P68-DETERMINISTIC",
            transport=fake_btc_transport,
            journal_timestamp="2026-06-21T00:00:00+00:00",
        )
    )

    assert first == second


def test_pipeline_safety_markers_are_explicit() -> None:
    assert PIPELINE_SAFETY_MARKERS == (
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
