from mvp_qaic_py.operator_decision_journal_handoff_r21e import (
    HANDOFF_MODE,
    QAIC_IMPORT_MODE,
    SAFETY_FLAGS,
    SCHEMA_ID,
    build_decision_journal_entry,
    build_review_queue_item,
    build_sample_entry,
    render_handoff_markdown,
    validate_decision_journal_entry,
)


def test_r21e_sample_entry_is_review_only_and_valid():
    entry = build_sample_entry()
    assert entry["schema_id"] == SCHEMA_ID
    assert entry["handoff_mode"] == HANDOFF_MODE
    assert entry["qaic_import_mode"] == QAIC_IMPORT_MODE
    assert validate_decision_journal_entry(entry) == []
    for key, expected in SAFETY_FLAGS.items():
        assert entry[key] is expected


def test_r21e_review_queue_blocks_invalid_execution_flags():
    entry = build_decision_journal_entry(
        operator_decision="approve_review",
        qaic_bridge_status="READY_FOR_QAIC_REVIEW_ONLY_HANDOFF",
        created_at_utc="2026-07-01T00:00:00Z",
    )
    entry["qaic_execution_allowed"] = True
    entry["provider_call_used"] = True
    errors = validate_decision_journal_entry(entry)
    assert "invalid_safety_flag:qaic_execution_allowed" in errors
    assert "forbidden_true:provider_call_used" in errors
    queue_item = build_review_queue_item(entry)
    assert queue_item["review_state"] == "blocked"


def test_r21e_markdown_is_plain_handoff_no_html_index_runtime():
    entry = build_sample_entry()
    markdown = render_handoff_markdown(entry)
    lower = markdown.lower()
    assert "r21e operator decision journal handoff" in lower
    assert "ready_for_qaic_review_only_handoff" in lower
    assert "<html" not in lower
    assert "index.html" not in lower
    assert "reflex run" not in lower
    assert "broker" not in entry["source"].lower()