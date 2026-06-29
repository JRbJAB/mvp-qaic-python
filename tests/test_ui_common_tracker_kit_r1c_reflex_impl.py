from __future__ import annotations

import importlib
import json
import subprocess
import sys
from pathlib import Path

from mvp_qaic_reflex_ui.common.tracker_ui_kit import COCKPIT_RENDER_BINDINGS, REFERENCE_RENDER_TYPES

ROOT = Path(__file__).resolve().parents[1]
REQUIRED_ROUTES = {"/dev-tracking", "/cdc-dev-tracker", "/cdc-tracker"}
FORBIDDEN_MARKERS = (
    "STRUCTURE" + "_READY",
    "CONTENT" + "_TO_CONNECT",
    "cette page " + "consolidera",
    "place" + "holder",
    "st" + "ub",
)


def test_common_reflex_adapter_and_cdc_page_import() -> None:
    adapter = importlib.import_module("mvp_qaic_reflex_ui.common.tracker_reflex_kit")
    page = importlib.import_module("mvp_qaic_reflex_ui.cdc_dev_tracker_reflex_page")

    assert callable(adapter.tracker_body)
    assert callable(adapter.tracker_section)
    assert callable(page.cdc_dev_tracker_reflex_page)
    assert callable(page.cdc_tracker_reflex_page)
    assert callable(page.dev_tracking_reflex_page)


def test_cdc_page_references_common_tracker_adapter() -> None:
    text = (ROOT / "mvp_qaic_reflex_ui" / "cdc_dev_tracker_reflex_page.py").read_text(
        encoding="utf-8"
    )
    assert "common.tracker_reflex_kit" in text
    assert "tracker_body(" in text
    assert "tracker_items_from_rows(" in text


def test_required_routes_remain_registered() -> None:
    app_text = (ROOT / "mvp_qaic_reflex_ui" / "mvp_qaic_reflex_ui.py").read_text(encoding="utf-8")
    page_text = (ROOT / "mvp_qaic_reflex_ui" / "cdc_dev_tracker_reflex_page.py").read_text(
        encoding="utf-8"
    )
    tracker = json.loads(
        (ROOT / "docs" / "dev_tracking" / "DEV_LIFECYCLE_TRACKER.json").read_text(encoding="utf-8")
    )

    assert set(tracker["views"].values()) == REQUIRED_ROUTES
    for route in REQUIRED_ROUTES:
        assert route in app_text
        assert route in page_text


def test_render_reference_registry_has_required_types_and_cockpit_mapping() -> None:
    required_types = {
        "migration_tracker_reference",
        "cdc_dev_tracker",
        "dev_tracker",
        "tool_registry_cdc",
    }
    assert required_types.issubset(REFERENCE_RENDER_TYPES)

    binding_types = {binding["render_type"] for binding in COCKPIT_RENDER_BINDINGS}
    binding_routes = {binding["route"] for binding in COCKPIT_RENDER_BINDINGS}
    assert required_types.issubset(binding_types)
    assert REQUIRED_ROUTES.issubset(binding_routes)

    registry = (ROOT / "docs" / "dev_tracking" / "TRACKER_RENDER_REFERENCE_REGISTRY.md").read_text(
        encoding="utf-8"
    )
    for token in [
        "migration_tracker_reference",
        "cdc_dev_tracker",
        "dev_tracker",
        "tool_registry_cdc",
        "Concerned cockpit/page/surface",
        "Preview command/path policy",
    ]:
        assert token in registry


def test_preview_command_exists_is_documented_and_reports_reference_types(tmp_path: Path) -> None:
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

    audit = json.loads(
        (tmp_path / "tracker_ui_common_preview_audit.json").read_text(encoding="utf-8")
    )
    for render_type in [
        "migration_tracker_reference",
        "cdc_dev_tracker",
        "dev_tracker",
        "tool_registry_cdc",
    ]:
        assert render_type in audit["render_types"]

    evidence = (
        ROOT
        / "docs"
        / "dev_tracking"
        / "UI_COMMON_TRACKER_KIT_R1C_REFLEX_IMPL_EVIDENCE_20260629.md"
    ).read_text(encoding="utf-8")
    assert "python tools/render_tracker_preview.py --out" in evidence


def test_visual_gate_docs_still_require_preview_before_deploy() -> None:
    docs = "\n".join(
        [
            (ROOT / "docs" / "dev_tracking" / "TRACKER_UI_VISUAL_CONTRACT.md").read_text(
                encoding="utf-8"
            ),
            (
                ROOT
                / "docs"
                / "dev_tracking"
                / "UI_COMMON_TRACKER_KIT_R1C_REFLEX_IMPL_EVIDENCE_20260629.md"
            ).read_text(encoding="utf-8"),
            (ROOT / "docs" / "dev_tracking" / "TRACKER_RENDER_REFERENCE_REGISTRY.md").read_text(
                encoding="utf-8"
            ),
        ]
    )
    assert "Visual tests are mandatory before Reflex deployment" in docs
    assert "Visual preview remains mandatory before deployment" in docs
    assert "Bun/frontend deploy blocker still applies" in docs


def test_new_r1c2_files_have_no_forbidden_marker_text() -> None:
    paths = [
        ROOT / "mvp_qaic_reflex_ui" / "common" / "tracker_reflex_kit.py",
        ROOT / "docs" / "dev_tracking" / "TRACKER_RENDER_REFERENCE_REGISTRY.md",
        ROOT
        / "docs"
        / "dev_tracking"
        / "UI_COMMON_TRACKER_KIT_R1C_REFLEX_IMPL_EVIDENCE_20260629.md",
        ROOT / "tests" / "test_ui_common_tracker_kit_r1c_reflex_impl.py",
    ]
    for path in paths:
        text = path.read_text(encoding="utf-8").lower()
        for marker in FORBIDDEN_MARKERS:
            assert marker.lower() not in text, path
