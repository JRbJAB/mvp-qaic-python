import csv
import json
import subprocess
import sys

from mvp_qaic_py.real_image_transcription_operator_test import (
    SAFETY_MARKERS,
    RealImageTranscriptionOperatorTestRequest,
    build_real_test_contract,
    discover_latest_p130_dir,
    write_real_image_transcription_operator_test,
)


def _make_p128(exports):
    p128 = exports / "P128_PROMPT_INPUT_IMAGE_CAPTURE_HUMAN_REVIEW_20260622_000001"
    p128.mkdir(parents=True)
    (p128 / "P128_MANUAL_TRANSCRIPTION_TEMPLATE.md").write_text("ASSET_1:\n", encoding="utf-8")
    return p128


def _make_p130(exports):
    p130 = exports / "P130_OPERATOR_E2E_IMAGE_PROMPT_LOOP_20260622_000001"
    p130.mkdir(parents=True)
    (p130 / "P130_E2E_MANIFEST.json").write_text("{}", encoding="utf-8")
    return p130


def test_p131_discovers_latest_p130_without_g_bug(tmp_path):
    exports = tmp_path / "05_EXPORTS"
    p130 = _make_p130(exports)

    latest = discover_latest_p130_dir(exports)

    assert latest == p130
    assert str(latest) != "G"


def test_p131_creates_real_operator_workspace(tmp_path):
    exports = tmp_path / "05_EXPORTS"
    p128 = _make_p128(exports)
    p130 = _make_p130(exports)

    result = write_real_image_transcription_operator_test(
        RealImageTranscriptionOperatorTestRequest(output_dir=tmp_path / "out", exports_dir=exports)
    )

    assert result["status"] == "REAL_IMAGE_TRANSCRIPTION_OPERATOR_TEST_READY"
    assert result["ready_for_real_operator_test"] is True
    assert result["p128_dir"] == str(p128)
    assert result["p130_dir"] == str(p130)
    assert result["p128_dir_valid"] is True
    assert result["p130_dir_valid"] is True


def test_p131_writes_expected_files(tmp_path):
    exports = tmp_path / "05_EXPORTS"
    _make_p128(exports)
    _make_p130(exports)

    write_real_image_transcription_operator_test(
        RealImageTranscriptionOperatorTestRequest(output_dir=tmp_path / "out", exports_dir=exports)
    )

    expected = [
        "P131_OPERATOR_TEST_GUIDE.md",
        "P131_REAL_IMAGE_INBOX/README.md",
        "P131_REAL_IMAGE_INBOX/.gitkeep",
        "P131_FILLED_TRANSCRIPTION_OUTBOX/P131_MANUAL_TRANSCRIPTION_REAL_TEST.md",
        "P131_FILLED_TRANSCRIPTION_OUTBOX/P131_SAFE_FAKE_EXAMPLE_NOT_REAL.md",
        "P131_OPERATOR_COMMANDS.md",
        "P131_REAL_TEST_CHECKLIST.csv",
        "P131_REAL_TEST_CONTRACT.json",
        "P131_REAL_TEST_MANIFEST.json",
        "P131_README.md",
    ]
    for file_name in expected:
        assert (tmp_path / "out" / file_name).exists()


def test_p131_manual_transcription_template_has_required_fields(tmp_path):
    exports = tmp_path / "05_EXPORTS"
    _make_p128(exports)
    _make_p130(exports)

    write_real_image_transcription_operator_test(
        RealImageTranscriptionOperatorTestRequest(output_dir=tmp_path / "out", exports_dir=exports)
    )

    template = (
        tmp_path
        / "out"
        / "P131_FILLED_TRANSCRIPTION_OUTBOX"
        / "P131_MANUAL_TRANSCRIPTION_REAL_TEST.md"
    ).read_text(encoding="utf-8")
    assert "- symbol:" in template
    assert "- quantity:" in template
    assert "- value_eur:" in template
    assert "NO_OCR_CLAIM" in template


def test_p131_operator_commands_rerun_p130_with_manual_transcription_path(tmp_path):
    exports = tmp_path / "05_EXPORTS"
    _make_p128(exports)
    _make_p130(exports)

    write_real_image_transcription_operator_test(
        RealImageTranscriptionOperatorTestRequest(output_dir=tmp_path / "out", exports_dir=exports)
    )

    commands = (tmp_path / "out" / "P131_OPERATOR_COMMANDS.md").read_text(encoding="utf-8")
    assert "operator_e2e_image_prompt_loop" in commands
    assert "--manual-transcription-path" in commands
    assert "E2E_READY_FOR_GEM_COPY_PASTE" in commands


def test_p131_fake_example_is_marked_not_real(tmp_path):
    exports = tmp_path / "05_EXPORTS"
    _make_p128(exports)
    _make_p130(exports)

    write_real_image_transcription_operator_test(
        RealImageTranscriptionOperatorTestRequest(output_dir=tmp_path / "out", exports_dir=exports)
    )

    example = (
        tmp_path / "out" / "P131_FILLED_TRANSCRIPTION_OUTBOX" / "P131_SAFE_FAKE_EXAMPLE_NOT_REAL.md"
    ).read_text(encoding="utf-8")
    assert "FAKE_EXAMPLE_NOT_REAL" in example
    assert "Do not use this as your portfolio" in example


def test_p131_checklist_is_operator_action_or_required(tmp_path):
    exports = tmp_path / "05_EXPORTS"
    _make_p128(exports)
    _make_p130(exports)

    write_real_image_transcription_operator_test(
        RealImageTranscriptionOperatorTestRequest(output_dir=tmp_path / "out", exports_dir=exports)
    )

    with (tmp_path / "out" / "P131_REAL_TEST_CHECKLIST.csv").open(
        encoding="utf-8-sig",
        newline="",
    ) as handle:
        rows = list(csv.DictReader(handle))

    assert len(rows) == 6
    assert "MANUAL_TRANSCRIPTION_REQUIRED" in {row["safety"] for row in rows}


def test_p131_contract_has_hard_boundaries():
    contract = build_real_test_contract()
    forbidden = set(contract["forbidden"])
    assert "ocr_claim" in forbidden
    assert "automated_visual_extraction" in forbidden
    assert "invented_portfolio_data" in forbidden
    assert "sheet_write" in forbidden
    assert "broker_execution" in forbidden
    assert contract["manual_transcription_required"] is True


def test_p131_cli_generates_workspace(tmp_path):
    exports = tmp_path / "05_EXPORTS"
    _make_p128(exports)
    _make_p130(exports)

    completed = subprocess.run(
        [
            sys.executable,
            "-m",
            "mvp_qaic_py.real_image_transcription_operator_test",
            "--output-dir",
            str(tmp_path / "out"),
            "--exports-dir",
            str(exports),
            "--run-id",
            "P131-CLI",
        ],
        check=True,
        text=True,
        capture_output=True,
    )

    assert "REAL_IMAGE_TRANSCRIPTION_OPERATOR_TEST_READY" in completed.stdout
    assert "True" in completed.stdout
    assert (tmp_path / "out" / "P131_REAL_TEST_MANIFEST.json").exists()


def test_p131_manifest_json_contains_required_safety(tmp_path):
    exports = tmp_path / "05_EXPORTS"
    _make_p128(exports)
    _make_p130(exports)

    write_real_image_transcription_operator_test(
        RealImageTranscriptionOperatorTestRequest(output_dir=tmp_path / "out", exports_dir=exports)
    )

    manifest = json.loads(
        (tmp_path / "out" / "P131_REAL_TEST_MANIFEST.json").read_text(encoding="utf-8")
    )
    assert manifest["manual_transcription_required"] is True
    assert manifest["no_ocr_claim"] is True
    assert manifest["no_invented_portfolio_data"] is True
    assert "NO_REVOLUTX_REAL_ACCESS_FROM_MVP" in manifest["safety_markers"]


def test_p131_safety_markers_are_explicit():
    required = {
        "LOCAL_ONLY",
        "REAL_OPERATOR_TEST_ONLY",
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
