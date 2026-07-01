"""Static operator binding for the MVP QAIC to QAIC review-only bridge."""

from __future__ import annotations

from typing import Any

from mvp_qaic_py.qaic_bridge_contract import (
    CONTRACT_ID,
    MODE,
    SOURCE_SYSTEM,
    TARGET_SYSTEM,
    build_bridge_contract_payload,
    validate_bridge_contract_payload,
)


CARD_ID = "mvp_qaic_to_qaic_bridge"
TITLE = "MVP to QAIC Bridge"
STATUS = "READY_FOR_QAIC_REVIEW_ONLY_HANDOFF"
ROUTE = "/qaic-bridge"


def build_qaic_bridge_operator_card() -> dict[str, Any]:
    """Return the private cockpit card for the sealed QAIC bridge handoff."""
    contract = build_bridge_contract_payload()
    errors = validate_bridge_contract_payload(contract)
    if errors:
        raise ValueError(f"Invalid QAIC bridge contract payload: {errors}")

    safety = contract["safety"]
    return {
        "card_id": CARD_ID,
        "contract_id": CONTRACT_ID,
        "title": TITLE,
        "mode": MODE,
        "source_system": SOURCE_SYSTEM,
        "target_system": TARGET_SYSTEM,
        "status": STATUS,
        "route": ROUTE,
        "target_route": ROUTE,
        "visibility": "private_operator_cockpit",
        "handoff_policy": "review_only_local_handoff",
        "qaic_import_mode": contract["qaic_import"]["import_mode"],
        "safety": {
            "no_runtime": safety["no_runtime"],
            "no_provider_call": safety["no_provider_call"],
            "no_broker_order_sizing": safety["no_broker_order_sizing"],
            "no_sheet_bq_write": safety["no_sheet_bq_write"],
            "human_review_required": safety["human_review_required"],
            "qaic_execution_allowed": safety["qaic_execution_allowed"],
        },
        "evidence": dict(contract["evidence"]),
    }


def build_qaic_bridge_operator_binding() -> dict[str, Any]:
    """Return the static binding payload consumed by UI and registries."""
    card = build_qaic_bridge_operator_card()
    return {
        "binding_id": "h9b_qaic_bridge_operator_binding",
        "status": STATUS,
        "route": ROUTE,
        "cards": [card],
        "tool_registry_entries": [
            {
                "tool_id": card["card_id"],
                "contract_id": card["contract_id"],
                "route": card["route"],
                "status": card["status"],
                "private_review_only": True,
                "qaic_execution_allowed": False,
            }
        ],
    }
