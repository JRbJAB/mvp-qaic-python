from qaic_core.benchmark.ai_trade_benchmark_model import BenchmarkDecision, BenchmarkRun
from qaic_core.benchmark.ai_trade_benchmark_seed import baseline_tools


def test_baseline_and_vipalgos_contract():
    tools = baseline_tools()
    assert len(tools) == 14
    vip = next(tool for tool in tools if tool.tool_name == "VIPAlgos")
    assert vip.tool_id == "AITRADE-0014"
    assert vip.decision is BenchmarkDecision.MONITOR
    assert BenchmarkRun("test-run", tools).safety.no_auto_signal_copy
