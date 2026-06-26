from __future__ import annotations

import json
from pathlib import Path


def test_p12g0_refresh_guard_files_exist() -> None:
    required = [
        "docs/MIGRATION_DECISION_OVERLAY.json",
        "docs/MIGRATION_OS_LIVE_PAYLOAD.json",
        "docs/MIGRATION_OS_REFRESH_SIGNAL.txt",
        "scripts/REFRESH_MIGRATION_OS.ps1",
        "scripts/WATCH_MIGRATION_OS.ps1",
        "scripts/ASSERT_NO_TRACKER_DIRECT_EDIT.ps1",
    ]
    for rel in required:
        assert Path(rel).exists(), rel


def test_p12g0_refresh_script_imports_from_explicit_repo_root() -> None:
    text = Path("scripts/REFRESH_MIGRATION_OS.ps1").read_text(encoding="utf-8")
    assert "QAIC_REPO_ROOT" in text
    assert "PYTHONPATH" in text
    assert "sys.path.insert(0, str(repo))" in text
    assert "STATUS=OK_MIGRATION_OS_REFRESH" in text
    assert "python refresh failed" in text


def test_p12g0_live_payload_contract() -> None:
    payload = json.loads(Path("docs/MIGRATION_OS_LIVE_PAYLOAD.json").read_text(encoding="utf-8"))
    assert payload["legacy_row_count"] == 15
    assert payload["row_count"] < 150
    assert payload["function_index_count"] >= 2738
    assert payload["missing_legacy"] == []
    assert payload["missing_essential"] == []
    assert payload["duplicate_sources"] == []
    assert payload["raw_function_rows_visible"] is False
    assert "live_meta" in payload
    assert payload["live_meta"]["data_hash"]


def test_p12g0_tracker_guard_script_blocks_direct_edit_policy() -> None:
    text = Path("scripts/ASSERT_NO_TRACKER_DIRECT_EDIT.ps1").read_text(encoding="utf-8")
    assert "mvp_qaic_reflex_ui/migration_tracker.py" in text
    assert "P12G+ must write migration decisions to JSON/overlay or migration_os.py" in text
    assert "STATUS=FAILED_NO_TRACKER_DIRECT_EDIT" in text
