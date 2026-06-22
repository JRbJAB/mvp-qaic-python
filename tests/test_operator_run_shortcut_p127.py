import csv
import json
import subprocess
import sys

from mvp_qaic_py.operator_run_shortcut import (
    OUTPUT_FILES,
    SAFETY_MARKERS,
    OperatorRunShortcutRequest,
    build_shortcut_contract,
    write_operator_run_shortcut_pack,
)


def test_p127_writes_expected_files(tmp_path):
    result = write_operator_run_shortcut_pack(
        OperatorRunShortcutRequest(output_dir=tmp_path, run_id="P127-TEST")
    )
    assert result["status"] == "OPERATOR_RUN_SHORTCUT_READY"
    for file_name in OUTPUT_FILES:
        assert (tmp_path / file_name).exists()


def test_p127_shortcut_contains_p124_p125_p126_commands(tmp_path):
    write_operator_run_shortcut_pack(OperatorRunShortcutRequest(output_dir=tmp_path))
    script = (tmp_path / "P127_OPERATOR_RUN_SHORTCUT.ps1").read_text(encoding="utf-8")
    assert "gem_loop_input_helper" in script
    assert "gem_manual_test_review_pack" in script
    assert "daily_run_registry" in script
    assert "NO_REVOLUTX_REAL_ACCESS_FROM_MVP" in script


def test_p127_guide_documents_manual_stop_points(tmp_path):
    write_operator_run_shortcut_pack(OperatorRunShortcutRequest(output_dir=tmp_path))
    guide = (tmp_path / "P127_ONE_COMMAND_OPERATOR_GUIDE.md").read_text(encoding="utf-8")
    assert "Fill `portfolio_input.txt` manually" in guide
    assert "Paste the GEM answer" in guide
    assert "NO_AUTO_APPLY_GEM_RESPONSE" in guide


def test_p127_contract_forbids_live_actions():
    contract = build_shortcut_contract()
    forbidden_text = "\n".join(contract["does_not"])
    assert "write Google Sheets" in forbidden_text
    assert "push clasp" in forbidden_text
    assert "execute broker operation" in forbidden_text
    assert "place order" in forbidden_text
    assert "auto-size position" in forbidden_text
    assert "access Revolut X real account from MVP" in forbidden_text


def test_p127_manifest_has_safety_markers(tmp_path):
    write_operator_run_shortcut_pack(OperatorRunShortcutRequest(output_dir=tmp_path))
    manifest = json.loads((tmp_path / "P127_SHORTCUT_MANIFEST.json").read_text(encoding="utf-8"))
    assert manifest["shortcut_ready"] is True
    assert manifest["no_sheet_write"] is True
    assert manifest["no_auto_apply_gem_response"] is True
    assert "NO_REVOLUTX_REAL_ACCESS_FROM_MVP" in manifest["safety_markers"]


def test_p127_checklist_is_operator_action_or_ready(tmp_path):
    write_operator_run_shortcut_pack(OperatorRunShortcutRequest(output_dir=tmp_path))
    with (tmp_path / "P127_SHORTCUT_CHECKLIST.csv").open(
        encoding="utf-8-sig", newline=""
    ) as handle:
        rows = list(csv.DictReader(handle))
    assert len(rows) == 5
    statuses = {row["status"] for row in rows}
    assert statuses.issubset({"READY", "OPERATOR_ACTION"})


def test_p127_cli_generates_pack(tmp_path):
    completed = subprocess.run(
        [
            sys.executable,
            "-m",
            "mvp_qaic_py.operator_run_shortcut",
            "--output-dir",
            str(tmp_path),
            "--run-id",
            "P127-CLI",
        ],
        check=True,
        text=True,
        capture_output=True,
    )
    assert "OPERATOR_RUN_SHORTCUT_READY" in completed.stdout
    assert (tmp_path / "P127_OPERATOR_RUN_SHORTCUT.ps1").exists()


def test_p127_safety_markers_are_explicit():
    required = {
        "LOCAL_ONLY",
        "OPERATOR_SHORTCUT_ONLY",
        "HUMAN_REVIEW_ONLY",
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
