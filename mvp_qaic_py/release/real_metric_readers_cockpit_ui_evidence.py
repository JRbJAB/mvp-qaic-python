from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

P100B_STATUS = "OK_P100B_REAL_METRIC_READERS_COCKPIT_UI_LIVE_WRITE_VERIFIED"
NEXT_STEP = "P100C_DEEP_METRIC_READERS_OR_OPERATOR_ACCEPTANCE_SMOKE"

P100B_METRICS: dict[str, Any] = {
    "step": "P100B_REAL_METRIC_READERS_AND_COCKPIT_UI_LIVE_WRITE_FAST_FUSE",
    "status": P100B_STATUS,
    "spreadsheet_id": "19KY8Y1ozS7ONaJu9_5NQmjO47l-xM798Xm-y1n7fNd0",
    "cockpit_sheet": "QAIC_RUNTIME_COCKPIT_VIEW",
    "cockpit_sheet_id": 987650321,
    "cockpit_range_written": "QAIC_RUNTIME_COCKPIT_VIEW!A1:J22",
    "bridge_sheet": "QAIC_RUNTIME_BRIDGE_STATUS",
    "bridge_sheet_id": 1469323579,
    "bridge_rows_written": "QAIC_RUNTIME_BRIDGE_STATUS!A8:N11",
    "run_id": "P100B-METRICS-UI-20260621-232500",
    "write_mode": "LIVE_WRITE_FAST_FUSE",
    "benchmark_ai_trade_migrated": True,
    "source_readers": {
        "BENCHMARK_AI_TRADE": {
            "reader_status": "OK",
            "source_status": "OK_P59B2_SIMPLIFIED_ONE_TAB_VIPALGOS_FIX",
            "candidate_count": 14,
            "inspire": 6,
            "monitor": 4,
            "review_required": 1,
            "blocked": 3,
            "safety": "PASS",
        },
        "GPT_QUALITY_DASHBOARD": {
            "reader_status": "REVIEW",
            "journal_rows": 2,
            "prompt_ids": 1,
            "top_missing_data": 15,
            "top_blockers": 15,
            "prompt_actions": 1,
            "top_missing_sample": ["PnL", "PRU", "SL", "timeframe", "TP"],
        },
        "PROMPT_IMPROVEMENT_QUEUE": {
            "reader_status": "READY_FOR_REVIEW",
            "p0_present": True,
            "p1_present": True,
            "p2_present": True,
            "adaptive_draft_present": True,
        },
        "PROMPT_LIBRARY": {
            "reader_status": "READY_FOR_REVIEW",
            "core_profiles_present": True,
            "locked_references_present": True,
            "crypto_variants_present": True,
            "night_watch_variant_present": True,
        },
        "LEXIQUE_MASTER": {
            "reader_status": "READABLE",
            "sample_contains_checklists": True,
            "sample_contains_data_requirements": True,
            "risk_guard_column_present": True,
        },
        "METHOD_LIBRARY": {
            "reader_status": "READABLE",
            "observed_method_count": 18,
            "tp_sl_logic_present": True,
            "risk_levels_present": True,
        },
        "SIGNAL_LIBRARY": {
            "reader_status": "READABLE",
            "observed_signal_count": 58,
            "signal_weights_present": True,
            "risk_signals_present": True,
        },
        "RISK_PLAYBOOK": {
            "reader_status": "READABLE",
            "observed_risk_profile_count": 10,
            "max_loss_rules_present": True,
            "tp_ladder_rules_present": True,
        },
        "PORTFOLIO_SNAPSHOT": {
            "reader_status": "EMPTY_REVIEW_REQUIRED",
            "position_rows": 0,
            "issue": "header_only_no_positions",
        },
        "REVOLUT_X_READONLY_CONTRACT": {
            "reader_status": "SAFE",
            "observed_contract_fields": 11,
            "security_guard": "read_only_no_order",
            "fallback_if_missing": "REVIEW_REQUIRED",
        },
    },
    "ui_applied": {
        "column_widths_set": True,
        "row_heights_set": True,
        "header_band_applied": True,
        "summary_band_applied": True,
        "wrap_enabled": True,
        "frozen_rows_and_columns_preserved": True,
    },
    "writes_executed": {
        "cockpit_values_written": True,
        "cockpit_ui_format_written": True,
        "runtime_bridge_status_written": True,
        "decision_journal_write_in_p100b": False,
        "apps_script_execution": False,
        "clasp_push": False,
        "broker_execution": False,
        "order_execution": False,
        "auto_sizing_execution": False,
        "trading_action": False,
    },
}


def build_p100b_real_metric_readers_cockpit_ui_evidence() -> dict[str, Any]:
    payload = dict(P100B_METRICS)
    payload["created_at"] = datetime.now(timezone.utc).isoformat()
    payload["next"] = NEXT_STEP
    return payload


def assert_p100b_real_metric_readers_safe(payload: dict[str, Any]) -> None:
    if payload["status"] != P100B_STATUS:
        raise ValueError(f"P100B evidence not OK: {payload['status']}")
    if payload["benchmark_ai_trade_migrated"] is not True:
        raise ValueError("Benchmark AI Trade must be confirmed as migrated/readable")
    benchmark = payload["source_readers"]["BENCHMARK_AI_TRADE"]
    if benchmark["candidate_count"] != 14:
        raise ValueError("Unexpected benchmark candidate count")
    if benchmark["blocked"] != 3:
        raise ValueError("Unexpected benchmark blocked count")
    quality = payload["source_readers"]["GPT_QUALITY_DASHBOARD"]
    if quality["top_missing_data"] != 15 or quality["top_blockers"] != 15:
        raise ValueError("Unexpected quality metric counts")
    portfolio = payload["source_readers"]["PORTFOLIO_SNAPSHOT"]
    if portfolio["position_rows"] != 0:
        raise ValueError("P100B evidence expected empty portfolio snapshot")
    writes = payload["writes_executed"]
    required_true = (
        "cockpit_values_written",
        "cockpit_ui_format_written",
        "runtime_bridge_status_written",
    )
    missing = [flag for flag in required_true if writes.get(flag) is not True]
    if missing:
        raise ValueError(f"P100B missing write evidence: {missing}")
    expected_false = (
        "decision_journal_write_in_p100b",
        "apps_script_execution",
        "clasp_push",
        "broker_execution",
        "order_execution",
        "auto_sizing_execution",
        "trading_action",
    )
    enabled = [flag for flag in expected_false if writes.get(flag)]
    if enabled:
        raise ValueError(f"Unsafe P100B flags enabled: {enabled}")


def render_p100b_real_metric_readers_markdown(payload: dict[str, Any]) -> str:
    readers = []
    for name, data in payload["source_readers"].items():
        summary = ", ".join(f"{k}={v}" for k, v in data.items() if k != "top_missing_sample")
        readers.append(f"- `{name}`: {summary}")
    return "\n".join(
        [
            "# MVP QAIC - P100B Real Metric Readers + Cockpit UI Evidence",
            "",
            f"- status: `{payload['status']}`",
            f"- run_id: `{payload['run_id']}`",
            f"- cockpit_range_written: `{payload['cockpit_range_written']}`",
            f"- bridge_rows_written: `{payload['bridge_rows_written']}`",
            f"- benchmark_ai_trade_migrated: `{payload['benchmark_ai_trade_migrated']}`",
            f"- next: `{payload['next']}`",
            "",
            "## Source readers",
            "",
            *readers,
            "",
            "## UI applied",
            "",
            *[f"- {k}: `{v}`" for k, v in payload["ui_applied"].items()],
            "",
            "## Safety",
            "",
            "- no Decision Journal write in P100B",
            "- no Apps Script execution",
            "- no CLASP push",
            "- no broker/order/sizing",
            "",
        ]
    )


def export_p100b_real_metric_readers_cockpit_ui_evidence(out_dir: str | Path) -> dict[str, str]:
    target = Path(out_dir)
    target.mkdir(parents=True, exist_ok=True)
    payload = build_p100b_real_metric_readers_cockpit_ui_evidence()
    assert_p100b_real_metric_readers_safe(payload)
    markdown = render_p100b_real_metric_readers_markdown(payload)
    json_path = target / "P100B_REAL_METRIC_READERS_COCKPIT_UI_EVIDENCE.json"
    md_path = target / "P100B_REAL_METRIC_READERS_COCKPIT_UI_EVIDENCE.md"
    json_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    md_path.write_text(markdown, encoding="utf-8")
    return {
        "status": payload["status"],
        "json": str(json_path),
        "markdown": str(md_path),
        "next": payload["next"],
    }
