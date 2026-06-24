"""P168A hierarchy and migration roadmap lock for MVP_QAIC_PY."""

from __future__ import annotations

import argparse
import csv
import json
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

STEP = "P168A_HIERARCHY_AND_MIGRATION_ROADMAP_LOCK"
STATUS = "P168A_HIERARCHY_AND_MIGRATION_ROADMAP_LOCK_READY_REVIEW_ONLY"

EXPORT_PREFIX_P165 = "P165_R3_INITIAL_SHEET_APPS_SCRIPT_FUNCTIONAL_LAYER_"
EXPORT_PREFIX_P166 = "P166_REFERENCE_PROMPT_REBUILD_FROM_SOURCE_INDEX_"
EXPORT_PREFIX_P167 = "P167_HUMAN_REVIEW_REFERENCE_PROMPT_GATE_"

SAFETY_FLAGS: dict[str, bool] = {
    "review_only": True,
    "runtime_prompt_modified": False,
    "apply_allowed": False,
    "google_sheets_write": False,
    "apps_script_execution": False,
    "clasp_push": False,
    "broker": False,
    "order": False,
    "sizing": False,
    "public_deploy": False,
}

DOMAIN_BOUNDARIES: list[dict[str, str]] = [
    {
        "domain": "MVP_QAIC_PY",
        "owner_role": "MVP product and operator layer",
        "allowed_scope": (
            "lexique, webapp/NiceGUI local private, prompt cockpit, prompt review, "
            "Sheets snapshots/read-only data migration, Apps Script functional recovery, "
            "operator handoff"
        ),
        "forbidden_scope": (
            "broker execution, real orders, auto sizing, Revolut X execution backend, "
            "QAIT assets, public deploy without explicit release gate"
        ),
        "source_of_truth": "mvp-qaic-python repository + reviewed Sheets/App Script snapshots",
    },
    {
        "domain": "QAIC_PY",
        "owner_role": "private crypto trading backend",
        "allowed_scope": (
            "technical backend, market/scoring/risk engine, Revolut X crypto lane, "
            "execution-capable modules locked by human review and safety gates"
        ),
        "forbidden_scope": "MVP public/webapp product surface, QAIT Revolut Invest lane, unreviewed prompt apply",
        "source_of_truth": "qaic-python-min-cost-dev-factory repository",
    },
    {
        "domain": "QAIT_PY",
        "owner_role": "actions and commodities trading backend",
        "allowed_scope": (
            "actions, commodities, Revolut Invest lane, BigQuery/read-only inventories, "
            "provider-specific evidence packs"
        ),
        "forbidden_scope": "MVP prompt cockpit, MVP lexique/webapp, QAIC Revolut X crypto lane",
        "source_of_truth": "qait-python-min-cost-dev-factory repository",
    },
]

MIGRATION_ROADMAP: list[dict[str, str]] = [
    {
        "priority": "P0",
        "next_batch": "P168B_SHEETS_DATA_SNAPSHOT_LAYER_READONLY",
        "domain": "MVP_QAIC_PY",
        "objective": (
            "Create a deterministic local Python snapshot layer for key MVP Sheets tabs "
            "using read-only exports or already-approved local snapshots."
        ),
        "inputs": "P165 source registry, live Sheets IDs, CONFIG/lexique/journal/prompt tables",
        "outputs": "tab registry, bounded CSV snapshots, schema/readiness report",
        "apply_mode": "READ_ONLY_NO_SHEET_WRITE",
        "status": "RECOMMENDED_NEXT",
    },
    {
        "priority": "P1",
        "next_batch": "P169_APPS_SCRIPT_TO_PYTHON_FUNCTIONAL_PORT_SELECTOR",
        "domain": "MVP_QAIC_PY",
        "objective": "Convert the 22 Apps Script modules and 2738 function index into a ranked Python migration backlog by feature lane.",
        "inputs": "P165_R3_APPS_SCRIPT_MODULE_INVENTORY.csv, P165_R3_FUNCTIONAL_MIGRATION_MAP.csv",
        "outputs": "module backlog, feature parity matrix, port/no-port decisions",
        "apply_mode": "LOCAL_REVIEW_ONLY",
        "status": "NEXT_AFTER_SNAPSHOT",
    },
    {
        "priority": "P2",
        "next_batch": "P170_PROMPT_COCKPIT_BINDING_TO_REFERENCE_PROMPT",
        "domain": "MVP_QAIC_PY",
        "objective": "Bind the reviewed reference prompt draft to local operator/NiceGUI prompt cockpit without automatic runtime replacement.",
        "inputs": "P166 reference draft, P167 review workbench, operator approval",
        "outputs": "prompt cockpit draft binding, preview smoke, manual apply gate",
        "apply_mode": "HUMAN_REVIEW_ONLY",
        "status": "WAIT_AFTER_P167_HUMAN_REVIEW",
    },
    {
        "priority": "P3",
        "next_batch": "QAIC_PY_HANDOFF_BACKEND_BOUNDARY_CHECK",
        "domain": "QAIC_PY",
        "objective": "Keep trading/backend execution outside MVP_QAIC_PY and document any later handoff contract to QAIC_PY.",
        "inputs": "MVP reviewed outputs only; no broker state copied into MVP",
        "outputs": "handoff contract, no-live safety checklist",
        "apply_mode": "SEPARATE_REPOSITORY_ONLY",
        "status": "NOT_MVP_NEXT_BATCH",
    },
    {
        "priority": "P4",
        "next_batch": "QAIT_PY_NOOP_BOUNDARY_CONFIRMATION",
        "domain": "QAIT_PY",
        "objective": "Keep actions/commodities and Revolut Invest work completely outside MVP_QAIC_PY.",
        "inputs": "none for MVP batch",
        "outputs": "boundary note only",
        "apply_mode": "NOOP_FOR_MVP",
        "status": "OUT_OF_SCOPE_FOR_MVP",
    },
]


def utc_stamp() -> str:
    return datetime.now(UTC).strftime("%Y%m%d_%H%M%S")


def discover_latest_export(project_root: Path, prefix: str) -> Path | None:
    exports_root = project_root / "05_EXPORTS"
    if not exports_root.exists():
        return None
    candidates = [p for p in exports_root.iterdir() if p.is_dir() and p.name.startswith(prefix)]
    if not candidates:
        return None
    return sorted(candidates, key=lambda item: item.name)[-1]


def read_json_if_exists(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return {"json_decode_error": str(path)}
    return data if isinstance(data, dict) else {"non_object_json": str(path)}


def find_summary_json(export_dir: Path | None) -> dict[str, Any]:
    if export_dir is None:
        return {}
    summary_files = sorted(export_dir.glob("*SUMMARY.json"), key=lambda item: item.name)
    if not summary_files:
        return {}
    return read_json_if_exists(summary_files[-1])


def _as_int(value: Any) -> int:
    try:
        return int(value or 0)
    except (TypeError, ValueError):
        return 0


def build_hierarchy_payload(project_root: Path) -> dict[str, Any]:
    p165_dir = discover_latest_export(project_root, EXPORT_PREFIX_P165)
    p166_dir = discover_latest_export(project_root, EXPORT_PREFIX_P166)
    p167_dir = discover_latest_export(project_root, EXPORT_PREFIX_P167)

    p165_summary = find_summary_json(p165_dir)
    p166_summary = find_summary_json(p166_dir)
    p167_summary = find_summary_json(p167_dir)

    blockers: list[str] = []
    if p165_dir is None:
        blockers.append("MISSING_P165_SOURCE_ACCESS_EXPORT")
    if p166_dir is None:
        blockers.append("MISSING_P166_REFERENCE_PROMPT_EXPORT")
    if p167_dir is None:
        blockers.append("MISSING_P167_HUMAN_REVIEW_GATE_EXPORT")

    source_milestones = {
        "p165_export_dir": str(p165_dir) if p165_dir else "",
        "p166_export_dir": str(p166_dir) if p166_dir else "",
        "p167_export_dir": str(p167_dir) if p167_dir else "",
        "p165_status": str(p165_summary.get("status") or p165_summary.get("P165_R3_STATUS") or ""),
        "p166_status": str(p166_summary.get("status") or p166_summary.get("P166_STATUS") or ""),
        "p167_status": str(p167_summary.get("status") or p167_summary.get("P167_STATUS") or ""),
        "apps_script_module_count": _as_int(
            p165_summary.get("apps_script_module_count")
            or p165_summary.get("APPS_SCRIPT_MODULE_COUNT")
        ),
        "apps_script_function_count": _as_int(
            p165_summary.get("apps_script_function_count")
            or p165_summary.get("APPS_SCRIPT_FUNCTION_COUNT")
        ),
        "prompt_engine_function_count": _as_int(
            p165_summary.get("prompt_engine_function_count")
            or p165_summary.get("PROMPT_ENGINE_FUNCTION_COUNT")
        ),
        "source_candidate_count": _as_int(
            p166_summary.get("source_candidate_count") or p166_summary.get("SOURCE_CANDIDATE_COUNT")
        ),
        "review_item_count": _as_int(
            p167_summary.get("review_item_count") or p167_summary.get("REVIEW_ITEM_COUNT")
        ),
        "pending_review_count": _as_int(
            p167_summary.get("pending_review_count") or p167_summary.get("PENDING_REVIEW_COUNT")
        ),
    }

    return {
        "step": STEP,
        "status": STATUS,
        "generated_at": datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z"),
        "project": "MVP_QAIC_PY",
        "hierarchy_locked": True,
        "domain_boundaries": DOMAIN_BOUNDARIES,
        "migration_roadmap": MIGRATION_ROADMAP,
        "source_milestones": source_milestones,
        "safety_flags": SAFETY_FLAGS,
        "blockers": blockers,
        "blocker_count": len(blockers),
        "next": "P168B_SHEETS_DATA_SNAPSHOT_LAYER_READONLY"
        if not blockers
        else "STOP_FIX_MISSING_EXPORTS",
    }


def _write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames: list[str] = sorted({key for row in rows for key in row.keys()})
    with path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def _write_markdown(path: Path, payload: dict[str, Any]) -> None:
    milestones = payload["source_milestones"]
    lines = [
        "# P168A — Hierarchy and Migration Roadmap Lock",
        "",
        f"- Status: `{payload['status']}`",
        f"- Project: `{payload['project']}`",
        f"- Hierarchy locked: `{payload['hierarchy_locked']}`",
        f"- Blocker count: `{payload['blocker_count']}`",
        f"- Next: `{payload['next']}`",
        "",
        "## Source milestones",
        "",
        f"- P165 export: `{milestones['p165_export_dir']}`",
        f"- Apps Script modules: `{milestones['apps_script_module_count']}`",
        f"- Apps Script functions: `{milestones['apps_script_function_count']}`",
        f"- Prompt/GPT/GEM functions: `{milestones['prompt_engine_function_count']}`",
        f"- P166 source candidates: `{milestones['source_candidate_count']}`",
        f"- P167 review items: `{milestones['review_item_count']}`",
        f"- P167 pending review: `{milestones['pending_review_count']}`",
        "",
        "## Locked domain boundaries",
        "",
    ]
    for boundary in payload["domain_boundaries"]:
        lines.extend(
            [
                f"### {boundary['domain']}",
                "",
                f"- Owner role: {boundary['owner_role']}",
                f"- Allowed scope: {boundary['allowed_scope']}",
                f"- Forbidden scope: {boundary['forbidden_scope']}",
                f"- Source of truth: {boundary['source_of_truth']}",
                "",
            ]
        )
    lines.extend(["## Recommended roadmap", ""])
    for item in payload["migration_roadmap"]:
        lines.extend(
            [
                f"### {item['priority']} — {item['next_batch']}",
                "",
                f"- Domain: `{item['domain']}`",
                f"- Objective: {item['objective']}",
                f"- Inputs: {item['inputs']}",
                f"- Outputs: {item['outputs']}",
                f"- Apply mode: `{item['apply_mode']}`",
                f"- Status: `{item['status']}`",
                "",
            ]
        )
    lines.extend(
        [
            "## Safety",
            "",
            "- No Google Sheets write.",
            "- No Apps Script execution.",
            "- No CLASP push.",
            "- No broker/order/sizing.",
            "- No runtime prompt modification.",
            "- Review-only roadmap lock.",
            "",
        ]
    )
    path.write_text("\n".join(lines), encoding="utf-8")


def build_export(project_root: Path, output_dir: Path | None = None) -> dict[str, Any]:
    payload = build_hierarchy_payload(project_root)
    if output_dir is None:
        output_dir = (
            project_root
            / "05_EXPORTS"
            / f"P168A_HIERARCHY_AND_MIGRATION_ROADMAP_LOCK_{utc_stamp()}"
        )
    output_dir.mkdir(parents=True, exist_ok=True)
    payload["output_dir"] = str(output_dir)
    (output_dir / "P168A_SUMMARY.json").write_text(
        json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8"
    )
    _write_csv(output_dir / "P168A_DOMAIN_BOUNDARY_MATRIX.csv", payload["domain_boundaries"])
    _write_csv(output_dir / "P168A_MIGRATION_ROADMAP.csv", payload["migration_roadmap"])
    _write_csv(
        output_dir / "P168A_NEXT_BATCH_QUEUE.csv",
        [
            row
            for row in payload["migration_roadmap"]
            if row["status"]
            in {"RECOMMENDED_NEXT", "NEXT_AFTER_SNAPSHOT", "WAIT_AFTER_P167_HUMAN_REVIEW"}
        ],
    )
    _write_markdown(output_dir / "P168A_HIERARCHY_AND_MIGRATION_ROADMAP_LOCK.md", payload)
    _write_markdown(output_dir / "P168A_GATE_REPORT.md", payload)
    return payload


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=STEP)
    parser.add_argument("--project-root", type=Path, default=Path.cwd())
    parser.add_argument("--output-dir", type=Path, default=None)
    args = parser.parse_args(argv)
    payload = build_export(args.project_root, args.output_dir)
    print(STATUS)
    print(f"hierarchy_locked={payload['hierarchy_locked']}")
    print(f"blocker_count={payload['blocker_count']}")
    print(f"output_dir={payload['output_dir']}")
    print(f"next={payload['next']}")
    return 0 if payload["blocker_count"] == 0 else 2


if __name__ == "__main__":
    raise SystemExit(main())
