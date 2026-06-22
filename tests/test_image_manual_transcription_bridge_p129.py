import csv
import json
import subprocess
import sys

from mvp_qaic_py.image_manual_transcription_bridge import (
    SAFETY_MARKERS,
    ImageManualTranscriptionBridgeRequest,
    build_bridge_contract,
    write_image_manual_transcription_bridge,
)


def _transcription_text(symbol="BTC", quantity="0.10", value="6500"):
    return f"""
# Manual Transcription

ASSET_1:
- symbol: {symbol}
- quantity: {quantity}
- value_eur: {value}
- source: manual_image_transcription
- confidence: REVIEW

HUMAN_REVIEW_ONLY
NO_OCR_CLAIM
NO_AUTOMATED_VISUAL_EXTRACTION
"""


def test_p129_ready_when_manual_transcription_has_asset_fields(tmp_path):
    transcription = tmp_path / "manual.md"
    transcription.write_text(_transcription_text(), encoding="utf-8")

    result = write_image_manual_transcription_bridge(
        ImageManualTranscriptionBridgeRequest(
            output_dir=tmp_path / "out",
            manual_transcription_path=transcription,
        )
    )

    assert result["status"] == "P124_PORTFOLIO_INPUT_READY"
    assert result["p124_input_ready"] is True
    assert result["blocker_count"] == 0


def test_p129_pending_when_transcription_template_is_blank(tmp_path):
    p128 = tmp_path / "p128"
    p128.mkdir()
    (p128 / "P128_MANUAL_TRANSCRIPTION_TEMPLATE.md").write_text(
        """
ASSET_1:
- symbol:
- quantity:
- value_eur:
""",
        encoding="utf-8",
    )

    result = write_image_manual_transcription_bridge(
        ImageManualTranscriptionBridgeRequest(output_dir=tmp_path / "out", p128_dir=p128)
    )

    assert result["status"] == "MANUAL_TRANSCRIPTION_PENDING"
    assert result["p124_input_ready"] is False
    assert result["missing_data_count"] == 1


def test_p129_blocks_automation_claims(tmp_path):
    transcription = tmp_path / "manual.md"
    transcription.write_text(
        _transcription_text() + "\nValues were automatically extracted by OCR.",
        encoding="utf-8",
    )

    result = write_image_manual_transcription_bridge(
        ImageManualTranscriptionBridgeRequest(
            output_dir=tmp_path / "out",
            manual_transcription_path=transcription,
        )
    )

    assert result["status"] == "BLOCKED_REVIEW_REQUIRED"
    assert result["blocker_count"] >= 1


def test_p129_writes_expected_files(tmp_path):
    transcription = tmp_path / "manual.md"
    transcription.write_text(_transcription_text("ETH", "1.2", "4200"), encoding="utf-8")

    write_image_manual_transcription_bridge(
        ImageManualTranscriptionBridgeRequest(
            output_dir=tmp_path / "out",
            manual_transcription_path=transcription,
        )
    )

    expected = [
        "P129_P124_PORTFOLIO_INPUT_FROM_MANUAL_TRANSCRIPTION.txt",
        "P129_IMAGE_TO_PROMPT_BRIDGE_REPORT.md",
        "P129_MANUAL_TRANSCRIPTION_REVIEW.csv",
        "P129_BRIDGE_CONTRACT.json",
        "P129_BRIDGE_MANIFEST.json",
        "P129_NEXT_ACTIONS.md",
        "P129_README.md",
    ]
    for file_name in expected:
        assert (tmp_path / "out" / file_name).exists()


def test_p129_p124_input_contains_manual_transcription_and_safety(tmp_path):
    transcription = tmp_path / "manual.md"
    transcription.write_text(_transcription_text("SOL", "12", "1600"), encoding="utf-8")

    write_image_manual_transcription_bridge(
        ImageManualTranscriptionBridgeRequest(
            output_dir=tmp_path / "out",
            manual_transcription_path=transcription,
        )
    )

    p124_input = (
        tmp_path / "out" / "P129_P124_PORTFOLIO_INPUT_FROM_MANUAL_TRANSCRIPTION.txt"
    ).read_text(encoding="utf-8")
    assert "SOL" in p124_input
    assert "MANUAL_TRANSCRIPTION_REQUIRED" in p124_input
    assert "NO_OCR_CLAIM" in p124_input
    assert "NO_AUTOMATED_VISUAL_EXTRACTION" in p124_input


def test_p129_review_csv_records_ok_status(tmp_path):
    transcription = tmp_path / "manual.md"
    transcription.write_text(_transcription_text(), encoding="utf-8")

    write_image_manual_transcription_bridge(
        ImageManualTranscriptionBridgeRequest(
            output_dir=tmp_path / "out",
            manual_transcription_path=transcription,
        )
    )

    with (tmp_path / "out" / "P129_MANUAL_TRANSCRIPTION_REVIEW.csv").open(
        encoding="utf-8-sig",
        newline="",
    ) as handle:
        rows = list(csv.DictReader(handle))

    assert rows[0]["severity"] == "OK"
    assert rows[0]["code"] == "P124_PORTFOLIO_INPUT_READY"


def test_p129_contract_has_hard_boundaries():
    contract = build_bridge_contract()
    forbidden = set(contract["forbidden"])
    assert "ocr_claim" in forbidden
    assert "automated_visual_extraction" in forbidden
    assert "invented_portfolio_data" in forbidden
    assert "broker_execution" in forbidden
    assert "sheet_write" in forbidden
    assert contract["manual_transcription_required"] is True


def test_p129_cli_generates_bridge(tmp_path):
    transcription = tmp_path / "manual.md"
    transcription.write_text(_transcription_text(), encoding="utf-8")

    completed = subprocess.run(
        [
            sys.executable,
            "-m",
            "mvp_qaic_py.image_manual_transcription_bridge",
            "--output-dir",
            str(tmp_path / "out"),
            "--manual-transcription-path",
            str(transcription),
            "--run-id",
            "P129-CLI",
        ],
        check=True,
        text=True,
        capture_output=True,
    )

    assert "P124_PORTFOLIO_INPUT_READY" in completed.stdout
    assert (tmp_path / "out" / "P129_BRIDGE_MANIFEST.json").exists()


def test_p129_safety_markers_are_explicit():
    required = {
        "LOCAL_ONLY",
        "IMAGE_TO_PROMPT_BRIDGE_ONLY",
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


def test_p129_manifest_json_contains_required_safety(tmp_path):
    transcription = tmp_path / "manual.md"
    transcription.write_text(_transcription_text(), encoding="utf-8")

    write_image_manual_transcription_bridge(
        ImageManualTranscriptionBridgeRequest(
            output_dir=tmp_path / "out",
            manual_transcription_path=transcription,
        )
    )

    manifest = json.loads(
        (tmp_path / "out" / "P129_BRIDGE_MANIFEST.json").read_text(encoding="utf-8")
    )
    assert manifest["manual_transcription_required"] is True
    assert manifest["no_ocr_claim"] is True
    assert manifest["no_invented_portfolio_data"] is True
    assert "NO_REVOLUTX_REAL_ACCESS_FROM_MVP" in manifest["safety_markers"]
