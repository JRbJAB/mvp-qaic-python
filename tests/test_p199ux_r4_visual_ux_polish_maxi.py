from __future__ import annotations

from pathlib import Path

import mvp_qaic_py.p199ux_r4_visual_ux_polish_maxi as p199ux_r4


def test_visual_ux_polish_adds_cards_top_planning_and_nav(monkeypatch, tmp_path: Path) -> None:
    def fake_base(project_root: Path) -> dict[str, object]:
        return {
            "STATUS": "OK",
            "generated_at": "2026-06-24T00:00:00+00:00",
            "project_root": str(project_root),
            "roadmap_status": "VISIBLE_PAST_CURRENT_FUTURE_POST_PYTHON",
            "roadmap_step_count": 15,
            "done_step_count": 5,
            "current_step_count": 3,
            "post_python_step_count": 4,
            "nicegui_tab_count": 9,
            "sheet_tab_count": 13,
            "ready_mapping_count": 12,
            "migration_coverage_percent": 97.7,
            "roadmap_rows": [
                {
                    "order": 1,
                    "period": "PASSÉ",
                    "lane": "A",
                    "status": "DONE",
                    "progress_percent": 100,
                    "visible_route": "/migration",
                    "next_action": "A",
                },
                {
                    "order": 2,
                    "period": "EN COURS",
                    "lane": "B",
                    "status": "ACTIVE",
                    "progress_percent": 90,
                    "visible_route": "/sheets-export",
                    "next_action": "B",
                },
                {
                    "order": 3,
                    "period": "EN ATTENTE",
                    "lane": "C",
                    "status": "WAITING",
                    "progress_percent": 60,
                    "visible_route": "/real-case-inputs",
                    "next_action": "C",
                },
                {
                    "order": 4,
                    "period": "AVENIR PROCHE",
                    "lane": "D",
                    "status": "NEXT",
                    "progress_percent": 80,
                    "visible_route": "/operator-release",
                    "next_action": "D",
                },
                {
                    "order": 5,
                    "period": "POST-PYTHON",
                    "lane": "E",
                    "status": "FUTURE",
                    "progress_percent": 20,
                    "visible_route": "/dev-roadmap",
                    "next_action": "E",
                },
            ],
            "nicegui_tab_rows": [],
            "decision_rows": [],
            "blocker_count": 0,
            "blockers": [],
            "parallel_waiting_next": "P196B",
        }

    monkeypatch.setattr(p199ux_r4, "build_dev_roadmap_tabs_ergonomics", fake_base)

    payload = p199ux_r4.build_visual_ux_polish(tmp_path)

    assert payload["ux_status"] == "VISUAL_PLANNING_TOP_COMPACT_TABLES_COLLAPSIBLE_NAV_READY"
    assert len(payload["metric_card_rows"]) >= 6
    assert len(payload["top_visual_planning_rows"]) == 5
    assert payload["compact_table_policy"]["density"] == "dense"
    assert payload["navigation_policy"]["mode"] == "collapsible_quick_navigation"
    assert payload["google_sheets_write"] is False
    assert payload["apps_script_execution"] is False
    assert payload["clasp_push"] is False
    assert payload["broker"] is False
    assert payload["order"] is False
    assert payload["sizing"] is False


def test_metric_cards_have_colors(monkeypatch, tmp_path: Path) -> None:
    payload = p199ux_r4.build_visual_ux_polish(tmp_path)

    assert all(row["color"] for row in payload["metric_card_rows"])
    assert any(row["unit"] == "%" for row in payload["metric_card_rows"])


def test_export_visual_ux_polish_writes_outputs(monkeypatch, tmp_path: Path) -> None:
    payload = p199ux_r4.export_visual_ux_polish(
        tmp_path, export_dir=tmp_path / "05_EXPORTS" / "P199UX_R4_TEST"
    )

    assert payload["nicegui_tab_count"] >= 8
    export_dir = Path(payload["export_dir"])
    assert (export_dir / "P199UX_R4_VISUAL_UX_POLISH.json").exists()
    assert (export_dir / "P199UX_R4_METRIC_CARDS.csv").exists()
    assert (export_dir / "P199UX_R4_TOP_VISUAL_PLANNING.csv").exists()
    assert (export_dir / "P199UX_R4_VISUAL_ROADMAP.csv").exists()
    assert (export_dir / "P199UX_R4_NICEGUI_TABS_USABILITY.csv").exists()
    assert (export_dir / "P199UX_R4_SUMMARY.json").exists()
    assert (export_dir / "P199UX_R4_REPORT.md").exists()
