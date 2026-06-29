from __future__ import annotations

import json
from collections.abc import Callable
from pathlib import Path
from typing import Any

import reflex as rx

from mvp_qaic_reflex_ui.cdc_dev_tracker_reflex_page import (
    cdc_dev_tracker_reflex_page,
    cdc_tracker_reflex_page,
)
from mvp_qaic_reflex_ui.pages_landing import dev_tracking


TRACKER_PATH = Path("docs/dev_tracking/DEV_LIFECYCLE_TRACKER.json")
EVIDENCE_PATH = Path("docs/dev_tracking/PRIVATE_RC_STATIC_RENDER_SMOKE_EVIDENCE_20260629.md")
ROUTE_PAGES: dict[str, Callable[[], rx.Component]] = {
    "/dev-tracking": dev_tracking,
    "/cdc-dev-tracker": cdc_dev_tracker_reflex_page,
    "/cdc-tracker": cdc_tracker_reflex_page,
}
REQUIRED_OPERATOR_CONTENT = (
    "CDC",
    "Dev Tracker",
    "lifecycle",
    "R6R",
    "PRIVATE_RC",
    "/dev-tracking",
    "/cdc-dev-tracker",
    "/cdc-tracker",
)
FORBIDDEN_MARKERS = (
    "STRUCTURE" + "_READY",
    "CONTENT" + "_TO_CONNECT",
    "cette page " + "consolidera",
    "place" + "holder",
    "st" + "ub",
)
ALLOWED_STATUSES = {"DONE", "ACTIVE", "NEXT", "BLOCKED", "PARKED", "FUTURE"}


def _rendered_tree_text(component: rx.Component) -> str:
    rendered: dict[str, Any] = component.render()
    return json.dumps(rendered, ensure_ascii=False, default=str)


def _phase_map() -> dict[str, dict[str, Any]]:
    tracker = json.loads(TRACKER_PATH.read_text(encoding="utf-8"))
    return {row["phase_id"]: row for row in tracker["phases"]}


def test_private_rc_routes_instantiate_and_render_static_component_trees() -> None:
    rendered_by_route = {}

    for route, page in ROUTE_PAGES.items():
        component = page()
        rendered = component.render()

        assert isinstance(component, rx.Component)
        assert isinstance(rendered, dict)
        assert rendered.get("children"), route
        rendered_by_route[route] = json.dumps(rendered, ensure_ascii=False, default=str)
        assert route in rendered_by_route[route]

    rendered_corpus = "\n".join(rendered_by_route.values())
    for expected in REQUIRED_OPERATOR_CONTENT:
        assert expected in rendered_corpus


def test_private_rc_rendered_trees_have_no_forbidden_placeholder_text() -> None:
    rendered_corpus = "\n".join(_rendered_tree_text(page()) for page in ROUTE_PAGES.values())
    lowered = rendered_corpus.lower()

    for marker in FORBIDDEN_MARKERS:
        assert marker.lower() not in lowered


def test_private_rc_lifecycle_status_and_evidence_contract_are_sealed() -> None:
    tracker = json.loads(TRACKER_PATH.read_text(encoding="utf-8"))
    phases = _phase_map()

    assert tracker["views"] == {
        "dev_tracking": "/dev-tracking",
        "cdc_dev_tracker": "/cdc-dev-tracker",
        "cdc_tracker": "/cdc-tracker",
    }
    assert all(row["status"] in ALLOWED_STATUSES for row in tracker["phases"])
    assert phases["PRIVATE_RC"]["status"] == "DONE"
    assert phases["PRIVATE_RC"]["progress_percent"] == 100
    assert phases["PUBLIC_READY_FUTURE"]["status"] == "FUTURE"
    assert EVIDENCE_PATH.exists()
    assert EVIDENCE_PATH.read_text(encoding="utf-8").strip()
