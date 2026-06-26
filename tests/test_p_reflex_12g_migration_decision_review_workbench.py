from __future__ import annotations

import json
from pathlib import Path

from mvp_qaic_reflex_ui.migration_decision_workbench import (
    ALLOWED_DECISION_STATUSES,
    build_decision_queue,
    export_decision_queue,
    load_decision_overlay,
    upsert_decision,
)


def test_p12g_workbench_files_and_guard_contract() -> None:
    required = [
        "mvp_qaic_reflex_ui/migration_decision_workbench.py",
        "scripts/APPLY_MIGRATION_DECISION.ps1",
        "scripts/EXPORT_MIGRATION_DECISION_QUEUE.ps1",
        "scripts/REFRESH_MIGRATION_OS.ps1",
        "docs/P_REFLEX_12G_MIGRATION_DECISION_REVIEW_WORKBENCH.md",
    ]
    for rel in required:
        assert Path(rel).exists(), rel
    tracker_text = Path("mvp_qaic_reflex_ui/migration_tracker.py").read_text(encoding="utf-8")
    assert "MIGRATION_DECISION_OVERLAY" not in tracker_text


def test_p12g_refresh_script_merges_decision_overlay_contract() -> None:
    text = Path("scripts/REFRESH_MIGRATION_OS.ps1").read_text(encoding="utf-8-sig")
    assert "MIGRATION_DECISION_OVERLAY.json" in text
    assert "decision_overlay_count" in text
    assert "decision_overlay_applied_count" in text
    assert "python refresh failed" in text
    assert "live_meta" in text


def test_p12g_decision_status_contract() -> None:
    for status in [
        "MIGRATE_NOW",
        "MIGRATE_LATER",
        "PYTHON_REWRITE",
        "KEEP_AS_EXPORT_SOURCE",
        "KEEP_SHEETS_MANUAL",
        "BIGQUERY_FUTURE_CANDIDATE",
        "REVIEW_REQUIRED",
        "RETIRE_NO_VALUE",
    ]:
        assert status in ALLOWED_DECISION_STATUSES


def test_p12g_decision_overlay_roundtrip(tmp_path: Path) -> None:
    docs = tmp_path / "docs"
    docs.mkdir()
    (docs / "MIGRATION_OS_LIVE_PAYLOAD.json").write_text(
        json.dumps(
            {
                "data_hash": "abc",
                "rows": [
                    {"type": "SHEETS_COCKPIT", "source": "Prompt Cockpit", "status": "MIGRATE_NOW"},
                    {
                        "type": "FEATURE_CLUSTER",
                        "source": "QAIC_BRIDGE",
                        "status": "PYTHON_REWRITE",
                    },
                ],
            }
        ),
        encoding="utf-8",
    )
    entry = upsert_decision(
        tmp_path,
        source="Prompt Cockpit",
        decision_status="MIGRATE_LATER",
        target="PYTHON + REFLEX_UI",
        note="test only",
        reviewer="pytest",
    )
    assert entry["decision_status"] == "MIGRATE_LATER"
    overlay = load_decision_overlay(tmp_path)
    assert len(overlay["decisions"]) == 1
    queue = build_decision_queue(tmp_path, limit=10)
    assert queue["overlay_decision_count"] == 1
    assert queue["queue_count"] >= 1
    exported = export_decision_queue(tmp_path, limit=10)
    assert exported["queue_count"] == queue["queue_count"]
    assert (docs / "MIGRATION_DECISION_QUEUE.json").exists()


def test_p12g_live_payload_contract_after_refresh() -> None:
    payload = json.loads(Path("docs/MIGRATION_OS_LIVE_PAYLOAD.json").read_text(encoding="utf-8"))
    assert payload["legacy_row_count"] == 15
    assert payload["row_count"] < 150
    assert payload["function_index_count"] >= 2738
    assert payload["missing_legacy"] == []
    assert payload["missing_essential"] == []
    assert payload["duplicate_sources"] == []
    assert payload["raw_function_rows_visible"] is False
    assert "live_meta" in payload
    assert "decision_overlay_count" in payload
    assert "decision_overlay_applied_count" in payload
