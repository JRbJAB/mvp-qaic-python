import json
import subprocess
import sys

from mvp_qaic_py.gem_prompt_runtime_cli import (
    GemRuntimeRequest,
    P116_SAFETY_MARKERS,
    build_runtime_contract,
    build_runtime_payload,
    write_runtime_pack,
)


def test_p116_image_review_payload_preserves_human_review_and_no_ocr():
    payload = build_runtime_payload(
        GemRuntimeRequest(
            input_mode="IMAGE_REVIEW_REQUIRED",
            image_reference="portfolio_capture.png",
            notes="capture reference only",
            run_id="P116-TEST",
            generated_at_utc="2026-06-22T00:00:00Z",
        )
    )

    assert payload["status"] == "REVIEW_REQUIRED"
    assert payload["runtime_mode"] == "LOCAL_COPY_PASTE_TO_GEM_ONLY"
    assert payload["human_review_only"] is True
    assert payload["no_ocr_claim"] is True
    assert payload["no_order_no_sizing"] is True
    assert "NO_IMAGE_VISUAL_EXTRACTION_WITHOUT_HUMAN" in payload["safety_markers"]
    assert "COPY_PASTE_TO_GEM_ONLY" in payload["safety_markers"]
    assert "human_confirmed_asset_symbols" in json.dumps(payload)


def test_p116_pasted_text_runtime_pack_writes_expected_files(tmp_path):
    result = write_runtime_pack(
        tmp_path,
        GemRuntimeRequest(
            input_mode="PASTED_TEXT_DRAFT",
            pasted_text="BTC 0.10 value EUR 6500",
            run_id="P116-PASTED",
            generated_at_utc="2026-06-22T00:00:00Z",
        ),
    )

    assert result["status"] == "EXPORTED"

    expected = {
        "P116_RUNTIME_PAYLOAD.json",
        "P116_GEM_PROMPT_COPY_PASTE.md",
        "P116_EXPECTED_GEM_OUTPUT_SCHEMA.json",
        "P116_RUNTIME_CONTRACT.json",
        "P116_RUNTIME_REPORT.md",
    }
    assert expected == {path.name for path in tmp_path.iterdir()}

    payload = json.loads((tmp_path / "P116_RUNTIME_PAYLOAD.json").read_text(encoding="utf-8"))
    prompt = (tmp_path / "P116_GEM_PROMPT_COPY_PASTE.md").read_text(encoding="utf-8")

    assert payload["request"]["input_mode"] == "PASTED_TEXT_DRAFT"
    assert payload["no_revolutx_real_access"] is True
    assert "BTC 0.10" in prompt


def test_p116_contract_blocks_live_actions():
    contract = build_runtime_contract()
    forbidden = set(contract["forbidden"])

    assert "apps_script_execution" in forbidden
    assert "sheet_write" in forbidden
    assert "clasp_push" in forbidden
    assert "broker_execution" in forbidden
    assert "order_execution" in forbidden
    assert "auto_sizing" in forbidden
    assert "revolutx_real_access_from_mvp" in forbidden


def test_p116_cli_module_generates_pack(tmp_path):
    output_dir = tmp_path / "cli_pack"
    completed = subprocess.run(
        [
            sys.executable,
            "-m",
            "mvp_qaic_py.gem_prompt_runtime_cli",
            "--output-dir",
            str(output_dir),
            "--input-mode",
            "IMAGE_REVIEW_REQUIRED",
            "--image-reference",
            "capture.png",
            "--notes",
            "human review only",
            "--run-id",
            "P116-CLI",
            "--generated-at-utc",
            "2026-06-22T00:00:00Z",
        ],
        check=True,
        text=True,
        capture_output=True,
    )

    assert "EXPORTED" in completed.stdout
    assert (output_dir / "P116_RUNTIME_PAYLOAD.json").exists()
    assert (output_dir / "P116_GEM_PROMPT_COPY_PASTE.md").exists()


def test_p116_safety_markers_are_explicit():
    required = {
        "HUMAN_REVIEW_ONLY",
        "NO_OCR_CLAIM",
        "NO_IMAGE_VISUAL_EXTRACTION_WITHOUT_HUMAN",
        "NO_BROKER",
        "NO_ORDER",
        "NO_AUTO_SIZING",
        "NO_REVOLUTX_REAL_ACCESS",
        "P116_MINI_CLI_LOCAL_ONLY",
        "NO_LIVE_PROVIDER_CALL",
        "NO_IMAGE_OCR_RUNTIME",
        "NO_AUTOMATED_VISUAL_EXTRACTION",
        "COPY_PASTE_TO_GEM_ONLY",
    }

    assert required.issubset(set(P116_SAFETY_MARKERS))
