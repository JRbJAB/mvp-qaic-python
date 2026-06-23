from __future__ import annotations

import argparse
import csv
import json
import sys
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

VERSION = "MVP_QAIC_P148_SYNC_STRATEGY_READONLY_1.0.0_SAFE"
STATUS_RENDERED = "P148_SYNC_STRATEGY_READONLY_RENDERED"

SAFETY_MARKERS = {
    "strategy_only": True,
    "live_google_sheets_read": False,
    "google_sheets_write": False,
    "apps_script_execution": False,
    "clasp_push": False,
    "broker": False,
    "order": False,
    "sizing": False,
    "auto_apply_gem_response": False,
    "public_deploy": False,
    "requires_explicit_future_go_for_any_write": True,
}


@dataclass(frozen=True)
class SyncStrategyRequest:
    p147_model_path: Path
    p143b_binding_path: Path
    output_dir: Path
    run_id: str
    generated_at_utc: str


def utc_now_iso() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def validate_sources(p147_model: dict[str, Any], p143b_binding: dict[str, Any]) -> None:
    if p147_model.get("status") != "P147_OPERATOR_POLISH_RENDERED_LOCAL_PRIVATE":
        raise ValueError(f"Invalid P147 status: {p147_model.get('status')}")
    if p143b_binding.get("status") != "P143B_DATA_PREVIEW_SOURCE_EXPANSION_RENDERED_LOCAL_READONLY":
        raise ValueError(f"Invalid P143B status: {p143b_binding.get('status')}")
    review_policy = p147_model.get("review_policy", {})
    if review_policy.get("apply_to_sheet_enabled") is not False:
        raise ValueError("P147 apply_to_sheet_enabled must remain false")
    if review_policy.get("auto_apply_gem_response_enabled") is not False:
        raise ValueError("P147 auto_apply_gem_response_enabled must remain false")


def build_source_registry(binding: dict[str, Any]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for index, item in enumerate(binding.get("bindings", []), start=1):
        rows.append(
            {
                "registry_id": f"P148-SOURCE-{index:03d}",
                "page_id": item.get("page_id", ""),
                "title": item.get("title", ""),
                "route": item.get("route", ""),
                "binding_mode": item.get("binding_mode", ""),
                "source_csv": item.get("source_csv", ""),
                "source_filename": item.get("source_filename", ""),
                "source_rows_total": item.get("source_rows_total", 0),
                "preview_row_count": item.get("preview_row_count", 0),
                "sync_direction": "SHEETS_TO_LOCAL_SNAPSHOT",
                "write_allowed": False,
                "read_live_allowed_now": False,
                "requires_future_explicit_go": True,
            }
        )
    return rows


def build_sync_steps(source_registry: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [
        {
            "step_id": "P148-STEP-001",
            "name": "freeze_current_local_sources",
            "description": "Geler les CSV/metadata locaux utilisés par le cockpit actuel.",
            "gate": "LOCAL_ONLY",
            "write_allowed": False,
        },
        {
            "step_id": "P148-STEP-002",
            "name": "define_sheet_to_snapshot_contract",
            "description": "Définir le contrat futur de snapshot depuis Sheets vers fichiers locaux, sans écriture Sheets.",
            "gate": "READONLY_DESIGN",
            "write_allowed": False,
        },
        {
            "step_id": "P148-STEP-003",
            "name": "map_11_cockpit_pages",
            "description": f"Mapper {len(source_registry)} pages cockpit vers leurs sources locales et fallback.",
            "gate": "METADATA_READY",
            "write_allowed": False,
        },
        {
            "step_id": "P148-STEP-004",
            "name": "prepare_future_write_gate",
            "description": "Préparer un futur GO séparé pour toute écriture Google Sheets, non activé ici.",
            "gate": "FUTURE_GO_REQUIRED",
            "write_allowed": False,
        },
        {
            "step_id": "P148-STEP-005",
            "name": "migration_close_readiness",
            "description": "Préparer P149 migration close gate avec preuves, tags, runbook.",
            "gate": "READY_FOR_P149",
            "write_allowed": False,
        },
    ]


def build_strategy(p147_model: dict[str, Any], p143b_binding: dict[str, Any]) -> dict[str, Any]:
    validate_sources(p147_model, p143b_binding)
    registry = build_source_registry(p143b_binding)
    steps = build_sync_steps(registry)
    return {
        "status": STATUS_RENDERED,
        "version": VERSION,
        "source_p147_status": p147_model.get("status"),
        "source_p143b_status": p143b_binding.get("status"),
        "registry_row_count": len(registry),
        "sync_step_count": len(steps),
        "source_registry": registry,
        "sync_steps": steps,
        "policy": {
            "default_sync_direction": "SHEETS_TO_LOCAL_SNAPSHOT",
            "local_snapshot_is_ui_source": True,
            "sheets_is_reference_source": True,
            "write_back_allowed_now": False,
            "live_read_allowed_now": False,
            "future_sheet_write_requires_explicit_go": True,
            "future_public_deploy_requires_explicit_go": True,
        },
        "p149_readiness": {
            "migration_close_gate_ready": True,
            "requires_no_more_preclose_dev_batches": False,
            "required_evidence": [
                "P147 operator polish sealed",
                "P143B 11 pages bound",
                "P145 GEM import local review validated",
                "P146 correction queue review-only sealed",
                "P148 sync strategy sealed",
            ],
        },
        "safety": dict(SAFETY_MARKERS),
        "next": "P149_MIGRATION_CLOSE_GATE",
    }


def write_outputs(strategy: dict[str, Any], output_dir: Path) -> dict[str, str]:
    output_dir.mkdir(parents=True, exist_ok=True)
    strategy_path = output_dir / "P148_SYNC_STRATEGY_READONLY.json"
    registry_path = output_dir / "P148_SOURCE_REGISTRY.csv"
    steps_path = output_dir / "P148_SYNC_STEPS.csv"
    md_path = output_dir / "P148_SYNC_STRATEGY_READONLY.md"
    summary_path = output_dir / "P148_SUMMARY.json"

    strategy_path.write_text(
        json.dumps(strategy, ensure_ascii=False, indent=2, sort_keys=True), encoding="utf-8"
    )

    with registry_path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=list(strategy["source_registry"][0].keys())
            if strategy["source_registry"]
            else ["registry_id"],
        )
        writer.writeheader()
        for row in strategy["source_registry"]:
            writer.writerow(row)

    with steps_path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(
            handle, fieldnames=["step_id", "name", "description", "gate", "write_allowed"]
        )
        writer.writeheader()
        for row in strategy["sync_steps"]:
            writer.writerow(row)

    md_path.write_text(
        "\n".join(
            [
                "# P148 — Sync Strategy Read-Only",
                "",
                f"- Status: `{strategy['status']}`",
                f"- Registry rows: `{strategy['registry_row_count']}`",
                f"- Sync steps: `{strategy['sync_step_count']}`",
                "",
                "## Politique",
                "",
                "- Sheets = source de référence",
                "- Local snapshots = source UI privée",
                "- Aucune écriture Sheets dans P148",
                "- Aucun live read dans P148",
                "- Toute écriture future nécessite un GO séparé",
                "",
                "## Safety",
                "",
                "- No Sheet write",
                "- No Apps Script / CLASP",
                "- No broker/order/sizing",
                "- No public deploy",
                "",
                f"Next: `{strategy['next']}`",
                "",
            ]
        ),
        encoding="utf-8",
    )

    summary = {
        "status": strategy["status"],
        "registry_row_count": strategy["registry_row_count"],
        "sync_step_count": strategy["sync_step_count"],
        "migration_close_gate_ready": strategy["p149_readiness"]["migration_close_gate_ready"],
        "google_sheets_write": False,
        "live_google_sheets_read": False,
        "future_sheet_write_requires_explicit_go": True,
        "public_deploy": False,
        "broker": False,
        "order": False,
        "sizing": False,
        "output_dir": str(output_dir),
        "next": strategy["next"],
    }
    summary_path.write_text(
        json.dumps(summary, ensure_ascii=False, indent=2, sort_keys=True), encoding="utf-8"
    )
    return {
        "strategy_json": str(strategy_path),
        "source_registry_csv": str(registry_path),
        "sync_steps_csv": str(steps_path),
        "markdown": str(md_path),
        "summary_json": str(summary_path),
    }


def run_strategy(request: SyncStrategyRequest) -> dict[str, Any]:
    p147_model = load_json(request.p147_model_path)
    p143b_binding = load_json(request.p143b_binding_path)
    strategy = build_strategy(p147_model, p143b_binding)
    strategy["run_id"] = request.run_id
    strategy["generated_at_utc"] = request.generated_at_utc
    strategy["source_p147_model_path"] = str(request.p147_model_path)
    strategy["source_p143b_binding_path"] = str(request.p143b_binding_path)
    outputs = write_outputs(strategy, request.output_dir)
    strategy["output_files"] = outputs
    (request.output_dir / "P148_SYNC_STRATEGY_READONLY.json").write_text(
        json.dumps(strategy, ensure_ascii=False, indent=2, sort_keys=True),
        encoding="utf-8",
    )
    return strategy


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="P148 sync strategy read-only.")
    parser.add_argument("--p147-model", required=True)
    parser.add_argument("--p143b-binding", required=True)
    parser.add_argument("--output-dir", required=True)
    parser.add_argument("--run-id", default="P148-SYNC-STRATEGY-READONLY")
    parser.add_argument("--generated-at-utc", default=utc_now_iso())
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    strategy = run_strategy(
        SyncStrategyRequest(
            p147_model_path=Path(args.p147_model),
            p143b_binding_path=Path(args.p143b_binding),
            output_dir=Path(args.output_dir),
            run_id=args.run_id,
            generated_at_utc=args.generated_at_utc,
        )
    )
    print(strategy["status"])
    print(f"registry_row_count={strategy['registry_row_count']}")
    print(f"sync_step_count={strategy['sync_step_count']}")
    print("migration_close_gate_ready=true")
    print("google_sheets_write=false")
    print("live_google_sheets_read=false")
    print("future_sheet_write_requires_explicit_go=true")
    print(f"output_dir={args.output_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
