from __future__ import annotations

import json

import pytest

from qaic_core.pipelines import pipeline_result_to_dict, run_runtime_to_journal_pipeline
from qaic_core.review_pack import (
    OPERATOR_REVIEW_PACK_SAFETY_MARKERS,
    build_operator_review_pack,
    operator_review_pack_to_dict,
    render_operator_review_markdown,
    write_operator_review_pack,
    write_result_to_dict,
)


def complete_trade_plan_without_price() -> dict[str, object]:
    return {
        "signal_id": "SIG-BTC-REVIEW-001",
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


def build_pipeline_payload(requested_action: str | None = None) -> dict[str, object]:
    trade_plan = complete_trade_plan_without_price()
    if requested_action is not None:
        trade_plan["requested_action"] = requested_action

    result = run_runtime_to_journal_pipeline(
        trade_plan=trade_plan,
        run_id="RUN-P69-001",
        transport=fake_btc_transport,
        journal_timestamp="2026-06-21T00:00:00+00:00",
    )
    return pipeline_result_to_dict(result)


def test_build_operator_review_pack_from_pipeline_payload() -> None:
    pack = build_operator_review_pack(
        build_pipeline_payload(),
        generated_at="2026-06-21T00:10:00+00:00",
    )
    payload = operator_review_pack_to_dict(pack)

    assert payload["review_pack_version"] == "mvp_qaic.operator_review_pack.v1"
    assert payload["run_id"] == "RUN-P69-001"
    assert payload["asset"] == "BTC"
    assert payload["status"] == "REVIEW_REQUIRED"
    assert payload["decision_status"] == "REVIEW_REQUIRED"
    assert payload["current_price"] == 68123.45
    assert payload["human_decision_only"] is True
    assert payload["no_order_no_sizing"] is True


def test_blocked_auto_order_is_visible_in_review_markdown() -> None:
    pack = build_operator_review_pack(
        build_pipeline_payload("Place an automatic trailing stop order after TP1"),
        generated_at="2026-06-21T00:10:00+00:00",
    )
    markdown = render_operator_review_markdown(pack)

    assert pack.status == "BLOCKED"
    assert "FORBIDDEN_AUTO_ORDER_REQUEST" in markdown
    assert "Do not execute: blocker present." in markdown
    assert "Remove any automatic order request." in markdown
    assert "NO_ORDER" in markdown
    assert "NO_SIZING" in markdown


def test_write_operator_review_pack_explicit_tmp_path_only(tmp_path) -> None:
    pack = build_operator_review_pack(
        build_pipeline_payload(),
        generated_at="2026-06-21T00:10:00+00:00",
    )

    result = write_operator_review_pack(pack, output_dir=tmp_path)
    payload = write_result_to_dict(result)

    assert payload["wrote_files"] is True
    assert payload["file_count"] == 3
    assert sorted(payload["files"]) == [
        "operator_review.json",
        "operator_review.md",
        "operator_review_manifest.json",
    ]

    review_json = json.loads((tmp_path / "operator_review.json").read_text(encoding="utf-8"))
    manifest_json = json.loads(
        (tmp_path / "operator_review_manifest.json").read_text(encoding="utf-8")
    )
    assert review_json["run_id"] == "RUN-P69-001"
    assert manifest_json["file_count"] == 2
    assert (tmp_path / "operator_review.md").exists()


def test_review_pack_is_deterministic_with_fixed_timestamps() -> None:
    first = operator_review_pack_to_dict(
        build_operator_review_pack(
            build_pipeline_payload(),
            generated_at="2026-06-21T00:10:00+00:00",
        )
    )
    second = operator_review_pack_to_dict(
        build_operator_review_pack(
            build_pipeline_payload(),
            generated_at="2026-06-21T00:10:00+00:00",
        )
    )

    assert first == second


def test_review_pack_rejects_non_mapping_payload() -> None:
    with pytest.raises(TypeError, match="pipeline_result must be a mapping"):
        build_operator_review_pack(  # type: ignore[arg-type]
            [("run_id", "BAD")],
            generated_at="2026-06-21T00:10:00+00:00",
        )


def test_review_pack_safety_summary_never_enables_execution() -> None:
    pack = build_operator_review_pack(
        build_pipeline_payload(),
        generated_at="2026-06-21T00:10:00+00:00",
    )
    payload = operator_review_pack_to_dict(pack)

    assert payload["pipeline_summary"]["broker_called"] is False
    assert payload["pipeline_summary"]["order_created"] is False
    assert payload["pipeline_summary"]["sizing_created"] is False
    assert payload["human_decision_only"] is True
    assert payload["no_order_no_sizing"] is True


def test_operator_review_safety_markers_are_explicit() -> None:
    assert OPERATOR_REVIEW_PACK_SAFETY_MARKERS == (
        "LOCAL_OPERATOR_REVIEW_ONLY",
        "HUMAN_REVIEW_ONLY",
        "NO_GOOGLE_LIVE_WRITE",
        "NO_SHEET_WRITE",
        "NO_BROKER",
        "NO_ORDER",
        "NO_SIZING",
        "NO_SECRET",
        "EXPLICIT_OUTPUT_DIR_REQUIRED_FOR_WRITE",
    )
