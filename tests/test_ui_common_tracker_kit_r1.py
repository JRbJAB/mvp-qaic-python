from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

from mvp_qaic_reflex_ui.common.tracker_ui_kit import (
    COCKPIT_RENDER_BINDINGS,
    REFERENCE_RENDER_TYPES,
    TrackerItem,
    render_preview_page,
)

ROOT = Path(__file__).resolve().parents[1]


def test_reference_render_types_cover_required_tracker_cockpits() -> None:
    assert "migration_tracker_oracle" in REFERENCE_RENDER_TYPES
    assert "cdc_tracker" in REFERENCE_RENDER_TYPES
    assert "dev_tracker" in REFERENCE_RENDER_TYPES
    assert "tool_registry_tracker" in REFERENCE_RENDER_TYPES

    binding_routes = {binding["route"] for binding in COCKPIT_RENDER_BINDINGS}
    assert "/dev-tracking" in binding_routes
    assert "/cdc-dev-tracker" in binding_routes
    assert "/cdc-tracker" in binding_routes


def test_preview_page_splits_cdc_tracker_and_dev_tracker() -> None:
    cdc_items = [TrackerItem("cdc_step", "CDC step", "DONE", 100, "CDC delivery", "/cdc-tracker")]
    dev_items = [
        TrackerItem("dev_phase", "Dev phase", "ACTIVE", 70, "Dev lifecycle", "/dev-tracking")
    ]
    html = render_preview_page(
        title="Test",
        cdc_items=cdc_items,
        dev_items=dev_items,
        generated_at="now",
        source_note="test",
    )
    assert "CDC Tracker" in html
    assert "Dev Tracker" in html
    assert 'data-render-type="cdc_tracker"' in html
    assert 'data-render-type="dev_tracker"' in html
    assert "progress-bar blue" in html
    assert "100%" in html
    assert "70%" in html
    assert "Migration Tracker Visual Oracle" in html


def test_render_tracker_preview_cli_generates_full_lifecycle_preview(tmp_path: Path) -> None:
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

    html_path = tmp_path / "tracker_ui_common_preview.html"
    audit_path = tmp_path / "tracker_ui_common_preview_audit.json"
    assert html_path.exists()
    assert audit_path.exists()

    html = html_path.read_text(encoding="utf-8")
    audit = json.loads(audit_path.read_text(encoding="utf-8"))

    assert audit["visual_oracle"] == "migration_tracker"
    assert audit["requires_browser_runtime_before_deploy"] is True

    for token in [
        "CDC Tracker",
        "Dev Tracker",
        "Migration Tracker Visual Oracle",
        "/dev-tracking",
        "/cdc-dev-tracker",
        "/cdc-tracker",
        "progress-bar blue",
        'data-ui-kit="tracker-common"',
    ]:
        assert token in html

    tracker_path = ROOT / "docs" / "dev_tracking" / "DEV_LIFECYCLE_TRACKER.json"
    tracker = json.loads(tracker_path.read_text(encoding="utf-8"))
    phases = tracker.get("phases", [])
    if isinstance(phases, dict):
        phases = list(phases.values())

    phase_ids = [
        str(phase.get("phase_id") or phase.get("id") or "")
        for phase in phases
        if isinstance(phase, dict)
    ]
    missing = [phase_id for phase_id in phase_ids if phase_id and phase_id not in html]
    assert not missing

    assert "font-family: Arial" not in html
    assert "background: #0f172a" not in html


def test_visual_contract_doc_locks_no_repetition_process() -> None:
    doc = (ROOT / "docs" / "dev_tracking" / "TRACKER_UI_VISUAL_CONTRACT.md").read_text(
        encoding="utf-8"
    )
    assert "Migration Tracker is the visual oracle" in doc
    assert "blue progress bars" in doc
    assert "percent per phase or step" in doc
    assert "Visual tests are mandatory before Reflex deployment" in doc
