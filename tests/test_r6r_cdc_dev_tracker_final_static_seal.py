from __future__ import annotations

import importlib
import json
from pathlib import Path


TRACKER_PATH = Path("docs/dev_tracking/DEV_LIFECYCLE_TRACKER.json")
R6R_EVIDENCE_PATH = Path("docs/dev_tracking/R6R_CDC_DEV_TRACKER_FINAL_EVIDENCE_20260629.md")
EVIDENCE_PATHS = (
    Path("docs/dev_tracking/R6P_LOCAL_STATIC_SMOKE_EVIDENCE_20260629.md"),
    Path("docs/dev_tracking/R6Q_REFLEX_RUNTIME_DIAGNOSTIC_EVIDENCE_20260629.md"),
    R6R_EVIDENCE_PATH,
)
LAYER_TEXT_PATHS = (
    TRACKER_PATH,
    *EVIDENCE_PATHS,
    Path("mvp_qaic_reflex_ui/dev_lifecycle_tracker.py"),
    Path("mvp_qaic_reflex_ui/cdc_dev_tracker_reflex_page.py"),
    Path("mvp_qaic_reflex_ui/pages_landing.py"),
)
REQUIRED_ROUTES = {"/dev-tracking", "/cdc-dev-tracker", "/cdc-tracker"}
REQUIRED_FIELDS = {
    "phase_id",
    "order",
    "status",
    "track",
    "title",
    "goal",
    "progress_percent",
    "evidence",
    "tests",
    "head",
    "tag",
    "next_action",
}
ALLOWED_STATUSES = {"DONE", "ACTIVE", "NEXT", "BLOCKED", "PARKED", "FUTURE"}
FORBIDDEN_MARKERS = (
    "STRUCTURE" + "_READY",
    "CONTENT" + "_TO_CONNECT",
    "cette page " + "consolidera",
    "place" + "holder",
    "st" + "ub",
)


def _tracker() -> dict:
    return json.loads(TRACKER_PATH.read_text(encoding="utf-8"))


def _phase_map() -> dict[str, dict]:
    return {row["phase_id"]: row for row in _tracker()["phases"]}


def test_r6r_routes_are_registered_in_static_contract() -> None:
    tracker = _tracker()
    app_text = Path("mvp_qaic_reflex_ui/mvp_qaic_reflex_ui.py").read_text(encoding="utf-8")
    cdc_text = Path("mvp_qaic_reflex_ui/cdc_dev_tracker_reflex_page.py").read_text(encoding="utf-8")

    assert set(tracker["views"].values()) == REQUIRED_ROUTES
    for route in REQUIRED_ROUTES:
        assert route in app_text
        assert route in cdc_text


def test_r6r_lifecycle_is_complete_from_r6j_to_r6r() -> None:
    phases = _phase_map()
    expected_ids = ["R6J", "R6K", "R6L", "R6M", "R6N", "R6P", "R6Q", "R6R"]

    assert list(phases)[:2] == ["FOUNDATION_HISTORY", "P59_P100_FOUNDATION"]
    assert all(phase_id in phases for phase_id in expected_ids)
    assert [phases[phase_id]["status"] for phase_id in expected_ids] == ["DONE"] * len(expected_ids)
    assert phases["PRIVATE_RC"]["status"] == "DONE"


def test_r6r_tracker_fields_statuses_and_evidence_docs_are_valid() -> None:
    tracker = _tracker()

    assert tracker["status"] == "ACTIVE"
    for row in tracker["phases"]:
        assert REQUIRED_FIELDS.issubset(row)
        assert row["status"] in ALLOWED_STATUSES
        assert str(row["phase_id"]).strip()
        assert str(row["evidence"]).strip()
        assert str(row["tests"]).strip()

    phases = _phase_map()
    assert phases["R6P"]["status"] == "DONE"
    assert phases["R6Q"]["status"] == "DONE"
    assert phases["R6R"]["status"] == "DONE"
    assert phases["PRIVATE_RC"]["status"] == "DONE"
    for path in EVIDENCE_PATHS:
        assert path.exists()
        assert path.read_text(encoding="utf-8").strip()


def test_r6r_layer_has_no_forbidden_marker_text() -> None:
    for path in LAYER_TEXT_PATHS:
        text = path.read_text(encoding="utf-8").lower()
        for marker in FORBIDDEN_MARKERS:
            assert marker.lower() not in text, path


def test_r6r_page_modules_import_successfully_without_runtime_probe() -> None:
    cdc_module = importlib.import_module("mvp_qaic_reflex_ui.cdc_dev_tracker_reflex_page")
    landing_module = importlib.import_module("mvp_qaic_reflex_ui.pages_landing")
    app_module = importlib.import_module("mvp_qaic_reflex_ui.mvp_qaic_reflex_ui")

    assert callable(cdc_module.cdc_dev_tracker_reflex_page)
    assert callable(cdc_module.cdc_tracker_reflex_page)
    assert callable(landing_module.dev_tracking)
    assert getattr(app_module, "app") is not None


def test_r6r_evidence_keeps_frontend_runtime_limitation_open() -> None:
    text = R6R_EVIDENCE_PATH.read_text(encoding="utf-8").lower()

    assert "r6q already diagnosed" in text
    assert "frontend/bun remediation is deferred" in text
    assert "does not mark full frontend runtime as passed" in text
