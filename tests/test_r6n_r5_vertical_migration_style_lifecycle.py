from __future__ import annotations

from pathlib import Path

from mvp_qaic_reflex_ui.dev_lifecycle_tracker import (
    STATUS_READY,
    build_dev_lifecycle_model,
    cdc_lifecycle_tracker_panel,
    dev_lifecycle_tracker_panel,
)


FORBIDDEN_MARKERS = (
    "structure" + "_ready",
    "content" + "_to_connect",
    "cette page " + "consolidera",
)


def test_r6n_r5_lifecycle_has_all_past_active_next_future_phases() -> None:
    model = build_dev_lifecycle_model()
    ids = [row["phase_id"] for row in model["phases"]]

    assert model["status"] == STATUS_READY
    assert model["ui_contract"] == "VERTICAL_MIGRATION_TRACKER_STYLE"
    assert model["phase_count"] >= 12
    assert (
        ids.index("FOUNDATION_HISTORY")
        < ids.index("R6J")
        < ids.index("R6K")
        < ids.index("R6L")
        < ids.index("R6M")
        < ids.index("R6N")
    )
    assert "R6M" in model["done_phase_ids"]
    assert "R6N" in model["done_phase_ids"]
    assert "R6P" in model["done_phase_ids"]
    assert "R6P" not in model["next_phase_ids"]
    assert "R6Q" in model["done_phase_ids"]
    assert "R6Q" not in model["next_phase_ids"]
    assert {"R6R", "PRIVATE_RC", "PUBLIC_READY_FUTURE"}.issubset(set(model["next_phase_ids"]))


def test_r6n_r5_evidence_contains_real_sealed_heads_and_tags() -> None:
    model = build_dev_lifecycle_model()
    joined = " ".join(
        row["phase_id"] + " " + row["evidence"] + " " + row["tests"] + " " + row.get("tag", "")
        for row in model["phases"]
    ).lower()

    assert "d94256b1b4a6" in joined
    assert "b4556e1c4fff" in joined
    assert "10348edcec37" in joined
    assert "mvp-qaic-reflex-r6m-auto-live-cdc-dev-tracker" in joined
    for marker in FORBIDDEN_MARKERS:
        assert marker not in joined


def test_r6n_r5_panels_are_vertical_migration_style_not_shell() -> None:
    dev_panel = dev_lifecycle_tracker_panel(compact=True)
    cdc_panel = cdc_lifecycle_tracker_panel(compact=True)
    assert dev_panel is not None
    assert cdc_panel is not None

    source = Path("mvp_qaic_reflex_ui/dev_lifecycle_tracker.py").read_text(encoding="utf-8").lower()
    assert "vertical_migration_tracker_style" in source
    assert "progress_percent" in source
    assert "border_left" in source
    assert "migration tracker" in source
    for marker in FORBIDDEN_MARKERS[:2]:
        assert marker not in source


def test_r6n_r5_pages_are_wired_to_vertical_lifecycle_panel() -> None:
    landing = Path("mvp_qaic_reflex_ui/pages_landing.py").read_text(encoding="utf-8")
    cdc = Path("mvp_qaic_reflex_ui/cdc_dev_tracker_reflex_page.py").read_text(encoding="utf-8")

    assert "R6N-R5_BEGIN_VERTICAL_MIGRATION_STYLE_DEV_TRACKING" in landing
    assert "dev_lifecycle_tracker_panel(compact=False" in landing
    assert "R6N-R5_BEGIN_VERTICAL_MIGRATION_STYLE_CDC_TRACKER" in cdc
    assert "cdc_lifecycle_tracker_panel(compact=False" in cdc
