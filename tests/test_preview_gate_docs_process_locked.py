from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOC_DIR = ROOT / "docs" / "dev_tracking"

DOCS = [
    DOC_DIR / "REFLEX_PREVIEW_GATE_MANDATORY_INSTRUCTIONS.md",
    DOC_DIR / "CDC_DEV_TRACKER_WEB_ARCHITECTURE.md",
    DOC_DIR / "DOCS_MAINTENANCE_PROTOCOL.md",
    DOC_DIR / "DOCS_CLEANUP_AGENDA_20260629.md",
    DOC_DIR / "FINAL_LIVE_INSTRUCTIONS_CDC_DEV_TRACKER.md",
    DOC_DIR / "CDC_DEV_TRACKER_PREVIEW_RENDER_AUDIT_20260629.md",
]


def _corpus() -> str:
    return "\n".join(path.read_text(encoding="utf-8") for path in DOCS)


def test_preview_gate_docs_exist() -> None:
    missing = [str(path) for path in DOCS if not path.exists()]
    assert not missing


def test_visual_tests_are_mandatory_before_reflex_deployment() -> None:
    text = _corpus()
    assert "Visual tests are mandatory before Reflex deployment" in text
    assert "No Reflex deployment is allowed" in text
    assert "No public deploy without browser/runtime visual evidence" in text


def test_cdc_dev_tracker_uses_migration_tracker_visual_oracle() -> None:
    text = _corpus()
    assert "Migration Tracker is the visual oracle" in text
    assert "CDC Dev Tracker preview must be visually coherent" in text
    assert "Generic HTML preview" in text
    assert "not accepted as release evidence" in text


def test_docs_process_is_locked_for_future_changes() -> None:
    text = _corpus()
    assert "must update the relevant docs in the same commit" in text
    assert "The operator must not need to remind" in text
    assert "Do not mark DONE if docs are queued but not updated" in text


def test_cdc_web_architecture_mentions_routes_sources_and_runtime_blocker() -> None:
    text = (DOC_DIR / "CDC_DEV_TRACKER_WEB_ARCHITECTURE.md").read_text(encoding="utf-8")
    for token in [
        "/dev-tracking",
        "/cdc-dev-tracker",
        "/cdc-tracker",
        "V25_CDC_DELIVERY_TRACKER",
        "DEV_LIFECYCLE_TRACKER.json",
        "Frontend Reflex runtime: blocked by Bun install crash",
    ]:
        assert token in text
