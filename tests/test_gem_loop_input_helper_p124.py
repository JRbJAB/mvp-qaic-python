import subprocess
import sys

import pytest

from mvp_qaic_py.gem_loop_input_helper import (
    DEFAULT_GEM_RESPONSE_TEMPLATE,
    DEFAULT_PORTFOLIO_TEMPLATE,
    SAFETY_MARKERS,
    InputHelperRequest,
    build_checklist_rows,
    build_input_helper_contract,
    write_input_helper_pack,
)


def test_p124_writes_input_helper_files(tmp_path):
    result = write_input_helper_pack(
        InputHelperRequest(
            output_dir=tmp_path,
            run_id="P124-TEST",
            generated_at_utc="2026-06-22T00:00:00Z",
        )
    )

    assert result["status"] == "INPUT_HELPER_READY"
    assert result["ready_for_real_gem_manual_test"] is True
    assert result["no_sheet_write"] is True
    assert result["no_auto_apply_gem_response"] is True

    assert (tmp_path / "portfolio_input.txt").exists()
    assert (tmp_path / "gem_response.txt").exists()
    assert (tmp_path / "run_notes.md").exists()
    assert (tmp_path / "P124_OPERATOR_COMMANDS.md").exists()
    assert (tmp_path / "P124_REAL_GEM_TEST_CHECKLIST.csv").exists()
    assert (tmp_path / "P124_INPUT_HELPER_CONTRACT.json").exists()
    assert (tmp_path / "P124_INPUT_HELPER_MANIFEST.json").exists()
    assert (tmp_path / "P124_README.md").exists()


def test_p124_commands_include_p118_p119_p120_p121_and_safety(tmp_path):
    write_input_helper_pack(InputHelperRequest(output_dir=tmp_path, run_id="P124-CMDS"))
    commands = (tmp_path / "P124_OPERATOR_COMMANDS.md").read_text(encoding="utf-8")

    assert "gem_prompt_daily_shortcut" in commands
    assert "gem_response_review_queue" in commands
    assert "gem_response_decision_journal_bridge" in commands
    assert "gem_daily_loop_smoke" in commands
    assert "NO_REVOLUTX_REAL_ACCESS_FROM_MVP" in commands


def test_p124_custom_portfolio_text_is_written(tmp_path):
    write_input_helper_pack(
        InputHelperRequest(
            output_dir=tmp_path,
            run_id="P124-CUSTOM",
            portfolio_text="BTC custom portfolio text",
        )
    )

    portfolio = (tmp_path / "portfolio_input.txt").read_text(encoding="utf-8")
    assert "BTC custom portfolio text" in portfolio


def test_p124_portfolio_text_file_is_supported(tmp_path):
    source = tmp_path / "source_portfolio.txt"
    source.write_text("ETH source portfolio text", encoding="utf-8")

    write_input_helper_pack(
        InputHelperRequest(
            output_dir=tmp_path / "out",
            run_id="P124-FILE",
            portfolio_text_file=source,
        )
    )

    portfolio = (tmp_path / "out" / "portfolio_input.txt").read_text(encoding="utf-8")
    assert "ETH source portfolio text" in portfolio


def test_p124_rejects_two_portfolio_sources(tmp_path):
    source = tmp_path / "source.txt"
    source.write_text("BTC", encoding="utf-8")

    with pytest.raises(ValueError, match="Use either portfolio_text or portfolio_text_file"):
        write_input_helper_pack(
            InputHelperRequest(
                output_dir=tmp_path / "out",
                portfolio_text="BTC",
                portfolio_text_file=source,
            )
        )


def test_p124_contract_forbids_live_actions():
    contract = build_input_helper_contract()
    forbidden = set(contract["forbidden"])

    assert "auto_apply_gem_response" in forbidden
    assert "apps_script_execution" in forbidden
    assert "sheet_write" in forbidden
    assert "clasp_push" in forbidden
    assert "broker_execution" in forbidden
    assert "order_execution" in forbidden
    assert "auto_sizing" in forbidden
    assert "revolutx_real_access_from_mvp" in forbidden


def test_p124_cli_generates_helper_pack(tmp_path):
    output_dir = tmp_path / "helper"
    completed = subprocess.run(
        [
            sys.executable,
            "-m",
            "mvp_qaic_py.gem_loop_input_helper",
            "--output-dir",
            str(output_dir),
            "--run-id",
            "P124-CLI",
            "--generated-at-utc",
            "2026-06-22T00:00:00Z",
        ],
        check=True,
        text=True,
        capture_output=True,
    )

    assert "INPUT_HELPER_READY" in completed.stdout
    assert (output_dir / "P124_INPUT_HELPER_MANIFEST.json").exists()


def test_p124_checklist_and_templates_are_explicit():
    rows = build_checklist_rows()
    text = str(rows)

    assert "NO_SHEET_WRITE" in text
    assert "NO_BROKER_NO_ORDER_NO_SIZING" in text
    assert "HUMAN_REVIEW_ONLY" in DEFAULT_PORTFOLIO_TEMPLATE
    assert "NO_AUTO_APPLY_GEM_RESPONSE" in DEFAULT_GEM_RESPONSE_TEMPLATE


def test_p124_safety_markers_are_explicit():
    required = {
        "LOCAL_ONLY",
        "HUMAN_REVIEW_ONLY",
        "REAL_GEM_MANUAL_TEST_PREP_ONLY",
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
