from __future__ import annotations

import json

import pytest

from qaic_core.runner import (
    LOCAL_MVP_RUNNER_SAFETY_MARKERS,
    local_mvp_run_result_to_dict,
    run_local_mvp_review,
)


def complete_trade_plan_without_price() -> dict[str, object]:
    return {
        "signal_id": "SIG-BTC-RUNNER-001",
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


def test_runner_builds_pipeline_and_review_pack_without_writing_by_default() -> None:
    result = run_local_mvp_review(
        trade_plan=complete_trade_plan_without_price(),
        run_id="RUN-P70-001",
        transport=fake_btc_transport,
        journal_timestamp="2026-06-21T00:00:00+00:00",
        review_generated_at="2026-06-21T00:10:00+00:00",
    )
    payload = local_mvp_run_result_to_dict(result)

    assert payload["runner_version"] == "mvp_qaic.local_mvp_runner.v1"
    assert payload["status"] == "REVIEW_REQUIRED"
    assert payload["asset"] == "BTC"
    assert payload["pipeline_result"]["trade_plan_request"]["current_price"] == 68123.45
    assert payload["review_pack"]["asset"] == "BTC"
    assert payload["journal_written"] is False
    assert payload["review_pack_written"] is False
    assert payload["review_write"] is None
    assert payload["broker_called"] is False
    assert payload["order_created"] is False
    assert payload["sizing_created"] is False


def test_runner_write_outputs_requires_explicit_output_dir() -> None:
    result = run_local_mvp_review(
        trade_plan=complete_trade_plan_without_price(),
        run_id="RUN-P70-NO-OUTPUT",
        transport=fake_btc_transport,
        write_outputs=True,
        journal_timestamp="2026-06-21T00:00:00+00:00",
        review_generated_at="2026-06-21T00:10:00+00:00",
    )
    payload = local_mvp_run_result_to_dict(result)

    assert payload["status"] == "REVIEW_REQUIRED"
    assert "OUTPUT_DIR_REQUIRED" in payload["blockers"]
    assert payload["journal_written"] is False
    assert payload["review_pack_written"] is False


def test_runner_writes_journal_and_review_only_to_explicit_tmp_path(tmp_path) -> None:
    result = run_local_mvp_review(
        trade_plan=complete_trade_plan_without_price(),
        run_id="RUN-P70-WRITE",
        transport=fake_btc_transport,
        write_outputs=True,
        output_dir=tmp_path,
        journal_timestamp="2026-06-21T00:00:00+00:00",
        review_generated_at="2026-06-21T00:10:00+00:00",
    )
    payload = local_mvp_run_result_to_dict(result)

    assert payload["journal_written"] is True
    assert payload["review_pack_written"] is True
    assert payload["review_write"] is not None
    assert (tmp_path / "journal" / "decision_journal.jsonl").exists()
    assert (tmp_path / "review_pack" / "operator_review.md").exists()
    assert (tmp_path / "review_pack" / "operator_review.json").exists()
    assert (tmp_path / "review_pack" / "operator_review_manifest.json").exists()

    review_json = json.loads(
        (tmp_path / "review_pack" / "operator_review.json").read_text(encoding="utf-8")
    )
    assert review_json["run_id"] == "RUN-P70-WRITE"


def test_runner_propagates_blocked_auto_order() -> None:
    trade_plan = complete_trade_plan_without_price()
    trade_plan["requested_action"] = "Place an automatic trailing stop order after TP1"

    result = run_local_mvp_review(
        trade_plan=trade_plan,
        run_id="RUN-P70-BLOCKED",
        transport=fake_btc_transport,
        journal_timestamp="2026-06-21T00:00:00+00:00",
        review_generated_at="2026-06-21T00:10:00+00:00",
    )
    payload = local_mvp_run_result_to_dict(result)

    assert payload["status"] == "BLOCKED"
    assert "FORBIDDEN_AUTO_ORDER_REQUEST" in payload["blockers"]
    assert payload["review_pack"]["status"] == "BLOCKED"
    assert payload["order_created"] is False
    assert payload["sizing_created"] is False


def test_runner_is_deterministic_with_fixed_timestamps() -> None:
    first = local_mvp_run_result_to_dict(
        run_local_mvp_review(
            trade_plan=complete_trade_plan_without_price(),
            run_id="RUN-P70-DETERMINISTIC",
            transport=fake_btc_transport,
            journal_timestamp="2026-06-21T00:00:00+00:00",
            review_generated_at="2026-06-21T00:10:00+00:00",
        )
    )
    second = local_mvp_run_result_to_dict(
        run_local_mvp_review(
            trade_plan=complete_trade_plan_without_price(),
            run_id="RUN-P70-DETERMINISTIC",
            transport=fake_btc_transport,
            journal_timestamp="2026-06-21T00:00:00+00:00",
            review_generated_at="2026-06-21T00:10:00+00:00",
        )
    )

    assert first == second


def test_runner_rejects_non_mapping_trade_plan() -> None:
    with pytest.raises(TypeError, match="trade_plan must be a mapping"):
        run_local_mvp_review(  # type: ignore[arg-type]
            trade_plan=[("asset", "BTC")],
            run_id="RUN-BAD",
        )


def test_runner_safety_markers_are_explicit() -> None:
    assert LOCAL_MVP_RUNNER_SAFETY_MARKERS == (
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
