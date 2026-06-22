import csv
import json
import subprocess
import sys

from mvp_qaic_py.prompt_image_capture_human_review import (
    OUTPUT_FILES,
    SAFETY_MARKERS,
    PromptImageCaptureRequest,
    build_image_input_contract,
    write_prompt_image_capture_pack,
)


def test_p128_writes_expected_files_and_inbox(tmp_path):
    result = write_prompt_image_capture_pack(
        PromptImageCaptureRequest(output_dir=tmp_path, run_id="P128-TEST")
    )
    assert result["status"] == "IMAGE_CAPTURE_HUMAN_REVIEW_READY"
    for file_name in OUTPUT_FILES:
        assert (tmp_path / file_name).exists()


def test_p128_contract_forbids_ocr_and_automated_extraction():
    contract = build_image_input_contract()
    forbidden = set(contract["forbidden"])
    assert "ocr_claim" in forbidden
    assert "automated_visual_extraction" in forbidden
    assert "invented_portfolio_data" in forbidden
    assert "sheet_write" in forbidden
    assert "broker_execution" in forbidden
    assert contract["manual_transcription_required"] is True
    assert contract["no_ocr_claim"] is True
    assert contract["no_automated_visual_extraction"] is True


def test_p128_guide_has_hard_boundaries(tmp_path):
    write_prompt_image_capture_pack(PromptImageCaptureRequest(output_dir=tmp_path))
    guide = (tmp_path / "P128_IMAGE_CAPTURE_GUIDE.md").read_text(encoding="utf-8")
    assert "P128 does not perform OCR" in guide
    assert "P128 does not claim automated visual extraction" in guide
    assert "NO_INVENTED_PORTFOLIO_DATA" in guide


def test_p128_manual_transcription_template_is_human_review_only(tmp_path):
    write_prompt_image_capture_pack(PromptImageCaptureRequest(output_dir=tmp_path))
    template = (tmp_path / "P128_MANUAL_TRANSCRIPTION_TEMPLATE.md").read_text(encoding="utf-8")
    assert "source: manual_image_transcription" in template
    assert "HUMAN_REVIEW_ONLY" in template
    assert "NO_OCR_CLAIM" in template


def test_p128_checklist_marks_operator_actions(tmp_path):
    write_prompt_image_capture_pack(PromptImageCaptureRequest(output_dir=tmp_path))
    with (tmp_path / "P128_IMAGE_CAPTURE_CHECKLIST.csv").open(
        encoding="utf-8-sig",
        newline="",
    ) as handle:
        rows = list(csv.DictReader(handle))
    assert len(rows) == 6
    assert rows[0]["status"] == "OPERATOR_ACTION"
    assert "MANUAL_TRANSCRIPTION_REQUIRED" in {row["safety"] for row in rows}


def test_p128_manifest_registers_image_path_without_extraction(tmp_path):
    image = tmp_path / "portfolio.png"
    image.write_bytes(b"fake-image-bytes")
    result = write_prompt_image_capture_pack(
        PromptImageCaptureRequest(output_dir=tmp_path / "out", image_path=image)
    )
    assert result["image_exists"] is True
    assert result["image_extension_allowed"] is True
    assert result["image_registered_only"] is True
    assert result["no_automated_visual_extraction"] is True


def test_p128_cli_generates_pack(tmp_path):
    completed = subprocess.run(
        [
            sys.executable,
            "-m",
            "mvp_qaic_py.prompt_image_capture_human_review",
            "--output-dir",
            str(tmp_path),
            "--run-id",
            "P128-CLI",
        ],
        check=True,
        text=True,
        capture_output=True,
    )
    assert "IMAGE_CAPTURE_HUMAN_REVIEW_READY" in completed.stdout
    assert "True" in completed.stdout
    assert (tmp_path / "P128_IMAGE_CAPTURE_MANIFEST.json").exists()


def test_p128_safety_markers_are_explicit():
    required = {
        "LOCAL_ONLY",
        "IMAGE_CAPTURE_ONLY",
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


def test_p128_manifest_json_contains_required_safety(tmp_path):
    write_prompt_image_capture_pack(PromptImageCaptureRequest(output_dir=tmp_path))
    manifest = json.loads(
        (tmp_path / "P128_IMAGE_CAPTURE_MANIFEST.json").read_text(encoding="utf-8")
    )
    assert manifest["manual_transcription_required"] is True
    assert manifest["no_ocr_claim"] is True
    assert manifest["no_invented_portfolio_data"] is True
    assert "NO_REVOLUTX_REAL_ACCESS_FROM_MVP" in manifest["safety_markers"]
