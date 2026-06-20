import pytest

from qaic_core.benchmark.ai_trade_benchmark_cli import create_run
from qaic_core.benchmark.ai_trade_benchmark_sheets import (
    ALLOWED_TAB,
    ALLOWED_TABS,
    FORBIDDEN_TABS,
    SheetsContractError,
    assert_no_forbidden_tabs,
    build_apply_payload,
    build_one_tab_values,
    build_sheets_dry_run_plan,
    validate_allowed_tabs,
)


def test_exactly_one_cockpit_tab_and_forbidden_rejection():
    assert ALLOWED_TABS == [ALLOWED_TAB]
    assert validate_allowed_tabs([ALLOWED_TAB])
    for tab in FORBIDDEN_TABS:
        with pytest.raises(SheetsContractError):
            assert_no_forbidden_tabs([tab])


def test_matrix_and_dry_run_default():
    run = create_run("run-1")
    values = build_one_tab_values(run)
    assert values[0] == [
        "section",
        "key",
        "value",
        "score_or_status",
        "source_url",
        "decision",
        "notes",
    ]
    assert build_sheets_dry_run_plan("sheet", run)["dry_run"] is True


def test_apply_gate(tmp_path):
    run = create_run("run-1")
    backup = tmp_path / "backup.json"
    backup.write_text("{}", encoding="utf-8")
    with pytest.raises(SheetsContractError, match="--apply"):
        build_apply_payload(spreadsheet_id="sheet", run=run, backup_path=backup)
    with pytest.raises(SheetsContractError, match="backup"):
        build_apply_payload(
            spreadsheet_id="sheet", run=run, backup_path="", apply=True, human_go=True
        )
