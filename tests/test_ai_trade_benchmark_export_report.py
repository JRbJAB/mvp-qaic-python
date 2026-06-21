from __future__ import annotations

import json
from dataclasses import dataclass

import pytest

from qaic_core.benchmark.ai_trade_benchmark_export import (
    SAFETY_MARKERS,
    benchmark_payload_to_csv,
    benchmark_payload_to_csv_rows,
    benchmark_payload_to_json,
    benchmark_payload_to_markdown,
    build_benchmark_export_bundle,
    build_benchmark_export_payload,
    normalize_benchmark_record,
)


@dataclass(frozen=True)
class SampleRecord:
    asset: str
    score: float
    decision_status: str


def sample_records() -> list[dict[str, object]]:
    return [
        {
            "asset": "BTC",
            "score": 81.25,
            "decision_status": "HUMAN_REVIEW_ONLY",
            "risk": {"level": "medium"},
        },
        {
            "asset": "ETH",
            "score": 73.5,
            "decision_status": "WATCH_ONLY",
            "notes": ["dry_run", "no_order"],
        },
    ]


def test_export_payload_contains_summary_and_safety_markers() -> None:
    payload = build_benchmark_export_payload(
        sample_records(),
        run_id="P60B_TEST",
        generated_at="2026-06-21T00:00:00Z",
        source="pytest",
    )

    assert payload["schema_version"].startswith("MVP_QAIC_BENCHMARK_EXPORT_REPORT")
    assert payload["run_id"] == "P60B_TEST"
    assert payload["summary"]["record_count"] == 2
    assert payload["safety"]["human_review_only"] is True
    assert payload["safety"]["no_broker"] is True
    assert payload["safety"]["no_order"] is True
    assert payload["safety"]["no_sizing"] is True
    assert payload["safety"]["no_google_live_write"] is True
    assert set(SAFETY_MARKERS).issubset(set(payload["safety"]["markers"]))


def test_export_payload_serializers_are_deterministic() -> None:
    payload = build_benchmark_export_payload(
        sample_records(),
        run_id="P60B_TEST",
        generated_at="2026-06-21T00:00:00Z",
    )

    first = benchmark_payload_to_json(payload)
    second = benchmark_payload_to_json(payload)

    assert first == second
    decoded = json.loads(first)
    assert decoded["summary"]["fields"] == sorted(decoded["summary"]["fields"])


def test_csv_export_includes_run_id_and_records() -> None:
    payload = build_benchmark_export_payload(sample_records(), run_id="P60B_TEST")

    rows = benchmark_payload_to_csv_rows(payload)
    csv_text = benchmark_payload_to_csv(payload)

    assert rows[0]["run_id"] == "P60B_TEST"
    assert rows[0]["record_index"] == "0"
    assert rows[0]["asset"] == "BTC"
    assert "run_id,record_index" in csv_text
    assert "P60B_TEST" in csv_text


def test_markdown_export_is_decision_readable() -> None:
    payload = build_benchmark_export_payload(sample_records(), run_id="P60B_TEST")
    markdown = benchmark_payload_to_markdown(payload)

    assert "# MVP QAIC Benchmark Export Report" in markdown
    assert "`HUMAN_REVIEW_ONLY`" in markdown
    assert "| record_index |" in markdown
    assert "BTC" in markdown
    assert "NO_BROKER" in markdown


def test_export_bundle_contains_json_csv_and_markdown_only() -> None:
    bundle = build_benchmark_export_bundle(sample_records(), run_id="P60B_TEST")

    assert set(bundle) == {"json", "csv", "markdown"}
    assert json.loads(bundle["json"])["run_id"] == "P60B_TEST"
    assert "P60B_TEST" in bundle["csv"]
    assert "P60B_TEST" in bundle["markdown"]


def test_normalize_record_supports_dataclass_and_nested_values() -> None:
    normalized = normalize_benchmark_record(
        SampleRecord(
            asset="SOL",
            score=64.0,
            decision_status="WATCH_ONLY",
        )
    )

    assert normalized == {
        "asset": "SOL",
        "decision_status": "WATCH_ONLY",
        "score": 64.0,
    }

    nested = normalize_benchmark_record({"risk": {"level": "high"}, "tags": ["a", "b"]})
    assert nested["risk"] == '{"level": "high"}'
    assert nested["tags"] == '["a", "b"]'


def test_export_rejects_non_mapping_record() -> None:
    with pytest.raises(TypeError, match="records must be mappings or dataclasses"):
        normalize_benchmark_record(object())
