from pathlib import Path

from mvp_qaic_py.qaic_bridge_contract import (
    build_bridge_contract_payload,
    validate_bridge_contract_payload,
)
from mvp_qaic_py.reflex_app.registry import qaic_bridge_operator_card
from mvp_qaic_reflex_ui.qaic_bridge_operator_binding import (
    build_qaic_bridge_operator_binding,
    build_qaic_bridge_operator_card,
)


MODULE = Path("mvp_qaic_reflex_ui/qaic_bridge_operator_binding.py")
REQUIRED_SAFETY = {
    "no_runtime": True,
    "no_provider_call": True,
    "no_broker_order_sizing": True,
    "no_sheet_bq_write": True,
    "human_review_required": True,
    "qaic_execution_allowed": False,
}


def test_h9a_bridge_contract_still_validates():
    assert validate_bridge_contract_payload(build_bridge_contract_payload()) == []


def test_h9b_binding_exists_and_returns_contract_id():
    card = build_qaic_bridge_operator_card()
    assert card["card_id"] == "mvp_qaic_to_qaic_bridge"
    assert card["contract_id"] == "MVP_QAIC_TO_QAIC_BRIDGE_R1"
    assert "MVP to QAIC Bridge" in card["title"]
    assert card["mode"] == "REVIEW_ONLY_LOCAL_HANDOFF"
    assert card["source_system"] == "MVP_QAIC"
    assert card["target_system"] == "QAIC_PY"


def test_binding_exposes_private_review_only_route():
    card = build_qaic_bridge_operator_card()
    route = card.get("route") or card.get("target_route")
    assert route == "/qaic-bridge"
    assert card["visibility"] == "private_operator_cockpit"
    assert card["handoff_policy"] == "review_only_local_handoff"


def test_binding_contains_required_safety_flags():
    safety = build_qaic_bridge_operator_card()["safety"]
    for key, expected in REQUIRED_SAFETY.items():
        assert safety[key] is expected


def test_binding_status_ready_for_review_only_handoff():
    binding = build_qaic_bridge_operator_binding()
    card = binding["cards"][0]
    assert binding["status"] == "READY_FOR_QAIC_REVIEW_ONLY_HANDOFF"
    assert card["status"] == "READY_FOR_QAIC_REVIEW_ONLY_HANDOFF"


def test_registry_can_consume_bridge_card():
    registry_card = qaic_bridge_operator_card()
    assert registry_card["card_id"] == "mvp_qaic_to_qaic_bridge"
    assert registry_card["contract_id"] == "MVP_QAIC_TO_QAIC_BRIDGE_R1"
    assert registry_card["route"] == "/qaic-bridge"


def test_new_h9b_source_has_no_forbidden_live_call_substrings():
    source = MODULE.read_text(encoding="utf-8").lower()
    forbidden = [
        "requests",
        "httpx",
        "aiohttp",
        "urllib",
        "subprocess",
        "docker",
        "reflex run",
        "npm",
        "bun",
        "googleapiclient",
        "gspread",
        "pandas",
    ]
    for term in forbidden:
        assert term not in source


def test_prior_guard_and_bridge_tests_remain_present():
    assert Path("tests/test_reflex_cli_contract_h8i.py").is_file()
    assert Path("tests/test_mvp_qaic_to_qaic_bridge_contract_r1.py").is_file()
