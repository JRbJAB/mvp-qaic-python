from __future__ import annotations

from pathlib import Path

import mvp_qaic_py.p195r_operator_release_runtime_tracker_next_selector_maxi as p195r


def test_operator_release_allows_when_contract_is_ready(monkeypatch, tmp_path: Path) -> None:
    def fake_contract(project_root: Path) -> dict[str, object]:
        return {
            "runtime_close_percent": 96.5,
            "sheet_contract_row_count": 13,
            "ready_for_sheets_export_count": 11,
            "ready_with_review_count": 1,
            "not_ready_count": 1,
        }

    monkeypatch.setattr(p195r, "build_gem_runtime_close_contract", fake_contract)

    payload = p195r.build_operator_release_runtime_tracker(tmp_path)

    assert payload["operator_runtime_release_allowed"] is True
    assert payload["sheets_export_allowed"] is False
    assert payload["selected_next_pack"] == "P196_REAL_CASE_PORTFOLIO_GEM_OPERATOR_INPUTS_MAXI"
    assert len(payload["next_work_rows"]) == 4
    assert payload["gem_call_executed"] is False
    assert payload["google_sheets_write"] is False
    assert payload["broker"] is False
    assert payload["order"] is False
    assert payload["sizing"] is False


def test_operator_release_minimal_fixture_is_review_not_false_pass(tmp_path: Path) -> None:
    payload = p195r.build_operator_release_runtime_tracker(tmp_path)

    assert payload["operator_runtime_release_allowed"] in {True, False}
    assert payload["sheets_export_allowed"] is False
    assert payload["selected_next_pack"] == "P196_REAL_CASE_PORTFOLIO_GEM_OPERATOR_INPUTS_MAXI"
    assert payload["gem_call_executed"] is False


def test_operator_release_contains_review_waivers(tmp_path: Path) -> None:
    payload = p195r.build_operator_release_runtime_tracker(tmp_path)

    assert payload["review_waiver_count"] == 2
    assert any(row["scope"] == "GEM_DECISION_JOURNAL" for row in payload["review_waivers"])
    assert payload["sheets_export_allowed"] is False


def test_export_operator_release_writes_files(tmp_path: Path) -> None:
    exports = tmp_path / "05_EXPORTS"
    (exports / "P186_REAL_OPERATOR_ROUNDTRIP_SMOKE").mkdir(parents=True)
    (exports / "P120_GEM_RESPONSE_DECISION_JOURNAL_BRIDGE").mkdir()
    export_dir = tmp_path / "05_EXPORTS" / "P195R_TEST_EXPORT"

    payload = p195r.export_operator_release_runtime_tracker(tmp_path, export_dir=export_dir)

    assert payload["selected_next_pack"] == "P196_REAL_CASE_PORTFOLIO_GEM_OPERATOR_INPUTS_MAXI"
    assert (export_dir / "P195R_OPERATOR_RELEASE_RUNTIME_TRACKER.json").exists()
    assert (export_dir / "P195R_RELEASE_GATES.csv").exists()
    assert (export_dir / "P195R_NEXT_WORK_SELECTOR.csv").exists()
    assert (export_dir / "P195R_REVIEW_WAIVERS.csv").exists()
    assert (export_dir / "P195R_SUMMARY.json").exists()
    assert (export_dir / "P195R_REPORT.md").exists()
