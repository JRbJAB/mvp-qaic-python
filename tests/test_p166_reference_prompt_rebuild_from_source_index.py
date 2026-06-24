from __future__ import annotations

import csv
import json
from pathlib import Path

from mvp_qaic_py.p166_reference_prompt_rebuild_from_source_index import (
    build_candidates,
    discover_latest_p165_export,
    run,
    score_row,
)


def _write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def test_score_row_prioritizes_prompt_gem_portfolio_json() -> None:
    score, matched = score_row(
        {
            "function_name": "BuildGemPortfolioPrompt",
            "description": "GEM portfolio image JSON human review",
        },
        "PROMPT_ENGINE_OR_PROMPT_SOURCE",
    )
    assert score >= 150
    assert "gem" in matched
    assert "portfolio" in matched


def test_build_candidates_from_p165_export(tmp_path: Path) -> None:
    p165 = (
        tmp_path
        / "05_EXPORTS"
        / "P165_R3_INITIAL_SHEET_APPS_SCRIPT_FUNCTIONAL_LAYER_20260623_010101"
    )
    _write_csv(
        p165 / "P165_R3_PROMPT_ENGINE_RECOVERY.csv",
        [
            {
                "function_name": "BuildGemPortfolioPrompt",
                "module_name": "PROMPT_ENGINE",
                "description": "demande globale prompt GEM portfolio image JSON human review no order",
            }
        ],
    )
    rows = build_candidates(p165)
    assert rows
    assert rows[0].name == "BuildGemPortfolioPrompt"
    assert rows[0].source_kind == "PROMPT_ENGINE_OR_PROMPT_SOURCE"


def test_discover_latest_p165_export(tmp_path: Path) -> None:
    older = (
        tmp_path
        / "05_EXPORTS"
        / "P165_R3_INITIAL_SHEET_APPS_SCRIPT_FUNCTIONAL_LAYER_20260623_010101"
    )
    newer = (
        tmp_path
        / "05_EXPORTS"
        / "P165_R3_INITIAL_SHEET_APPS_SCRIPT_FUNCTIONAL_LAYER_20260623_020202"
    )
    older.mkdir(parents=True)
    newer.mkdir(parents=True)
    assert discover_latest_p165_export(tmp_path).name.endswith("020202")


def test_run_creates_review_only_outputs(tmp_path: Path) -> None:
    p165 = (
        tmp_path
        / "05_EXPORTS"
        / "P165_R3_INITIAL_SHEET_APPS_SCRIPT_FUNCTIONAL_LAYER_20260623_010101"
    )
    _write_csv(
        p165 / "P165_R3_PROMPT_ENGINE_RECOVERY.csv",
        [
            {
                "function_name": "BuildGemPortfolioPrompt",
                "module_name": "PROMPT_ENGINE",
                "description": "prompt GEM portfolio capture image JSON review_required no broker no sizing",
            }
        ],
    )
    out = tmp_path / "out"
    summary = run(tmp_path, out)
    assert summary["status"] == "P166_REFERENCE_PROMPT_REBUILD_READY_REVIEW_ONLY"
    assert summary["runtime_prompt_modified"] is False
    assert summary["apply_allowed"] is False
    assert summary["blocker_count"] == 0
    assert (out / "P166_REFERENCE_PROMPT_DRAFT_V1.md").exists()
    assert (out / "P166_OPERATOR_QUICK_USE_PROMPT.md").exists()
    loaded = json.loads((out / "P166_SUMMARY.json").read_text(encoding="utf-8"))
    assert loaded["reference_prompt_draft_created"] is True
