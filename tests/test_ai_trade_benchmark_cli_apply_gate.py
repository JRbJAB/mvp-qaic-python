import json

from qaic_core.benchmark.ai_trade_benchmark_cli import main
from qaic_core.benchmark.ai_trade_benchmark_sheets import TARGET_SPREADSHEET_ID


def test_cli_dry_run_builds_offline_payload(capsys):
    assert (
        main(
            [
                "sheets-dry-run",
                "--spreadsheet-id",
                TARGET_SPREADSHEET_ID,
                "--run-id",
                "P59D-cli-dry",
            ]
        )
        == 0
    )
    payload = json.loads(capsys.readouterr().out)
    assert payload["status"] == "DRY_RUN"
    assert payload["google_live_call"] is False


def test_cli_apply_without_apply_is_not_live(capsys):
    assert (
        main(
            [
                "sheets-apply",
                "--spreadsheet-id",
                TARGET_SPREADSHEET_ID,
                "--run-id",
                "P59D-no-apply",
            ]
        )
        == 0
    )
    payload = json.loads(capsys.readouterr().out)
    assert payload["status"] == "DRY_RUN"
    assert payload["sheet_write"] is False


def test_cli_apply_is_ready_but_not_executed(capsys):
    assert (
        main(
            [
                "sheets-apply",
                "--spreadsheet-id",
                TARGET_SPREADSHEET_ID,
                "--run-id",
                "P59D-cli-apply",
                "--apply",
                "--human-go",
                "--backup-confirmed",
                "--credentials-ref",
                "EXTERNAL",
            ]
        )
        == 0
    )
    payload = json.loads(capsys.readouterr().out)
    assert payload["status"] == "APPLY_READY_BUT_NOT_EXECUTED"
    assert payload["google_live_call"] is False
    assert payload["sheet_write"] is False
