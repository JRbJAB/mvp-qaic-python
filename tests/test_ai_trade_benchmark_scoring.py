import pytest

from qaic_core.benchmark.ai_trade_benchmark_model import BenchmarkDecision
from qaic_core.benchmark.ai_trade_benchmark_scoring import (
    determine_decision,
    validate_seed_decision,
)
from qaic_core.benchmark.ai_trade_benchmark_seed import baseline_tools


def test_execution_language_is_blocked():
    assert determine_decision("Connect exchange and place orders") is BenchmarkDecision.BLOCKED


def test_fixed_risk_products_are_blocked():
    decisions = {tool.tool_name: tool.decision for tool in baseline_tools()}
    for name in ("3Commas", "Cryptohopper", "Tickeron"):
        assert decisions[name] is BenchmarkDecision.BLOCKED
        with pytest.raises(ValueError):
            validate_seed_decision(name, BenchmarkDecision.MONITOR)
