import json
import subprocess
import sys

from mvp_qaic_py.gem_loop_operator_handoff import (
    SAFETY_MARKERS,
    OperatorHandoffRequest,
    build_handoff_contract,
    build_ready_checklist_rows,
    discover_latest_smoke_dir,
    write_operator_handoff_pack,
)


def test_p122_writes_operator_handoff_pack(tmp_path):
    result = write_operator_handoff_pack(
        OperatorHandoffRequest(
            output_dir=tmp_path,
            generated_at_utc="2026-06-22T00:00:00Z",
            notes="unit test",
        )
    )

    assert result["status"] == "HANDOFF_READY"
    assert result["stop_after_handoff"] is True
    assert result["ready_check_count"] >= 6

    assert (tmp_path / "P122_OPERATOR_HANDOFF_CONTRACT.json").exists()
    assert (tmp_path / "P122_OPERATOR_HANDOFF.md").exists()
    assert (tmp_path / "P122_DAILY_OPERATOR_COMMANDS.md").exists()
    assert (tmp_path / "P122_DAILY_GEM_LOOP_RUNBOOK.md").exists()
    assert (tmp_path / "P122_READY_CHECKLIST.csv").exists()
    assert (tmp_path / "P122_HANDOFF_MANIFEST.json").exists()
    assert (tmp_path / "P122_STOP_REPORT.md").exists()

    handoff = (tmp_path / "P122_OPERATOR_HANDOFF.md").read_text(encoding="utf-8")
    assert "NO_SHEET_WRITE" in handoff
    assert "NO_BROKER" in handoff


def test_p122_discovers_latest_p121_smoke_dir(tmp_path):
    old_dir = tmp_path / "P121_DAILY_GEM_LOOP_E2E_LOCAL_SMOKE_20260622_100000"
    new_dir = tmp_path / "P121_DAILY_GEM_LOOP_E2E_LOCAL_SMOKE_20260622_110000"
    old_dir.mkdir()
    new_dir.mkdir()

    assert discover_latest_smoke_dir(tmp_path) in {old_dir, new_dir}


def test_p122_reads_latest_smoke_manifest_when_present(tmp_path):
    smoke_dir = tmp_path / "P121_DAILY_GEM_LOOP_E2E_LOCAL_SMOKE_20260622_120000"
    smoke_dir.mkdir()
    (smoke_dir / "P121_E2E_SMOKE_MANIFEST.json").write_text(
        json.dumps({"status": "PASS"}),
        encoding="utf-8",
    )

    result = write_operator_handoff_pack(
        OperatorHandoffRequest(
            output_dir=tmp_path / "handoff",
            latest_smoke_dir=smoke_dir,
        )
    )

    assert result["latest_smoke_status"] == "PASS"
    assert result["latest_smoke_chain_verified"] is True


def test_p122_contract_forbids_live_actions():
    contract = build_handoff_contract()
    forbidden = set(contract["forbidden"])

    assert "auto_apply_gem_response" in forbidden
    assert "apps_script_execution" in forbidden
    assert "sheet_write" in forbidden
    assert "clasp_push" in forbidden
    assert "broker_execution" in forbidden
    assert "order_execution" in forbidden
    assert "auto_sizing" in forbidden


def test_p122_checklist_contains_stop_and_human_review():
    rows = build_ready_checklist_rows()
    text = json.dumps(rows, ensure_ascii=False)

    assert "HUMAN_REVIEW_ONLY" in text
    assert "STOP_AFTER_HANDOFF" in text
    assert "NO_SHEET_WRITE" in text


def test_p122_cli_generates_handoff_pack(tmp_path):
    output_dir = tmp_path / "handoff"
    completed = subprocess.run(
        [
            sys.executable,
            "-m",
            "mvp_qaic_py.gem_loop_operator_handoff",
            "--output-dir",
            str(output_dir),
            "--generated-at-utc",
            "2026-06-22T00:00:00Z",
        ],
        check=True,
        text=True,
        capture_output=True,
    )

    assert "HANDOFF_READY" in completed.stdout
    assert (output_dir / "P122_HANDOFF_MANIFEST.json").exists()


def test_p122_safety_markers_are_explicit():
    required = {
        "MVP_PUBLIC_SCOPE",
        "HUMAN_REVIEW_ONLY",
        "LOCAL_ONLY",
        "OPERATOR_HANDOFF_ONLY",
        "STOP_AFTER_HANDOFF",
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
