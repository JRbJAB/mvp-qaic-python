from __future__ import annotations

import html
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from mvp_qaic_py.release.runtime_cockpit_extended_module import (
    build_runtime_cockpit_extended_module,
)

P98E_STATUS = "OK_P98E_COCKPIT_UI_EXPORT_LOCAL_READY"
NEXT_STEP = "P99_MVP_FREEZE_RELEASE_HANDOFF"


def _escape(value: object) -> str:
    return html.escape(str(value), quote=True)


def build_cockpit_ui_export() -> dict[str, Any]:
    cockpit = build_runtime_cockpit_extended_module()
    blockers: list[str] = []
    if cockpit.get("status") != "OK_P98D_RUNTIME_COCKPIT_EXTENDED_MODULE_LOCAL_READY":
        blockers.append("P98D_EXTENDED_COCKPIT_NOT_READY")
    if cockpit.get("card_count") != 17:
        blockers.append("P98D_CARD_COUNT_MISMATCH")

    cards = list(cockpit.get("cards", []))
    sections = list(cockpit.get("visual_sections", []))
    card_ids = {card["card_id"] for card in cards}
    if len(cards) != 17:
        blockers.append("P98E_UI_EXPORT_CARD_COUNT_MISMATCH")
    if not sections:
        blockers.append("P98E_UI_EXPORT_SECTIONS_MISSING")
    if "benchmark_status" not in card_ids:
        blockers.append("P98E_BENCHMARK_CARD_MISSING")

    safety = {
        "local_export_only": True,
        "live_write_executed_in_p98e": False,
        "decision_journal_write_in_p98e": False,
        "apps_script_execution": False,
        "clasp_push": False,
        "broker_execution": False,
        "order_execution": False,
        "auto_sizing_execution": False,
        "trading_action": False,
    }
    status = P98E_STATUS if not blockers else "BLOCKED_P98E_COCKPIT_UI_EXPORT"
    return {
        "step": "P98E_COCKPIT_UI_EXPORT_LOCAL",
        "status": status,
        "created_at": datetime.now(timezone.utc).isoformat(),
        "source_p98d_status": cockpit.get("status"),
        "card_count": len(cards),
        "section_count": len(sections),
        "ui_export": {
            "export_formats": ["json", "markdown", "html"],
            "render_mode": "local_static_readonly",
            "json_file": "P98E_COCKPIT_UI_EXPORT.json",
            "markdown_file": "P98E_COCKPIT_UI_EXPORT.md",
            "html_file": "P98E_COCKPIT_UI_EXPORT.html",
            "cards_rendered": len(cards),
            "sections_rendered": len(sections),
        },
        "cards": cards,
        "visual_sections": sections,
        "safety": safety,
        "blockers": blockers,
        "next": NEXT_STEP if not blockers else "FIX_BLOCKERS_BEFORE_P99",
    }


def assert_cockpit_ui_export_safe(payload: dict[str, Any]) -> None:
    if payload["status"] != P98E_STATUS:
        raise ValueError(f"P98E UI export not OK: {payload['status']}")
    if payload["blockers"]:
        raise ValueError(f"P98E blockers present: {payload['blockers']}")
    if payload["card_count"] != 17:
        raise ValueError("P98E must render all 17 extended cockpit cards")
    safety = payload["safety"]
    expected_false = (
        "live_write_executed_in_p98e",
        "decision_journal_write_in_p98e",
        "apps_script_execution",
        "clasp_push",
        "broker_execution",
        "order_execution",
        "auto_sizing_execution",
        "trading_action",
    )
    enabled = [flag for flag in expected_false if safety.get(flag)]
    if enabled:
        raise ValueError(f"Unsafe P98E flags enabled: {enabled}")
    if safety.get("local_export_only") is not True:
        raise ValueError("P98E must remain local export only")


def _card_by_id(cards: list[dict[str, Any]], card_id: str) -> dict[str, Any]:
    return next(card for card in cards if card["card_id"] == card_id)


def render_cockpit_ui_export_markdown(payload: dict[str, Any]) -> str:
    cards = payload["cards"]
    lines: list[str] = []
    for section in payload["visual_sections"]:
        lines.extend([f"### {section['title']}", ""])
        for card_id in section["cards"]:
            card = _card_by_id(cards, card_id)
            lines.append(f"- `{card['card_id']}` - {card['state']} - `{card['sheet_name']}`")
        lines.append("")
    return "
".join(
        [
            "# MVP QAIC - P98E Cockpit UI Export Local",
            "",
            f"- status: `{payload['status']}`",
            f"- card_count: `{payload['card_count']}`",
            f"- section_count: `{payload['section_count']}`",
            f"- next: `{payload['next']}`",
            "",
            "## Planning visuel exporte",
            "",
            *lines,
            "## Fichiers exportes",
            "",
            f"- `{payload['ui_export']['json_file']}`",
            f"- `{payload['ui_export']['markdown_file']}`",
            f"- `{payload['ui_export']['html_file']}`",
            "",
            "## Safety",
            "",
            "- local static export only",
            "- no live write in P98E",
            "- no Decision Journal write in P98E",
            "- no Apps Script execution",
            "- no CLASP push",
            "- no broker/order/sizing",
            "",
        ]
    )


def render_cockpit_ui_export_html(payload: dict[str, Any]) -> str:
    cards = payload["cards"]
    sections_html: list[str] = []
    for section in payload["visual_sections"]:
        card_blocks: list[str] = []
        for card_id in section["cards"]:
            card = _card_by_id(cards, card_id)
            card_blocks.append(
                "<article class='card'>"
                f"<h3>{_escape(card['card_id'])}</h3>"
                f"<p class='state'>{_escape(card['state'])}</p>"
                f"<p><strong>Surface:</strong> {_escape(card['sheet_name'])}</p>"
                f"<p>{_escape(card['operator_question'])}</p>"
                "</article>"
            )
        sections_html.append(
            "<section>"
            f"<h2>{_escape(section['title'])}</h2>"
            "<div class='grid'>"
            + "
".join(card_blocks)
            + "</div></section>"
        )
    return "
".join(
        [
            "<!doctype html>",
            "<html lang='fr'>",
            "<head>",
            "<meta charset='utf-8'>",
            "<meta name='viewport' content='width=device-width, initial-scale=1'>",
            "<title>MVP QAIC - Cockpit UI Export Local</title>",
            "<style>",
            "body{font-family:Arial,sans-serif;margin:24px;background:#f7f7f7;color:#111}",
            ".hero{background:#111;color:#fff;border-radius:14px;padding:18px;margin-bottom:18px}",
            ".grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(230px,1fr));gap:12px}",
            ".card{background:#fff;border:1px solid #ddd;border-radius:12px;padding:14px}",
            ".state{font-weight:bold}",
            ".safety{background:#fff4d6;border:1px solid #e4c86a;border-radius:12px;padding:14px}",
            "</style>",
            "</head>",
            "<body>",
            "<div class='hero'>",
            "<h1>MVP QAIC - Cockpit etendu local</h1>",
            f"<p>Status: {_escape(payload['status'])}</p>",
            f"<p>Cards: {_escape(payload['card_count'])} - Next: {_escape(payload['next'])}</p>",
            "</div>",
            *sections_html,
            "<section class='safety'>",
            "<h2>Safety</h2>",
            "<p>HUMAN_REVIEW_ONLY - NO_BROKER - NO_ORDER - NO_SIZING - NO_LIVE_WRITE_IN_P98E</p>",
            "</section>",
            "</body>",
            "</html>",
        ]
    )


def export_cockpit_ui_export(out_dir: str | Path) -> dict[str, str]:
    target = Path(out_dir)
    target.mkdir(parents=True, exist_ok=True)
    payload = build_cockpit_ui_export()
    assert_cockpit_ui_export_safe(payload)
    markdown = render_cockpit_ui_export_markdown(payload)
    html_text = render_cockpit_ui_export_html(payload)
    json_path = target / "P98E_COCKPIT_UI_EXPORT.json"
    md_path = target / "P98E_COCKPIT_UI_EXPORT.md"
    html_path = target / "P98E_COCKPIT_UI_EXPORT.html"
    json_path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    md_path.write_text(markdown, encoding="utf-8")
    html_path.write_text(html_text, encoding="utf-8")
    return {
        "status": payload["status"],
        "json": str(json_path),
        "markdown": str(md_path),
        "html": str(html_path),
        "next": payload["next"],
    }
