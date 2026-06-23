from __future__ import annotations

import csv
import json
from pathlib import Path

from mvp_qaic_py.p156_prompt_patch_candidate_or_stop_after_human_review import (
    PROMPT_SOURCE_ID,
    build_export,
    load_p155_source,
    p155_safety_gate_ok,
    row_decision_state,
    summarize_workbench,
)


def _write_json(path: Path, payload: dict) -> None:
    path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True), encoding="utf-8"
    )


def _write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def make_repo(tmp_path: Path) -> Path:
    repo = tmp_path / "repo"
    (repo / "mvp_qaic_py").mkdir(parents=True)
    (repo / "05_EXPORTS").mkdir()
    (repo / "pyproject.toml").write_text("[project]\nname='test'\n", encoding="utf-8")
    return repo


def make_p155_export(repo: Path, rows: list[dict[str, str]] | None = None) -> Path:
    source = repo / "05_EXPORTS" / "P155_PROMPT_CORRECTION_WORKBENCH_OR_STOP_20260623_120000"
    source.mkdir()
    rows = (
        rows
        if rows is not None
        else [
            {"action_id": "A1", "human_decision": "PENDING", "summary": "one"},
            {"action_id": "A2", "human_decision": "PENDING", "summary": "two"},
            {"action_id": "A3", "human_decision": "PENDING", "summary": "three"},
            {"action_id": "A4", "human_decision": "PENDING", "summary": "four"},
        ]
    )
    _write_json(
        source / "P155_SUMMARY.json",
        {
            "P155_STATUS": "P155_PROMPT_CORRECTION_WORKBENCH_READY_REVIEW_ONLY",
            "PROMPT_SOURCE_ID": PROMPT_SOURCE_ID,
            "WORKBENCH_ROW_COUNT": len(rows),
            "PENDING_HUMAN_REVIEW_COUNT": len(rows),
            "APPLY_ALLOWED": False,
            "PROMPT_SOURCE_MODIFIED": False,
            "BLOCKER_COUNT": 0,
            "GOOGLE_SHEETS_WRITE": False,
            "PUBLIC_DEPLOY": False,
        },
    )
    _write_csv(source / "P155_WORKBENCH.csv", rows)
    return source


def test_p156_stops_when_p155_rows_are_pending(tmp_path: Path, monkeypatch) -> None:
    repo = make_repo(tmp_path)
    make_p155_export(repo)
    monkeypatch.chdir(repo)

    summary = build_export(repo_root=repo)

    assert summary["p156_status"] == "P156_STOP_WAITING_HUMAN_REVIEW"
    assert summary["workbench_row_count"] == 4
    assert summary["pending_human_review_count"] == 4
    assert summary["patch_candidate_created"] is False
    assert summary["apply_allowed"] is False
    assert summary["prompt_source_modified"] is False
    assert summary["google_sheets_write"] is False
    assert summary["public_deploy"] is False
    assert summary["next"] == "FILL_P155_WORKBENCH_THEN_RETRY_P156"


def test_p156_creates_candidate_only_after_all_rows_reviewed(tmp_path: Path, monkeypatch) -> None:
    repo = make_repo(tmp_path)
    make_p155_export(
        repo,
        rows=[
            {"action_id": "A1", "human_decision": "ACCEPT", "summary": "one"},
            {"action_id": "A2", "human_decision": "REJECT", "summary": "two"},
        ],
    )
    monkeypatch.chdir(repo)

    summary = build_export(repo_root=repo)

    assert summary["p156_status"] == "P156_PROMPT_PATCH_CANDIDATE_READY_REVIEW_ONLY"
    assert summary["pending_human_review_count"] == 0
    assert summary["accepted_for_patch_candidate_count"] == 1
    assert summary["patch_candidate_created"] is True
    assert summary["apply_allowed"] is False
    assert summary["prompt_source_modified"] is False


def test_p155_safety_gate_rejects_source_prompt_modification(tmp_path: Path) -> None:
    repo = make_repo(tmp_path)
    source = make_p155_export(repo)
    payload = json.loads((source / "P155_SUMMARY.json").read_text(encoding="utf-8"))
    payload["PROMPT_SOURCE_MODIFIED"] = True
    _write_json(source / "P155_SUMMARY.json", payload)

    loaded = load_p155_source(source)

    assert p155_safety_gate_ok(loaded.summary) is False


def test_p155_safety_gate_accepts_lowercase_keys(tmp_path: Path) -> None:
    repo = make_repo(tmp_path)
    source = make_p155_export(repo)
    payload = {
        "p155_status": "P155_PROMPT_CORRECTION_WORKBENCH_READY_REVIEW_ONLY",
        "prompt_source_id": PROMPT_SOURCE_ID,
        "apply_allowed": False,
        "prompt_source_modified": False,
        "blocker_count": 0,
        "google_sheets_write": False,
        "public_deploy": False,
    }
    _write_json(source / "P155_SUMMARY.json", payload)

    loaded = load_p155_source(source)

    assert p155_safety_gate_ok(loaded.summary) is True


def test_row_decision_state_values() -> None:
    assert row_decision_state({"human_decision": "ACCEPT"}) == "ACCEPTED_FOR_PATCH_CANDIDATE"
    assert row_decision_state({"human_decision": "REJECT"}) == "REJECTED_OR_DEFERRED"
    assert row_decision_state({"human_decision": ""}) == "PENDING_HUMAN_REVIEW"
    assert row_decision_state({}) == "PENDING_HUMAN_REVIEW"


def test_summarize_workbench_uses_summary_when_no_csv_rows(tmp_path: Path) -> None:
    repo = make_repo(tmp_path)
    source = repo / "05_EXPORTS" / "P155_PROMPT_CORRECTION_WORKBENCH_OR_STOP_20260623_120000"
    source.mkdir()
    _write_json(
        source / "P155_SUMMARY.json",
        {
            "P155_STATUS": "P155_PROMPT_CORRECTION_WORKBENCH_READY_REVIEW_ONLY",
            "PROMPT_SOURCE_ID": PROMPT_SOURCE_ID,
            "WORKBENCH_ROW_COUNT": 4,
            "PENDING_HUMAN_REVIEW_COUNT": 4,
            "APPLY_ALLOWED": False,
            "PROMPT_SOURCE_MODIFIED": False,
            "BLOCKER_COUNT": 0,
            "GOOGLE_SHEETS_WRITE": False,
            "PUBLIC_DEPLOY": False,
        },
    )

    loaded = load_p155_source(source)
    counts = summarize_workbench(loaded)

    assert counts["workbench_row_count"] == 4
    assert counts["pending_human_review_count"] == 4


def test_p156_writes_stop_files(tmp_path: Path, monkeypatch) -> None:
    repo = make_repo(tmp_path)
    make_p155_export(repo)
    monkeypatch.chdir(repo)

    summary = build_export(repo_root=repo)
    output_dir = Path(summary["output_dir"])

    assert (output_dir / "P156_SUMMARY.json").exists()
    assert (output_dir / "P156_PROMPT_PATCH_CANDIDATE_OR_STOP_REPORT.json").exists()
    assert (output_dir / "P156_STOP_WAITING_HUMAN_REVIEW.md").exists()
    assert (output_dir / "P156_WORKBENCH_DECISION_READBACK.csv").exists()
    assert not (output_dir / "P156_PROMPT_PATCH_CANDIDATE.md").exists()
