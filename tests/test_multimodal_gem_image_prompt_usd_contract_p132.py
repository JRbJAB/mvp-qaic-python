import csv
import json
import subprocess
import sys

from mvp_qaic_py.multimodal_gem_image_prompt_usd_contract import (
    REFERENCE_CURRENCY,
    SAFETY_MARKERS,
    MultimodalGemImagePromptUsdContractRequest,
    build_contract,
    build_expected_gem_output_schema,
    write_multimodal_gem_image_prompt_usd_contract,
)


def _make_p131(exports):
    p131 = exports / "P131_REAL_IMAGE_TRANSCRIPTION_OPERATOR_TEST_20260622_000001"
    p131.mkdir(parents=True)
    (p131 / "P131_REAL_TEST_MANIFEST.json").write_text("{}", encoding="utf-8")
    return p131


def test_p132_creates_functional_pack_today(tmp_path):
    exports = tmp_path / "05_EXPORTS"
    p131 = _make_p131(exports)

    result = write_multimodal_gem_image_prompt_usd_contract(
        MultimodalGemImagePromptUsdContractRequest(output_dir=tmp_path / "out", exports_dir=exports)
    )

    assert result["status"] == "MULTIMODAL_GEM_IMAGE_PROMPT_USD_CONTRACT_READY"
    assert result["functional_today"] is True
    assert result["p131_dir"] == str(p131)
    assert result["p131_dir_valid"] is True


def test_p132_prompt_says_image_is_in_main_prompt_no_pre_step(tmp_path):
    exports = tmp_path / "05_EXPORTS"
    _make_p131(exports)

    write_multimodal_gem_image_prompt_usd_contract(
        MultimodalGemImagePromptUsdContractRequest(output_dir=tmp_path / "out", exports_dir=exports)
    )

    prompt = (tmp_path / "out" / "P132_GEM_MULTIMODAL_PORTFOLIO_PROMPT.md").read_text(
        encoding="utf-8"
    )
    assert "The image is part of this main prompt" in prompt
    assert "Do not ask for or create a separate preliminary step" in prompt
    assert "Reference currency is USD" in prompt


def test_p132_prompt_requires_image_usage_evidence(tmp_path):
    exports = tmp_path / "05_EXPORTS"
    _make_p131(exports)

    write_multimodal_gem_image_prompt_usd_contract(
        MultimodalGemImagePromptUsdContractRequest(output_dir=tmp_path / "out", exports_dir=exports)
    )

    prompt = (tmp_path / "out" / "P132_GEM_MULTIMODAL_PORTFOLIO_PROMPT.md").read_text(
        encoding="utf-8"
    )
    assert "image_used" in prompt
    assert "image_usage_evidence.status" in prompt
    assert "visual_evidence_summary" in prompt
    assert "IMAGE_NOT_USED_OR_NOT_EVIDENCED" in prompt


def test_p132_expected_schema_is_usd_and_contains_assets():
    schema = build_expected_gem_output_schema()
    assert schema["properties"]["reference_currency"]["const"] == "USD"
    asset_props = schema["properties"]["assets"]["items"]["properties"]
    assert "value_usd" in asset_props
    assert "price_usd" in asset_props
    assert "value_eur" not in asset_props


def test_p132_schema_requires_human_review_and_no_order():
    schema = build_expected_gem_output_schema()
    assert "human_review_required" in schema["required"]
    assert "no_order_no_sizing" in schema["required"]
    assert schema["properties"]["human_review_required"]["const"] is True
    assert schema["properties"]["no_order_no_sizing"]["const"] is True


def test_p132_gate_checklist_blocks_missing_image_usage(tmp_path):
    exports = tmp_path / "05_EXPORTS"
    _make_p131(exports)

    write_multimodal_gem_image_prompt_usd_contract(
        MultimodalGemImagePromptUsdContractRequest(output_dir=tmp_path / "out", exports_dir=exports)
    )

    with (tmp_path / "out" / "P132_RESPONSE_IMAGE_USAGE_GATE_CHECKLIST.csv").open(
        encoding="utf-8-sig",
        newline="",
    ) as handle:
        rows = list(csv.DictReader(handle))

    assert any(row["safety_or_gate"] == "IMAGE_NOT_USED_OR_NOT_EVIDENCED" for row in rows)
    assert any(row["safety_or_gate"] == "USD_REFERENCE_CURRENCY" for row in rows)


def test_p132_correction_plan_defers_reference_prompt_patch_until_real_gate(tmp_path):
    exports = tmp_path / "05_EXPORTS"
    _make_p131(exports)

    write_multimodal_gem_image_prompt_usd_contract(
        MultimodalGemImagePromptUsdContractRequest(output_dir=tmp_path / "out", exports_dir=exports)
    )

    plan = (tmp_path / "out" / "P132_REFERENCE_PROMPTS_CORRECTION_PLAN.md").read_text(
        encoding="utf-8"
    )
    assert "Today functional version" in plan
    assert "Controlled reference prompt sync" in plan
    assert "P134" in plan
    assert "P135" in plan


def test_p132_today_runbook_is_actionable(tmp_path):
    exports = tmp_path / "05_EXPORTS"
    _make_p131(exports)

    write_multimodal_gem_image_prompt_usd_contract(
        MultimodalGemImagePromptUsdContractRequest(output_dir=tmp_path / "out", exports_dir=exports)
    )

    runbook = (tmp_path / "out" / "P132_TODAY_FUNCTIONAL_RUNBOOK.md").read_text(encoding="utf-8")
    assert "Get a functional real GEM test today" in runbook
    assert "Attach the Revolut X screenshot/image directly in GEM" in runbook
    assert 'reference_currency="USD"' in runbook


def test_p132_contract_records_architecture_decision():
    contract = build_contract()
    assert contract["reference_currency"] == "USD"
    assert "attached directly to the main GEM portfolio prompt" in contract["architecture_decision"]
    assert "separate first-pass GEM extraction as mandatory workflow" in contract["forbidden"]


def test_p132_writes_expected_files(tmp_path):
    exports = tmp_path / "05_EXPORTS"
    _make_p131(exports)

    write_multimodal_gem_image_prompt_usd_contract(
        MultimodalGemImagePromptUsdContractRequest(output_dir=tmp_path / "out", exports_dir=exports)
    )

    expected = [
        "P132_GEM_MULTIMODAL_PORTFOLIO_PROMPT.md",
        "P132_EXPECTED_GEM_OUTPUT_SCHEMA.json",
        "P132_COPY_PASTE_TEXT_OPTIONAL_TEMPLATE.md",
        "P132_IMAGE_ATTACHMENT_GUIDE.md",
        "P132_RESPONSE_IMAGE_USAGE_GATE_CHECKLIST.csv",
        "P132_REFERENCE_PROMPTS_CORRECTION_PLAN.md",
        "P132_TODAY_FUNCTIONAL_RUNBOOK.md",
        "P132_CONTRACT.json",
        "P132_MANIFEST.json",
        "P132_README.md",
    ]
    for file_name in expected:
        assert (tmp_path / "out" / file_name).exists()


def test_p132_cli_generates_pack(tmp_path):
    exports = tmp_path / "05_EXPORTS"
    _make_p131(exports)

    completed = subprocess.run(
        [
            sys.executable,
            "-m",
            "mvp_qaic_py.multimodal_gem_image_prompt_usd_contract",
            "--output-dir",
            str(tmp_path / "out"),
            "--exports-dir",
            str(exports),
            "--run-id",
            "P132-CLI",
        ],
        check=True,
        text=True,
        capture_output=True,
    )

    assert "MULTIMODAL_GEM_IMAGE_PROMPT_USD_CONTRACT_READY" in completed.stdout
    assert "USD" in completed.stdout
    assert (tmp_path / "out" / "P132_MANIFEST.json").exists()


def test_p132_manifest_json_contains_required_safety(tmp_path):
    exports = tmp_path / "05_EXPORTS"
    _make_p131(exports)

    write_multimodal_gem_image_prompt_usd_contract(
        MultimodalGemImagePromptUsdContractRequest(output_dir=tmp_path / "out", exports_dir=exports)
    )

    manifest = json.loads((tmp_path / "out" / "P132_MANIFEST.json").read_text(encoding="utf-8"))
    assert manifest["reference_currency"] == REFERENCE_CURRENCY
    assert manifest["image_included_in_main_prompt"] is True
    assert manifest["no_preliminary_image_extraction_step"] is True
    assert manifest["image_usage_evidence_required"] is True
    assert "NO_REVOLUTX_REAL_ACCESS_FROM_MVP" in manifest["safety_markers"]


def test_p132_safety_markers_are_explicit():
    required = {
        "LOCAL_ONLY",
        "GEM_MULTIMODAL_IMAGE_INPUT_ALLOWED",
        "IMAGE_INCLUDED_IN_MAIN_PROMPT",
        "NO_PRELIMINARY_IMAGE_EXTRACTION_STEP",
        "IMAGE_USAGE_EVIDENCE_REQUIRED",
        "USD_REFERENCE_CURRENCY",
        "HUMAN_REVIEW_REQUIRED",
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
