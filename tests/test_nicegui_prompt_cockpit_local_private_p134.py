from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import pytest

from mvp_qaic_py.nicegui_prompt_cockpit_local_private import (
    DEFAULT_HOST,
    DEFAULT_PORT,
    SAFETY_MARKERS,
    PromptCockpitRequest,
    build_prompt_cockpit_payload,
    discover_prompt_cockpit_sources,
    write_prompt_cockpit_pack,
)


def _make_p132_r2_export(exports: Path) -> Path:
    folder = exports / "P132_R2_PRETTY_JSON_PROMPT_SYNC_20260622_184031"
    folder.mkdir(parents=True)
    prompt = folder / "P132_GEM_MULTIMODAL_PORTFOLIO_PROMPT.md"
    prompt.write_text(
        "# P132 GEM Multimodal Portfolio Prompt — Revolut X / USD\n\n"
        "## Résumé lisible\n\n"
        "## JSON strict pretty-printed\n\n"
        '```json\n{\n  "status": "REVIEW_REQUIRED"\n}\n```\n',
        encoding="utf-8",
    )
    return prompt


def _make_p133_export(exports: Path) -> Path:
    folder = exports / "P133_REAL_GEM_RESPONSE_CAPTURE_IMAGE_USAGE_GATE_20260622_190000"
    folder.mkdir(parents=True)
    gate = folder / "P133_GEM_RESPONSE_CAPTURE_GATE.json"
    gate.write_text(
        json.dumps({"gate_status": "PASS_WITH_HUMAN_REVIEW"}, indent=2),
        encoding="utf-8",
    )
    (folder / "P133_GEM_RESPONSE_HUMAN_REVIEW.md").write_text("# Review\n", encoding="utf-8")
    (folder / "P133_GEM_RESPONSE_PRETTY.json").write_text("{}\n", encoding="utf-8")
    return gate


def test_p134_discovers_latest_p132_and_p133_sources(tmp_path):
    exports = tmp_path / "05_EXPORTS"
    prompt = _make_p132_r2_export(exports)
    gate = _make_p133_export(exports)

    sources = discover_prompt_cockpit_sources(
        PromptCockpitRequest(output_dir=tmp_path / "out", exports_dir=exports)
    )

    assert sources["prompt_exists"] is True
    assert sources["p133_gate_exists"] is True
    assert sources["latest_prompt_path"] == str(prompt)
    assert sources["latest_p133_gate_path"] == str(gate)


def test_p134_payload_is_local_private_and_safe(tmp_path):
    exports = tmp_path / "05_EXPORTS"
    _make_p132_r2_export(exports)

    payload = build_prompt_cockpit_payload(
        PromptCockpitRequest(
            output_dir=tmp_path / "out",
            exports_dir=exports,
            generated_at_utc="2026-06-22T00:00:00Z",
        )
    )

    assert payload["status"] == "NICEGUI_PROMPT_COCKPIT_LOCAL_PRIVATE_READY"
    assert payload["host"] == DEFAULT_HOST
    assert payload["port"] == DEFAULT_PORT
    assert payload["local_url"] == "http://127.0.0.1:8088"
    assert payload["features"]["no_public_deploy"] is True
    assert payload["features"]["no_sheet_write"] is True
    assert payload["features"]["no_broker_execution"] is True
    assert "LOCAL_PRIVATE_ONLY" in payload["safety_markers"]
    assert "NO_PUBLIC_DEPLOY" in payload["safety_markers"]
    assert "NO_REVOLUTX_REAL_ACCESS_FROM_MVP" in payload["safety_markers"]


def test_p134_rejects_public_host(tmp_path):
    with pytest.raises(ValueError, match="local-private only"):
        build_prompt_cockpit_payload(
            PromptCockpitRequest(output_dir=tmp_path / "out", host="0.0.0.0")
        )


def test_p134_rejects_invalid_port(tmp_path):
    with pytest.raises(ValueError, match="port"):
        build_prompt_cockpit_payload(PromptCockpitRequest(output_dir=tmp_path / "out", port=80))


def test_p134_writes_contract_runbook_preview_and_prompt_copy(tmp_path):
    exports = tmp_path / "05_EXPORTS"
    _make_p132_r2_export(exports)

    out = tmp_path / "out"
    payload = write_prompt_cockpit_pack(
        PromptCockpitRequest(
            output_dir=out,
            exports_dir=exports,
            generated_at_utc="2026-06-22T00:00:00Z",
        )
    )

    assert payload["sources"]["prompt_exists"] is True
    assert (out / "P134_NICEGUI_PROMPT_COCKPIT_CONTRACT.json").exists()
    assert (out / "P134_NICEGUI_PROMPT_COCKPIT_RUNBOOK.md").exists()
    assert (out / "P134_NICEGUI_PROMPT_COCKPIT_STATIC_PREVIEW.html").exists()
    assert (out / "P134_LATEST_P132_PROMPT_COPY.md").exists()

    contract = json.loads(
        (out / "P134_NICEGUI_PROMPT_COCKPIT_CONTRACT.json").read_text(encoding="utf-8")
    )
    assert contract["local_url"] == "http://127.0.0.1:8088"
    assert contract["features"]["run_p133_gate_instruction"] is True

    runbook = (out / "P134_NICEGUI_PROMPT_COCKPIT_RUNBOOK.md").read_text(encoding="utf-8")
    assert "Local privé uniquement" in runbook
    assert "python -m mvp_qaic_py.nicegui_prompt_cockpit_local_private --launch" in runbook


def test_p134_module_import_does_not_require_nicegui():
    assert "NO_PUBLIC_DEPLOY" in SAFETY_MARKERS
    assert "NO_ORDER" in SAFETY_MARKERS
    assert "P132_R2_PROMPT_SOURCE" in SAFETY_MARKERS


def test_p134_cli_dry_run_export(tmp_path):
    exports = tmp_path / "05_EXPORTS"
    _make_p132_r2_export(exports)

    completed = subprocess.run(
        [
            sys.executable,
            "-m",
            "mvp_qaic_py.nicegui_prompt_cockpit_local_private",
            "--output-dir",
            str(tmp_path / "out"),
            "--exports-dir",
            str(exports),
            "--dry-run-export",
            "--generated-at-utc",
            "2026-06-22T00:00:00Z",
        ],
        check=True,
        capture_output=True,
        text=True,
    )

    assert "NICEGUI_PROMPT_COCKPIT_LOCAL_PRIVATE_READY" in completed.stdout
    assert "http://127.0.0.1:8088" in completed.stdout
    assert (tmp_path / "out" / "P134_NICEGUI_PROMPT_COCKPIT_CONTRACT.json").exists()
