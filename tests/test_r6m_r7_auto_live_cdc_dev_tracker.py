from __future__ import annotations

import json
from pathlib import Path

from mvp_qaic_reflex_ui.dev_lifecycle_tracker import (
    STATUS_READY,
    build_dev_lifecycle_model,
    dev_lifecycle_tracker_panel,
)


FORBIDDEN_MARKERS = ("structure" + "_ready", "content" + "_to_connect")


def test_r6m_r7_lifecycle_contract_covers_past_active_future() -> None:
    model = build_dev_lifecycle_model()

    assert model["status"] == STATUS_READY
    assert model["counts"]["done"] >= 3
    assert model["counts"]["active"] >= 1
    assert model["counts"]["next"] >= 3
    assert "R6J" in model["done_phase_ids"]
    assert "R6K" in model["done_phase_ids"]
    assert "R6L" in model["done_phase_ids"]
    assert "R6M" in model["done_phase_ids"]
    assert "R6N" in model["active_phase_ids"]


def test_r6m_r7_evidence_contains_real_heads_tags_and_no_shell_status() -> None:
    model = build_dev_lifecycle_model()
    joined = " ".join(
        " ".join(
            str(row.get(key, ""))
            for key in ("phase_id", "title", "head", "tag", "tests", "evidence", "next_action")
        )
        for row in model["phases"]
    )
    lowered = joined.lower()

    assert "d94256b1b4a6" in joined
    assert "b4556e1c4fff" in joined
    assert "mvp-qaic-reflex-r6j-real-cdc-dev-tracker-cockpit" in joined
    assert "mvp-qaic-reflex-r6k-global-migration-decision-workbench" in joined
    for marker in FORBIDDEN_MARKERS:
        assert marker not in lowered
    assert "route-only" in lowered


def test_r6m_r7_git_live_state_is_present() -> None:
    model = build_dev_lifecycle_model()
    git = model["git"]

    assert len(git["head"]) >= 7
    assert git["branch"] == "master"
    assert isinstance(git["dirty_count"], int)
    assert isinstance(git["recent_commits"], list)


def test_r6m_r7_json_source_is_versioned_and_clean() -> None:
    path = Path("docs/dev_tracking/DEV_LIFECYCLE_TRACKER.json")
    payload = json.loads(path.read_text(encoding="utf-8"))
    text = path.read_text(encoding="utf-8").lower()

    assert payload["schema_version"] == "R6N_VERTICAL_MIGRATION_STYLE_LIFECYCLE"
    assert payload["status"] == STATUS_READY
    assert "past_phases" in payload["required_coverage"]
    assert "active_phases" in payload["required_coverage"]
    assert "future_phases" in payload["required_coverage"]
    for marker in FORBIDDEN_MARKERS:
        assert marker not in text


def test_r6m_r7_dev_tracking_page_is_overridden_by_live_model() -> None:
    text = Path("mvp_qaic_reflex_ui/pages_landing.py").read_text(encoding="utf-8")

    assert "BEGIN_R6M_R7_AUTO_LIVE_DEV_TRACKING_OVERRIDE" in text
    assert "dev_lifecycle_tracker_page" in text
    assert "READY_AUTO_LIVE_CDC_DEV_TRACKER" not in text


def test_r6m_r7_cdc_pages_include_lifecycle_panel() -> None:
    text = Path("mvp_qaic_reflex_ui/cdc_dev_tracker_reflex_page.py").read_text(encoding="utf-8")

    assert "BEGIN_R6M_R7_AUTO_LIVE_CDC_LIFECYCLE_PANEL" in text
    assert "dev_lifecycle_tracker_panel" in text
    assert "cdc_dev_tracker_reflex_page" in text
    assert "cdc_tracker_reflex_page" in text


def test_r6m_r7_panel_is_content_model_not_shell() -> None:
    panel = dev_lifecycle_tracker_panel(compact=True)
    assert panel is not None
    model = build_dev_lifecycle_model()
    assert "R6M" in model["done_phase_ids"]
    assert model["active_phase_ids"] == ["R6N"]
