from __future__ import annotations

import json
from pathlib import Path

from mvp_qaic_reflex_ui.cdc_dev_tracker_migration_style import (
    default_tracker_rows,
    migration_style_contract,
    tracker_rows_as_dicts,
    tracker_summary,
)
from mvp_qaic_reflex_ui.cdc_dev_tracker_navigation_migration_style import (
    build_cdc_dev_tracker_navigation_item,
    build_navigation_contract,
)
from mvp_qaic_reflex_ui.cdc_dev_tracker_screen_migration_style import (
    build_cdc_dev_tracker_screen_model,
    screen_route,
)


def test_contract_rows_and_summary() -> None:
    rows = default_tracker_rows()
    assert rows
    assert tracker_rows_as_dicts()[0]["tracker_kind"] == "CDC_TRACKER"
    assert tracker_summary(rows)["total"] == len(rows)
    assert migration_style_contract()["ui_style_source"] == "MIGRATION_TRACKER"


def test_screen_model_uses_migration_tracker_style() -> None:
    model = build_cdc_dev_tracker_screen_model()
    assert model["route"] == "/cdc-dev-tracker"
    assert screen_route() == "/cdc-dev-tracker"
    assert model["summary_kpi_bar"]["total"] >= 2
    assert model["filter_bar"]["enabled"] is True
    assert model["detail_panel"]["enabled"] is True
    assert model["next_actions_panel"]["enabled"] is True


def test_navigation_contract_is_runtime_free() -> None:
    item = build_cdc_dev_tracker_navigation_item()
    contract = build_navigation_contract()
    assert item["route"] == "/cdc-dev-tracker"
    assert item["dirty_file_gate_required"] is True
    assert contract["must_not_edit_dirty_ui_shell_in_r3"] is True
    assert contract["no_runtime"] is True


def test_status_json_is_valid() -> None:
    status_path = Path(
        "docs/mvp_ui/"
        "MVP_UI_CDC_DEV_TRACKER_NAVIGATION_MIGRATION_STYLE_R3H_STATUS.json"
    )
    data = json.loads(status_path.read_text(encoding="utf-8"))
    assert data["status"] == "READY_FOR_DIRTY_FILE_GATE_R4"
    assert data["no_runtime"] is True
    assert data["next"] == "MVP_UI_ATTACH_CDC_DEV_TRACKER_TO_NAVIGATION_DIRTY_FILE_GATE_R4"


def test_sample_json_is_valid() -> None:
    sample_path = Path(
        "docs/mvp_ui/samples/"
        "MVP_UI_CDC_DEV_TRACKER_NAVIGATION_MIGRATION_STYLE_R3H_SAMPLE.json"
    )
    data = json.loads(sample_path.read_text(encoding="utf-8"))
    assert data["navigation_item"]["route"] == "/cdc-dev-tracker"
