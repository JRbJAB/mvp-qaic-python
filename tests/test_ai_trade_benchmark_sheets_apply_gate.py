import sys

import pytest

from qaic_core.benchmark.ai_trade_benchmark_cli import create_run
from qaic_core.benchmark.ai_trade_benchmark_sheets import (
    ALLOWED_TAB,
    FORBIDDEN_TABS,
    TARGET_SPREADSHEET_ID,
    SheetsApplyGateError,
    SheetsContractError,
    assert_google_sheets_apply_allowed,
    build_google_sheets_apply_plan,
    render_apply_gate_audit,
    validate_google_sheets_apply_gate,
)


def _gate(**overrides):
    inputs = {
        "spreadsheet_id": TARGET_SPREADSHEET_ID,
        "allowed_tab_name": ALLOWED_TAB,
        "run_id": "P59D-test",
        "backup_confirmed": True,
        "human_go": True,
        "apply": True,
        "dry_run": False,
        "credentials_ref": "EXTERNAL",
    }
    inputs.update(overrides)
    return validate_google_sheets_apply_gate(**inputs)


def test_dry_run_needs_no_credentials_and_builds_one_tab_payload():
    plan = build_google_sheets_apply_plan(
        spreadsheet_id=TARGET_SPREADSHEET_ID,
        run=create_run("P59D-dry"),
    )
    assert plan["status"] == "DRY_RUN"
    assert plan["allowed_tabs"] == [ALLOWED_TAB]
    assert len(plan["batch_update_payload"]["data"]) == 1
    assert plan["google_live_call"] is False
    assert plan["sheet_write"] is False


@pytest.mark.parametrize("tab", FORBIDDEN_TABS)
def test_forbidden_old_tabs_are_blocked(tab):
    with pytest.raises(SheetsContractError, match="Forbidden"):
        _gate(allowed_tab_name=tab)


def test_multiple_tabs_and_missing_run_id_are_controlled_errors():
    with pytest.raises(SheetsContractError, match="Exactly one"):
        _gate(allowed_tab_name=[ALLOWED_TAB, ALLOWED_TAB])
    with pytest.raises(SheetsApplyGateError, match="run_id"):
        _gate(run_id="")


@pytest.mark.parametrize(
    ("overrides", "reason"),
    [
        ({"human_go": False}, "human_go"),
        ({"backup_confirmed": False}, "backup_confirmed"),
        ({"spreadsheet_id": "wrong"}, "spreadsheet_id"),
        ({"credentials_ref": None}, "credentials"),
    ],
)
def test_apply_gate_blocks_missing_requirements(overrides, reason):
    decision = _gate(**overrides)
    assert decision["status"] == "BLOCKED"
    assert reason in " ".join(decision["blocked_reasons"])


def test_correct_gates_are_ready_but_never_executed():
    decision = _gate()
    assert decision["status"] == "APPLY_READY_BUT_NOT_EXECUTED"
    assert (
        assert_google_sheets_apply_allowed(
            spreadsheet_id=TARGET_SPREADSHEET_ID,
            allowed_tab_name=ALLOWED_TAB,
            run_id="P59D-test",
            backup_confirmed=True,
            human_go=True,
            apply=True,
            dry_run=False,
            credentials_ref="EXTERNAL",
        )
        == decision
    )
    audit = render_apply_gate_audit(decision)
    assert "credentials_ref" not in audit
    assert not any(name.startswith("googleapiclient") for name in sys.modules)
    assert not any(word in repr(decision).lower() for word in ("broker", "order", "sizing"))
