import json
import subprocess
import sys

import pytest

from mvp_qaic_py.gem_prompt_daily_shortcut import (
    DEFAULT_PORTFOLIO_INPUT,
    SAFETY_MARKERS,
    DailyShortcutRequest,
    build_daily_contract,
    resolve_input_mode,
    write_daily_shortcut_pack,
)


def test_p118_default_sample_generates_daily_runtime_pack(tmp_path):
    result = write_daily_shortcut_pack(
        DailyShortcutRequest(
            output_dir=tmp_path,
            use_default_sample=True,
            run_id="P118-SAMPLE",
            generated_at_utc="2026-06-22T00:00:00Z",
        )
    )

    assert result["status"] == "EXPORTED"
    assert result["input_mode"] == "PASTED_TEXT_DRAFT"

    prompt = tmp_path / "P118_RUNTIME_PACK" / "P116_GEM_PROMPT_COPY_PASTE.md"
    assert prompt.exists()
    assert "BTC 0.10" in prompt.read_text(encoding="utf-8")

    assert (tmp_path / "P118_DAILY_README.md").exists()
    assert (tmp_path / "P118_DAILY_COMMANDS.md").exists()
    assert (tmp_path / "P118_DAILY_MANIFEST.json").exists()


def test_p118_pasted_text_file_mode(tmp_path):
    source = tmp_path / "portfolio_input.txt"
    source.write_text("SOL 10 value EUR 1500", encoding="utf-8")

    result = write_daily_shortcut_pack(
        DailyShortcutRequest(
            output_dir=tmp_path / "out",
            pasted_text_file=str(source),
            run_id="P118-FILE",
        )
    )

    prompt = tmp_path / "out" / "P118_RUNTIME_PACK" / "P116_GEM_PROMPT_COPY_PASTE.md"
    assert result["input_mode"] == "PASTED_TEXT_DRAFT"
    assert "SOL 10" in prompt.read_text(encoding="utf-8")


def test_p118_image_mode_is_review_required_and_no_ocr(tmp_path):
    result = write_daily_shortcut_pack(
        DailyShortcutRequest(
            output_dir=tmp_path,
            image_reference="portfolio_capture.png",
            notes="image reference only",
        )
    )

    prompt = tmp_path / "P118_RUNTIME_PACK" / "P116_GEM_PROMPT_COPY_PASTE.md"
    payload = json.loads(
        (tmp_path / "P118_RUNTIME_PACK" / "P116_RUNTIME_PAYLOAD.json").read_text(encoding="utf-8")
    )

    assert result["input_mode"] == "IMAGE_REVIEW_REQUIRED"
    assert "No OCR claim" in prompt.read_text(encoding="utf-8")
    assert payload["no_ocr_claim"] is True


def test_p118_rejects_multiple_input_types(tmp_path):
    with pytest.raises(ValueError, match="Use only one input type"):
        resolve_input_mode(
            DailyShortcutRequest(
                output_dir=tmp_path,
                pasted_text="BTC",
                image_reference="capture.png",
            )
        )


def test_p118_contract_blocks_live_and_broker_actions():
    contract = build_daily_contract()
    forbidden = set(contract["forbidden"])

    assert "apps_script_execution" in forbidden
    assert "sheet_write" in forbidden
    assert "clasp_push" in forbidden
    assert "broker_execution" in forbidden
    assert "order_execution" in forbidden
    assert "auto_sizing" in forbidden
    assert "revolutx_real_access_from_mvp" in forbidden


def test_p118_cli_generates_pack(tmp_path):
    output_dir = tmp_path / "daily"
    completed = subprocess.run(
        [
            sys.executable,
            "-m",
            "mvp_qaic_py.gem_prompt_daily_shortcut",
            "--output-dir",
            str(output_dir),
            "--use-default-sample",
            "--run-id",
            "P118-CLI",
        ],
        check=True,
        text=True,
        capture_output=True,
    )

    assert "EXPORTED" in completed.stdout
    assert (output_dir / "P118_RUNTIME_PACK" / "P116_GEM_PROMPT_COPY_PASTE.md").exists()


def test_p118_safety_markers_and_sample_are_explicit():
    assert "BTC 0.10" in DEFAULT_PORTFOLIO_INPUT

    required = {
        "MVP_PUBLIC_SCOPE",
        "HUMAN_REVIEW_ONLY",
        "LOCAL_ONLY",
        "DAILY_OPERATOR_SHORTCUT",
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
