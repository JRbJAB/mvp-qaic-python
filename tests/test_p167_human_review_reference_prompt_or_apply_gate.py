from __future__ import annotations

import csv
import json
from pathlib import Path

from mvp_qaic_py.p167_human_review_reference_prompt_or_apply_gate import (
    build_review_items,
    discover_latest_p166_export,
    run,
    validate_p166_export,
)


def _write_file(path: Path, text: str = "ok") -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def _write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def _seed_p166(tmp_path: Path, suffix: str = "010101") -> Path:
    p166 = (
        tmp_path
        / "05_EXPORTS"
        / f"P166_REFERENCE_PROMPT_REBUILD_FROM_SOURCE_INDEX_20260623_{suffix}"
    )
    _write_file(p166 / "P166_REFERENCE_PROMPT_DRAFT_V1.md")
    _write_file(p166 / "P166_OPERATOR_QUICK_USE_PROMPT.md")
    _write_file(p166 / "P166_JSON_OUTPUT_SCHEMA_DRAFT.md")
    _write_csv(
        p166 / "P166_PROMPT_SOURCE_SELECTION.csv",
        [{"name": "BuildGemPrompt", "score": "150"}],
    )
    _write_file(p166 / "P166_REBUILD_REPORT.md")
    _write_file(
        p166 / "P166_SUMMARY.json",
        json.dumps(
            {
                "runtime_prompt_modified": False,
                "apply_allowed": False,
                "blocker_count": 0,
            }
        ),
    )
    return p166


def test_discover_latest_p166_export_by_deterministic_name(tmp_path: Path) -> None:
    older = (
        tmp_path / "05_EXPORTS" / "P166_REFERENCE_PROMPT_REBUILD_FROM_SOURCE_INDEX_20260623_010101"
    )
    newer = (
        tmp_path / "05_EXPORTS" / "P166_REFERENCE_PROMPT_REBUILD_FROM_SOURCE_INDEX_20260623_020202"
    )
    older.mkdir(parents=True)
    newer.mkdir(parents=True)
    assert discover_latest_p166_export(tmp_path).name.endswith("020202")


def test_validate_p166_export_passes_seed(tmp_path: Path) -> None:
    p166 = _seed_p166(tmp_path)
    assert validate_p166_export(p166) == []


def test_build_review_items_keeps_apply_no(tmp_path: Path) -> None:
    p166 = _seed_p166(tmp_path)
    items = build_review_items(p166)
    assert items
    assert all(item.human_decision == "PENDING" for item in items)
    assert all(item.apply_now == "NO" for item in items)


def test_run_creates_review_gate_outputs(tmp_path: Path) -> None:
    _seed_p166(tmp_path)
    out = tmp_path / "out"
    summary = run(tmp_path, out)
    assert summary["status"] == "P167_REFERENCE_PROMPT_HUMAN_REVIEW_GATE_READY_REVIEW_ONLY"
    assert summary["runtime_prompt_modified"] is False
    assert summary["apply_allowed"] is False
    assert summary["human_review_required"] is True
    assert summary["apply_now_yes_count"] == 0
    assert summary["blocker_count"] == 0
    assert (out / "P167_REFERENCE_PROMPT_REVIEW_WORKBENCH.csv").exists()
    assert (out / "P167_GATE_REPORT.md").exists()
    loaded = json.loads((out / "P167_SUMMARY.json").read_text(encoding="utf-8"))
    assert loaded["next"] == "P168_REFERENCE_PROMPT_MANUAL_APPLY_OR_STOP"
