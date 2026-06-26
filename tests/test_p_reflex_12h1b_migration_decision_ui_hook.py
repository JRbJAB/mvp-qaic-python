from __future__ import annotations

import inspect
from pathlib import Path

import mvp_qaic_reflex_ui.migration_decision_workbench as workbench


def test_p12h1b_workbench_ui_functions_exist() -> None:
    assert workbench.MIGRATION_DECISION_WORKBENCH_ROUTE == "/migration/decisions"
    assert inspect.isfunction(workbench.migration_decision_workbench_compact_panel)
    assert inspect.isfunction(workbench.migration_decision_workbench_page)


def test_p12h1b_mission_control_imports_compact_panel() -> None:
    text = Path("mvp_qaic_reflex_ui/pages_landing.py").read_text(encoding="utf-8")
    assert "migration_decision_workbench_compact_panel" in text
    assert "migration_tracker_compact_panel()" in text
    assert "migration_decision_workbench_compact_panel()" in text


def test_p12h1b_app_registers_decision_route() -> None:
    text = Path("mvp_qaic_reflex_ui/mvp_qaic_reflex_ui.py").read_text(encoding="utf-8")
    assert "P_REFLEX_12H1B_BEGIN_DECISION_WORKBENCH_ROUTE" in text
    assert "MIGRATION_DECISION_WORKBENCH_ROUTE" in text
    assert "migration_decision_workbench_page" in text
    assert 'title="Migration Decision Workbench"' in text


def test_p12h1b_does_not_edit_migration_tracker_directly() -> None:
    text = Path("mvp_qaic_reflex_ui/migration_tracker.py").read_text(encoding="utf-8")
    assert "P_REFLEX_12H1B" not in text
    assert "migration_decision_workbench_compact_panel" not in text


def test_p12h1b_workbench_queue_still_builds() -> None:
    queue = workbench.build_decision_queue(".", limit=5)
    assert isinstance(queue, dict)
    assert queue["queue_count"] >= 1
    assert isinstance(queue["rows"], list)
