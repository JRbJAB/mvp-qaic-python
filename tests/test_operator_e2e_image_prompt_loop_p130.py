import csv
import json
import subprocess
import sys

from mvp_qaic_py.operator_e2e_image_prompt_loop import (
    SAFETY_MARKERS,
    OperatorE2EImagePromptLoopRequest,
    build_e2e_contract,
    write_operator_e2e_image_prompt_loop,
)


def _make_p128(exports, text):
    p128 = exports / "P128_PROMPT_INPUT_IMAGE_CAPTURE_HUMAN_REVIEW_20260622_000001"
    p128.mkdir(parents=True)
    (p128 / "P128_MANUAL_TRANSCRIPTION_TEMPLATE.md").write_text(text, encoding="utf-8")
    return p128


def _filled_transcription():
    return """
ASSET_1:
- symbol: BTC
- quantity: 0.10
- value_eur: 6500
- source: manual_image_transcription
- confidence: REVIEW
"""


def _blank_transcription():
    return """
ASSET_1:
- symbol:
- quantity:
- value_eur:
"""


def test_p130_waits_when_p128_transcription_blank(tmp_path):
    exports = tmp_path / "05_EXPORTS"
    p128 = _make_p128(exports, _blank_transcription())

    result = write_operator_e2e_image_prompt_loop(
        OperatorE2EImagePromptLoopRequest(output_dir=tmp_path / "out", exports_dir=exports)
    )

    assert result["status"] == "E2E_WAITING_FOR_MANUAL_TRANSCRIPTION"
    assert result["waiting_for_manual_transcription"] is True
    assert result["p128_dir"] == str(p128)
    assert result["p128_dir_valid"] is True


def test_p130_ready_when_p128_transcription_filled(tmp_path):
    exports = tmp_path / "05_EXPORTS"
    _make_p128(exports, _filled_transcription())

    result = write_operator_e2e_image_prompt_loop(
        OperatorE2EImagePromptLoopRequest(output_dir=tmp_path / "out", exports_dir=exports)
    )

    assert result["status"] == "E2E_READY_FOR_GEM_COPY_PASTE"
    assert result["e2e_ready_for_gem"] is True
    assert result["p129_status"] == "P124_PORTFOLIO_INPUT_READY"


def test_p130_writes_p124_handoff_files(tmp_path):
    exports = tmp_path / "05_EXPORTS"
    _make_p128(exports, _filled_transcription())

    write_operator_e2e_image_prompt_loop(
        OperatorE2EImagePromptLoopRequest(output_dir=tmp_path / "out", exports_dir=exports)
    )

    handoff = tmp_path / "out" / "P130_P124_HANDOFF"
    assert (handoff / "portfolio_input.txt").exists()
    assert (handoff / "gem_response.txt").exists()
    assert (handoff / "run_notes.md").exists()


def test_p130_p124_handoff_contains_safety_and_payload(tmp_path):
    exports = tmp_path / "05_EXPORTS"
    _make_p128(exports, _filled_transcription())

    write_operator_e2e_image_prompt_loop(
        OperatorE2EImagePromptLoopRequest(output_dir=tmp_path / "out", exports_dir=exports)
    )

    text = (tmp_path / "out" / "P130_P124_HANDOFF" / "portfolio_input.txt").read_text(
        encoding="utf-8"
    )
    assert "BTC" in text
    assert "MANUAL_TRANSCRIPTION_REQUIRED" in text
    assert "NO_OCR_CLAIM" in text
    assert "NO_AUTOMATED_VISUAL_EXTRACTION" in text


def test_p130_operator_commands_include_p125_and_p126(tmp_path):
    exports = tmp_path / "05_EXPORTS"
    _make_p128(exports, _filled_transcription())

    write_operator_e2e_image_prompt_loop(
        OperatorE2EImagePromptLoopRequest(output_dir=tmp_path / "out", exports_dir=exports)
    )

    commands = (tmp_path / "out" / "P130_OPERATOR_COMMANDS.md").read_text(encoding="utf-8")
    assert "gem_manual_test_review_pack" in commands
    assert "daily_run_registry" in commands
    assert "NO_AUTO_APPLY_GEM_RESPONSE" in commands


def test_p130_manifest_guards_against_g_scalar_bug(tmp_path):
    exports = tmp_path / "05_EXPORTS"
    _make_p128(exports, _blank_transcription())

    result = write_operator_e2e_image_prompt_loop(
        OperatorE2EImagePromptLoopRequest(output_dir=tmp_path / "out", exports_dir=exports)
    )

    assert result["p128_dir"] != "G"
    assert result["p128_dir_valid"] is True


def test_p130_contract_has_boundaries():
    contract = build_e2e_contract()
    forbidden = set(contract["forbidden"])
    assert "ocr_claim" in forbidden
    assert "automated_visual_extraction" in forbidden
    assert "invented_portfolio_data" in forbidden
    assert "sheet_write" in forbidden
    assert "broker_execution" in forbidden
    assert contract["manual_transcription_required"] is True


def test_p130_checklist_is_written(tmp_path):
    exports = tmp_path / "05_EXPORTS"
    _make_p128(exports, _blank_transcription())

    write_operator_e2e_image_prompt_loop(
        OperatorE2EImagePromptLoopRequest(output_dir=tmp_path / "out", exports_dir=exports)
    )

    with (tmp_path / "out" / "P130_E2E_CHECKLIST.csv").open(
        encoding="utf-8-sig",
        newline="",
    ) as handle:
        rows = list(csv.DictReader(handle))

    assert len(rows) == 6
    assert "MANUAL_TRANSCRIPTION_REQUIRED" in {row["safety"] for row in rows}


def test_p130_cli_generates_loop(tmp_path):
    exports = tmp_path / "05_EXPORTS"
    _make_p128(exports, _blank_transcription())

    completed = subprocess.run(
        [
            sys.executable,
            "-m",
            "mvp_qaic_py.operator_e2e_image_prompt_loop",
            "--output-dir",
            str(tmp_path / "out"),
            "--exports-dir",
            str(exports),
            "--run-id",
            "P130-CLI",
        ],
        check=True,
        text=True,
        capture_output=True,
    )

    assert "E2E_WAITING_FOR_MANUAL_TRANSCRIPTION" in completed.stdout
    assert "True" in completed.stdout
    assert (tmp_path / "out" / "P130_E2E_MANIFEST.json").exists()


def test_p130_manifest_json_contains_required_safety(tmp_path):
    exports = tmp_path / "05_EXPORTS"
    _make_p128(exports, _filled_transcription())

    write_operator_e2e_image_prompt_loop(
        OperatorE2EImagePromptLoopRequest(output_dir=tmp_path / "out", exports_dir=exports)
    )

    manifest = json.loads((tmp_path / "out" / "P130_E2E_MANIFEST.json").read_text(encoding="utf-8"))
    assert manifest["manual_transcription_required"] is True
    assert manifest["no_ocr_claim"] is True
    assert manifest["no_invented_portfolio_data"] is True
    assert "NO_REVOLUTX_REAL_ACCESS_FROM_MVP" in manifest["safety_markers"]


def test_p130_safety_markers_are_explicit():
    required = {
        "LOCAL_ONLY",
        "OPERATOR_E2E_LOOP_ONLY",
        "HUMAN_REVIEW_ONLY",
        "MANUAL_TRANSCRIPTION_REQUIRED",
        "NO_OCR_CLAIM",
        "NO_AUTOMATED_VISUAL_EXTRACTION",
        "NO_INVENTED_PORTFOLIO_DATA",
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
