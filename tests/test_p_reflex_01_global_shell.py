from pathlib import Path

from mvp_qaic_py.reflex_app import registry
from mvp_qaic_py.reflex_app.app import page_registry_payload


def test_page_registry_contains_all_expected_sections():
    assert registry.required_sections_present()
    assert len(registry.PAGES) >= 16
    routes = registry.list_routes()
    assert "/" in routes
    assert "/cdc-tracker" in routes
    assert "/architecture-web" in routes
    assert "/lexique-knowledge" in routes
    assert "/methods-library" in routes
    assert "/prompt-lab" in routes
    assert "/gem-portfolio" in routes
    assert "/responses-review" in routes
    assert "/qaic-bridge" in routes


def test_architecture_asset_and_cdc_exist():
    assert registry.architecture_asset_exists()
    assert registry.current_cdc_exists()
    assert registry.ARCHITECTURE_ASSET.as_posix().endswith(".png")
    assert registry.CURRENT_CDC.as_posix().endswith(".md")


def test_docs_registry_has_current_cdc_schema_and_pack():
    doc_ids = {doc["doc_id"] for doc in registry.DOCS_REGISTRY}
    assert "webapp_architecture_cdc" in doc_ids
    assert "webapp_architecture_schema_png" in doc_ids
    assert "webapp_architecture_pack" in doc_ids


def test_safety_flags_are_locked():
    assert registry.SAFETY_FLAGS["HUMAN_REVIEW_ONLY"] is True
    assert registry.SAFETY_FLAGS["NO_AUTO_ORDER"] is True
    assert registry.SAFETY_FLAGS["NO_AUTO_SIZING"] is True
    assert registry.SAFETY_FLAGS["NO_BROKER_EXECUTION"] is True
    assert registry.SAFETY_FLAGS["NO_REAL_ORDER"] is True
    assert registry.SAFETY_FLAGS["NO_APPS_SCRIPT_EXECUTION"] is True
    assert registry.SAFETY_FLAGS["NO_CLASP_PUSH"] is True
    assert registry.SAFETY_FLAGS["NO_SHEET_WRITE"] is True
    assert registry.SAFETY_FLAGS["NO_BIGQUERY_WRITE"] is True
    assert registry.SAFETY_FLAGS["NO_PUBLIC_PUBLISH"] is True
    assert registry.SAFETY_FLAGS["NO_QAIT"] is True
    assert registry.no_live_action_policy()


def test_qait_is_out_of_scope_and_qaic_is_read_only_liaison():
    assert registry.QAIT_OUT_OF_SCOPE is True
    assert registry.QAIC_SCOPE == "read_only_private_liaison_future"


def test_app_payload_imports_without_reflex_runtime_requirement():
    payload = page_registry_payload()
    assert payload["route_count"] >= 16
    assert payload["architecture_asset"]
    assert payload["safety_flags"]["NO_QAIT"] is True


def test_no_execution_markers_in_shell_source():
    root = Path("mvp_qaic_py/reflex_app")
    text = "\n".join(path.read_text(encoding="utf-8") for path in root.glob("*.py"))
    forbidden = [
        "place_order(",
        "cancel_order(",
        "auto_sizing",
        "clasp push",
        "SpreadsheetApp",
        "qait_core",
    ]
    for marker in forbidden:
        assert marker not in text
