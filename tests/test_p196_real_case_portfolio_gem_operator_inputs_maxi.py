from __future__ import annotations

from pathlib import Path

from mvp_qaic_py.p196_real_case_portfolio_gem_operator_inputs_maxi import (
    build_real_case_portfolio_gem_inputs,
    ensure_real_case_input_folders,
    export_real_case_portfolio_gem_inputs,
)


def test_real_case_inputs_wait_when_required_files_missing(tmp_path: Path) -> None:
    ensure_real_case_input_folders(tmp_path)

    payload = build_real_case_portfolio_gem_inputs(tmp_path)

    assert payload["input_status"] == "WAITING_OPERATOR_CAPTURE_AND_GEM_RESPONSE"
    assert payload["ready_for_review"] is False
    assert "WAITING_PORTFOLIO_CAPTURE_IMAGE" in payload["blockers"]
    assert "WAITING_REAL_GEM_RESPONSE_PASTE" in payload["blockers"]
    assert payload["gem_call_executed"] is False
    assert payload["google_sheets_write"] is False
    assert payload["broker"] is False
    assert payload["order"] is False
    assert payload["sizing"] is False


def test_real_case_inputs_ready_when_capture_and_response_exist(
    monkeypatch, tmp_path: Path
) -> None:
    import mvp_qaic_py.p196_real_case_portfolio_gem_operator_inputs_maxi as p196

    def fake_release(project_root: Path) -> dict[str, object]:
        return {
            "operator_runtime_release_allowed": True,
            "operator_release_status": "READY_WITH_REVIEW_WAIVERS",
            "runtime_close_percent": 96.5,
            "selected_next_pack": "P196_REAL_CASE_PORTFOLIO_GEM_OPERATOR_INPUTS_MAXI",
        }

    monkeypatch.setattr(p196, "build_operator_release_runtime_tracker", fake_release)

    ensure_real_case_input_folders(tmp_path)
    root = tmp_path / "00_OPERATOR_EXPORTS" / "P196_REAL_CASE_PORTFOLIO_GEM_INPUTS"
    (root / "CAPTURES" / "portfolio.png").write_bytes(b"image")
    (root / "RESPONSES" / "gem_response.txt").write_text("réponse GEM", encoding="utf-8")

    payload = p196.build_real_case_portfolio_gem_inputs(tmp_path)

    assert payload["input_status"] == "READY_FOR_REAL_CASE_REVIEW"
    assert payload["ready_for_review"] is True
    assert payload["capture_count"] == 1
    assert payload["response_count"] == 1
    assert (
        payload["recommended_next"]
        == "P196B_REAL_CASE_PORTFOLIO_GEM_REVIEW_AFTER_OPERATOR_INPUTS_MAXI"
    )


def test_export_real_case_inputs_writes_expected_files(tmp_path: Path) -> None:
    export_dir = tmp_path / "05_EXPORTS" / "P196_TEST_EXPORT"

    payload = export_real_case_portfolio_gem_inputs(
        tmp_path,
        export_dir=export_dir,
        prepare_folders=True,
    )

    assert payload["capture_count"] == 0
    assert (export_dir / "P196_REAL_CASE_PORTFOLIO_GEM_INPUTS.json").exists()
    assert (export_dir / "P196_INPUT_CONTRACT.csv").exists()
    assert (export_dir / "P196_OPERATOR_STEPS.csv").exists()
    assert (export_dir / "P196_SUMMARY.json").exists()
    assert (export_dir / "P196_REPORT.md").exists()
