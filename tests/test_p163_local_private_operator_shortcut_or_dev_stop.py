from __future__ import annotations

import json
from pathlib import Path

import pytest

from mvp_qaic_py.p163_local_private_operator_shortcut_or_dev_stop import (
    NEXT_STEP,
    P163BlockedError,
    build_and_write_export,
    shortcut_markdown,
    validate_p162,
)


def _write_p162_summary(repo_root: Path, **overrides: object) -> Path:
    export_dir = (
        repo_root / "05_EXPORTS" / "P162_LOCAL_PRIVATE_OPERATOR_HANDOFF_OR_DEV_STOP_20260623_154739"
    )
    export_dir.mkdir(parents=True, exist_ok=True)
    payload = {
        "P162_STATUS": "P162_LOCAL_PRIVATE_OPERATOR_HANDOFF_READY_DEV_STOP_RECOMMENDED",
        "PROMPT_SOURCE_ID": "P132_P133_PORTFOLIO_MULTIMODAL_REVIEW",
        "LOCAL_PRIVATE_RELEASE_SEALED": True,
        "OPERATOR_HANDOFF_READY": True,
        "DEV_STOP_RECOMMENDED": True,
        "P160B_REAL_CASE_REVIEW_PACK_REQUIRED": False,
        "PUBLIC_DEPLOY_READY": False,
        "BLOCKER_COUNT": 0,
        "ROLLBACK_REQUIRED": False,
        "NEXT": "MVP_QAIC_LOCAL_PRIVATE_RELEASE_CLOSED_DEV_STOP_OR_P163_OPERATOR_SHORTCUT",
    }
    payload.update(overrides)
    summary_path = export_dir / "P162_SUMMARY.json"
    summary_path.write_text(json.dumps(payload), encoding="utf-8")
    return summary_path


def test_p163_builds_operator_shortcut_and_final_close(tmp_path: Path) -> None:
    _write_p162_summary(tmp_path)
    summary = build_and_write_export(tmp_path)

    assert summary.STATUS == "OK_P163_LOCAL_PRIVATE_OPERATOR_SHORTCUT_OR_DEV_STOP_READY_TO_SEAL"
    assert summary.P163_STATUS == "P163_LOCAL_PRIVATE_OPERATOR_SHORTCUT_READY_DEV_STOP_NEXT"
    assert summary.LOCAL_PRIVATE_RELEASE_SEALED is True
    assert summary.OPERATOR_SHORTCUT_READY is True
    assert summary.OPERATOR_HANDOFF_READY is True
    assert summary.DEV_STOP_RECOMMENDED is True
    assert summary.FINAL_CLOSE_READY is True
    assert summary.PUBLIC_DEPLOY_READY is False
    assert summary.GOOGLE_SHEETS_WRITE is False
    assert summary.PUBLIC_DEPLOY is False
    assert summary.NO_BROKER is True
    assert summary.NO_ORDER is True
    assert summary.NO_SIZING is True
    assert summary.BLOCKER_COUNT == 0
    assert summary.ROLLBACK_REQUIRED is False
    assert summary.NEXT == NEXT_STEP
    assert Path(summary.SHORTCUT_FILE).exists()

    export_dir = Path(summary.EXPORT_DIR)
    assert (export_dir / "P163_SUMMARY.json").exists()
    assert (export_dir / "P163_OPERATOR_SHORTCUT.md").exists()
    assert (export_dir / "P163_LOCAL_PRIVATE_OPERATOR_SHORTCUT.ps1").exists()
    assert (export_dir / "P163_FINAL_CLOSE_DECISION.md").exists()
    assert (export_dir / "P163_OPERATOR_SHORTCUT_REPORT.csv").exists()
    assert (export_dir / "P163_OPERATOR_SHORTCUT_REPORT.json").exists()


def test_p163_blocks_when_p162_not_ready(tmp_path: Path) -> None:
    _write_p162_summary(tmp_path, P162_STATUS="P162_STOP")
    with pytest.raises(P163BlockedError, match="P162_STATUS_NOT_HANDOFF_READY_DEV_STOP"):
        build_and_write_export(tmp_path)


def test_p163_blocks_public_deploy_ready(tmp_path: Path) -> None:
    _write_p162_summary(tmp_path, PUBLIC_DEPLOY_READY=True)
    summary_path = (
        tmp_path
        / "05_EXPORTS"
        / "P162_LOCAL_PRIVATE_OPERATOR_HANDOFF_OR_DEV_STOP_20260623_154739"
        / "P162_SUMMARY.json"
    )
    blockers = validate_p162(json.loads(summary_path.read_text()))
    assert "PUBLIC_DEPLOY_READY_UNEXPECTED" in blockers


def test_p163_blocks_missing_operator_handoff(tmp_path: Path) -> None:
    _write_p162_summary(tmp_path, OPERATOR_HANDOFF_READY=False)
    with pytest.raises(P163BlockedError, match="OPERATOR_HANDOFF_NOT_READY"):
        build_and_write_export(tmp_path)


def test_p163_shortcut_markdown_preserves_safety_flags(tmp_path: Path) -> None:
    _write_p162_summary(tmp_path)
    summary = build_and_write_export(tmp_path)
    text = shortcut_markdown(summary)
    assert "No Google Sheets write" in text
    assert "No public deploy" in text
    assert "No Apps Script execution" in text
    assert "No broker / order / sizing" in text
    assert "P132_P133_PORTFOLIO_MULTIMODAL_REVIEW" in text
    assert "MVP_QAIC_LOCAL_PRIVATE_RELEASE_CLOSED_DEV_STOP" in text


def test_p163_shortcut_script_is_local_private_only(tmp_path: Path) -> None:
    _write_p162_summary(tmp_path)
    summary = build_and_write_export(tmp_path)
    script = Path(summary.SHORTCUT_FILE).read_text(encoding="utf-8")
    assert "NO_SHEETS_WRITE=true" in script
    assert "NO_PUBLIC_DEPLOY=true" in script
    assert "NO_BROKER_ORDER_SIZING=true" in script
    assert "P162_OPERATOR_HANDOFF.md" in script
