from __future__ import annotations

from mvp_qaic_py.operator_qaic_review_queue_r21j import (
    build_cockpit_traces,
    build_review_queue_items,
    build_review_queue_payload,
    payload_to_dict,
    render_review_queue_markdown,
    validate_review_queue,
)


def test_r21j_payload_has_all_cockpit_ready_traces() -> None:
    payload = build_review_queue_payload()
    trace_ids = {trace.trace_id for trace in payload.cockpit_traces}

    assert "qaic_bridge_trace" in trace_ids
    assert "ui_tracker_trace" in trace_ids
    assert "tool_registry_cdc_trace" in trace_ids
    assert "cdc_contract_trace" in trace_ids
    assert "brand_config_trace" in trace_ids
    assert "execution_safety_trace" in trace_ids
    assert all(trace.cockpit_visibility for trace in payload.cockpit_traces)
    assert all(trace.required_in_future_cockpit for trace in payload.cockpit_traces)


def test_r21j_brand_config_trace_uses_validated_public_assets() -> None:
    traces = {trace.trace_id: trace for trace in build_cockpit_traces()}
    brand = traces["brand_config_trace"]

    assert brand.status == "VALIDATED_BOUND"
    assert "public/brand/mvp-qaic/logo-mvp-qaic-official-name.png" in brand.source_refs
    assert "public/brand/mvp-qaic/logo-mvp-qaic-icon-only.png" in brand.source_refs
    assert "public/brand/mvp-qaic/charte-graphique.png" in brand.source_refs
    assert "QAIT_CHARTE_TEMPLATE=BOUND" in brand.evidence
    assert "NO_GENERATED_PREVIEW_REPLACES_VALIDATED_LOGO=True" in brand.evidence
    assert "PRESERVE_Q_CANDLESTICKS_SIGNAL_LINE=True" in brand.evidence


def test_r21j_queue_items_are_review_only_and_trace_bound() -> None:
    items = build_review_queue_items()
    payload = build_review_queue_payload()
    trace_ids = {trace.trace_id for trace in payload.cockpit_traces}

    assert len(items) >= 6
    assert all(item.human_review_required for item in items)
    assert all(item.qaic_execution_allowed is False for item in items)
    for item in items:
        assert item.cockpit_trace_ids
        assert set(item.cockpit_trace_ids).issubset(trace_ids)


def test_r21j_safety_flags_block_runtime_and_execution() -> None:
    payload = build_review_queue_payload()
    data = payload_to_dict(payload)
    flags = data["safety_flags"]

    assert flags["no_runtime"] is True
    assert flags["no_docker"] is True
    assert flags["no_reflex_run"] is True
    assert flags["no_provider_call"] is True
    assert flags["no_broker_order_sizing"] is True
    assert flags["no_sheet_bq_write"] is True
    assert flags["no_html_output"] is True
    assert flags["qaic_execution_allowed"] is False
    assert validate_review_queue(payload) == []


def test_r21j_markdown_only_render_contains_required_trace_names() -> None:
    markdown = render_review_queue_markdown()

    assert "R21J Operator QAIC Review Queue" in markdown
    assert "qaic_bridge_trace" in markdown
    assert "ui_tracker_trace" in markdown
    assert "tool_registry_cdc_trace" in markdown
    assert "cdc_contract_trace" in markdown
    assert "brand_config_trace" in markdown
    assert "execution_safety_trace" in markdown
    assert "<html" not in markdown.lower()
