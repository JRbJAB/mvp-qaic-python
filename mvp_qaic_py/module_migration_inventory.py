from __future__ import annotations

import csv
import json
from collections import Counter
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, Mapping

VERSION = "MVP_QAIC_P115_MODULE_MIGRATION_INVENTORY_0_1_0_SAFE"

SAFETY_MARKERS = (
    "MVP_PUBLIC_SCOPE",
    "HUMAN_REVIEW_ONLY",
    "NO_INDEX_EDIT",
    "NO_CLASP",
    "NO_APPS_SCRIPT_EXECUTION",
    "NO_SHEET_WRITE",
    "NO_PUBLIC_DEPLOY",
    "NO_BROKER",
    "NO_ORDER",
    "NO_AUTO_SIZING",
    "NO_REVOLUTX_REAL_ACCESS_FROM_MVP",
    "QAIC_BACKEND_PRIVATE_SEPARATE",
)

SKIP_DIRS = {".git", ".venv", "venv", "__pycache__", ".pytest_cache", ".ruff_cache", "node_modules"}
ALLOWED_SUFFIXES = {".py", ".gs", ".js", ".html", ".json", ".md", ".csv", ".ts"}

PRIORITY_ORDER = {
    "PROMPT_GEM_RUNTIME": 1,
    "PORTFOLIO_INPUT_NORMALIZER": 2,
    "BENCHMARK_PROMPT_QUALITY": 3,
    "WEBAPP_DATA_PACKS": 4,
    "LEXIQUE_METHODS_SIGNALS": 5,
    "DECISION_JOURNAL_REVIEW_PACK": 6,
    "UI_APPS_SCRIPT_INDEX": 7,
    "QAIC_BACKEND_PRIVATE_REVOLUTX": 8,
    "UNKNOWN_REVIEW_REQUIRED": 99,
}


@dataclass(frozen=True)
class MigrationCandidate:
    path: str
    suffix: str
    source_area: str
    category: str
    priority_rank: int
    migration_decision: str
    suggested_python_target: str
    reason: str
    safety_boundary: str


def _iter_project_files(root: Path, max_files: int) -> list[Path]:
    files: list[Path] = []
    for path in sorted(root.rglob("*")):
        if not path.is_file():
            continue
        rel_parts = set(path.relative_to(root).parts)
        if rel_parts & SKIP_DIRS:
            continue
        if path.name.lower() == "desktop.ini":
            continue
        if path.suffix.lower() not in ALLOWED_SUFFIXES:
            continue
        files.append(path)
        if len(files) >= max_files:
            break
    return files


def detect_source_area(relpath: str, suffix: str) -> str:
    text = relpath.lower()
    if suffix == ".gs":
        return "apps_script_gs"
    if suffix in {".html", ".js", ".ts"}:
        if "apps_script" in text or "index" in text or "webapp" in text:
            return "apps_script_webapp_or_frontend"
        return "frontend_or_script"
    if suffix == ".py":
        return "python"
    if suffix in {".json", ".csv"}:
        return "data_or_export"
    if suffix == ".md":
        return "documentation"
    return "other"


def classify_path(relpath: str, suffix: str) -> tuple[str, str, str, str]:
    text = relpath.lower()

    if "revolut" in text or "broker" in text or "order" in text or "execution" in text:
        return (
            "QAIC_BACKEND_PRIVATE_REVOLUTX",
            "OUT_OF_SCOPE_FOR_MVP_KEEP_QAIC_PRIVATE",
            "qaic_backend_private_not_mvp",
            "Revolut X, broker and execution belong to private QAIC backend, not public MVP.",
        )

    if (
        "mvpqaic_index" in text
        or text.endswith("index.html")
        or ("index" in text and suffix == ".html")
    ):
        return (
            "UI_APPS_SCRIPT_INDEX",
            "DO_NOT_MIGRATE_NOW_REVIEW_ONLY",
            "no_immediate_python_target",
            "Canonical Index/WebApp UI must not be migrated or patched in this batch.",
        )

    if "normalizer" in text or "portfolio_input" in text:
        return (
            "PORTFOLIO_INPUT_NORMALIZER",
            "KEEP_AND_HARDEN_IN_PYTHON",
            "mvp_qaic_py.portfolio_input_normalizer",
            "Portfolio input normalization should stay MVP-safe in Python.",
        )

    if "prompt" in text or "gem" in text or "runner" in text:
        return (
            "PROMPT_GEM_RUNTIME",
            "MIGRATE_OR_KEEP_IN_PYTHON_PRIORITY_1",
            "mvp_qaic_py.gem_prompt_runtime",
            "Prompt/GEM runtime is the first migration priority for usable portfolio tests.",
        )

    if "benchmark" in text or "quality" in text or "eval" in text:
        return (
            "BENCHMARK_PROMPT_QUALITY",
            "MIGRATE_TO_PYTHON_AFTER_PROMPT_RUNTIME",
            "mvp_qaic_py.benchmark_prompt_quality",
            "Benchmark and prompt quality logic belongs in local Python tests and exports.",
        )

    if "webapp" in text or "payload" in text or "data_pack" in text or "runtime" in text:
        return (
            "WEBAPP_DATA_PACKS",
            "MIGRATE_DATA_PACK_GENERATION_TO_PYTHON",
            "mvp_qaic_py.webapp_data_packs",
            "WebApp static data packs can be generated in Python without touching Apps Script live.",
        )

    if "lexique" in text or "method" in text or "methode" in text or "signal" in text:
        return (
            "LEXIQUE_METHODS_SIGNALS",
            "MIGRATE_CONTENT_PIPELINE_TO_PYTHON",
            "mvp_qaic_py.lexique_content_pipeline",
            "Lexique, methods and signals content should be curated in Python data pipelines.",
        )

    if "journal" in text or "decision" in text or "review" in text:
        return (
            "DECISION_JOURNAL_REVIEW_PACK",
            "MIGRATE_REVIEW_PACKS_TO_PYTHON",
            "mvp_qaic_py.decision_review_pack",
            "Decision journal and review packs should become reproducible Python exports.",
        )

    return (
        "UNKNOWN_REVIEW_REQUIRED",
        "REVIEW_REQUIRED_BEFORE_MIGRATION",
        "to_be_decided",
        "No stable migration category detected from bounded local scan.",
    )


def build_migration_inventory(project_root: str | Path, max_files: int = 5000) -> dict[str, Any]:
    root = Path(project_root).resolve()
    candidates: list[MigrationCandidate] = []

    for path in _iter_project_files(root, max_files):
        relpath = path.relative_to(root).as_posix()
        suffix = path.suffix.lower()
        category, decision, target, reason = classify_path(relpath, suffix)
        boundary = (
            "QAIC_PRIVATE_BACKEND_SEPARATE_FROM_MVP"
            if category == "QAIC_BACKEND_PRIVATE_REVOLUTX"
            else "MVP_PUBLIC_HUMAN_REVIEW_ONLY"
        )
        candidates.append(
            MigrationCandidate(
                path=relpath,
                suffix=suffix,
                source_area=detect_source_area(relpath, suffix),
                category=category,
                priority_rank=PRIORITY_ORDER.get(category, 99),
                migration_decision=decision,
                suggested_python_target=target,
                reason=reason,
                safety_boundary=boundary,
            )
        )

    ranked = sorted(candidates, key=lambda c: (c.priority_rank, c.category, c.path.lower()))
    return {
        "step": "P115_MODULE_MIGRATION_INVENTORY_APPS_SCRIPT_TO_PYTHON",
        "version": VERSION,
        "status": "REVIEW_REQUIRED",
        "project_scope": "MVP_QAIC_PUBLIC_LEXIQUE_WEBAPP_PROMPTS_METHODS_BENCHMARK_PORTFOLIO_REVIEW",
        "qaic_backend_scope": "SEPARATE_PRIVATE_QAIC_BACKEND_REVOLUTX_RISK_ENGINE_EXECUTION_LOCKED",
        "safety_markers": list(SAFETY_MARKERS),
        "candidate_count": len(ranked),
        "category_counts": dict(sorted(Counter(c.category for c in ranked).items())),
        "decision_counts": dict(sorted(Counter(c.migration_decision for c in ranked).items())),
        "source_area_counts": dict(sorted(Counter(c.source_area for c in ranked).items())),
        "priority_order": PRIORITY_ORDER,
        "candidates": [asdict(candidate) for candidate in ranked],
    }


def build_boundary_contract() -> dict[str, Any]:
    return {
        "contract": "P115_MODULE_MIGRATION_BOUNDARY_CONTRACT",
        "version": VERSION,
        "mvp_allowed_scope": [
            "lexique",
            "webapp_static_data_packs",
            "prompts",
            "methods",
            "benchmark",
            "portfolio_review_human_review_only",
            "decision_review_exports",
        ],
        "mvp_forbidden_scope": [
            "revolutx_real_access",
            "broker_execution",
            "order_execution",
            "auto_sizing",
            "secret_storage",
            "public_deploy_in_this_batch",
            "apps_script_live_execution",
            "sheet_write",
            "clasp_push",
        ],
        "qaic_private_scope": [
            "risk_engine",
            "revolutx_adapter",
            "broker_contracts",
            "execution_capable_but_locked",
            "private_backend",
        ],
        "index_policy": "DO_NOT_EDIT_OR_MIGRATE_NOW_SEPARATE_BATCH_REQUIRED",
        "safety_markers": list(SAFETY_MARKERS),
    }


def _write_json(path: Path, payload: Mapping[str, Any]) -> None:
    path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )


def _write_csv(path: Path, candidates: list[dict[str, Any]]) -> None:
    fields = [
        "priority_rank",
        "category",
        "migration_decision",
        "source_area",
        "path",
        "suffix",
        "suggested_python_target",
        "safety_boundary",
        "reason",
    ]
    with path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        for row in candidates:
            writer.writerow({field: row.get(field, "") for field in fields})


def _priority_markdown(inventory: Mapping[str, Any]) -> str:
    lines = [
        "# P115 Module Migration Priority Matrix",
        "",
        f"- status: {inventory['status']}",
        f"- version: {inventory['version']}",
        f"- candidate_count: {inventory['candidate_count']}",
        "- safety: HUMAN_REVIEW_ONLY / NO_CLASP / NO_APPS_SCRIPT_EXECUTION / NO_SHEET_WRITE",
        "",
        "## Priority order",
        "",
        "1. Prompt / GEM runtime",
        "2. Portfolio input normalizer",
        "3. Benchmark prompt quality",
        "4. WebApp static data packs",
        "5. Lexique / methods / signals",
        "6. Decision journal / review packs",
        "7. UI Apps Script / Index: no immediate migration",
        "8. QAIC backend / Revolut X: private QAIC project, out of MVP",
        "",
        "## Category counts",
        "",
    ]
    lines.extend(f"- {k}: {v}" for k, v in inventory["category_counts"].items())
    lines.extend(["", "## Top candidates", ""])
    for candidate in inventory["candidates"][:30]:
        lines.append(
            f"- P{candidate['priority_rank']} | {candidate['category']} | "
            f"{candidate['migration_decision']} | `{candidate['path']}`"
        )
    lines.extend(["", "## Next", "", "P116_PROMPT_GEM_RUNTIME_MINI_CLI", ""])
    return "\n".join(lines)


def _report_markdown(inventory: Mapping[str, Any], output_dir: str) -> str:
    return "\n".join(
        [
            "# P115 Module Migration Inventory Report",
            "",
            f"- status: {inventory['status']}",
            f"- version: {inventory['version']}",
            f"- output_dir: {output_dir}",
            f"- candidate_count: {inventory['candidate_count']}",
            "- mvp_scope: lexique + webapp + prompts + methods + benchmark + portfolio review",
            "- qaic_backend_scope: separate private backend, Revolut X and execution locked",
            "- index_policy: no edit / no migration now",
            "- safety: no clasp / no Apps Script / no Sheet write / no public deploy / no broker/order/sizing",
            "",
            "## Recommendation",
            "",
            "Start P116 with the Prompt/GEM runtime mini CLI.",
            "",
        ]
    )


def export_migration_inventory_pack(
    output_dir: str | Path, project_root: str | Path
) -> dict[str, Any]:
    out = Path(output_dir)
    out.mkdir(parents=True, exist_ok=True)

    inventory = build_migration_inventory(project_root)
    contract = build_boundary_contract()

    json_path = out / "P115_MODULE_MIGRATION_INVENTORY.json"
    csv_path = out / "P115_MODULE_MIGRATION_INVENTORY.csv"
    matrix_path = out / "P115_MIGRATION_PRIORITY_MATRIX.md"
    contract_path = out / "P115_MIGRATION_BOUNDARY_CONTRACT.json"
    report_path = out / "P115_RUNNER_REPORT.md"

    _write_json(json_path, inventory)
    _write_csv(csv_path, inventory["candidates"])
    matrix_path.write_text(_priority_markdown(inventory), encoding="utf-8")
    _write_json(contract_path, contract)
    report_path.write_text(_report_markdown(inventory, str(out)), encoding="utf-8")

    return {
        "status": "EXPORTED",
        "step": "P115_MODULE_MIGRATION_INVENTORY_APPS_SCRIPT_TO_PYTHON",
        "output_dir": str(out),
        "files": [
            str(json_path),
            str(csv_path),
            str(matrix_path),
            str(contract_path),
            str(report_path),
        ],
        "candidate_count": inventory["candidate_count"],
        "category_counts": inventory["category_counts"],
        "safety_markers": list(SAFETY_MARKERS),
    }
