from __future__ import annotations

import json
from pathlib import Path

import pytest

from mvp_qaic_py.p160_real_gem_response_smoke_with_patch_or_release_seal import (
    PATCH_MARKER,
    P160BlockedError,
    build_and_write_export,
    count_unsafe_markers,
    validate_p152_summary,
    validate_p159_summary,
)


def write_json(path: Path, payload: dict[str, object]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2), encoding="utf-8")


def make_repo(tmp_path: Path) -> Path:
    repo = tmp_path
    (repo / "mvp_qaic_py").mkdir()
    (repo / "mvp_qaic_py" / "__init__.py").write_text("", encoding="utf-8")
    (repo / "mvp_qaic_py" / "multimodal_gem_image_prompt_usd_contract.py").write_text(
        f'PROMPT_TEXT = "human review only {PATCH_MARKER}"\n',
        encoding="utf-8",
    )
    write_json(
        repo
        / "05_EXPORTS"
        / "P152_REAL_GEM_RESPONSE_IMPORT_OR_STOP_20260623_142527"
        / "P152_SUMMARY.json",
        {
            "P152_STATUS": "P152_REAL_GEM_RESPONSE_IMPORTED_LOCAL_REVIEW",
            "VALIDATION_STATUS": "VALIDATED_FOR_HUMAN_REVIEW",
            "JSON_PAYLOAD_DETECTED": True,
            "BLOCKER_COUNT": 0,
            "HUMAN_REVIEW_REQUIRED": True,
        },
    )
    write_json(
        repo
        / "05_EXPORTS"
        / "P159_PROMPT_PATCH_RUNTIME_SMOKE_OR_ROLLBACK_GATE_20260623_150735"
        / "P159_SUMMARY.json",
        {
            "STATUS": "OK_P159_R2_PROMPT_PATCH_RUNTIME_SMOKE_GATE_COMMIT_TAG_PUSH_SEALED",
            "P159_STATUS": "P159_PROMPT_PATCH_RUNTIME_SMOKE_OK_REVIEW_ONLY",
            "PATCH_MARKER_FOUND": True,
            "SOURCE_IMPORT_OK": True,
            "RUNTIME_SMOKE_OK": True,
            "UNSAFE_RUNTIME_MARKER_COUNT": 0,
            "BLOCKER_COUNT": 0,
            "ROLLBACK_REQUIRED": False,
        },
    )
    return repo


def test_validate_p152_accepts_real_gem_human_review_summary() -> None:
    blockers = validate_p152_summary(
        {
            "p152_status": "P152_REAL_GEM_RESPONSE_IMPORTED_LOCAL_REVIEW",
            "validation_status": "VALIDATED_FOR_HUMAN_REVIEW",
            "json_payload_detected": True,
            "blocker_count": 0,
            "human_review_required": True,
        }
    )
    assert blockers == []


def test_validate_p152_accepts_global_sealed_status_when_runtime_status_absent() -> None:
    blockers = validate_p152_summary(
        {
            "STATUS": "OK_P152_REAL_GEM_RESPONSE_IMPORT_OR_STOP_COMMIT_TAG_PUSH_SEALED",
            "validation_status": "VALIDATED_FOR_HUMAN_REVIEW",
            "json_payload_detected": True,
            "blocker_count": 0,
            "human_review_required": True,
        }
    )
    assert blockers == []


def test_validate_p152_accepts_complete_real_gem_evidence_when_status_varies() -> None:
    blockers = validate_p152_summary(
        {
            "STATUS": "OK_P152_IMPORT_CHAIN_SEALED",
            "validation_status": "VALIDATED_FOR_HUMAN_REVIEW",
            "json_payload_detected": True,
            "blocker_count": 0,
            "human_review_required": True,
        }
    )
    assert blockers == []


def test_validate_p159_accepts_runtime_smoke_ok_summary() -> None:
    blockers = validate_p159_summary(
        {
            "status": "OK_P159_R2_PROMPT_PATCH_RUNTIME_SMOKE_GATE_COMMIT_TAG_PUSH_SEALED",
            "p159_status": "P159_PROMPT_PATCH_RUNTIME_SMOKE_OK_REVIEW_ONLY",
            "patch_marker_found": True,
            "source_import_ok": True,
            "runtime_smoke_ok": True,
            "unsafe_runtime_marker_count": 0,
            "blocker_count": 0,
            "rollback_required": False,
        }
    )
    assert blockers == []


def test_unsafe_marker_counter_is_targeted() -> None:
    safe_negative_text = "NO_ORDER=true and NO_SIZING=true. Do not place orders."
    unsafe_text = "AUTO_APPLY_GEM_RESPONSE=true"
    assert count_unsafe_markers(safe_negative_text) == 0
    assert count_unsafe_markers(unsafe_text) == 1


def test_build_and_write_export_creates_release_seal_ready(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    repo = make_repo(tmp_path)
    monkeypatch.syspath_prepend(str(repo))
    monkeypatch.chdir(repo)

    summary = build_and_write_export(repo)

    assert summary.P160_STATUS == "P160_REAL_GEM_RESPONSE_SMOKE_WITH_PATCH_OK_RELEASE_SEAL_READY"
    assert summary.P152_REAL_GEM_RESPONSE_OK is True
    assert summary.P159_RUNTIME_SMOKE_OK is True
    assert summary.PATCH_MARKER_FOUND is True
    assert summary.SOURCE_IMPORT_OK is True
    assert summary.REAL_CASE_SMOKE_OK is True
    assert summary.RELEASE_SEAL_READY is True
    assert summary.ROLLBACK_REQUIRED is False
    assert summary.BLOCKER_COUNT == 0
    assert (Path(summary.EXPORT_DIR) / "P160_SUMMARY.json").exists()
    assert (Path(summary.EXPORT_DIR) / "P160_RELEASE_SEAL_DECISION.md").exists()


def test_build_blocks_when_marker_missing(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    repo = make_repo(tmp_path)
    (repo / "mvp_qaic_py" / "multimodal_gem_image_prompt_usd_contract.py").write_text(
        'PROMPT_TEXT = "human review only"\n',
        encoding="utf-8",
    )
    monkeypatch.syspath_prepend(str(repo))
    monkeypatch.chdir(repo)

    with pytest.raises(P160BlockedError, match="PATCH_MARKER_NOT_FOUND"):
        build_and_write_export(repo)


def test_build_blocks_when_p159_requires_rollback(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    repo = make_repo(tmp_path)
    write_json(
        repo
        / "05_EXPORTS"
        / "P159_PROMPT_PATCH_RUNTIME_SMOKE_OR_ROLLBACK_GATE_20260623_150735"
        / "P159_SUMMARY.json",
        {
            "STATUS": "OK_P159_R2_PROMPT_PATCH_RUNTIME_SMOKE_GATE_COMMIT_TAG_PUSH_SEALED",
            "P159_STATUS": "P159_PROMPT_PATCH_RUNTIME_SMOKE_OK_REVIEW_ONLY",
            "PATCH_MARKER_FOUND": True,
            "SOURCE_IMPORT_OK": True,
            "RUNTIME_SMOKE_OK": True,
            "UNSAFE_RUNTIME_MARKER_COUNT": 0,
            "BLOCKER_COUNT": 0,
            "ROLLBACK_REQUIRED": True,
        },
    )
    monkeypatch.syspath_prepend(str(repo))
    monkeypatch.chdir(repo)

    with pytest.raises(P160BlockedError, match="P159_ROLLBACK_REQUIRED"):
        build_and_write_export(repo)
