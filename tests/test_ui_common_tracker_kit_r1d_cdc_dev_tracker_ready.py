from __future__ import annotations

import importlib
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOC_DIR = ROOT / "docs" / "dev_tracking"
FORBIDDEN_MARKERS = (
    "STRUCTURE" + "_READY",
    "CONTENT" + "_TO_CONNECT",
    "cette page " + "consolidera",
    "place" + "holder",
    "st" + "ub",
)


def test_r1d_preview_cli_generates_required_cdc_and_dev_tracker_html(tmp_path: Path) -> None:
    result = subprocess.run(
        [
            sys.executable,
            str(ROOT / "tools" / "render_tracker_preview.py"),
            "--out",
            str(tmp_path),
        ],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    assert result.returncode == 0, result.stderr + result.stdout
    assert "PREVIEW_FILE=" in result.stdout

    html_path = tmp_path / "tracker_ui_common_preview.html"
    assert html_path.exists()
    html = html_path.read_text(encoding="utf-8")

    for token in [
        "CDC Tracker",
        "Dev Tracker",
        "/dev-tracking",
        "/cdc-dev-tracker",
        "/cdc-tracker",
        "%",
        "progress",
        "--blue",
        "runtime_browser_visual_smoke_future",
        "Lifecycle Tracker",
        "Cockpit coverage",
    ]:
        assert token in html


def test_r1d_reflex_tracker_modules_import_successfully() -> None:
    page = importlib.import_module("mvp_qaic_reflex_ui.cdc_dev_tracker_reflex_page")
    kit = importlib.import_module("mvp_qaic_reflex_ui.common.tracker_reflex_kit")

    assert callable(page.cdc_dev_tracker_reflex_page)
    assert callable(page.cdc_tracker_reflex_page)
    assert callable(page.dev_tracking_reflex_page)
    assert callable(kit.tracker_body)
    assert callable(kit.tracker_section)


def test_r1d_runtime_readiness_selector_emits_json_without_runtime(tmp_path: Path) -> None:
    out_path = tmp_path / "runtime_readiness.json"
    result = subprocess.run(
        [
            sys.executable,
            str(ROOT / "tools" / "check_reflex_runtime_readiness.py"),
            "--out",
            str(out_path),
        ],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    assert result.returncode == 0, result.stderr + result.stdout
    assert "RUNTIME_READY=" in result.stdout
    assert "STATUS=" in result.stdout
    assert out_path.exists()

    report = json.loads(out_path.read_text(encoding="utf-8"))
    assert isinstance(report["runtime_ready"], bool)
    assert isinstance(report["blockers"], list)
    assert report["policy"]["process_free"] is True
    assert report["policy"]["no_bun"] is True
    assert report["policy"]["no_npm"] is True
    assert report["policy"]["no_reflex"] is True
    assert report["policy"]["no_browser"] is True
    assert report["policy"]["no_deploy"] is True

    if not report["checks"]["react_router_bin_exists"]:
        assert report["runtime_ready"] is False
        blocker_text = " ".join(report["blockers"]).lower()
        assert "frontend" in blocker_text or "react-router" in blocker_text


def test_r1d_evidence_docs_and_registry_lock_visual_gate_and_public_block() -> None:
    evidence = (
        DOC_DIR / "UI_COMMON_TRACKER_KIT_R1D_CDC_DEV_TRACKER_READY_EVIDENCE_20260629.md"
    ).read_text(encoding="utf-8")
    registry = (DOC_DIR / "TRACKER_RENDER_REFERENCE_REGISTRY.md").read_text(encoding="utf-8")
    corpus = evidence + "\n" + registry

    for token in [
        "CDC Tracker and Dev Tracker are implemented through the common tracker kit",
        "The preview oracle is `tools/render_tracker_preview.py`",
        "Visual tests are mandatory before Reflex deployment",
        "Public deploy is still blocked until real browser/runtime visual smoke passes",
        "C:\\JRb_TRADING_OS\\_RUN_REPORTS\\MVP_QAIC_PY",
        "migration_tracker_oracle",
        "cdc_dev_tracker_common_preview",
        "runtime_browser_visual_smoke_future",
        "CDC Tracker",
        "Dev Tracker",
        "Tool Registry CDC",
        "Lifecycle Tracker",
    ]:
        assert token in corpus


def test_r1d_new_artifacts_have_no_forbidden_generic_tokens(tmp_path: Path) -> None:
    subprocess.run(
        [
            sys.executable,
            str(ROOT / "tools" / "render_tracker_preview.py"),
            "--out",
            str(tmp_path),
        ],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=True,
    )
    paths = [
        DOC_DIR / "UI_COMMON_TRACKER_KIT_R1D_CDC_DEV_TRACKER_READY_EVIDENCE_20260629.md",
        DOC_DIR / "TRACKER_RENDER_REFERENCE_REGISTRY.md",
        ROOT / "tools" / "check_reflex_runtime_readiness.py",
        tmp_path / "tracker_ui_common_preview.html",
    ]
    for path in paths:
        text = path.read_text(encoding="utf-8").lower()
        for marker in FORBIDDEN_MARKERS:
            assert marker.lower() not in text, path
