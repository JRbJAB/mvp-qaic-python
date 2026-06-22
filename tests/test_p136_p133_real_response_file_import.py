from __future__ import annotations

import json
import subprocess
import sys

import pytest

from mvp_qaic_py.p136_p133_real_response_file_import import (
    DEFAULT_GEM_ID,
    P136Request,
    build_p133_capture_command,
    build_p136_payload,
    build_stitch_ui_logic_spec,
    get_active_gem_ids,
    get_active_gem_profiles,
    validate_gem_id,
    write_p136_import_pack,
)


def test_p136_active_gem_profiles_are_controlled():
    profiles = get_active_gem_profiles()
    ids = get_active_gem_ids()

    assert DEFAULT_GEM_ID in ids
    assert profiles
    assert all(profile["status"] == "ACTIVE" for profile in profiles)
    assert len(ids) == len(set(ids))


def test_p136_rejects_inactive_or_unknown_gem():
    with pytest.raises(ValueError):
        validate_gem_id("NOT_A_REAL_GEM")


def test_p136_builds_pass_partout_p133_command(tmp_path):
    response_file = tmp_path / "response.md"
    output_dir = tmp_path / "p133"
    command = build_p133_capture_command(
        response_file=response_file,
        output_dir=output_dir,
        run_id="P136-P133",
        generated_at_utc="2026-06-22T00:00:00Z",
    )

    assert "rev-parse --show-toplevel" in command
    assert "MVP_QAIC_PY" in command
    assert "gem_multimodal_response_capture_gate" in command
    assert "--response-text" in command
    assert str(response_file) in command
    assert str(output_dir) in command


def test_p136_stitch_ui_logic_spec_is_local_only():
    gem = validate_gem_id("GEM_GENERAL_REVIEW")
    spec = build_stitch_ui_logic_spec(gem)

    assert spec["status"] == "STITCH_UI_BLUEPRINT_READY"
    assert spec["handoff_mode"] == "LOCAL_SPEC_ONLY"
    assert spec["target_runtime"] == "NiceGUI local private"
    assert spec["screens"]
    assert any(screen["screen_id"] == "response_import" for screen in spec["screens"])
    assert "no_broker" in spec["forbidden_behaviors"]
    assert "no_order" in spec["forbidden_behaviors"]
    assert "no_sizing" in spec["forbidden_behaviors"]


def test_p136_write_pack_without_response_file_creates_template(tmp_path):
    out = tmp_path / "out"
    payload = write_p136_import_pack(
        P136Request(
            output_dir=out,
            generated_at_utc="2026-06-22T00:00:00Z",
            gem_id="GEM_GENERAL_REVIEW",
        )
    )

    assert payload["status"] == "P136_REAL_RESPONSE_IMPORT_READY"
    assert payload["selected_gem"]["gem_id"] == "GEM_GENERAL_REVIEW"
    assert payload["features"]["stitch_ui_logic_integrated"] is True
    assert payload["stitch_ui_logic"]["status"] == "STITCH_UI_BLUEPRINT_READY"
    assert payload["response_import"]["source_response_file_exists"] is False
    assert (out / "P136_IMPORTED_GEM_RESPONSE.md").exists()
    assert (out / "P136_REAL_RESPONSE_FILE_IMPORT_CONTRACT.json").exists()
    assert (out / "P136_ACTIVE_GEM_PROFILES.json").exists()
    assert (out / "P136_STITCH_UI_LOGIC_SPEC.json").exists()
    assert (out / "P136_STITCH_UI_LOGIC_SPEC.md").exists()
    assert (out / "P136_P133_CAPTURE_COMMAND.ps1").exists()
    assert (out / "P136_PROMPT_CORRECTIONS_QUEUE.md").exists()
    assert (out / "P136_RUNBOOK.md").exists()


def test_p136_write_pack_with_real_response_file(tmp_path):
    source = tmp_path / "gem_response.md"
    source.write_text(
        '## Résumé lisible\n\n```json\n{"status":"REVIEW_REQUIRED"}\n```\n',
        encoding="utf-8",
    )
    out = tmp_path / "out"

    payload = write_p136_import_pack(
        P136Request(
            output_dir=out,
            response_file=source,
            generated_at_utc="2026-06-22T00:00:00Z",
            gem_id="GEM_PORTFOLIO_REVIEW",
        )
    )

    imported = out / "P136_IMPORTED_GEM_RESPONSE.md"
    assert imported.read_text(encoding="utf-8") == source.read_text(encoding="utf-8")
    assert payload["selected_gem"]["gem_id"] == "GEM_PORTFOLIO_REVIEW"
    assert payload["response_import"]["source_response_file_exists"] is True
    assert payload["response_import"]["response_char_count"] > 0
    assert payload["response_import"]["response_sha256"]

    contract = json.loads(
        (out / "P136_REAL_RESPONSE_FILE_IMPORT_CONTRACT.json").read_text(encoding="utf-8")
    )
    assert contract["features"]["active_gem_selection"] is True
    assert contract["features"]["prompt_corrections_queue"] is True
    assert contract["features"]["stitch_ui_logic_integrated"] is True
    assert "P136_R1_STITCH_UI_LOGIC_INTEGRATED" in contract["safety_markers"]


def test_p136_cli_dry_run_export(tmp_path):
    completed = subprocess.run(
        [
            sys.executable,
            "-m",
            "mvp_qaic_py.p136_p133_real_response_file_import",
            "--output-dir",
            str(tmp_path / "out"),
            "--exports-dir",
            str(tmp_path / "exports"),
            "--dry-run-export",
            "--gem-id",
            "GEM_RISK_GUARD_REVIEW",
            "--generated-at-utc",
            "2026-06-22T00:00:00Z",
        ],
        check=True,
        capture_output=True,
        text=True,
    )

    assert "P136_REAL_RESPONSE_IMPORT_READY" in completed.stdout
    assert "GEM_RISK_GUARD_REVIEW" in completed.stdout
    assert (tmp_path / "out" / "P136_REAL_RESPONSE_FILE_IMPORT_CONTRACT.json").exists()
    assert (tmp_path / "out" / "P136_P133_CAPTURE_COMMAND.ps1").exists()
    assert (tmp_path / "out" / "P136_STITCH_UI_LOGIC_SPEC.json").exists()


def test_p136_payload_safety_flags(tmp_path):
    payload = build_p136_payload(
        P136Request(
            output_dir=tmp_path / "out",
            generated_at_utc="2026-06-22T00:00:00Z",
        )
    )

    assert payload["features"]["local_private_only"] is True
    assert payload["features"]["no_broker_execution"] is True
    assert payload["features"]["no_order"] is True
    assert payload["features"]["no_sizing"] is True
    assert payload["features"]["no_auto_apply"] is True
