import json
import subprocess
import sys

from mvp_qaic_py.gem_prompt_usability_pack import (
    DEFAULT_SAMPLE_PASTED_TEXT,
    SAFETY_MARKERS,
    build_cli_commands,
    build_operator_checklist,
    build_usability_contract,
    write_usability_pack,
)


def test_p117_usability_pack_writes_expected_files_and_runtime_sample(tmp_path):
    result = write_usability_pack(tmp_path)

    assert result["status"] == "EXPORTED"

    top_level = {path.name for path in tmp_path.iterdir()}
    assert {
        "P117_USABILITY_CONTRACT.json",
        "P117_QUICKSTART.md",
        "P117_CLI_COMMANDS.md",
        "P117_OPERATOR_CHECKLIST.md",
        "P117_SAMPLE_PASTED_PORTFOLIO.txt",
        "P117_SAMPLE_STRUCTURED_PORTFOLIO.json",
        "P117_USABILITY_REPORT.md",
        "P117_SAMPLE_RUNTIME_PACK_PASTED_TEXT",
    }.issubset(top_level)

    prompt = tmp_path / "P117_SAMPLE_RUNTIME_PACK_PASTED_TEXT" / "P116_GEM_PROMPT_COPY_PASTE.md"
    assert prompt.exists()
    assert "BTC 0.10" in prompt.read_text(encoding="utf-8")


def test_p117_contract_forbids_live_actions():
    contract = build_usability_contract()
    forbidden = set(contract["forbidden"])

    assert "apps_script_execution" in forbidden
    assert "sheet_write" in forbidden
    assert "clasp_push" in forbidden
    assert "public_deploy" in forbidden
    assert "broker_execution" in forbidden
    assert "order_execution" in forbidden
    assert "auto_sizing" in forbidden
    assert "revolutx_real_access_from_mvp" in forbidden


def test_p117_cli_commands_are_operator_ready_and_local_only():
    commands = build_cli_commands()
    joined = "\n".join(commands.values())

    assert "python -m mvp_qaic_py.gem_prompt_runtime_cli" in joined
    assert "--input-mode PASTED_TEXT_DRAFT" in joined
    assert "--input-mode IMAGE_REVIEW_REQUIRED" in joined
    assert "--input-mode STRUCTURED" in joined
    assert "clasp" not in joined.lower()
    assert "broker" not in joined.lower()
    assert "order" not in joined.lower()


def test_p117_operator_checklist_has_human_review_and_no_ocr():
    checklist = "\n".join(build_operator_checklist()).lower()

    assert "human review" in checklist
    assert "ocr" in checklist
    assert "revolut x" in checklist
    assert "order" in checklist


def test_p117_cli_generates_pack(tmp_path):
    output_dir = tmp_path / "pack"
    completed = subprocess.run(
        [
            sys.executable,
            "-m",
            "mvp_qaic_py.gem_prompt_usability_pack",
            "--output-dir",
            str(output_dir),
        ],
        check=True,
        text=True,
        capture_output=True,
    )

    assert "EXPORTED" in completed.stdout
    assert (output_dir / "P117_QUICKSTART.md").exists()
    assert (
        output_dir / "P117_SAMPLE_RUNTIME_PACK_PASTED_TEXT" / "P116_RUNTIME_PAYLOAD.json"
    ).exists()


def test_p117_sample_and_safety_markers_are_explicit():
    assert "BTC 0.10" in DEFAULT_SAMPLE_PASTED_TEXT

    required = {
        "MVP_PUBLIC_SCOPE",
        "HUMAN_REVIEW_ONLY",
        "LOCAL_ONLY",
        "COPY_PASTE_TO_GEM_ONLY",
        "NO_INDEX_EDIT",
        "NO_CLASP",
        "NO_APPS_SCRIPT_EXECUTION",
        "NO_SHEET_WRITE",
        "NO_PUBLIC_DEPLOY",
        "NO_BROKER",
        "NO_ORDER",
        "NO_AUTO_SIZING",
        "NO_OCR_CLAIM",
        "NO_AUTOMATED_VISUAL_EXTRACTION",
        "NO_REVOLUTX_REAL_ACCESS_FROM_MVP",
    }

    assert required.issubset(set(SAFETY_MARKERS))


def test_p117_export_payload_has_no_desktop_ini(tmp_path):
    result = write_usability_pack(tmp_path)
    serialized = json.dumps(result, ensure_ascii=False).lower()

    assert "desktop.ini" not in serialized
