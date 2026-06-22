import subprocess
import sys


from mvp_qaic_py.gem_daily_loop_smoke import (
    DEFAULT_GEM_RESPONSE,
    DEFAULT_PORTFOLIO_TEXT,
    SAFETY_MARKERS,
    DailyGemLoopSmokeRequest,
    build_smoke_contract,
    write_daily_gem_loop_smoke_pack,
)


def test_p121_smoke_runs_p118_p119_p120_and_exports_manifest(tmp_path):
    result = write_daily_gem_loop_smoke_pack(
        DailyGemLoopSmokeRequest(
            output_dir=tmp_path,
            run_id="P121-TEST",
            generated_at_utc="2026-06-22T00:00:00Z",
        )
    )

    assert result["status"] == "PASS"
    assert result["p118"]["status"] == "EXPORTED"
    assert result["p119"]["status"] == "EXPORTED"
    assert result["p119"]["queue_rows"] == 3
    assert result["p120"]["status"] == "EXPORTED"
    assert result["p120"]["journal_status"] == "REVIEW_REQUIRED"
    assert result["human_review_only"] is True
    assert result["no_sheet_write"] is True

    assert (tmp_path / "P121_E2E_SMOKE_MANIFEST.json").exists()
    assert (tmp_path / "P121_E2E_SMOKE_REPORT.md").exists()
    assert (
        tmp_path
        / "P121_STEP_P118_DAILY_SHORTCUT"
        / "P118_RUNTIME_PACK"
        / "P116_GEM_PROMPT_COPY_PASTE.md"
    ).exists()
    assert (tmp_path / "P121_STEP_P119_RESPONSE_CAPTURE_QUEUE" / "P119_REVIEW_QUEUE.csv").exists()
    assert (
        tmp_path / "P121_STEP_P120_DECISION_JOURNAL_BRIDGE" / "P120_DECISION_JOURNAL_ENTRY.csv"
    ).exists()


def test_p121_custom_gem_response_with_blocker_propagates_to_journal(tmp_path):
    result = write_daily_gem_loop_smoke_pack(
        DailyGemLoopSmokeRequest(
            output_dir=tmp_path,
            run_id="P121-BLOCK",
            gem_response={
                "decision_status": "BLOCKED",
                "missing_data": [],
                "blockers": ["FORBIDDEN_ACTION_TERM:place order"],
                "summary": "Blocked.",
            },
        )
    )

    assert result["p119"]["decision_status"] == "BLOCKED"
    assert result["p119"]["blocker_count"] == 1
    assert result["p120"]["journal_status"] == "BLOCKED"
    assert result["p120"]["blocker_count"] == 1


def test_p121_contract_forbids_live_actions():
    contract = build_smoke_contract()
    forbidden = set(contract["forbidden"])

    assert "auto_apply_gem_response" in forbidden
    assert "apps_script_execution" in forbidden
    assert "sheet_write" in forbidden
    assert "clasp_push" in forbidden
    assert "broker_execution" in forbidden
    assert "order_execution" in forbidden
    assert "auto_sizing" in forbidden


def test_p121_cli_generates_e2e_smoke_pack(tmp_path):
    output_dir = tmp_path / "smoke"
    completed = subprocess.run(
        [
            sys.executable,
            "-m",
            "mvp_qaic_py.gem_daily_loop_smoke",
            "--output-dir",
            str(output_dir),
            "--run-id",
            "P121-CLI",
            "--generated-at-utc",
            "2026-06-22T00:00:00Z",
        ],
        check=True,
        text=True,
        capture_output=True,
    )

    assert "PASS" in completed.stdout
    assert (output_dir / "P121_E2E_SMOKE_MANIFEST.json").exists()
    assert (
        output_dir / "P121_STEP_P120_DECISION_JOURNAL_BRIDGE" / "P120_DECISION_JOURNAL_ENTRY.json"
    ).exists()


def test_p121_rejects_two_portfolio_input_sources(tmp_path):
    source = tmp_path / "portfolio.txt"
    source.write_text("BTC", encoding="utf-8")

    completed = subprocess.run(
        [
            sys.executable,
            "-m",
            "mvp_qaic_py.gem_daily_loop_smoke",
            "--output-dir",
            str(tmp_path / "out"),
            "--portfolio-text",
            "BTC",
            "--portfolio-text-file",
            str(source),
        ],
        text=True,
        capture_output=True,
    )

    assert completed.returncode != 0
    assert "Use either --portfolio-text or --portfolio-text-file" in completed.stderr


def test_p121_defaults_and_safety_markers_are_explicit():
    assert "BTC 0.10" in DEFAULT_PORTFOLIO_TEXT
    assert DEFAULT_GEM_RESPONSE["decision_status"] == "REVIEW_REQUIRED"

    required = {
        "MVP_PUBLIC_SCOPE",
        "HUMAN_REVIEW_ONLY",
        "LOCAL_ONLY",
        "E2E_LOCAL_SMOKE_ONLY",
        "PROMPT_TO_GEM_TO_CAPTURE_TO_JOURNAL_LOCAL_LOOP",
        "NO_AUTO_APPLY_GEM_RESPONSE",
        "NO_INDEX_EDIT",
        "NO_CLASP",
        "NO_APPS_SCRIPT_EXECUTION",
        "NO_SHEET_WRITE",
        "NO_PUBLIC_DEPLOY",
        "NO_BROKER",
        "NO_ORDER",
        "NO_AUTO_SIZING",
        "NO_REVOLUTX_REAL_ACCESS_FROM_MVP",
    }

    assert required.issubset(set(SAFETY_MARKERS))
