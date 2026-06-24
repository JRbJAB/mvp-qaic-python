from __future__ import annotations

from pathlib import Path

from mvp_qaic_py.p197_prompt_master_from_historical_audit_and_regression_maxi import (
    build_prompt_master_historical_regression,
    export_prompt_master_historical_regression,
)


def test_prompt_master_detects_active_prompt_candidate(tmp_path: Path) -> None:
    pkg = tmp_path / "mvp_qaic_py"
    pkg.mkdir()
    prompt = pkg / "multimodal_gem_image_prompt_usd_contract.py"
    prompt.write_text(
        "PROMPT = '''Portfolio image capture USD JSON human review no broker no order no sizing invent missing data'''",
        encoding="utf-8",
    )

    payload = build_prompt_master_historical_regression(tmp_path)

    assert payload["candidate_count"] >= 1
    assert payload["selected_master_candidate"]["classification"] == "ACTIVE_RUNTIME_PROMPT"
    assert payload["gem_call_executed"] is False
    assert payload["google_sheets_write"] is False
    assert payload["broker"] is False
    assert payload["order"] is False
    assert payload["sizing"] is False


def test_prompt_master_no_candidates_is_blocked(tmp_path: Path) -> None:
    payload = build_prompt_master_historical_regression(tmp_path)

    assert payload["candidate_count"] == 0
    assert payload["STATUS"].startswith("BLOCKED")
    assert "NO_PROMPT_CANDIDATES_FOUND" in payload["blockers"]


def test_export_prompt_master_writes_expected_files(tmp_path: Path) -> None:
    pkg = tmp_path / "mvp_qaic_py"
    pkg.mkdir()
    (pkg / "prompt_demo.py").write_text(
        "PROMPT = 'gem portfolio image json usd review no broker no order no sizing'",
        encoding="utf-8",
    )
    export_dir = tmp_path / "05_EXPORTS" / "P197_TEST_EXPORT"

    payload = export_prompt_master_historical_regression(tmp_path, export_dir=export_dir)

    assert payload["candidate_count"] >= 1
    assert (export_dir / "P197_PROMPT_MASTER_HISTORICAL_REGRESSION.json").exists()
    assert (export_dir / "P197_PROMPT_MASTER_CANDIDATES.csv").exists()
    assert (export_dir / "P197_PROMPT_REGRESSION_CHECKLIST.csv").exists()
    assert (export_dir / "P197_PROMPT_MASTER_CANDIDATE.md").exists()
    assert (export_dir / "P197_SUMMARY.json").exists()
    assert (export_dir / "P197_REPORT.md").exists()
