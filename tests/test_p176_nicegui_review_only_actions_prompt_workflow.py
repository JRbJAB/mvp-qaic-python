from __future__ import annotations

import csv
import json
from pathlib import Path

from mvp_qaic_py.p170_nicegui_local_cache_read_binding import REQUIRED_CACHE_SOURCES
from mvp_qaic_py.p176_nicegui_review_only_actions_prompt_workflow import (
    build_review_only_prompt_workflow,
    export_review_only_prompt_workflow,
)


def _write_cache(project_root: Path) -> None:
    cache_dir = project_root / "00_OPERATOR_EXPORTS" / "P168G_LOCAL_CACHE"
    cache_dir.mkdir(parents=True, exist_ok=True)
    for spec in REQUIRED_CACHE_SOURCES:
        with (cache_dir / spec["file_name"]).open("w", encoding="utf-8", newline="") as file_obj:
            writer = csv.writer(file_obj)
            writer.writerow(["id", "status", "value"])
            writer.writerow([spec["source_id"], "READY", "sample"])


def test_build_review_only_prompt_workflow_ready(tmp_path: Path) -> None:
    _write_cache(tmp_path)

    payload = build_review_only_prompt_workflow(
        tmp_path,
        generated_at="2026-06-24T00:00:00+00:00",
    )

    assert payload["STATUS"] == "OK_P176_NICEGUI_REVIEW_ONLY_ACTIONS_PROMPT_WORKFLOW_READY"
    assert payload["workflow_ready"] is True
    assert payload["step_count"] == 6
    assert payload["allowed_step_count"] == 4
    assert payload["blocked_step_count"] == 2
    assert payload["blocker_count"] == 0
    assert payload["auto_apply_gem_response"] is False
    assert payload["source_prompt_modified"] is False
    assert payload["broker"] is False
    assert payload["order"] is False
    assert payload["sizing"] is False


def test_review_only_prompt_workflow_blocks_apply_steps(tmp_path: Path) -> None:
    _write_cache(tmp_path)

    payload = build_review_only_prompt_workflow(tmp_path)
    steps = {row["step_id"]: row for row in payload["steps"]}

    assert steps["copy_prompt_to_gem"]["allowed"] is True
    assert steps["save_gem_response_local_review_file"]["allowed"] is True
    assert steps["preview_review_decision"]["allowed"] is True
    assert steps["apply_review_decision"]["allowed"] is False
    assert steps["apply_prompt_patch"]["allowed"] is False


def test_export_review_only_prompt_workflow_writes_expected_files(tmp_path: Path) -> None:
    _write_cache(tmp_path)
    export_dir = tmp_path / "05_EXPORTS" / "P176_TEST_EXPORT"

    payload = export_review_only_prompt_workflow(tmp_path, export_dir=export_dir)

    assert payload["workflow_ready"] is True
    assert (export_dir / "P176_REVIEW_ONLY_PROMPT_WORKFLOW_MODEL.json").exists()
    assert (export_dir / "P176_SUMMARY.json").exists()
    assert (export_dir / "P176_WORKFLOW_STEPS.csv").exists()
    assert (export_dir / "P176_REVIEW_ONLY_PROMPT_WORKFLOW_REPORT.md").exists()

    summary = json.loads((export_dir / "P176_SUMMARY.json").read_text(encoding="utf-8"))
    assert summary["recommended_next"] == "P177_GEM_PORTFOLIO_PROMPT_WORKFLOW_USABLE_SMOKE"
