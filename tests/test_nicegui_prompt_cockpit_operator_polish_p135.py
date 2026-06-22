from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

from mvp_qaic_py.nicegui_prompt_cockpit_local_private import (
    SAFETY_MARKERS,
    PromptCockpitRequest,
    build_operator_polish_payload,
    build_p133_capture_command,
    write_operator_polish_pack,
)


def test_p135_safety_markers_are_present():
    assert "P135_OPERATOR_POLISH" in SAFETY_MARKERS
    assert "PROMPT_COPY_BUTTON" in SAFETY_MARKERS
    assert "GEM_RESPONSE_LOCAL_SAVE" in SAFETY_MARKERS
    assert "P133_COMMAND_PREVIEW" in SAFETY_MARKERS
    assert "NO_BROWSER_CLIPBOARD_REQUIRED" in SAFETY_MARKERS


def test_p135_builds_p133_capture_command(tmp_path):
    response_file = tmp_path / "response.md"
    output_dir = tmp_path / "p133"
    command = build_p133_capture_command(
        response_file=response_file,
        output_dir=output_dir,
        run_id="P135-P133",
        generated_at_utc="2026-06-22T00:00:00Z",
    )

    assert "gem_multimodal_response_capture_gate" in command
    assert "--response-text" in command
    assert str(response_file) in command
    assert str(output_dir) in command
    assert "P135-P133" in command
    assert "P133_GEM_RESPONSE_HUMAN_REVIEW.md" in command


def test_p135_operator_payload_extends_p134_payload(tmp_path):
    payload = build_operator_polish_payload(
        PromptCockpitRequest(
            output_dir=tmp_path / "out",
            generated_at_utc="2026-06-22T00:00:00Z",
        )
    )

    assert payload["status"] == "NICEGUI_PROMPT_COCKPIT_LOCAL_PRIVATE_READY"
    assert payload["p135_operator_polish"]["status"] == "OPERATOR_POLISH_READY"
    assert payload["p135_operator_polish"]["ux_features"]["prompt_copy_button"] is True
    assert payload["p135_operator_polish"]["ux_features"]["p133_command_preview"] is True
    assert payload["p135_operator_polish"]["ux_features"]["no_clipboard_roundtrip_required"] is True
    assert payload["features"]["no_broker_execution"] is True


def test_p135_write_operator_polish_pack(tmp_path):
    out = tmp_path / "out"
    payload = write_operator_polish_pack(
        PromptCockpitRequest(
            output_dir=out,
            generated_at_utc="2026-06-22T00:00:00Z",
        )
    )

    assert payload["p135_operator_polish"]["status"] == "OPERATOR_POLISH_READY"
    assert (out / "P135_OPERATOR_POLISH_CONTRACT.json").exists()
    assert (out / "P135_P133_CAPTURE_COMMAND.ps1").exists()
    assert (out / "P135_GEM_RESPONSE_INPUT.md").exists()
    assert (out / "P135_OPERATOR_POLISH_RUNBOOK.md").exists()

    contract = json.loads((out / "P135_OPERATOR_POLISH_CONTRACT.json").read_text(encoding="utf-8"))
    assert contract["p135_operator_polish"]["ux_features"]["prompt_copy_button"] is True
    assert "P133_FROM_P135_OPERATOR_POLISH" in contract["p135_operator_polish"]["p133_output_dir"]


def test_p135_source_has_operator_ui_cards_and_copy_button():
    source = Path("mvp_qaic_py/nicegui_prompt_cockpit_local_private.py").read_text(encoding="utf-8")
    assert "Copier le prompt" in source
    assert "Commande P133 locale" in source
    assert "navigator.clipboard.writeText" in source
    assert '@ui.page("/")' in source


def test_p135_cli_dry_run_writes_operator_polish_pack(tmp_path):
    completed = subprocess.run(
        [
            sys.executable,
            "-m",
            "mvp_qaic_py.nicegui_prompt_cockpit_local_private",
            "--output-dir",
            str(tmp_path / "out"),
            "--exports-dir",
            str(tmp_path / "exports"),
            "--dry-run-export",
            "--generated-at-utc",
            "2026-06-22T00:00:00Z",
        ],
        check=True,
        capture_output=True,
        text=True,
    )

    assert "NICEGUI_PROMPT_COCKPIT_LOCAL_PRIVATE_READY" in completed.stdout
    assert (tmp_path / "out" / "P135_OPERATOR_POLISH_CONTRACT.json").exists()
    assert (tmp_path / "out" / "P135_P133_CAPTURE_COMMAND.ps1").exists()


def test_p135_r2_pack_keeps_p134_compatibility_files(tmp_path):
    out = tmp_path / "out"
    payload = write_operator_polish_pack(
        PromptCockpitRequest(
            output_dir=out,
            generated_at_utc="2026-06-22T00:00:00Z",
        )
    )

    assert payload["p135_operator_polish"]["status"] == "OPERATOR_POLISH_READY"
    assert (out / "P134_NICEGUI_PROMPT_COCKPIT_CONTRACT.json").exists()
    assert (out / "P134_NICEGUI_PROMPT_COCKPIT_RUNBOOK.md").exists()
    assert (out / "P134_NICEGUI_PROMPT_COCKPIT_STATIC_PREVIEW.html").exists()
    assert (out / "P134_LATEST_P132_PROMPT_COPY.md").exists()
    assert (out / "P135_OPERATOR_POLISH_CONTRACT.json").exists()
    assert (out / "P135_P133_CAPTURE_COMMAND.ps1").exists()
