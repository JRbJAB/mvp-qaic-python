from __future__ import annotations

import subprocess
import sys

from mvp_qaic_py.p137_prompt_corrections_apply_queue import (
    P137Request,
    build_corrected_prompt,
    build_output_contract,
    build_p137_payload,
    build_prompt_corrections_queue,
    validate_gem_id,
    write_p137_prompt_pack,
)


def test_p137_queue_contains_core_gem_corrections():
    gem = validate_gem_id("GEM_GENERAL_REVIEW")
    queue = build_prompt_corrections_queue(gem)

    scopes = {row["scope"] for row in queue}
    assert "OUTPUT_FORMAT" in scopes
    assert "IMAGE_USAGE_EVIDENCE" in scopes
    assert "USD_REFERENCE" in scopes
    assert "SAFETY_GUARDS" in scopes
    assert "MISSING_DATA" in scopes
    assert all(row["status"] == "APPLIED_TO_LOCAL_DRAFT" for row in queue)


def test_p137_corrected_prompt_contains_required_contract_markers():
    gem = validate_gem_id("GEM_PORTFOLIO_REVIEW")
    corrected = build_corrected_prompt(
        "# Source prompt\nAnalyse portefeuille.",
        gem,
        generated_at_utc="2026-06-22T00:00:00Z",
    )

    assert "P137 — GEM Prompt Corrections Overlay" in corrected
    assert "reference_currency" in corrected
    assert '"USD"' in corrected
    assert "image_usage_evidence" in corrected
    assert "human_review_required" in corrected
    assert "no_order_no_sizing" in corrected
    assert "no_invented_portfolio_data" in corrected
    assert "```json" in corrected
    assert "# Source prompt" in corrected


def test_p137_output_contract_is_p133_compatible():
    gem = validate_gem_id("GEM_RISK_GUARD_REVIEW")
    contract = build_output_contract(gem)

    assert contract["hard_safety"]["human_review_required"] is True
    assert contract["hard_safety"]["no_order_no_sizing"] is True
    assert contract["hard_safety"]["no_broker_execution"] is True
    assert "image_used" in contract["required_json_keys"]
    assert "blockers" in contract["required_json_keys"]
    assert "REVIEW_REQUIRED" in contract["required_enums"]["status"]


def test_p137_write_pack_does_not_mutate_source_prompt(tmp_path):
    source = tmp_path / "source_prompt.md"
    original = "# Original prompt\nNe pas écraser."
    source.write_text(original, encoding="utf-8")

    out = tmp_path / "out"
    payload = write_p137_prompt_pack(
        P137Request(
            output_dir=out,
            exports_dir=tmp_path,
            prompt_file=source,
            gem_id="GEM_GENERAL_REVIEW",
            generated_at_utc="2026-06-22T00:00:00Z",
        )
    )

    assert source.read_text(encoding="utf-8") == original
    assert payload["corrected_prompt"]["local_draft_only"] is True
    assert payload["corrected_prompt"]["source_overwritten"] is False
    assert payload["features"]["no_prompt_source_overwrite"] is True
    assert (out / "P137_CORRECTED_GEM_PROMPT.md").exists()
    assert (out / "P137_SOURCE_PROMPT_COPY.md").exists()
    assert (out / "P137_PROMPT_CORRECTIONS_QUEUE.json").exists()
    assert (out / "P137_GEM_OUTPUT_CONTRACT.json").exists()


def test_p137_payload_safety_flags(tmp_path):
    payload = build_p137_payload(
        P137Request(
            output_dir=tmp_path / "out",
            exports_dir=tmp_path,
            gem_id="GEM_GENERAL_REVIEW",
            generated_at_utc="2026-06-22T00:00:00Z",
        )
    )

    assert payload["status"] == "P137_PROMPT_CORRECTIONS_READY_FOR_HUMAN_REVIEW"
    assert payload["features"]["prompt_corrections_apply_queue"] is True
    assert payload["features"]["corrected_prompt_local_draft"] is True
    assert payload["features"]["human_review_required"] is True
    assert payload["features"]["no_broker_execution"] is True
    assert payload["features"]["no_order"] is True
    assert payload["features"]["no_sizing"] is True
    assert "P137_PROMPT_CORRECTIONS_APPLY_QUEUE" in payload["safety_markers"]


def test_p137_cli_dry_run_export(tmp_path):
    source = tmp_path / "prompt.md"
    source.write_text("# Prompt source\n", encoding="utf-8")
    out = tmp_path / "out"

    completed = subprocess.run(
        [
            sys.executable,
            "-m",
            "mvp_qaic_py.p137_prompt_corrections_apply_queue",
            "--output-dir",
            str(out),
            "--exports-dir",
            str(tmp_path),
            "--prompt-file",
            str(source),
            "--gem-id",
            "GEM_RISK_GUARD_REVIEW",
            "--generated-at-utc",
            "2026-06-22T00:00:00Z",
            "--dry-run-export",
        ],
        check=True,
        capture_output=True,
        text=True,
    )

    assert "P137_PROMPT_CORRECTIONS_READY_FOR_HUMAN_REVIEW" in completed.stdout
    assert "GEM_RISK_GUARD_REVIEW" in completed.stdout
    assert (out / "P137_CORRECTED_GEM_PROMPT.md").exists()
    assert (out / "P137_PROMPT_CORRECTIONS_APPLY_PAYLOAD.json").exists()
