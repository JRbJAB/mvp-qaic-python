from __future__ import annotations

from pathlib import Path

from mvp_qaic_py.p189h_historical_prompt_quality_audit import (
    audit_historical_prompts,
    export_historical_prompt_quality_audit,
)


def test_audit_historical_prompts_classifies_good_prompt(tmp_path: Path) -> None:
    prompt_dir = tmp_path / "mvp_qaic_py"
    prompt_dir.mkdir()
    (prompt_dir / "good_prompt.md").write_text(
        """
        GEM portfolio prompt.
        image_used must be explicit.
        reference_currency USD.
        status REVIEW_REQUIRED.
        missing_data and blockers required.
        no_order true. no_sizing true. no_auto_apply.
        JSON schema contract.
        """,
        encoding="utf-8",
    )

    payload = audit_historical_prompts(tmp_path)

    assert payload["migration_matrix_ready"] is True
    assert payload["audited_prompt_count"] == 1
    row = payload["rows"][0]
    assert row["has_gem"] is True
    assert row["has_portfolio"] is True
    assert row["has_no_order"] is True
    assert row["has_no_sizing"] is True
    assert row["migration_decision"] in {
        "MERGE_INTO_MASTER",
        "REFERENCE_ONLY",
        "ACTIVE_KEEP",
    }
    assert payload["gem_call_executed"] is False
    assert payload["broker"] is False
    assert payload["order"] is False
    assert payload["sizing"] is False


def test_audit_historical_prompts_rejects_unsafe_prompt(tmp_path: Path) -> None:
    prompt_dir = tmp_path / "mvp_qaic_py"
    prompt_dir.mkdir()
    (prompt_dir / "old_trade_prompt.md").write_text(
        "Prompt: buy BTC, sell ETH, market order, position size, leverage.",
        encoding="utf-8",
    )

    payload = audit_historical_prompts(tmp_path)

    assert payload["audited_prompt_count"] == 1
    row = payload["rows"][0]
    assert row["risk_score"] >= 55
    assert row["migration_decision"] == "REJECT_UNSAFE"


def test_export_historical_prompt_quality_audit_writes_files(tmp_path: Path) -> None:
    prompt_dir = tmp_path / "mvp_qaic_py"
    prompt_dir.mkdir()
    (prompt_dir / "prompt.md").write_text(
        "GEM portfolio image_used REVIEW_REQUIRED USD no_order no_sizing "
        "missing_data blockers schema no_auto_apply",
        encoding="utf-8",
    )
    export_dir = tmp_path / "05_EXPORTS" / "P189H_TEST_EXPORT"

    payload = export_historical_prompt_quality_audit(
        tmp_path,
        export_dir=export_dir,
    )

    assert payload["migration_matrix_ready"] is True
    assert (export_dir / "P189H_HISTORICAL_PROMPT_QUALITY_AUDIT.json").exists()
    assert (export_dir / "P189H_PROMPT_MIGRATION_MATRIX.csv").exists()
    assert (export_dir / "P189H_SUMMARY.json").exists()
    assert (export_dir / "P189H_REPORT.md").exists()
