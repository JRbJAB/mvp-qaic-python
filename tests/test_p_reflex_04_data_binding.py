from mvp_qaic_py.reflex_app.app import page_registry_payload
from mvp_qaic_py.reflex_app.data_binding import (
    build_local_data_binding_payload,
    docs_registry_sources,
    export_evidence_sources,
)


def test_docs_registry_sources_are_local_and_existing():
    sources = docs_registry_sources()

    assert len(sources) >= 3
    assert all(source.exists for source in sources)
    assert all(not source.path.startswith("http") for source in sources)
    assert {source.kind for source in sources} >= {"markdown", "png", "zip"}


def test_export_evidence_sources_are_local_readonly():
    sources = export_evidence_sources(limit=8)

    assert sources
    assert all(source.kind == "export_dir" for source in sources)
    assert all(source.status == "LOCAL_READONLY" for source in sources)
    assert all(not source.path.startswith("http") for source in sources)


def test_local_data_binding_payload_is_readonly_and_no_live():
    payload = build_local_data_binding_payload()

    assert payload["binding_mode"] == "LOCAL_READONLY"
    assert payload["server_required"] is False
    assert payload["browser_required"] is False
    assert payload["public_deploy_required"] is False
    assert payload["live_action_required"] is False
    assert payload["sheet_write_allowed"] is False
    assert payload["bigquery_write_allowed"] is False
    assert payload["broker_action_allowed"] is False
    assert payload["missing_doc_sources"] == []
    assert payload["docs_source_count"] >= 3
    assert payload["export_source_count"] >= 1


def test_app_payload_includes_local_data_binding():
    payload = page_registry_payload()

    assert "local_data_binding" in payload
    assert payload["local_data_binding"]["binding_mode"] == "LOCAL_READONLY"
    assert payload["local_data_binding"]["live_action_required"] is False
