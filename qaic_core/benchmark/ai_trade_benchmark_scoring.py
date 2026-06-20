"""Deterministic, non-advisory benchmark decision rules."""

from __future__ import annotations

from .ai_trade_benchmark_model import BenchmarkDecision

_BLOCK_TERMS = (
    "bot",
    "exchange connection",
    "connect exchange",
    "copy bot",
    "copy trading",
    "auto trading",
    "automatic trading",
    "broker execution",
    "automatic order",
    "order placement",
    "place orders",
    "automatic sizing",
)


def determine_decision(
    evidence: str,
    *,
    safeguards_clear: bool = True,
    strong_inspiration: bool = False,
) -> BenchmarkDecision:
    """Classify product evidence without producing an investment recommendation."""
    normalized = evidence.casefold()
    if any(term in normalized for term in _BLOCK_TERMS):
        return BenchmarkDecision.BLOCKED
    if not safeguards_clear:
        return BenchmarkDecision.REVIEW_REQUIRED
    if strong_inspiration:
        return BenchmarkDecision.INSPIRE
    return BenchmarkDecision.MONITOR


def validate_seed_decision(tool_name: str, decision: BenchmarkDecision | str) -> None:
    """Keep known execution-risk products blocked for this baseline."""
    parsed = BenchmarkDecision(decision)
    if (
        tool_name in {"3Commas", "Cryptohopper", "Tickeron"}
        and parsed is not BenchmarkDecision.BLOCKED
    ):
        raise ValueError(f"{tool_name} must remain BLOCKED")
