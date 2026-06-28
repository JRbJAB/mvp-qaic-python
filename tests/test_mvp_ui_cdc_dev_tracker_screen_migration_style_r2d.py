from __future__ import annotations

import json
from pathlib import Path

from mvp_qaic_reflex_ui.cdc_dev_tracker_screen_migration_style import (
    SCREEN_ROUTE,
    SCREEN_SECTIONS,
    assert_screen_contract,
    build_cdc_dev_tracker_screen_model,
)


def test_screen_model_uses_expected_route_and_style() -> None:
    model = build_cdc_dev_tracker_screen_model()
    assert model["screen_route"] == SCREEN_ROUTE
    assert model["ui_style_source"] == "MIGRATION_TRACKER"
    assert model["runtime_free_default"] is True


def test_screen_model_contains_migration_tracker_sections() -> None:
    model = build_cdc_dev_tracker_screen_model()
    assert tuple(model["sections"]) == SCREEN_SECTIONS
    assert model["summary_kpi_bar"]["total_rows"] >= 2
    assert model["cdc_tracker_table"]
    assert model["dev_tracker_table"]


def test_screen_contract_assertion_accepts_default_model() -> None:
    model = build_cdc_dev_tracker_screen_model()
    assert_screen_contract(model)


def test_detail_panel_can_select_a_tracker_row() -> None:
    model = build_cdc_dev_tracker_screen_model("CDC-001")
    assert model["detail_panel"]["tracker_id"] == "CDC-001"


def test_status_and_sample_json_are_valid() -> None:
    status_path = Path(
        "docs/mvp_ui/"
        "MVP_UI_CDC_DEV_TRACKER_SCREEN_MIGRATION_STYLE_R2D_STATUS.json"
    )
    sample_path = Path(
        "docs/mvp_ui/samples/"
        "MVP_UI_CDC_DEV_TRACKER_SCREEN_MIGRATION_STYLE_R2D_SAMPLE.json"
    )
    status = json.loads(status_path.read_text(encoding="utf-8"))
    sample = json.loads(sample_path.read_text(encoding="utf-8"))
    assert status["no_runtime"] is True
    assert status["no_archive"] is True
    assert sample["qait_handoff_guard"]["required"] is True
