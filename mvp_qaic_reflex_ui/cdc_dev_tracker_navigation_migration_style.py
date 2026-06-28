"""Navigation contract for attaching CDC + Dev Tracker to the MVP UI."""

from __future__ import annotations

from mvp_qaic_reflex_ui.cdc_dev_tracker_screen_migration_style import (
    SCREEN_ROUTE,
    SCREEN_TITLE,
    build_cdc_dev_tracker_screen_model,
)

NAVIGATION_ITEM_ID = "cdc_dev_tracker"
NAVIGATION_GROUP = "trackers"


def build_cdc_dev_tracker_navigation_item() -> dict[str, object]:
    """Build a route/navigation item without editing the dirty UI shell."""

    model = build_cdc_dev_tracker_screen_model()
    return {
        "item_id": NAVIGATION_ITEM_ID,
        "label": SCREEN_TITLE,
        "route": SCREEN_ROUTE,
        "group": NAVIGATION_GROUP,
        "ui_style_source": model["ui_style_source"],
        "enabled": True,
        "runtime_free_default": True,
        "attach_target": "mvp_qaic_reflex_ui.mvp_qaic_reflex_ui",
        "dirty_file_gate_required": True,
        "next": "MVP_UI_ATTACH_CDC_DEV_TRACKER_TO_NAVIGATION_DIRTY_FILE_GATE_R4",
    }


def build_navigation_contract() -> dict[str, object]:
    """Return the navigation attach contract for R3H."""

    item = build_cdc_dev_tracker_navigation_item()
    return {
        "status": "READY_FOR_DIRTY_FILE_GATE_R4",
        "navigation_item": item,
        "screen_route": SCREEN_ROUTE,
        "screen_title": SCREEN_TITLE,
        "must_not_edit_dirty_ui_shell_in_r3": True,
        "no_runtime": True,
        "no_archive": True,
        "no_broker_order_sizing": True,
        "no_sheet_bq_write": True,
    }
