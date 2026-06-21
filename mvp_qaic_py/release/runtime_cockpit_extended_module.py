from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from mvp_qaic_py.release.extended_cockpit_scope_audit import build_extended_cockpit_scope_audit
from mvp_qaic_py.release.runtime_cockpit_module import build_runtime_cockpit_module

P98D_STATUS = "OK_P98D_RUNTIME_COCKPIT_EXTENDED_MODULE_LOCAL_READY"
NEXT_STEP = "P98E_COCKPIT_UI_EXPORT_OR_P99_MVP_FREEZE_RELEASE_HANDOFF"

CARD_PRIORITY: dict[str, int] = {
    "journal_queue_status": 10,
    "decision_journal_status": 11,
    "runtime_bridge_status": 12,
    "run_queue_status": 13,
    "response_intake_status": 14,
    "latest_payload_status": 15,
    "benchmark_status": 20,
    "prompt_quality_status": 21,
    "prompt_improvement_backlog": 22,
    "prompt_library_readiness": 23,
    "lexique_readiness": 30,
    "method_library_status": 31,
    "trade_plan_methods_status": 32,
    "signal_library_coverage": 33,
    "risk_guard_status": 34,
    "portfolio_snapshot_status": 40,
    "revolut_readonly_status": 41,
}

CARD_STATE_BY_CLASSIFICATION: dict[str, str] = {
    "ALREADY_IN_P98B_CORE": "OK_CORE",
    "READY_FOR_COCKPIT_CARD": "READY",
    "READY_FOR_SCOPE_MAPPING": "SCOPE_READY",
    "READONLY_ONLY_SAFE": "READONLY_SAFE",
}

LANE_LABELS: dict[str, str] = {
    "journal_flow": "Journal pipeline",
    "runtime_flow": "Runtime flow",
    "quality_and_benchmark": "Benchmark & quality",
    "quality_and_backlog": "Quality backlog",
    "prompt_control": "Prompt control",
    "knowledge_base": "Knowledge base",
    "method_and_signal_base": "Methods & signals",
    "risk_and_safety": "Risk & safety",
    "portfolio_context": "Portfolio context",
    "broker_readonly_only": "Broker read-only",
}


def _build_card(surface: dict[str, Any]) -> dict[str, Any]:
    card_id = surface["target_card"]
    classification = surface["classification"]
    return {
        "card_id": card_id,
        "surface_id": surface["surface_id"],
        "title": surface["surface_id"].replace("_", " ").title(),
        "sheet_name": surface["sheet_name"],
        "cockpit_lane": surface["cockpit_lane"],
        "lane_label": LANE_LABELS[surface["cockpit_lane"]],
        "state": CARD_STATE_BY_CLASSIFICATION[classification],
        "classification": classification,
        "priority": CARD_PRIORITY.get(card_id, 99),
        "operator_question": surface["operator_question"],
        "write_in_p98d": False,
        "live_read_in_p98d": False,
        "requires_scope_contract": surface["requires_next_scope_contract"],
    }


def build_runtime_cockpit_extended_module() -> dict[str, Any]:
    core = build_runtime_cockpit_module()
    audit = build_extended_cockpit_scope_audit()
    blockers: list[str] = []

    if core.get("status") != "OK_P98B_RUNTIME_COCKPIT_MODULE_LOCAL_READY":
        blockers.append("P98B_CORE_COCKPIT_NOT_READY")
    if audit.get("status") != "OK_P98C_EXTENDED_COCKPIT_SCOPE_AUDIT_READY_READONLY":
        blockers.append("P98C_SCOPE_AUDIT_NOT_READY")
    if audit.get("surface_count") != 17:
        blockers.append("P98C_SURFACE_COUNT_MISMATCH")

    cards = sorted(
        [_build_card(surface) for surface in audit.get("surfaces", [])],
        key=lambda card: (card["priority"], card["card_id"]),
    )

    card_ids = [card["card_id"] for card in cards]
    if len(card_ids) != len(set(card_ids)):
        blockers.append("DUPLICATE_COCKPIT_CARD_ID")

    required_cards = set(audit.get("required_p98d_cards", []))
    missing_cards = sorted(required_cards - set(card_ids))
    if missing_cards:
        blockers.append("MISSING_REQUIRED_P98D_CARDS:" + ",".join(missing_cards))

    lanes: dict[str, list[str]] = {}
    for card in cards:
        lanes.setdefault(card["cockpit_lane"], []).append(card["card_id"])

    visual_sections = [
        {
            "section_id": "JOURNAL_AND_RUNTIME",
            "title": "Runtime & journal pipeline",
            "cards": [
                "journal_queue_status",
                "decision_journal_status",
                "runtime_bridge_status",
                "run_queue_status",
                "response_intake_status",
                "latest_payload_status",
            ],
        },
        {
            "section_id": "QUALITY_AND_BENCHMARK",
            "title": "Quality, prompts & benchmark",
            "cards": [
                "benchmark_status",
                "prompt_quality_status",
                "prompt_improvement_backlog",
                "prompt_library_readiness",
            ],
        },
        {
            "section_id": "KNOWLEDGE_METHODS_SIGNALS_RISK",
            "title": "Knowledge, methods, signals & risk",
            "cards": [
                "lexique_readiness",
                "method_library_status",
                "trade_plan_methods_status",
                "signal_library_coverage",
                "risk_guard_status",
            ],
        },
        {
            "section_id": "PORTFOLIO_AND_READONLY_BROKER",
            "title": "Portfolio & broker read-only",
            "cards": ["portfolio_snapshot_status", "revolut_readonly_status"],
        },
    ]

    operating_summary = {
        "tool_mode": "extended_human_review_cockpit",
        "what_operator_sees": [
            "live journal workflow seal status",
            "benchmark readiness",
            "prompt quality/backlog",
            "lexique/method/signal/risk readiness",
            "portfolio context and broker readonly status",
        ],
        "what_tool_does_not_do": [
            "no broker execution",
            "no order placement",
            "no auto sizing",
            "no Apps Script execution in P98D",
            "no CLASP push in P98D",
            "no live Sheet write in P98D",
        ],
        "next_operator_choice": NEXT_STEP,
    }

    safety = {
        "local_module_only": True,
        "live_write_executed_in_p98d": False,
        "decision_journal_write_in_p98d": False,
        "apps_script_execution": False,
        "clasp_push": False,
        "broker_execution": False,
        "order_execution": False,
        "auto_sizing_execution": False,
        "trading_action": False,
    }

    status = P98D_STATUS if not blockers else "BLOCKED_P98D_RUNTIME_COCKPIT_EXTENDED_MODULE"

    return {
        "step": "P98D_RUNTIME_COCKPIT_EXTENDED_MODULE_LOCAL",
        "status": status,
        "created_at": datetime.now(timezone.utc).isoformat(),
        "source_p98b_status": core.get("status"),
        "source_p98c_status": audit.get("status"),
        "card_count": len(cards),
        "lane_count": len(lanes),
        "cards": cards,
        "lanes": lanes,
        "visual_sections": visual_sections,
        "operating_summary": operating_summary,
        "safety": safety,
        "blockers": blockers,
        "next": NEXT_STEP if not blockers else "FIX_BLOCKERS_BEFORE_P98E_OR_P99",
    }


def assert_runtime_cockpit_extended_module_safe(payload: dict[str, Any]) -> None:
    if payload["status"] != P98D_STATUS:
        raise ValueError(f"P98D extended cockpit not OK: {payload['status']}")
    if payload["blockers"]:
        raise ValueError(f"P98D blockers present: {payload['blockers']}")
    if payload["card_count"] != 17:
        raise ValueError("P98D must expose all 17 P98C cockpit cards")

    safety = payload["safety"]
    expected_false = (
        "live_write_executed_in_p98d",
        "decision_journal_write_in_p98d",
        "apps_script_execution",
        "clasp_push",
        "broker_execution",
        "order_execution",
        "auto_sizing_execution",
        "trading_action",
    )
    enabled = [flag for flag in expected_false if safety.get(flag)]
    if enabled:
        raise ValueError(f"Unsafe P98D flags enabled: {enabled}")
    if safety.get("local_module_only") is not True:
        raise ValueError("P98D must remain local module only")

    for card in payload["cards"]:
        if card.get("write_in_p98d") is not False:
            raise ValueError(f"P98D card write requested: {card}")
        if card.get("live_read_in_p98d") is not False:
            raise ValueError(f"P98D card live read requested: {card}")


def render_runtime_cockpit_extended_module_markdown(payload: dict[str, Any]) -> str:
    section_lines: list[str] = []
    for section in payload["visual_sections"]:
        section_lines.append(f"### {section['title']}")
        section_lines.append("")
        for card_id in section["cards"]:
            card = next(item for item in payload["cards"] if item["card_id"] == card_id)
            section_lines.append(
                f"- `{card['card_id']}` — {card['state']} — `{card['sheet_name']}`"
            )
        section_lines.append("")

    card_lines = [
        (
            f"- {card['priority']:02d} `{card['card_id']}` / {card['lane_label']} / "
            f"{card['state']} / {card['operator_question']}"
        )
        for card in payload["cards"]
    ]
    blocked_lines = [f"- {item}" for item in payload["operating_summary"]["what_tool_does_not_do"]]

    return "\n".join(
        [
            "# MVP QAIC — P98D Runtime Cockpit Extended Module Local",
            "",
            f"- status: `{payload['status']}`",
            f"- card_count: `{payload['card_count']}`",
            f"- lane_count: `{payload['lane_count']}`",
            f"- next: `{payload['next']}`",
            "",
            "## Planning visuel cockpit etendu",
            "",
            *section_lines,
            "## Cartes cockpit etendues",
            "",
            *card_lines,
            "",
            "## Actions bloquees",
            "",
            *blocked_lines,
            "",
            "## Safety",
            "",
            "- local module only",
            "- no live write in P98D",
            "- no Decision Journal write in P98D",
            "- no Apps Script execution",
            "- no CLASP push",
            "- no broker/order/sizing",
            "",
        ]
    )


def export_runtime_cockpit_extended_module(out_dir: str | Path) -> dict[str, str]:
    target = Path(out_dir)
    target.mkdir(parents=True, exist_ok=True)
    payload = build_runtime_cockpit_extended_module()
    assert_runtime_cockpit_extended_module_safe(payload)
    markdown = render_runtime_cockpit_extended_module_markdown(payload)
    json_path = target / "P98D_RUNTIME_COCKPIT_EXTENDED_MODULE.json"
    md_path = target / "P98D_RUNTIME_COCKPIT_EXTENDED_MODULE.md"
    json_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    md_path.write_text(markdown, encoding="utf-8")
    return {
        "status": payload["status"],
        "json": str(json_path),
        "markdown": str(md_path),
        "next": payload["next"],
    }
