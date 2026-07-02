from __future__ import annotations

import re
import subprocess
from pathlib import Path

import pytest

from mvp_qaic_py.cockpit_queue_local_preview_r21n import (
    PREVIEW_HTML_FILENAME,
    build_local_preview_payload,
    render_local_preview_html,
    render_local_preview_manifest,
    validate_preview_output_path,
    write_local_preview,
)


R21N_FILES = (
    Path("mvp_qaic_py/cockpit_queue_local_preview_r21n.py"),
    Path("docs/PRODUCT/R21N_LOCAL_COCKPIT_PREVIEW_NO_RUNTIME.md"),
    Path("tests/test_r21n_cockpit_queue_local_preview.py"),
)

TRACE_TOKENS = (
    "BRAND_CONFIG_TRACE_COCKPIT_READY",
    "UI_TRACKER_TRACE_COCKPIT_READY",
    "TOOL_REGISTRY_CDC_TRACE_COCKPIT_READY",
    "CDC_CONTRACT_TRACE_COCKPIT_READY",
    "QAIC_BRIDGE_TRACE_COCKPIT_READY",
)


def test_payload_contains_r21k_r21l_r21m_source_binding_markers() -> None:
    payload = build_local_preview_payload()
    bindings = payload["source_bindings"]

    assert bindings["SOURCE_R21K_CONTRACT_BOUND"] is True
    assert bindings["SOURCE_R21L_MODEL_BINDING_BOUND"] is True
    assert bindings["SOURCE_R21M_VISUAL_PLANNING_BOUND"] is True
    assert payload["r21k_contract"]["contract_id"] == "R21K_COCKPIT_QUEUE_DATA_CONTRACT_NO_RUNTIME"
    assert payload["r21l_model"]["model_id"] == "R21L_COCKPIT_QUEUE_MODEL_BINDING_NO_RUNTIME"
    assert payload["r21m_visual_plan"]["workflow_id"] == (
        "R21M_COCKPIT_QUEUE_VISUAL_PLANNING_NO_RUNTIME"
    )


def test_html_render_contains_required_cockpit_trace_tokens() -> None:
    html = render_local_preview_html()

    for token in TRACE_TOKENS:
        assert token in html
    assert "NO-RUNTIME SAFETY BANNER" in html
    assert "Review queue / QAIC handoff" in html


def test_brand_config_trace_is_present_and_preserves_validated_assets() -> None:
    payload = build_local_preview_payload()
    html = render_local_preview_html(payload)
    brand = payload["brand_config"]

    assert brand["QAIT_CHARTE_TEMPLATE"] == "BOUND"
    assert brand["MVP_QAIC_LOGO_VALIDATED"] == "BOUND"
    assert brand["preserve_q_candlesticks_signal_line"] is True
    assert "logo-mvp-qaic-official-name.png" in html
    assert "logo-mvp-qaic-icon-only.png" in html
    assert "charte-graphique.png" in html
    assert "preserve_q_candlesticks_signal_line" in html


def test_manifest_declares_run_report_only_policy() -> None:
    manifest = render_local_preview_manifest()

    assert manifest["output_policy"]["LOCAL_PREVIEW_RENDERER"] is True
    assert manifest["output_policy"]["NO_COMMITTED_HTML_OUTPUT"] is True
    assert manifest["output_policy"]["PREVIEW_OUTPUT_RUN_REPORT_ONLY"] is True
    assert manifest["output_policy"]["NO_05_EXPORTS"] is True


def test_write_local_preview_rejects_repo_public_docs_and_export_paths(tmp_path: Path) -> None:
    forbidden_paths = (
        Path.cwd() / "_RUN_REPORTS" / "R21N",
        Path.cwd() / "public" / "_RUN_REPORTS" / "R21N",
        Path.cwd() / "docs" / "_RUN_REPORTS" / "R21N",
        Path.cwd().parent / "05_EXPORTS" / "_RUN_REPORTS" / "R21N",
        tmp_path / "arbitrary" / "R21N",
    )

    for target in forbidden_paths:
        with pytest.raises(ValueError):
            validate_preview_output_path(target)


def test_write_local_preview_allows_supplied_run_reports_path(tmp_path: Path) -> None:
    out_dir = tmp_path / "_RUN_REPORTS" / "MVP_QAIC_PY" / "R21N"
    result = write_local_preview(out_dir)

    assert result["LOCAL_PREVIEW_RENDERER"] is True
    assert (out_dir / PREVIEW_HTML_FILENAME).exists()
    assert "BRAND_CONFIG_TRACE_COCKPIT_READY" in (out_dir / PREVIEW_HTML_FILENAME).read_text(
        encoding="utf-8"
    )


def test_r21n_files_have_no_forbidden_runtime_strings() -> None:
    forbidden = (
        r"\b" + "reflex" + r"\s+" + "run" + r"\b",
        r"\b" + "docker" + r"\s+" + "run" + r"\b",
        "--frontend" + "-host",
        "provider_call_allowed" + "=True",
        "broker_order_sizing_allowed" + "=True",
        "sheet_bq_write_allowed" + "=True",
        "execution_allowed" + "=True",
    )

    for target in R21N_FILES:
        text = target.read_text(encoding="utf-8")
        for pattern in forbidden:
            assert re.search(pattern, text, flags=re.IGNORECASE) is None


def test_no_r21n_generated_html_file_is_tracked() -> None:
    tracked = subprocess.run(
        ["git", "ls-files", "*.html"],
        check=True,
        capture_output=True,
        text=True,
    ).stdout.splitlines()

    assert all("r21n" not in path.lower() for path in tracked)
    assert all("local_cockpit_preview" not in path.lower() for path in tracked)
