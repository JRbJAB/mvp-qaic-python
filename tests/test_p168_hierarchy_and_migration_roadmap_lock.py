from __future__ import annotations

import json
from pathlib import Path

from mvp_qaic_py.p168_hierarchy_and_migration_roadmap_lock import (
    EXPORT_PREFIX_P165,
    EXPORT_PREFIX_P166,
    EXPORT_PREFIX_P167,
    build_export,
    build_hierarchy_payload,
    discover_latest_export,
)


def _write_summary(export_dir: Path, name: str, payload: dict[str, object]) -> None:
    export_dir.mkdir(parents=True, exist_ok=True)
    (export_dir / name).write_text(json.dumps(payload), encoding="utf-8")


def test_discover_latest_export_uses_name_order(tmp_path: Path) -> None:
    older = tmp_path / "05_EXPORTS" / f"{EXPORT_PREFIX_P165}20260623_010101"
    newer = tmp_path / "05_EXPORTS" / f"{EXPORT_PREFIX_P165}20260623_020202"
    older.mkdir(parents=True)
    newer.mkdir(parents=True)
    assert discover_latest_export(tmp_path, EXPORT_PREFIX_P165) == newer


def test_build_hierarchy_payload_locks_project_boundaries(tmp_path: Path) -> None:
    p165 = tmp_path / "05_EXPORTS" / f"{EXPORT_PREFIX_P165}20260623_010101"
    p166 = tmp_path / "05_EXPORTS" / f"{EXPORT_PREFIX_P166}20260623_010101"
    p167 = tmp_path / "05_EXPORTS" / f"{EXPORT_PREFIX_P167}20260623_010101"
    _write_summary(
        p165,
        "P165_R3_SUMMARY.json",
        {
            "status": "OK_P165",
            "apps_script_module_count": 22,
            "apps_script_function_count": 2738,
            "prompt_engine_function_count": 2296,
        },
    )
    _write_summary(p166, "P166_SUMMARY.json", {"status": "OK_P166", "source_candidate_count": 4288})
    _write_summary(
        p167,
        "P167_SUMMARY.json",
        {"status": "OK_P167", "review_item_count": 5, "pending_review_count": 5},
    )
    payload = build_hierarchy_payload(tmp_path)
    assert payload["status"] == "P168A_HIERARCHY_AND_MIGRATION_ROADMAP_LOCK_READY_REVIEW_ONLY"
    assert payload["hierarchy_locked"] is True
    assert payload["blocker_count"] == 0
    assert payload["next"] == "P168B_SHEETS_DATA_SNAPSHOT_LAYER_READONLY"
    assert payload["source_milestones"]["apps_script_module_count"] == 22
    assert payload["source_milestones"]["apps_script_function_count"] == 2738
    assert payload["source_milestones"]["source_candidate_count"] == 4288
    assert payload["source_milestones"]["review_item_count"] == 5
    domains = {row["domain"]: row for row in payload["domain_boundaries"]}
    assert "MVP_QAIC_PY" in domains
    assert "QAIC_PY" in domains
    assert "QAIT_PY" in domains
    assert "broker execution" in domains["MVP_QAIC_PY"]["forbidden_scope"]
    assert "Revolut X" in domains["QAIC_PY"]["allowed_scope"]
    assert "Revolut Invest" in domains["QAIT_PY"]["allowed_scope"]


def test_build_hierarchy_payload_blocks_when_source_exports_missing(tmp_path: Path) -> None:
    payload = build_hierarchy_payload(tmp_path)
    assert payload["blocker_count"] == 3
    assert payload["next"] == "STOP_FIX_MISSING_EXPORTS"
    assert "MISSING_P165_SOURCE_ACCESS_EXPORT" in payload["blockers"]
    assert "MISSING_P166_REFERENCE_PROMPT_EXPORT" in payload["blockers"]
    assert "MISSING_P167_HUMAN_REVIEW_GATE_EXPORT" in payload["blockers"]


def test_build_export_writes_review_only_roadmap_files(tmp_path: Path) -> None:
    p165 = tmp_path / "05_EXPORTS" / f"{EXPORT_PREFIX_P165}20260623_010101"
    p166 = tmp_path / "05_EXPORTS" / f"{EXPORT_PREFIX_P166}20260623_010101"
    p167 = tmp_path / "05_EXPORTS" / f"{EXPORT_PREFIX_P167}20260623_010101"
    _write_summary(
        p165,
        "P165_R3_SUMMARY.json",
        {
            "apps_script_module_count": 22,
            "apps_script_function_count": 2738,
            "prompt_engine_function_count": 2296,
        },
    )
    _write_summary(p166, "P166_SUMMARY.json", {"source_candidate_count": 4288})
    _write_summary(p167, "P167_SUMMARY.json", {"review_item_count": 5, "pending_review_count": 5})
    output_dir = tmp_path / "out"
    payload = build_export(tmp_path, output_dir)
    assert payload["blocker_count"] == 0
    assert (output_dir / "P168A_SUMMARY.json").exists()
    assert (output_dir / "P168A_DOMAIN_BOUNDARY_MATRIX.csv").exists()
    assert (output_dir / "P168A_MIGRATION_ROADMAP.csv").exists()
    assert (output_dir / "P168A_NEXT_BATCH_QUEUE.csv").exists()
    assert (output_dir / "P168A_HIERARCHY_AND_MIGRATION_ROADMAP_LOCK.md").exists()
    assert (output_dir / "P168A_GATE_REPORT.md").exists()
    summary = json.loads((output_dir / "P168A_SUMMARY.json").read_text(encoding="utf-8"))
    assert summary["safety_flags"]["google_sheets_write"] is False
    assert summary["safety_flags"]["apps_script_execution"] is False
    assert summary["safety_flags"]["broker"] is False
    assert summary["safety_flags"]["order"] is False
    assert summary["safety_flags"]["sizing"] is False
    assert summary["safety_flags"]["runtime_prompt_modified"] is False
