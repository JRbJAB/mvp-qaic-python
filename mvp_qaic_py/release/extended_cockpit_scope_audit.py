from __future__ import annotations

import json
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from mvp_qaic_py.release.runtime_cockpit_module import build_runtime_cockpit_module

P98C_STATUS = "OK_P98C_EXTENDED_COCKPIT_SCOPE_AUDIT_READY_READONLY"
NEXT_STEP = "P98D_RUNTIME_COCKPIT_EXTENDED_MODULE_LOCAL_OR_P99_MVP_FREEZE"


EXTENDED_COCKPIT_SURFACES: tuple[dict[str, Any], ...] = (
    {
        "surface_id": "BENCHMARK_AI_TRADE",
        "sheet_name": "🎛️ BENCHMARK_AI_TRADE",
        "domain": "benchmark",
        "classification": "READY_FOR_SCOPE_MAPPING",
        "target_card": "benchmark_status",
        "operator_question": "Les tests benchmark IA trading sont-ils pass/fail et exploitables ?",
    },
    {
        "surface_id": "GPT_INPUT_PAYLOADS",
        "sheet_name": "GPT_INPUT_PAYLOADS",
        "domain": "runtime_input",
        "classification": "READY_FOR_COCKPIT_CARD",
        "target_card": "latest_payload_status",
        "operator_question": "Quel payload a lance le dernier run ?",
    },
    {
        "surface_id": "PROMPT_RUN_QUEUE",
        "sheet_name": "🚀 PROMPT_RUN_QUEUE",
        "domain": "runtime_queue",
        "classification": "READY_FOR_COCKPIT_CARD",
        "target_card": "run_queue_status",
        "operator_question": "Quel run est pret, en cours, bloque ou journalise ?",
    },
    {
        "surface_id": "RESPONSE_INTAKE_QUEUE",
        "sheet_name": "📥 RESPONSE_INTAKE_QUEUE",
        "domain": "runtime_intake",
        "classification": "READY_FOR_COCKPIT_CARD",
        "target_card": "response_intake_status",
        "operator_question": "La reponse IA est-elle captee et exploitable ?",
    },
    {
        "surface_id": "JOURNAL_APPEND_QUEUE",
        "sheet_name": "📤 JOURNAL_APPEND_QUEUE",
        "domain": "journal_pipeline",
        "classification": "ALREADY_IN_P98B_CORE",
        "target_card": "journal_queue_status",
        "operator_question": "La candidate journal est-elle approuvee ou appendue ?",
    },
    {
        "surface_id": "DECISION_JOURNAL",
        "sheet_name": "🧾 DECISION_JOURNAL",
        "domain": "journal_pipeline",
        "classification": "ALREADY_IN_P98B_CORE",
        "target_card": "decision_journal_status",
        "operator_question": "Le journal officiel contient-il la preuve appendue ?",
    },
    {
        "surface_id": "GPT_QUALITY_DASHBOARD",
        "sheet_name": "📊 GPT_QUALITY_DASHBOARD",
        "domain": "quality",
        "classification": "READY_FOR_SCOPE_MAPPING",
        "target_card": "prompt_quality_status",
        "operator_question": "Quels blockers/missing data reviennent le plus souvent ?",
    },
    {
        "surface_id": "PROMPT_IMPROVEMENT_QUEUE",
        "sheet_name": "🧭 PROMPT_IMPROVEMENT_QUEUE",
        "domain": "quality",
        "classification": "READY_FOR_SCOPE_MAPPING",
        "target_card": "prompt_improvement_backlog",
        "operator_question": "Quelles corrections prompt sont prioritaires ?",
    },
    {
        "surface_id": "PROMPT_LIBRARY",
        "sheet_name": "📘 PROMPT_LIBRARY",
        "domain": "prompt_library",
        "classification": "READY_FOR_SCOPE_MAPPING",
        "target_card": "prompt_library_readiness",
        "operator_question": "Quels prompts sont utilisables, a revoir ou bloques ?",
    },
    {
        "surface_id": "LEXIQUE_MASTER",
        "sheet_name": "📚 LEXIQUE_MASTER",
        "domain": "knowledge",
        "classification": "READY_FOR_SCOPE_MAPPING",
        "target_card": "lexique_readiness",
        "operator_question": "Le lexique crypto est-il suffisamment valide pour le runtime ?",
    },
    {
        "surface_id": "METHOD_LIBRARY",
        "sheet_name": "METHOD_LIBRARY",
        "domain": "methods",
        "classification": "READY_FOR_SCOPE_MAPPING",
        "target_card": "method_library_status",
        "operator_question": "Les methodes de decision sont-elles disponibles et versionnees ?",
    },
    {
        "surface_id": "SIGNAL_LIBRARY",
        "sheet_name": "SIGNAL_LIBRARY",
        "domain": "signals",
        "classification": "READY_FOR_SCOPE_MAPPING",
        "target_card": "signal_library_coverage",
        "operator_question": "Quels signaux existent et lesquels manquent pour scorer ?",
    },
    {
        "surface_id": "RISK_PLAYBOOK",
        "sheet_name": "RISK_PLAYBOOK",
        "domain": "risk",
        "classification": "READY_FOR_SCOPE_MAPPING",
        "target_card": "risk_guard_status",
        "operator_question": "Les garde-fous risque bloquent-ils les sorties dangereuses ?",
    },
    {
        "surface_id": "TRADE_PLAN_METHODS",
        "sheet_name": "TRADE_PLAN_METHODS",
        "domain": "methods",
        "classification": "READY_FOR_SCOPE_MAPPING",
        "target_card": "trade_plan_methods_status",
        "operator_question": "Les methodes entree/TP/SL/trailing sont-elles disponibles ?",
    },
    {
        "surface_id": "REVOLUT_X_READONLY_CONTRACT",
        "sheet_name": "REVOLUT_X_READONLY_CONTRACT",
        "domain": "broker_readonly",
        "classification": "READONLY_ONLY_SAFE",
        "target_card": "revolut_readonly_status",
        "operator_question": "Le contrat broker reste-t-il strictement read-only ?",
    },
    {
        "surface_id": "PORTFOLIO_SNAPSHOT",
        "sheet_name": "PORTFOLIO_SNAPSHOT",
        "domain": "portfolio",
        "classification": "READY_FOR_SCOPE_MAPPING",
        "target_card": "portfolio_snapshot_status",
        "operator_question": "Le contexte portefeuille est-il present pour eviter les hallucinations ?",
    },
    {
        "surface_id": "QAIC_RUNTIME_BRIDGE_STATUS",
        "sheet_name": "QAIC_RUNTIME_BRIDGE_STATUS",
        "domain": "bridge_status",
        "classification": "READY_FOR_COCKPIT_CARD",
        "target_card": "runtime_bridge_status",
        "operator_question": "Le bridge local/live est-il pret, bloque ou scelle ?",
    },
)


DOMAIN_TO_COCKPIT_LANE = {
    "benchmark": "quality_and_benchmark",
    "runtime_input": "runtime_flow",
    "runtime_queue": "runtime_flow",
    "runtime_intake": "runtime_flow",
    "journal_pipeline": "journal_flow",
    "quality": "quality_and_backlog",
    "prompt_library": "prompt_control",
    "knowledge": "knowledge_base",
    "methods": "method_and_signal_base",
    "signals": "method_and_signal_base",
    "risk": "risk_and_safety",
    "broker_readonly": "broker_readonly_only",
    "portfolio": "portfolio_context",
    "bridge_status": "runtime_flow",
}


def build_extended_cockpit_scope_audit() -> dict[str, Any]:
    base = build_runtime_cockpit_module()
    blockers: list[str] = []

    if base.get("status") != "OK_P98B_RUNTIME_COCKPIT_MODULE_LOCAL_READY":
        blockers.append("P98B_COCKPIT_MODULE_NOT_READY")

    surfaces = []
    for item in EXTENDED_COCKPIT_SURFACES:
        surface = dict(item)
        surface["cockpit_lane"] = DOMAIN_TO_COCKPIT_LANE[surface["domain"]]
        surface["write_in_p98c"] = False
        surface["live_read_in_p98c"] = False
        surface["requires_next_scope_contract"] = surface["classification"] in {
            "READY_FOR_SCOPE_MAPPING",
            "READONLY_ONLY_SAFE",
        }
        surfaces.append(surface)

    classification_counts = dict(Counter(surface["classification"] for surface in surfaces))
    lane_counts = dict(Counter(surface["cockpit_lane"] for surface in surfaces))

    benchmark_surface = next(
        surface for surface in surfaces if surface["surface_id"] == "BENCHMARK_AI_TRADE"
    )
    if benchmark_surface["classification"] != "READY_FOR_SCOPE_MAPPING":
        blockers.append("BENCHMARK_SURFACE_NOT_CLASSIFIED")

    safety = {
        "readonly_audit_only": True,
        "local_module_only": True,
        "live_write_executed_in_p98c": False,
        "decision_journal_write_in_p98c": False,
        "apps_script_execution": False,
        "clasp_push": False,
        "broker_execution": False,
        "order_execution": False,
        "auto_sizing_execution": False,
        "trading_action": False,
    }

    status = P98C_STATUS if not blockers else "BLOCKED_P98C_EXTENDED_COCKPIT_SCOPE_AUDIT"

    return {
        "step": "P98C_EXTENDED_COCKPIT_SCOPE_AUDIT_READONLY",
        "status": status,
        "created_at": datetime.now(timezone.utc).isoformat(),
        "source_p98b_status": base.get("status"),
        "surface_count": len(surfaces),
        "classification_counts": classification_counts,
        "lane_counts": lane_counts,
        "surfaces": surfaces,
        "required_p98d_cards": [surface["target_card"] for surface in surfaces],
        "safety": safety,
        "blockers": blockers,
        "next": NEXT_STEP if not blockers else "FIX_BLOCKERS_BEFORE_P98D_OR_P99",
    }


def assert_extended_cockpit_scope_audit_safe(payload: dict[str, Any]) -> None:
    if payload["status"] != P98C_STATUS:
        raise ValueError(f"P98C audit not OK: {payload['status']}")
    if payload["blockers"]:
        raise ValueError(f"P98C blockers present: {payload['blockers']}")
    if payload["surface_count"] < 15:
        raise ValueError("P98C extended audit must cover benchmark and related functions")

    safety = payload["safety"]
    expected_false = (
        "live_write_executed_in_p98c",
        "decision_journal_write_in_p98c",
        "apps_script_execution",
        "clasp_push",
        "broker_execution",
        "order_execution",
        "auto_sizing_execution",
        "trading_action",
    )
    enabled = [flag for flag in expected_false if safety.get(flag)]
    if enabled:
        raise ValueError(f"Unsafe P98C flags enabled: {enabled}")
    if safety.get("readonly_audit_only") is not True:
        raise ValueError("P98C must remain readonly audit only")

    for surface in payload["surfaces"]:
        if surface.get("write_in_p98c") is not False:
            raise ValueError(f"P98C surface write requested: {surface}")
        if surface.get("live_read_in_p98c") is not False:
            raise ValueError(f"P98C live read requested: {surface}")


def render_extended_cockpit_scope_audit_markdown(payload: dict[str, Any]) -> str:
    surface_lines = [
        (
            f"- {surface['surface_id']} / `{surface['sheet_name']}`: "
            f"{surface['classification']} -> {surface['target_card']}"
        )
        for surface in payload["surfaces"]
    ]
    card_lines = [f"- {card}" for card in payload["required_p98d_cards"]]

    return "\n".join(
        [
            "# MVP QAIC — P98C Extended Cockpit Scope Audit READONLY",
            "",
            f"- status: `{payload['status']}`",
            f"- surface_count: `{payload['surface_count']}`",
            f"- source_p98b_status: `{payload['source_p98b_status']}`",
            f"- next: `{payload['next']}`",
            "",
            "## Surfaces et fonctions a couvrir",
            "",
            *surface_lines,
            "",
            "## Cartes cockpit P98D proposees",
            "",
            *card_lines,
            "",
            "## Safety",
            "",
            "- read-only audit only",
            "- no live write in P98C",
            "- no Decision Journal write in P98C",
            "- no Apps Script execution",
            "- no CLASP push",
            "- no broker/order/sizing",
            "",
        ]
    )


def export_extended_cockpit_scope_audit(out_dir: str | Path) -> dict[str, str]:
    target = Path(out_dir)
    target.mkdir(parents=True, exist_ok=True)
    payload = build_extended_cockpit_scope_audit()
    assert_extended_cockpit_scope_audit_safe(payload)
    markdown = render_extended_cockpit_scope_audit_markdown(payload)
    json_path = target / "P98C_EXTENDED_COCKPIT_SCOPE_AUDIT_READONLY.json"
    md_path = target / "P98C_EXTENDED_COCKPIT_SCOPE_AUDIT_READONLY.md"
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
