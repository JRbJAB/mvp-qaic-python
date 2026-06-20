"""Fixed P59C baseline data; no network lookup is performed."""

from __future__ import annotations

from .ai_trade_benchmark_model import BenchmarkCategory as C
from .ai_trade_benchmark_model import BenchmarkDecision as D
from .ai_trade_benchmark_model import BenchmarkTool
from .ai_trade_benchmark_scoring import validate_seed_decision


def _tool(
    index: int, name: str, category: C, score: int, url: str, decision: D, notes: str
) -> BenchmarkTool:
    tool = BenchmarkTool(f"AITRADE-{index:04d}", name, category, score, url, decision, notes)
    validate_seed_decision(name, decision)
    return tool


def baseline_tools() -> tuple[BenchmarkTool, ...]:
    tools = (
        _tool(
            1,
            "TradingView",
            C.CHARTING,
            88,
            "https://www.tradingview.com/",
            D.INSPIRE,
            "Charting and cockpit UX reference. Human-review only.",
        ),
        _tool(
            2,
            "TrendSpider",
            C.MARKET_ANALYTICS,
            72,
            "https://trendspider.com/",
            D.REVIEW_REQUIRED,
            "Automation claims require safeguard validation.",
        ),
        _tool(
            3,
            "Tickeron",
            C.TRADING_AUTOMATION,
            35,
            "https://tickeron.com/",
            D.BLOCKED,
            "AI trading automation risk. Blocked from execution use.",
        ),
        _tool(
            4,
            "Token Metrics",
            C.MARKET_ANALYTICS,
            68,
            "https://www.tokenmetrics.com/",
            D.MONITOR,
            "Analytics inspiration; claims require validation.",
        ),
        _tool(
            5,
            "Glassnode",
            C.ONCHAIN_ANALYTICS,
            84,
            "https://glassnode.com/",
            D.INSPIRE,
            "On-chain data and dashboard inspiration.",
        ),
        _tool(
            6,
            "CryptoQuant",
            C.ONCHAIN_ANALYTICS,
            82,
            "https://cryptoquant.com/",
            D.INSPIRE,
            "On-chain metrics cockpit inspiration.",
        ),
        _tool(
            7,
            "Nansen",
            C.ONCHAIN_ANALYTICS,
            80,
            "https://www.nansen.ai/",
            D.INSPIRE,
            "Wallet and on-chain analytics inspiration.",
        ),
        _tool(
            8,
            "Santiment",
            C.MARKET_ANALYTICS,
            75,
            "https://santiment.net/",
            D.MONITOR,
            "Data and social analytics require evidence review.",
        ),
        _tool(
            9,
            "Messari",
            C.RESEARCH,
            79,
            "https://messari.io/",
            D.INSPIRE,
            "Research and data presentation inspiration.",
        ),
        _tool(
            10,
            "Sentora / IntoTheBlock",
            C.ONCHAIN_ANALYTICS,
            74,
            "https://www.intotheblock.com/",
            D.MONITOR,
            "On-chain analytics baseline; validate current evidence.",
        ),
        _tool(
            11,
            "Arkham Intelligence",
            C.ONCHAIN_ANALYTICS,
            73,
            "https://arkm.com/",
            D.MONITOR,
            "Entity and wallet intelligence requires human validation.",
        ),
        _tool(
            12,
            "3Commas",
            C.TRADING_AUTOMATION,
            20,
            "https://3commas.io/",
            D.BLOCKED,
            "Bots and exchange execution risk. Blocked.",
        ),
        _tool(
            13,
            "Cryptohopper",
            C.TRADING_AUTOMATION,
            20,
            "https://www.cryptohopper.com/",
            D.BLOCKED,
            "Bots and exchange execution risk. Blocked.",
        ),
        _tool(
            14,
            "VIPAlgos",
            C.TRADINGVIEW_INDICATORS,
            61,
            "https://www.vipalgos.com/",
            D.MONITOR,
            "Requested baseline. TradingView AI indicators, buy/sell alerts, TP/SL zones. No auto trades per FAQ. Human-review only.",
        ),
    )
    if len(tools) != 14 or len({tool.tool_name for tool in tools}) != 14:
        raise AssertionError("The baseline must contain exactly 14 unique tools")
    return tools


SEED_TOOLS = baseline_tools()
