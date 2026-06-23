from pathlib import Path
import json

import pytest

from mvp_qaic_py.p161_release_seal_or_p160b_real_case_review_pack import (
    P160_READY_STATUS,
    P161_READY_STATUS,
    build_and_write_export,
    validate_p160_release_ready,
)


def _write_p160_summary(repo_root: Path, overrides: dict | None = None) -> Path:
    export_dir = (
        repo_root
        / "05_EXPORTS"
        / "P160_REAL_GEM_RESPONSE_SMOKE_WITH_PATCH_OR_RELEASE_SEAL_20260623_153748"
    )
    export_dir.mkdir(parents=True, exist_ok=True)
    payload = {
        "STATUS": "OK_P160_R3_REAL_GEM_RESPONSE_SMOKE_WITH_PATCH_RELEASE_SEAL_COMMIT_TAG_PUSH_SEALED",
        "P160_STATUS": P160_READY_STATUS,
        "PROMPT_SOURCE_ID": "P132_P133_PORTFOLIO_MULTIMODAL_REVIEW",
        "P152_REAL_GEM_RESPONSE_OK": True,
        "P159_RUNTIME_SMOKE_OK": True,
        "PATCH_MARKER_FOUND": True,
        "SOURCE_IMPORT_OK": True,
        "REAL_CASE_SMOKE_OK": True,
        "RELEASE_SEAL_READY": True,
        "UNSAFE_RUNTIME_MARKER_COUNT": 0,
        "BLOCKER_COUNT": 0,
        "ROLLBACK_REQUIRED": False,
        "NEXT": "P161_RELEASE_SEAL_OR_P160B_REAL_CASE_REVIEW_PACK",
    }
    if overrides:
        payload.update(overrides)
    path = export_dir / "P160_SUMMARY.json"
    path.write_text(json.dumps(payload), encoding="utf-8")
    return path


def _make_repo(tmp_path: Path) -> Path:
    (tmp_path / "mvp_qaic_py").mkdir()
    (tmp_path / "pyproject.toml").write_text("[project]\nname='x'\n", encoding="utf-8")
    return tmp_path


def test_p161_validates_ready_p160_summary():
    blockers = validate_p160_release_ready(
        {
            "P160_STATUS": P160_READY_STATUS,
            "PROMPT_SOURCE_ID": "P132_P133_PORTFOLIO_MULTIMODAL_REVIEW",
            "P152_REAL_GEM_RESPONSE_OK": True,
            "P159_RUNTIME_SMOKE_OK": True,
            "PATCH_MARKER_FOUND": True,
            "SOURCE_IMPORT_OK": True,
            "REAL_CASE_SMOKE_OK": True,
            "RELEASE_SEAL_READY": True,
            "UNSAFE_RUNTIME_MARKER_COUNT": 0,
            "BLOCKER_COUNT": 0,
            "ROLLBACK_REQUIRED": False,
        }
    )
    assert blockers == []


def test_p161_blocks_when_p160_has_blocker():
    blockers = validate_p160_release_ready(
        {
            "P160_STATUS": P160_READY_STATUS,
            "PROMPT_SOURCE_ID": "P132_P133_PORTFOLIO_MULTIMODAL_REVIEW",
            "P152_REAL_GEM_RESPONSE_OK": True,
            "P159_RUNTIME_SMOKE_OK": True,
            "PATCH_MARKER_FOUND": True,
            "SOURCE_IMPORT_OK": True,
            "REAL_CASE_SMOKE_OK": True,
            "RELEASE_SEAL_READY": True,
            "UNSAFE_RUNTIME_MARKER_COUNT": 0,
            "BLOCKER_COUNT": 1,
            "ROLLBACK_REQUIRED": False,
        }
    )
    assert "BLOCKER_COUNT_NOT_ZERO" in blockers


def test_p161_writes_release_seal_pack(tmp_path: Path):
    repo = _make_repo(tmp_path)
    _write_p160_summary(repo)

    summary = build_and_write_export(repo)

    assert summary.P161_STATUS == P161_READY_STATUS
    assert summary.BLOCKER_COUNT == 0
    assert summary.ROLLBACK_REQUIRED is False
    assert summary.P160B_REAL_CASE_REVIEW_PACK_REQUIRED is False
    export_dir = Path(summary.EXPORT_DIR)
    assert (export_dir / "P161_SUMMARY.json").exists()
    assert (export_dir / "P161_RELEASE_SEAL_DECISION.md").exists()
    assert (export_dir / "P161_HANDOFF.md").exists()
    payload = json.loads((export_dir / "P161_SUMMARY.json").read_text(encoding="utf-8"))
    assert payload["GOOGLE_SHEETS_WRITE"] is False
    assert payload["PUBLIC_DEPLOY"] is False
    assert payload["NO_BROKER"] is True
    assert payload["NO_ORDER"] is True
    assert payload["NO_SIZING"] is True


def test_p161_accepts_ok_p160_status_without_exact_p160_status(tmp_path: Path):
    repo = _make_repo(tmp_path)
    _write_p160_summary(
        repo,
        {
            "P160_STATUS": "",
            "STATUS": "OK_P160_R3_REAL_GEM_RESPONSE_SMOKE_WITH_PATCH_RELEASE_SEAL_COMMIT_TAG_PUSH_SEALED",
        },
    )

    summary = build_and_write_export(repo)

    assert summary.P161_STATUS == P161_READY_STATUS
    assert summary.RELEASE_DECISION == "LOCAL_PRIVATE_RELEASE_SEALED"


def test_p161_raises_when_review_pack_required(tmp_path: Path):
    repo = _make_repo(tmp_path)
    _write_p160_summary(repo, {"RELEASE_SEAL_READY": False})

    with pytest.raises(RuntimeError, match="P161_RELEASE_SEAL_BLOCKED"):
        build_and_write_export(repo)
