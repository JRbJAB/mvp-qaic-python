from __future__ import annotations

import json
from pathlib import Path

from mvp_qaic_py.p157_prompt_patch_candidate_review_or_apply_gate import (
    P156_READY_STATUS,
    P157_BLOCKED_STATUS,
    P157_READY_STATUS,
    build_and_write_export,
    detect_unsafe_markers,
    review_patch_candidate,
)


def make_repo_with_p156_candidate(
    tmp_path: Path, candidate_text: str | None = None, **summary_overrides: object
) -> Path:
    repo = tmp_path
    source_dir = (
        repo
        / "05_EXPORTS"
        / "P156_PROMPT_PATCH_CANDIDATE_OR_STOP_AFTER_HUMAN_REVIEW_20990101_010101"
    )
    source_dir.mkdir(parents=True)
    summary = {
        "P156_STATUS": P156_READY_STATUS,
        "PROMPT_SOURCE_ID": "P132_P133_PORTFOLIO_MULTIMODAL_REVIEW",
        "PATCH_CANDIDATE_CREATED": True,
        "PENDING_HUMAN_REVIEW_COUNT": 0,
        "ACCEPTED_FOR_PATCH_CANDIDATE_COUNT": 1,
        "APPLY_ALLOWED": False,
        "APPLY_NOW_YES_COUNT": 0,
        "PROMPT_SOURCE_MODIFIED": False,
        "GOOGLE_SHEETS_WRITE": False,
        "PUBLIC_DEPLOY": False,
    }
    summary.update(summary_overrides)
    (source_dir / "P156_SUMMARY.json").write_text(json.dumps(summary), encoding="utf-8")
    (source_dir / "P156_PROMPT_PATCH_CANDIDATE.md").write_text(
        candidate_text
        or """# Patch candidat P132/P133\n\nAméliorer la précision et la structure de la réponse GEM, sans apply automatique.\n\nReview-only. Human review required. apply_allowed=false. No apply.\n""",
        encoding="utf-8",
    )
    return repo


def test_p157_reviews_safe_p156_candidate(tmp_path: Path) -> None:
    repo = make_repo_with_p156_candidate(tmp_path)
    summary = review_patch_candidate(repo)

    assert summary.status == P157_READY_STATUS
    assert summary.patch_candidate_found is True
    assert summary.patch_safe_for_review is True
    assert summary.blocker_count == 0
    assert summary.apply_allowed is False
    assert summary.prompt_source_modified is False
    assert summary.next == "P158_MANUAL_PROMPT_PATCH_APPLY_OR_STOP"


def test_p157_blocks_unsafe_candidate_text(tmp_path: Path) -> None:
    repo = make_repo_with_p156_candidate(
        tmp_path,
        candidate_text="Please buy now and place order. apply_allowed=true",
    )
    summary = review_patch_candidate(repo)

    assert summary.status == P157_BLOCKED_STATUS
    assert summary.patch_safe_for_review is False
    assert "UNSAFE_PATCH_CANDIDATE_MARKERS" in summary.blockers
    assert summary.unsafe_marker_count >= 2


def test_p157_blocks_when_p156_summary_is_not_ready(tmp_path: Path) -> None:
    repo = make_repo_with_p156_candidate(tmp_path, P156_STATUS="P156_STOP_WAITING_HUMAN_REVIEW")
    summary = review_patch_candidate(repo)

    assert summary.status == P157_BLOCKED_STATUS
    assert "P156_STATUS_NOT_READY" in summary.blockers


def test_detect_unsafe_markers_reads_summary_flags() -> None:
    unsafe = detect_unsafe_markers(
        "safe text",
        {
            "APPLY_ALLOWED": True,
            "APPLY_NOW_YES_COUNT": 1,
            "PROMPT_SOURCE_MODIFIED": True,
        },
    )

    assert "summary.APPLY_ALLOWED=true" in unsafe
    assert "summary.APPLY_NOW_YES_COUNT!=0" in unsafe
    assert "summary.PROMPT_SOURCE_MODIFIED=true" in unsafe


def test_p157_writes_review_export_without_source_apply(tmp_path: Path, monkeypatch) -> None:
    repo = make_repo_with_p156_candidate(tmp_path)
    monkeypatch.chdir(repo)
    summary = build_and_write_export(repo)
    output_dir = Path(summary.output_dir)

    assert summary.status == P157_READY_STATUS
    assert (output_dir / "P157_SUMMARY.json").exists()
    assert (output_dir / "P157_REVIEW_GATE_DECISION.md").exists()
    assert (output_dir / "P157_PROMPT_PATCH_CANDIDATE_READBACK.md").exists()
    payload = json.loads((output_dir / "P157_SUMMARY.json").read_text(encoding="utf-8"))
    assert payload["apply_allowed"] is False
    assert payload["prompt_source_modified"] is False
    assert payload["google_sheets_write"] is False
    assert payload["public_deploy"] is False
