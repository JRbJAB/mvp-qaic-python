from __future__ import annotations

import csv
import json
from pathlib import Path

from mvp_qaic_py.p170_nicegui_local_cache_read_binding import REQUIRED_CACHE_SOURCES
from mvp_qaic_py.p177_gem_portfolio_prompt_workflow_usable_smoke import (
    build_gem_portfolio_prompt_smoke,
    export_gem_portfolio_prompt_smoke,
)


def _write_cache(project_root: Path) -> None:
    cache_dir = project_root / "00_OPERATOR_EXPORTS" / "P168G_LOCAL_CACHE"
    cache_dir.mkdir(parents=True, exist_ok=True)
    for spec in REQUIRED_CACHE_SOURCES:
        with (cache_dir / spec["file_name"]).open("w", encoding="utf-8", newline="") as file_obj:
            writer = csv.writer(file_obj)
            writer.writerow(["id", "status", "value"])
            writer.writerow([spec["source_id"], "READY", "sample"])


def test_build_gem_portfolio_prompt_smoke_ready(tmp_path: Path) -> None:
    _write_cache(tmp_path)

    payload = build_gem_portfolio_prompt_smoke(
        tmp_path,
        generated_at="2026-06-24T00:00:00+00:00",
    )

    assert payload["STATUS"] == "OK_P177_GEM_PORTFOLIO_PROMPT_WORKFLOW_USABLE_SMOKE_READY"
    assert payload["smoke_ready"] is True
    assert payload["check_count"] == 6
    assert payload["pass_count"] == 6
    assert payload["fail_count"] == 0
    assert payload["blocker_count"] == 0
    assert payload["gem_call_executed"] is False
    assert payload["auto_apply_gem_response"] is False
    assert payload["source_prompt_modified"] is False
    assert payload["broker"] is False
    assert payload["order"] is False
    assert payload["sizing"] is False


def test_gem_portfolio_prompt_smoke_keeps_apply_blocked(tmp_path: Path) -> None:
    _write_cache(tmp_path)

    payload = build_gem_portfolio_prompt_smoke(tmp_path)

    assert payload["required_guards"]["no_order"] is True
    assert payload["required_guards"]["no_sizing"] is True
    assert payload["required_guards"]["no_broker"] is True
    assert payload["required_guards"]["no_auto_apply"] is True
    assert payload["required_guards"]["review_required_if_missing_data"] is True


def test_export_gem_portfolio_prompt_smoke_writes_expected_files(tmp_path: Path) -> None:
    _write_cache(tmp_path)
    export_dir = tmp_path / "05_EXPORTS" / "P177_TEST_EXPORT"

    payload = export_gem_portfolio_prompt_smoke(tmp_path, export_dir=export_dir)

    assert payload["smoke_ready"] is True
    assert (export_dir / "P177_GEM_PORTFOLIO_PROMPT_SMOKE_MODEL.json").exists()
    assert (export_dir / "P177_SUMMARY.json").exists()
    assert (export_dir / "P177_OPERATOR_PROMPT_SMOKE_TEXT.md").exists()
    assert (export_dir / "P177_GEM_PORTFOLIO_PROMPT_SMOKE_REPORT.md").exists()

    summary = json.loads((export_dir / "P177_SUMMARY.json").read_text(encoding="utf-8"))
    assert summary["recommended_next"] == "P178_OPERATOR_SHORTCUT_AND_PRIVATE_COCKPIT_HANDOFF"
