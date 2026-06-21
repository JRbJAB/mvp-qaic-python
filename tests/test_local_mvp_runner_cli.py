from __future__ import annotations

import json

from qaic_core.runner.cli import (
    LOCAL_MVP_CLI_SAFETY_MARKERS,
    main,
    run_cli,
)


def complete_trade_plan_without_price() -> dict[str, object]:
    return {
        "signal_id": "SIG-BTC-CLI-001",
        "risk_guard": "HUMAN_REVIEW_ONLY,NO_BROKER,NO_ORDER,NO_SIZING",
        "asset": "BTC",
        "entry_price": 67200,
        "tp1": 70000,
        "tp2": 73500,
        "tp3": 78000,
        "stop_loss": 65000,
        "invalidation_level": 65000,
    }


def write_input(tmp_path, payload: object):
    path = tmp_path / "trade_plan.json"
    path.write_text(json.dumps(payload), encoding="utf-8")
    return path


def test_run_cli_outputs_review_required_without_writing_by_default(tmp_path) -> None:
    input_path = write_input(tmp_path, complete_trade_plan_without_price())

    exit_code, payload = run_cli(
        [
            "--input-json",
            str(input_path),
            "--run-id",
            "RUN-P71-001",
            "--mock-current-price",
            "68123.45",
            "--journal-timestamp",
            "2026-06-21T00:00:00+00:00",
            "--review-generated-at",
            "2026-06-21T00:10:00+00:00",
        ]
    )

    assert exit_code == 0
    assert payload["cli_version"] == "mvp_qaic.local_mvp_cli.v1"
    assert payload["status"] == "REVIEW_REQUIRED"
    assert payload["asset"] == "BTC"
    assert payload["pipeline_result"]["trade_plan_request"]["current_price"] == 68123.45
    assert payload["journal_written"] is False
    assert payload["review_pack_written"] is False
    assert payload["broker_called"] is False
    assert payload["order_created"] is False
    assert payload["sizing_created"] is False


def test_run_cli_write_outputs_requires_explicit_output_dir(tmp_path) -> None:
    input_path = write_input(tmp_path, complete_trade_plan_without_price())

    exit_code, payload = run_cli(
        [
            "--input-json",
            str(input_path),
            "--run-id",
            "RUN-P71-NO-OUTPUT",
            "--mock-current-price",
            "68123.45",
            "--write-outputs",
            "--journal-timestamp",
            "2026-06-21T00:00:00+00:00",
            "--review-generated-at",
            "2026-06-21T00:10:00+00:00",
        ]
    )

    assert exit_code == 0
    assert payload["status"] == "REVIEW_REQUIRED"
    assert "OUTPUT_DIR_REQUIRED" in payload["blockers"]
    assert payload["journal_written"] is False
    assert payload["review_pack_written"] is False


def test_run_cli_writes_outputs_to_explicit_output_dir(tmp_path) -> None:
    input_path = write_input(tmp_path, complete_trade_plan_without_price())
    output_dir = tmp_path / "out"

    exit_code, payload = run_cli(
        [
            "--input-json",
            str(input_path),
            "--run-id",
            "RUN-P71-WRITE",
            "--mock-current-price",
            "68123.45",
            "--write-outputs",
            "--output-dir",
            str(output_dir),
            "--journal-timestamp",
            "2026-06-21T00:00:00+00:00",
            "--review-generated-at",
            "2026-06-21T00:10:00+00:00",
        ]
    )

    assert exit_code == 0
    assert payload["journal_written"] is True
    assert payload["review_pack_written"] is True
    assert (output_dir / "journal" / "decision_journal.jsonl").exists()
    assert (output_dir / "review_pack" / "operator_review.md").exists()
    assert (output_dir / "review_pack" / "operator_review.json").exists()


def test_run_cli_propagates_blocked_auto_order(tmp_path) -> None:
    trade_plan = complete_trade_plan_without_price()
    trade_plan["requested_action"] = "Place an automatic trailing stop order after TP1"
    input_path = write_input(tmp_path, trade_plan)

    exit_code, payload = run_cli(
        [
            "--input-json",
            str(input_path),
            "--run-id",
            "RUN-P71-BLOCKED",
            "--mock-current-price",
            "68123.45",
            "--journal-timestamp",
            "2026-06-21T00:00:00+00:00",
            "--review-generated-at",
            "2026-06-21T00:10:00+00:00",
        ]
    )

    assert exit_code == 0
    assert payload["status"] == "BLOCKED"
    assert "FORBIDDEN_AUTO_ORDER_REQUEST" in payload["blockers"]
    assert payload["order_created"] is False
    assert payload["sizing_created"] is False


def test_main_prints_json_to_stdout(tmp_path, capsys) -> None:
    input_path = write_input(tmp_path, complete_trade_plan_without_price())

    exit_code = main(
        [
            "--input-json",
            str(input_path),
            "--run-id",
            "RUN-P71-STDOUT",
            "--mock-current-price",
            "68123.45",
            "--journal-timestamp",
            "2026-06-21T00:00:00+00:00",
            "--review-generated-at",
            "2026-06-21T00:10:00+00:00",
        ]
    )

    assert exit_code == 0
    captured = capsys.readouterr()
    payload = json.loads(captured.out)
    assert payload["run_id"] == "RUN-P71-STDOUT"
    assert payload["status"] == "REVIEW_REQUIRED"


def test_main_returns_error_for_non_object_json(tmp_path, capsys) -> None:
    input_path = write_input(tmp_path, ["not", "object"])

    exit_code = main(
        [
            "--input-json",
            str(input_path),
            "--run-id",
            "RUN-P71-BAD",
        ]
    )

    assert exit_code == 2
    captured = capsys.readouterr()
    payload = json.loads(captured.err)
    assert payload["status"] == "ERROR"
    assert payload["human_decision_only"] is True
    assert payload["no_order_no_sizing"] is True
    assert payload["broker_called"] is False


def test_local_mvp_cli_safety_markers_are_explicit() -> None:
    assert LOCAL_MVP_CLI_SAFETY_MARKERS == (
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
