from __future__ import annotations

from pathlib import Path

from mvp_qaic_py.p193r_gem_decision_journal_roundtrip_evidence_binding import (
    build_gem_evidence_binding,
    export_gem_evidence_binding,
)


def test_gem_evidence_binding_finds_roundtrip_and_journal(tmp_path: Path) -> None:
    exports = tmp_path / "05_EXPORTS"
    (exports / "P186_REAL_OPERATOR_ROUNDTRIP_SMOKE_20260624").mkdir(parents=True)
    (exports / "P186_REAL_OPERATOR_ROUNDTRIP_SMOKE_20260624" / "P186_SUMMARY.json").write_text(
        "{}",
        encoding="utf-8",
    )
    (exports / "P120_GEM_RESPONSE_DECISION_JOURNAL_BRIDGE_20260622").mkdir()
    (
        exports / "P120_GEM_RESPONSE_DECISION_JOURNAL_BRIDGE_20260622" / "DECISION_JOURNAL.csv"
    ).write_text(
        "run_id,status\nr1,REVIEW\n",
        encoding="utf-8",
    )

    payload = build_gem_evidence_binding(tmp_path)

    assert payload["roundtrip_evidence_count"] >= 1
    assert payload["decision_journal_evidence_count"] >= 1
    assert payload["blocker_count"] == 0
    assert payload["gem_call_executed"] is False
    assert payload["google_sheets_write"] is False
    assert payload["broker"] is False
    assert payload["order"] is False
    assert payload["sizing"] is False


def test_gem_evidence_binding_reports_missing_evidence(tmp_path: Path) -> None:
    payload = build_gem_evidence_binding(tmp_path)

    assert payload["roundtrip_evidence_count"] == 0
    assert payload["decision_journal_evidence_count"] == 0
    assert "NO_ROUNDTRIP_EVIDENCE_FOUND" in payload["blockers"]
    assert "NO_DECISION_JOURNAL_EVIDENCE_FOUND" in payload["blockers"]


def test_export_gem_evidence_binding_writes_files(tmp_path: Path) -> None:
    exports = tmp_path / "05_EXPORTS"
    (exports / "P185_REAL_OPERATOR_CAPTURE_RESPONSE_UI_ROUNDTRIP").mkdir(parents=True)
    (exports / "P185_REAL_OPERATOR_CAPTURE_RESPONSE_UI_ROUNDTRIP" / "P185_REPORT.md").write_text(
        "roundtrip",
        encoding="utf-8",
    )
    (exports / "P153_CORRECTION_LOOP_REAL_CASE").mkdir()
    (exports / "P153_CORRECTION_LOOP_REAL_CASE" / "P153_CORRECTION_ACTIONS.csv").write_text(
        "decision,status\nreview,ok\n",
        encoding="utf-8",
    )

    export_dir = tmp_path / "05_EXPORTS" / "P193R_TEST_EXPORT"
    payload = export_gem_evidence_binding(tmp_path, export_dir=export_dir)

    assert payload["roundtrip_evidence_count"] >= 1
    assert payload["decision_journal_evidence_count"] >= 1
    assert (export_dir / "P193R_GEM_EVIDENCE_BINDING.json").exists()
    assert (export_dir / "P193R_GEM_EVIDENCE_BINDING.csv").exists()
    assert (export_dir / "P193R_GEM_ROUNDTRIP_EVIDENCE.csv").exists()
    assert (export_dir / "P193R_GEM_DECISION_JOURNAL_EVIDENCE.csv").exists()
    assert (export_dir / "P193R_SUMMARY.json").exists()
    assert (export_dir / "P193R_REPORT.md").exists()
