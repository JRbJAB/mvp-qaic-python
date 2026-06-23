from __future__ import annotations

import json
from pathlib import Path

import pytest

from mvp_qaic_py.p162_local_private_operator_handoff_or_dev_stop import (
    NEXT_STEP,
    P162BlockedError,
    build_and_write_export,
    handoff_markdown,
    validate_p161,
)


def _write_p161_summary(repo_root: Path, **overrides: object) -> Path:
    export_dir = (
        repo_root
        / "05_EXPORTS"
        / "P161_RELEASE_SEAL_OR_P160B_REAL_CASE_REVIEW_PACK_20260623_154249"
    )
    export_dir.mkdir(parents=True, exist_ok=True)
    payload = {
        "P161_STATUS": "P161_LOCAL_PRIVATE_RELEASE_SEAL_READY",
        "PROMPT_SOURCE_ID": "P132_P133_PORTFOLIO_MULTIMODAL_REVIEW",
        "P160_RELEASE_SEAL_READY": True,
        "RELEASE_DECISION": "LOCAL_PRIVATE_RELEASE_SEALED",
        "P160B_REAL_CASE_REVIEW_PACK_REQUIRED": False,
        "BLOCKER_COUNT": 0,
        "ROLLBACK_REQUIRED": False,
    }
    payload.update(overrides)
    summary_path = export_dir / "P161_SUMMARY.json"
    summary_path.write_text(json.dumps(payload), encoding="utf-8")
    return summary_path


def test_p162_builds_operator_handoff_and_dev_stop(tmp_path: Path) -> None:
    _write_p161_summary(tmp_path)
    summary = build_and_write_export(tmp_path)

    assert summary.STATUS == "OK_P162_LOCAL_PRIVATE_OPERATOR_HANDOFF_OR_DEV_STOP_READY_TO_SEAL"
    assert summary.P162_STATUS == "P162_LOCAL_PRIVATE_OPERATOR_HANDOFF_READY_DEV_STOP_RECOMMENDED"
    assert summary.LOCAL_PRIVATE_RELEASE_SEALED is True
    assert summary.OPERATOR_HANDOFF_READY is True
    assert summary.DEV_STOP_RECOMMENDED is True
    assert summary.P160B_REAL_CASE_REVIEW_PACK_REQUIRED is False
    assert summary.BLOCKER_COUNT == 0
    assert summary.NEXT == NEXT_STEP

    export_dir = Path(summary.EXPORT_DIR)
    assert (export_dir / "P162_SUMMARY.json").exists()
    assert (export_dir / "P162_OPERATOR_HANDOFF.md").exists()
    assert (export_dir / "P162_DEV_STOP_DECISION.md").exists()
    assert (export_dir / "P162_OPERATOR_HANDOFF_REPORT.csv").exists()


def test_p162_blocks_if_p161_not_sealed(tmp_path: Path) -> None:
    _write_p161_summary(tmp_path, P161_STATUS="REVIEW")
    with pytest.raises(P162BlockedError, match="P161_STATUS_NOT_RELEASE_SEAL_READY"):
        build_and_write_export(tmp_path)


def test_p162_blocks_if_review_pack_required(tmp_path: Path) -> None:
    _write_p161_summary(tmp_path, P160B_REAL_CASE_REVIEW_PACK_REQUIRED=True)
    blockers = validate_p161(
        json.loads(
            (
                tmp_path
                / "05_EXPORTS"
                / "P161_RELEASE_SEAL_OR_P160B_REAL_CASE_REVIEW_PACK_20260623_154249"
                / "P161_SUMMARY.json"
            ).read_text()
        )
    )
    assert "P160B_REVIEW_PACK_REQUIRED" in blockers


def test_p162_blocks_on_prompt_source_mismatch(tmp_path: Path) -> None:
    _write_p161_summary(tmp_path, PROMPT_SOURCE_ID="OTHER_PROMPT")
    with pytest.raises(P162BlockedError, match="PROMPT_SOURCE_ID_MISMATCH"):
        build_and_write_export(tmp_path)


def test_p162_handoff_markdown_contains_safety_flags(tmp_path: Path) -> None:
    _write_p161_summary(tmp_path)
    summary = build_and_write_export(tmp_path)
    text = handoff_markdown(summary)
    assert "No Google Sheets write" in text
    assert "No public deploy" in text
    assert "No broker/order/sizing" in text
    assert "P132_P133_PORTFOLIO_MULTIMODAL_REVIEW" in text
