"""Typed model for the human-review-only AI trading tools benchmark."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any

SAFETY_MARKERS = (
    "HUMAN_REVIEW_ONLY",
    "NO_BROKER",
    "NO_ORDER",
    "NO_SIZING",
    "NO_AUTO_SIGNAL_COPY",
    "NO_FINANCIAL_ADVICE",
    "NO_SECRET",
    "NO_APPS_SCRIPT",
    "NO_CLASP",
    "DRY_RUN_DEFAULT",
    "APPLY_REQUIRES_EXPLICIT_FLAG",
    "GOOGLE_CREDENTIALS_OUTSIDE_REPO",
)


class BenchmarkDecision(str, Enum):
    INSPIRE = "INSPIRE"
    MONITOR = "MONITOR"
    IGNORE = "IGNORE"
    REVIEW_REQUIRED = "REVIEW_REQUIRED"
    BLOCKED = "BLOCKED"


class BenchmarkCategory(str, Enum):
    CHARTING = "CHARTING"
    MARKET_ANALYTICS = "MARKET_ANALYTICS"
    ONCHAIN_ANALYTICS = "ONCHAIN_ANALYTICS"
    RESEARCH = "RESEARCH"
    TRADING_AUTOMATION = "TRADING_AUTOMATION"
    TRADINGVIEW_INDICATORS = "TRADINGVIEW_INDICATORS"


@dataclass(frozen=True)
class SafetyContract:
    human_review_only: bool = True
    no_broker: bool = True
    no_order: bool = True
    no_sizing: bool = True
    no_auto_signal_copy: bool = True
    no_financial_advice: bool = True
    no_secret: bool = True
    no_apps_script: bool = True
    no_clasp: bool = True
    dry_run_default: bool = True
    apply_requires_explicit_flag: bool = True
    google_credentials_outside_repo: bool = True

    def assert_safe(self) -> None:
        if not all(asdict(self).values()):
            raise ValueError("All benchmark safety markers must remain true")


@dataclass(frozen=True)
class BenchmarkTool:
    tool_id: str
    tool_name: str
    category: BenchmarkCategory | str
    overall_score: int
    source_url: str
    decision: BenchmarkDecision | str
    notes: str
    human_review_only: bool = True
    no_broker: bool = True
    no_order: bool = True
    no_sizing: bool = True
    missing_data: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        object.__setattr__(self, "category", BenchmarkCategory(self.category))
        object.__setattr__(self, "decision", BenchmarkDecision(self.decision))
        object.__setattr__(self, "missing_data", tuple(self.missing_data))
        if not 0 <= self.overall_score <= 100:
            raise ValueError("overall_score must be between 0 and 100")
        if not all((self.human_review_only, self.no_broker, self.no_order, self.no_sizing)):
            raise ValueError("Unsafe benchmark tool contract")

    def to_dict(self) -> dict[str, Any]:
        result = asdict(self)
        result["category"] = self.category.value
        result["decision"] = self.decision.value
        result["missing_data"] = list(self.missing_data)
        return result


@dataclass(frozen=True)
class BenchmarkRun:
    run_id: str
    tools: tuple[BenchmarkTool, ...]
    generated_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    status: str = "HUMAN_REVIEW_ONLY"
    safety: SafetyContract = field(default_factory=SafetyContract)

    def __post_init__(self) -> None:
        if not self.run_id.strip():
            raise ValueError("run_id is required")
        object.__setattr__(self, "tools", tuple(self.tools))
        self.safety.assert_safe()

    def to_dict(self) -> dict[str, Any]:
        result = {
            "run_id": self.run_id,
            "generated_at": self.generated_at,
            "status": self.status,
            "safety": asdict(self.safety),
            "tools": [tool.to_dict() for tool in self.tools],
        }
        result.update(
            {
                key: value
                for key, value in asdict(self.safety).items()
                if key
                in {
                    "human_review_only",
                    "no_broker",
                    "no_order",
                    "no_sizing",
                    "no_auto_signal_copy",
                }
            }
        )
        return result
