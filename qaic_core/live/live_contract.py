from __future__ import annotations

from dataclasses import dataclass, field
from typing import Mapping, Any

LIVE_RUNTIME_VERSION = "mvp_qaic.python_live_readonly_runtime.v1"
LIVE_READONLY_MODE = "LIVE_READONLY"

REQUIRED_LIVE_SAFETY_MARKERS: tuple[str, ...] = (
    "LIVE_READONLY",
    "HUMAN_REVIEW_ONLY",
    "NO_BROKER",
    "NO_ORDER",
    "NO_SIZING",
    "NO_AUTO_TRAILING_ORDER",
    "NO_SECRET",
    "NO_NETWORK_CALL_BY_DEFAULT",
)


@dataclass(frozen=True)
class LiveRuntimeInput:
    mode: str
    provider: str
    payload: Mapping[str, Any]
    safety_markers: tuple[str, ...] = REQUIRED_LIVE_SAFETY_MARKERS


@dataclass(frozen=True)
class LiveRuntimeResult:
    runtime_version: str = LIVE_RUNTIME_VERSION
    mode: str = LIVE_READONLY_MODE
    provider: str = "LOCAL_PAYLOAD"
    decision_status: str = "REVIEW_REQUIRED"
    missing_data: tuple[str, ...] = field(default_factory=tuple)
    blockers: tuple[str, ...] = field(default_factory=tuple)
    human_decision_only: bool = True
    no_order_no_sizing: bool = True
    safety_markers: tuple[str, ...] = REQUIRED_LIVE_SAFETY_MARKERS
    live_readonly: bool = True
    network_called: bool = False
    broker_called: bool = False
    order_created: bool = False
    sizing_created: bool = False
    notes: tuple[str, ...] = field(default_factory=tuple)


def live_runtime_result_to_dict(result: LiveRuntimeResult) -> dict[str, object]:
    return {
        "runtime_version": result.runtime_version,
        "mode": result.mode,
        "provider": result.provider,
        "decision_status": result.decision_status,
        "missing_data": list(result.missing_data),
        "blockers": list(result.blockers),
        "human_decision_only": result.human_decision_only,
        "no_order_no_sizing": result.no_order_no_sizing,
        "safety_markers": list(result.safety_markers),
        "live_readonly": result.live_readonly,
        "network_called": result.network_called,
        "broker_called": result.broker_called,
        "order_created": result.order_created,
        "sizing_created": result.sizing_created,
        "notes": list(result.notes),
    }
