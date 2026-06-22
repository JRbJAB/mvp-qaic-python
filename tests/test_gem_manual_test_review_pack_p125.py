import csv
import subprocess
import sys

from mvp_qaic_py.gem_manual_test_review_pack import (
    SAFETY_MARKERS,
    ManualTestReviewRequest,
    build_review_contract,
    discover_latest_p124_run_dir,
    write_manual_test_review_pack,
)


def _make_p124_dir(tmp_path, portfolio_text, gem_response_text):
    p124 = tmp_path / "P124_LOCAL_INPUT_HELPER_REAL_GEM_TEST_20260622_000000"
    p124.mkdir()
    (p124 / "portfolio_input.txt").write_text(portfolio_text, encoding="utf-8")
    (p124 / "gem_response.txt").write_text(gem_response_text, encoding="utf-8")
    (p124 / "P124_OPERATOR_COMMANDS.md").write_text(
        "NO_REVOLUTX_REAL_ACCESS_FROM_MVP",
        encoding="utf-8",
    )
    return p124


def test_p125_pending_template_p124_folder_reports_missing_data(tmp_path):
    p124 = _make_p124_dir(
        tmp_path,
        "Portfolio input for MVP QAIC GEM manual test\nPaste or type the portfolio snapshot here.",
        "GEM response paste area\nPaste the GEM response here after running the prompt manually.",
    )

    result = write_manual_test_review_pack(
        ManualTestReviewRequest(output_dir=tmp_path / "out", p124_run_dir=p124)
    )

    assert result["status"] == "PENDING_PORTFOLIO_INPUT"
    assert result["missing_data_count"] == 2
    assert result["blocker_count"] == 0
    assert (tmp_path / "out" / "P125_OPERATOR_REVIEW_DASHBOARD.md").exists()


def test_p125_real_input_without_gem_response_is_pending_gem(tmp_path):
    p124 = _make_p124_dir(
        tmp_path,
        "BTC quantity=0.1 value_eur=6500 source=manual",
        "GEM response paste area\nPaste the GEM response here after running the prompt manually.",
    )

    result = write_manual_test_review_pack(
        ManualTestReviewRequest(output_dir=tmp_path / "out", p124_run_dir=p124)
    )

    assert result["status"] == "PENDING_GEM_RESPONSE"
    assert result["gem_response_missing"] is True


def test_p125_real_input_and_response_is_ready_for_review(tmp_path):
    p124 = _make_p124_dir(
        tmp_path,
        "BTC quantity=0.1 value_eur=6500 source=manual",
        '{"decision_status":"REVIEW_REQUIRED","missing_data":["human_confirmed_asset_symbols"],"blockers":[]}',
    )

    result = write_manual_test_review_pack(
        ManualTestReviewRequest(output_dir=tmp_path / "out", p124_run_dir=p124)
    )

    assert result["status"] == "READY_FOR_OPERATOR_REVIEW"
    assert result["missing_data_count"] == 0
    assert result["blocker_count"] == 0


def test_p125_detects_forbidden_order_language(tmp_path):
    p124 = _make_p124_dir(
        tmp_path,
        "BTC quantity=0.1 value_eur=6500",
        "Please place order automatically.",
    )

    result = write_manual_test_review_pack(
        ManualTestReviewRequest(output_dir=tmp_path / "out", p124_run_dir=p124)
    )

    assert result["status"] == "BLOCKED_REVIEW_REQUIRED"
    assert result["blocker_count"] >= 1


def test_p125_writes_findings_csv(tmp_path):
    p124 = _make_p124_dir(
        tmp_path,
        "Portfolio input for MVP QAIC GEM manual test\nPaste or type the portfolio snapshot here.",
        "GEM response paste area\nPaste the GEM response here after running the prompt manually.",
    )

    write_manual_test_review_pack(
        ManualTestReviewRequest(output_dir=tmp_path / "out", p124_run_dir=p124)
    )

    with (tmp_path / "out" / "P125_MISSING_DATA_AND_BLOCKERS.csv").open(
        encoding="utf-8-sig",
        newline="",
    ) as handle:
        rows = list(csv.DictReader(handle))

    assert rows
    assert rows[0]["kind"] == "missing_data"


def test_p125_discovers_latest_p124_folder(tmp_path):
    old_dir = tmp_path / "P124_LOCAL_INPUT_HELPER_REAL_GEM_TEST_20260622_100000"
    new_dir = tmp_path / "P124_LOCAL_INPUT_HELPER_REAL_GEM_TEST_20260622_110000"
    old_dir.mkdir()
    new_dir.mkdir()

    assert discover_latest_p124_run_dir(tmp_path) in {old_dir, new_dir}


def test_p125_cli_generates_review_pack(tmp_path):
    p124 = _make_p124_dir(
        tmp_path,
        "BTC quantity=0.1 value_eur=6500 source=manual",
        '{"decision_status":"REVIEW_REQUIRED","missing_data":[],"blockers":[]}',
    )

    output_dir = tmp_path / "out"
    completed = subprocess.run(
        [
            sys.executable,
            "-m",
            "mvp_qaic_py.gem_manual_test_review_pack",
            "--output-dir",
            str(output_dir),
            "--p124-run-dir",
            str(p124),
            "--run-id",
            "P125-CLI",
        ],
        check=True,
        text=True,
        capture_output=True,
    )

    assert "READY_FOR_OPERATOR_REVIEW" in completed.stdout
    assert (output_dir / "P125_RUN_MANIFEST.json").exists()


def test_p125_contract_forbids_live_actions():
    contract = build_review_contract()
    forbidden = set(contract["forbidden"])

    assert "auto_apply_gem_response" in forbidden
    assert "apps_script_execution" in forbidden
    assert "sheet_write" in forbidden
    assert "broker_execution" in forbidden
    assert "order_execution" in forbidden
    assert "auto_sizing" in forbidden
    assert "revolutx_real_access_from_mvp" in forbidden


def test_p125_safety_markers_are_explicit():
    required = {
        "LOCAL_ONLY",
        "HUMAN_REVIEW_ONLY",
        "REVIEW_UX_ONLY",
        "NO_INDEX_EDIT",
        "NO_CLASP",
        "NO_APPS_SCRIPT_EXECUTION",
        "NO_SHEET_WRITE",
        "NO_PUBLIC_DEPLOY",
        "NO_BROKER",
        "NO_ORDER",
        "NO_AUTO_SIZING",
        "NO_AUTO_APPLY_GEM_RESPONSE",
        "NO_REVOLUTX_REAL_ACCESS_FROM_MVP",
    }

    assert required.issubset(set(SAFETY_MARKERS))
