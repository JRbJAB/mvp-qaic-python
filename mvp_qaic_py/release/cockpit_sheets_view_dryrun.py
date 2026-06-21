from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from mvp_qaic_py.release.cockpit_ui_export import build_cockpit_ui_export

P98F_STATUS = "OK_P98F_COCKPIT_SHEETS_VIEW_DRYRUN_READY"
NEXT_STEP = "P98G_CREATE_OR_UPDATE_COCKPIT_SHEET_AFTER_EXPLICIT_GO_OR_P99_MVP_FREEZE"
COCKPIT_SHEET_NAME = "QAIC_RUNTIME_COCKPIT_VIEW"
NL = chr(10)


def _card_row(card: dict[str, Any]) -> dict[str, Any]:
    return {
        "row_type": "CARD",
        "card_id": card["card_id"],
        "section": card["lane_label"],
        "state": card["state"],
        "surface": card["sheet_name"],
        "operator_question": card["operator_question"],
        "write_in_p98f": False,
    }


def build_cockpit_sheets_view_dryrun() -> dict[str, Any]:
    ui_export = build_cockpit_ui_export()
    blockers: list[str] = []

    if ui_export.get("status") != "OK_P98E_COCKPIT_UI_EXPORT_LOCAL_READY":
        blockers.append("P98E_R1_UI_EXPORT_NOT_READY")
    if ui_export.get("card_count") != 17:
        blockers.append("P98E_R1_CARD_COUNT_MISMATCH")

    cards = list(ui_export.get("cards", []))
    sections = list(ui_export.get("visual_sections", []))

    planned_header = [
        "card_id",
        "section",
        "state",
        "surface",
        "operator_question",
        "write_in_p98f",
    ]
    planned_rows = [_card_row(card) for card in cards]

    section_summary = [
        {
            "section_id": section["section_id"],
            "title": section["title"],
            "card_count": len(section["cards"]),
            "cards": list(section["cards"]),
            "write_in_p98f": False,
        }
        for section in sections
    ]

    sheets_view_plan = {
        "target_sheet_name": COCKPIT_SHEET_NAME,
        "target_action": "DRYRUN_ONLY_NO_SHEET_WRITE",
        "create_sheet_in_p98f": False,
        "update_cells_in_p98f": False,
        "write_rows_in_p98f": False,
        "freeze_rows_planned": 1,
        "planned_header": planned_header,
        "planned_row_count": len(planned_rows),
        "planned_sections": section_summary,
        "planned_rows": planned_rows,
    }

    safety = {
        "local_dryrun_only": True,
        "live_write_executed_in_p98f": False,
        "decision_journal_write_in_p98f": False,
        "sheet_create_or_update_in_p98f": False,
        "apps_script_execution": False,
        "clasp_push": False,
        "broker_execution": False,
        "order_execution": False,
        "auto_sizing_execution": False,
        "trading_action": False,
    }

    status = P98F_STATUS if not blockers else "BLOCKED_P98F_COCKPIT_SHEETS_VIEW_DRYRUN"
    return {
        "step": "P98F_COCKPIT_SHEETS_VIEW_DRYRUN",
        "status": status,
        "created_at": datetime.now(timezone.utc).isoformat(),
        "source_p98e_status": ui_export.get("status"),
        "target_sheet_name": COCKPIT_SHEET_NAME,
        "card_count": len(cards),
        "section_count": len(sections),
        "sheets_view_plan": sheets_view_plan,
        "safety": safety,
        "blockers": blockers,
        "next": NEXT_STEP if not blockers else "FIX_BLOCKERS_BEFORE_P98G_OR_P99",
    }


def assert_cockpit_sheets_view_dryrun_safe(payload: dict[str, Any]) -> None:
    if payload["status"] != P98F_STATUS:
        raise ValueError(f"P98F dryrun not OK: {payload['status']}")
    if payload["blockers"]:
        raise ValueError(f"P98F blockers present: {payload['blockers']}")
    if payload["card_count"] != 17:
        raise ValueError("P98F must plan all 17 cockpit cards")

    plan = payload["sheets_view_plan"]
    if plan["target_action"] != "DRYRUN_ONLY_NO_SHEET_WRITE":
        raise ValueError("P98F must remain dryrun only")
    if plan["create_sheet_in_p98f"] is not False:
        raise ValueError("P98F must not create a Sheet")
    if plan["update_cells_in_p98f"] is not False:
        raise ValueError("P98F must not update Sheet cells")
    if plan["write_rows_in_p98f"] is not False:
        raise ValueError("P98F must not write rows")

    safety = payload["safety"]
    expected_false = (
        "live_write_executed_in_p98f",
        "decision_journal_write_in_p98f",
        "sheet_create_or_update_in_p98f",
        "apps_script_execution",
        "clasp_push",
        "broker_execution",
        "order_execution",
        "auto_sizing_execution",
        "trading_action",
    )
    enabled = [flag for flag in expected_false if safety.get(flag)]
    if enabled:
        raise ValueError(f"Unsafe P98F flags enabled: {enabled}")
    if safety.get("local_dryrun_only") is not True:
        raise ValueError("P98F must remain local dryrun only")

    for row in plan["planned_rows"]:
        if row.get("write_in_p98f") is not False:
            raise ValueError(f"P98F planned row writes during dryrun: {row}")


def render_cockpit_sheets_view_dryrun_markdown(payload: dict[str, Any]) -> str:
    plan = payload["sheets_view_plan"]
    section_lines: list[str] = []
    for section in plan["planned_sections"]:
        section_lines.append(
            f"- {section['section_id']}: {section['card_count']} cards -> {', '.join(section['cards'])}"
        )
    row_lines = [
        f"- `{row['card_id']}` / {row['section']} / {row['state']} / `{row['surface']}`"
        for row in plan["planned_rows"]
    ]
    return NL.join(
        [
            "# MVP QAIC - P98F Cockpit Sheets View Dryrun",
            "",
            f"- status: `{payload['status']}`",
            f"- target_sheet_name: `{payload['target_sheet_name']}`",
            f"- target_action: `{plan['target_action']}`",
            f"- planned_row_count: `{plan['planned_row_count']}`",
            f"- next: `{payload['next']}`",
            "",
            "## Sections planifiees",
            "",
            *section_lines,
            "",
            "## Lignes cockpit planifiees",
            "",
            *row_lines,
            "",
            "## Safety",
            "",
            "- local dry-run only",
            "- no live write in P98F",
            "- no Decision Journal write in P98F",
            "- no Sheet create/update in P98F",
            "- no Apps Script execution",
            "- no CLASP push",
            "- no broker/order/sizing",
            "",
        ]
    )


def export_cockpit_sheets_view_dryrun(out_dir: str | Path) -> dict[str, str]:
    target = Path(out_dir)
    target.mkdir(parents=True, exist_ok=True)
    payload = build_cockpit_sheets_view_dryrun()
    assert_cockpit_sheets_view_dryrun_safe(payload)
    markdown = render_cockpit_sheets_view_dryrun_markdown(payload)
    json_path = target / "P98F_COCKPIT_SHEETS_VIEW_DRYRUN.json"
    md_path = target / "P98F_COCKPIT_SHEETS_VIEW_DRYRUN.md"
    json_path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    md_path.write_text(markdown, encoding="utf-8")
    return {
        "status": payload["status"],
        "json": str(json_path),
        "markdown": str(md_path),
        "next": payload["next"],
    }
