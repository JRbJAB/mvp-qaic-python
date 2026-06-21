from __future__ import annotations

import json

import pytest

from qaic_core.benchmark.ai_trade_benchmark_cli import (
    build_cli_benchmark_export_bundle,
    build_cli_benchmark_export_payload,
)


def sample_cli_records() -> list[dict[str, object]]:
    return [
        {
            "asset": "BTC",
            "decision_status": "HUMAN_REVIEW_ONLY",
            "score": 81.25,
        }
    ]


def test_cli_export_payload_uses_export_layer_safety_contract() -> None:
    payload = build_cli_benchmark_export_payload(
        sample_cli_records(),
        run_id="P60D_CLI_TEST",
        generated_at="2026-06-21T00:00:00Z",
    )

    assert payload["run_id"] == "P60D_CLI_TEST"
    assert payload["source"] == "cli"
    assert payload["summary"]["record_count"] == 1
    assert payload["safety"]["human_review_only"] is True
    assert payload["safety"]["no_broker"] is True
    assert payload["safety"]["no_order"] is True
    assert payload["safety"]["no_sizing"] is True
    assert payload["safety"]["no_google_live_write"] is True
    assert "LOCAL_FILES_ONLY" in payload["safety"]["markers"]


def test_cli_export_bundle_contains_json_csv_markdown_without_file_write() -> None:
    bundle = build_cli_benchmark_export_bundle(
        sample_cli_records(),
        run_id="P60D_CLI_TEST",
        generated_at="2026-06-21T00:00:00Z",
    )

    assert set(bundle) == {"json", "csv", "markdown"}
    assert json.loads(bundle["json"])["run_id"] == "P60D_CLI_TEST"
    assert "P60D_CLI_TEST" in bundle["csv"]
    assert "# MVP QAIC Benchmark Export Report" in bundle["markdown"]
    assert "NO_BROKER" in bundle["markdown"]


def test_cli_export_accepts_single_mapping_record() -> None:
    payload = build_cli_benchmark_export_payload(
        {
            "asset": "ETH",
            "decision_status": "WATCH_ONLY",
            "score": 73.5,
        },
        run_id="P60D_SINGLE",
    )

    assert payload["summary"]["record_count"] == 1
    assert payload["records"][0]["asset"] == "ETH"


def test_cli_export_is_deterministic() -> None:
    first = build_cli_benchmark_export_bundle(sample_cli_records(), run_id="P60D_DETERMINISTIC")
    second = build_cli_benchmark_export_bundle(sample_cli_records(), run_id="P60D_DETERMINISTIC")

    assert first == second


def test_cli_export_rejects_scalar_string_record() -> None:
    with pytest.raises(TypeError, match="records must be mappings or dataclasses"):
        build_cli_benchmark_export_payload("BTC", run_id="P60D_BAD_STRING")
