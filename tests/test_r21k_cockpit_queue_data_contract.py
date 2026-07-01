from pathlib import Path

from mvp_qaic_py.cockpit_queue_data_contract_r21k import (
    CONTRACT_ID,
    build_cockpit_queue_contract,
    contract_to_dict,
    validate_cockpit_queue_contract,
)


def test_r21k_contract_identity_and_source_chain() -> None:
    contract = build_cockpit_queue_contract()

    assert contract.contract_id == CONTRACT_ID
    assert contract.source_chain == "R21J_R6_VALIDATED_BY_READONLY_HEAD_AUDIT"
    assert contract.source_tag == "mvp-qaic-r21j-r6-docs-only-supersede-seal-no-runtime-20260701"
    assert contract.status == "COCKPIT_QUEUE_DATA_CONTRACT_READY_NO_RUNTIME"


def test_r21k_cockpit_ready_traces_are_present() -> None:
    payload = contract_to_dict()
    flags = payload["cockpit_ready_flags"]

    assert flags["BRAND_CONFIG_TRACE_COCKPIT_READY"] is True
    assert flags["UI_TRACKER_TRACE_COCKPIT_READY"] is True
    assert flags["TOOL_REGISTRY_CDC_TRACE_COCKPIT_READY"] is True
    assert flags["CDC_CONTRACT_TRACE_COCKPIT_READY"] is True
    assert flags["QAIC_BRIDGE_TRACE_COCKPIT_READY"] is True
    assert flags["QAIT_CHARTE_TEMPLATE_BOUND"] is True
    assert flags["MVP_QAIC_LOGO_VALIDATED_BOUND"] is True
    assert flags["preserve_q_candlesticks_signal_line"] is True


def test_r21k_policy_is_review_only_and_no_write() -> None:
    payload = contract_to_dict()
    policy = payload["policy_flags"]

    assert policy["no_code_runner"] is True
    assert policy["no_ui_process_start"] is True
    assert policy["no_container_process"] is True
    assert policy["no_provider_call"] is True
    assert policy["no_broker_order_sizing"] is True
    assert policy["no_sheet_bq_write"] is True
    assert policy["no_markup_file_output"] is True
    assert policy["no_export_directory_output"] is True
    assert policy["human_review_required"] is True
    assert policy["qaic_execution_allowed"] is False


def test_r21k_fields_are_cockpit_consumable() -> None:
    payload = contract_to_dict()
    field_keys = {field["key"] for field in payload["fields"]}
    item_ids = {item["item_id"] for item in payload["queue_items"]}

    assert "qaic_bridge_trace" in field_keys
    assert "brand_config_trace" in field_keys
    assert "ui_tracker_trace" in field_keys
    assert "tool_registry_cdc_trace" in field_keys
    assert "cdc_contract_trace" in field_keys
    assert "operator_review_queue" in field_keys
    assert "R21K-BRAND-CONFIG" in item_ids
    assert "R21K-QAIC-BRIDGE" in item_ids


def test_r21k_validation_summary() -> None:
    result = validate_cockpit_queue_contract()

    assert result["status_ready"] is True
    assert result["required_groups_present"] is True
    assert result["brand_config_ready"] is True
    assert result["ui_tracker_ready"] is True
    assert result["tool_registry_cdc_ready"] is True
    assert result["cdc_contract_ready"] is True
    assert result["qaic_bridge_ready"] is True
    assert result["qait_charte_template_bound"] is True
    assert result["mvp_qaic_logo_validated_bound"] is True
    assert result["qaic_execution_allowed"] is False
    assert result["safe_for_review_only"] is True


def test_r21k_payload_contains_no_forbidden_runtime_or_export_text() -> None:
    targets = [
        Path("mvp_qaic_py/cockpit_queue_data_contract_r21k.py"),
        Path("docs/PRODUCT/R21K_COCKPIT_QUEUE_DATA_CONTRACT_NO_RUNTIME.md"),
    ]
    forbidden_phrases = [
        "reflex" + " run",
        "docker" + " run",
        ("--frontend" + "-host"),
        "provider_call_allowed" + "=True",
        "broker_order_sizing_allowed" + "=True",
        "sheet_bq_write_allowed" + "=True",
        "execution_allowed" + "=True",
        "index" + ".html",
        "05" + "_EXPORTS",
    ]

    for target in targets:
        text = target.read_text(encoding="utf-8").lower()
        for phrase in forbidden_phrases:
            assert phrase.lower() not in text
