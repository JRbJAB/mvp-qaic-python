import json
from pathlib import Path

from mvp_qaic_py.qaic_bridge_contract import (
    CONTRACT_ID,
    REQUIRED_SAFETY_FLAGS,
    REQUIRED_TOP_LEVEL_KEYS,
    build_bridge_contract_payload,
    load_bridge_contract_sample,
    validate_bridge_contract_payload,
)


DOCS = [
    Path("docs/BRIDGE/MVP_QAIC_TO_QAIC_BRIDGE_CONTRACT_R1.md"),
    Path("docs/BRIDGE/MVP_QAIC_TO_QAIC_BRIDGE_STATUS_R1.md"),
]
SAMPLE = Path(
    "data/samples/mvp_qaic_bridge/MVP_QAIC_TO_QAIC_BRIDGE_SAMPLE_R1.json"
)
MODULE = Path("mvp_qaic_py/qaic_bridge_contract.py")


def test_docs_exist_and_contain_contract_id():
    for path in DOCS:
        assert path.exists(), f"Missing bridge doc: {path}"
        assert CONTRACT_ID in path.read_text(encoding="utf-8")


def test_sample_json_exists_and_validates():
    assert SAMPLE.exists()
    payload = load_bridge_contract_sample(SAMPLE)
    assert validate_bridge_contract_payload(payload) == []
    assert payload == json.loads(SAMPLE.read_text(encoding="utf-8"))


def test_builder_returns_valid_payload():
    payload = build_bridge_contract_payload()
    assert validate_bridge_contract_payload(payload) == []


def test_required_top_level_keys_exist():
    payload = build_bridge_contract_payload()
    for key in REQUIRED_TOP_LEVEL_KEYS:
        assert key in payload


def test_safety_flags_are_locked_and_execution_is_false():
    payload = build_bridge_contract_payload()
    safety = payload["safety"]
    for key, expected in REQUIRED_SAFETY_FLAGS.items():
        assert safety[key] is expected
    assert payload["qaic_import"]["execution_allowed"] is False
    assert safety["qaic_execution_allowed"] is False


def test_forbidden_terms_are_not_enabled():
    payload = build_bridge_contract_payload()
    forbidden_actions = payload["safety"]["forbidden_actions"]
    assert "broker action" in forbidden_actions
    assert "order action" in forbidden_actions
    assert "sizing action" in forbidden_actions
    assert "provider live call" in forbidden_actions
    assert "Sheet/BQ write" in forbidden_actions
    assert "Apps Script execution" in forbidden_actions
    assert "runtime launch" in forbidden_actions
    assert "public deploy" in forbidden_actions
    assert payload["safety"]["no_broker_order_sizing"] is True
    assert payload["safety"]["no_provider_call"] is True
    assert payload["safety"]["no_sheet_bq_write"] is True
    assert payload["safety"]["no_runtime"] is True


def test_required_scope_modules_are_present():
    payload = build_bridge_contract_payload()
    scope = payload["safety"]["scope_modules"]
    for module in (
        "P112_GEM_PORTFOLIO_PROMPT_MODULE",
        "P113_PORTFOLIO_INPUT_NORMALIZER_IMAGE_REVIEW",
        "P119_GEM_RESPONSE_CAPTURE_REVIEW_QUEUE",
        "P120_GEM_RESPONSE_DECISION_JOURNAL_BRIDGE",
        "P121_DAILY_GEM_LOOP_E2E_LOCAL_SMOKE",
        "P196_REAL_CASE_PORTFOLIO_GEM_INPUTS",
    ):
        assert module in scope


def test_sample_references_required_sources():
    payload = load_bridge_contract_sample(SAMPLE)
    assert (
        "01_OPERATOR_INPUTS/P196_REAL_CASE_PORTFOLIO_GEM_INPUTS/"
        in payload["portfolio_input"]["reference_path"]
    )
    assert payload["gem_prompt"]["source_module"] == "P112_GEM_PORTFOLIO_PROMPT_MODULE"
    assert (
        payload["gem_response"]["source_module"]
        == "P119_GEM_RESPONSE_CAPTURE_REVIEW_QUEUE"
    )
    assert (
        payload["review_queue"]["source_module"]
        == "P119_GEM_RESPONSE_CAPTURE_REVIEW_QUEUE"
    )
    assert (
        payload["decision_journal"]["source_module"]
        == "P120_GEM_RESPONSE_DECISION_JOURNAL_BRIDGE"
    )
    assert payload["qaic_import"]["import_mode"] == "review_only_import_ready"
    assert payload["qaic_import"]["execution_allowed"] is False


def test_module_source_has_no_forbidden_imports_or_live_call_substrings():
    source = MODULE.read_text(encoding="utf-8").lower()
    forbidden = [
        "requests",
        "httpx",
        "aiohttp",
        "urllib",
        "subprocess",
        "reflex",
        "docker",
        "place_order",
        "cancel_order",
        "googleapiclient",
        "gspread",
        "pandas",
    ]
    for term in forbidden:
        assert term not in source
    assert "no_broker_order_sizing" in source


def test_prior_h8i_guard_test_file_exists():
    assert Path("tests/test_reflex_cli_contract_h8i.py").exists()
