import json

import pytest

from qaic_core.benchmark.ai_trade_benchmark_cli import main


def test_local_build_writes_expected_outputs(tmp_path):
    assert main(["build", "--output-dir", str(tmp_path), "--run-id", "test-run"]) == 0
    expected = {
        "BENCHMARK_AI_TRADE.csv",
        "P59C_BENCHMARK_AI_TRADE.json",
        "P59C_BENCHMARK_AI_TRADE_AUDIT.json",
    }
    assert expected <= {path.name for path in tmp_path.iterdir()}
    payload = json.loads((tmp_path / "P59C_BENCHMARK_AI_TRADE.json").read_text(encoding="utf-8"))
    assert payload["human_review_only"] is True
    assert payload["no_broker"] is True
    assert payload["no_order"] is True
    assert payload["no_sizing"] is True
    assert payload["no_auto_signal_copy"] is True


def test_apply_without_required_flags_is_refused():
    with pytest.raises(SystemExit):
        main(["sheets-apply", "--spreadsheet-id", "sheet"])
