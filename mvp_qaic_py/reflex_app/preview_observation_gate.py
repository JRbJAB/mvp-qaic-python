"""Manual private preview observation gate.

The gate prepares observation evidence and a manual launch command.
It does not start Reflex, open a browser, publish, write to external systems,
or perform broker/order/sizing actions.
"""

from __future__ import annotations

from dataclasses import dataclass

from .preview_selector import (
    build_private_preview_command,
    build_private_preview_selector_payload,
    selector_is_safe_for_local_private_preview,
)


@dataclass(frozen=True)
class PreviewObservationGate:
    gate_status: str
    manual_command: tuple[str, ...]
    expected_local_url: str
    server_started_by_gate: bool
    browser_opened_by_gate: bool
    public_deploy_allowed: bool
    live_action_allowed: bool
    observation_required: bool
    operator_next_action: str


def build_preview_observation_gate() -> PreviewObservationGate:
    command = build_private_preview_command()
    return PreviewObservationGate(
        gate_status="READY_FOR_OPERATOR_MANUAL_RUN",
        manual_command=command.command,
        expected_local_url=f"http://{command.host}:{command.port}",
        server_started_by_gate=False,
        browser_opened_by_gate=False,
        public_deploy_allowed=False,
        live_action_allowed=False,
        observation_required=True,
        operator_next_action=(
            "Run the generated manual preview command, observe the local UI, "
            "then provide screenshot/log feedback for the next gate."
        ),
    )


def build_preview_observation_payload() -> dict[str, object]:
    selector_payload = build_private_preview_selector_payload()
    gate = build_preview_observation_gate()

    return {
        "gate_status": gate.gate_status,
        "selector_safe": selector_is_safe_for_local_private_preview(),
        "manual_command": list(gate.manual_command),
        "expected_local_url": gate.expected_local_url,
        "server_started_by_gate": gate.server_started_by_gate,
        "browser_opened_by_gate": gate.browser_opened_by_gate,
        "public_deploy_allowed": gate.public_deploy_allowed,
        "live_action_allowed": gate.live_action_allowed,
        "observation_required": gate.observation_required,
        "operator_next_action": gate.operator_next_action,
        "selector_status": selector_payload["selector_status"],
        "data_binding_mode": selector_payload["data_binding_mode"],
        "ui_navigation_group_count": selector_payload["ui_navigation_group_count"],
        "ui_navigation_item_count": selector_payload["ui_navigation_item_count"],
        "next_recommended_batch": "P_REFLEX_07_PRIVATE_PREVIEW_OBSERVATION_REVIEW",
    }


def gate_is_safe_and_ready() -> bool:
    payload = build_preview_observation_payload()
    return (
        payload["selector_safe"] is True
        and payload["gate_status"] == "READY_FOR_OPERATOR_MANUAL_RUN"
        and payload["expected_local_url"] == "http://127.0.0.1:3000"
        and payload["server_started_by_gate"] is False
        and payload["browser_opened_by_gate"] is False
        and payload["public_deploy_allowed"] is False
        and payload["live_action_allowed"] is False
        and payload["observation_required"] is True
    )
