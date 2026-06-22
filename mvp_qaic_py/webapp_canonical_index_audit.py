from __future__ import annotations

import json
from datetime import UTC, datetime
from pathlib import Path
from typing import Any


CANONICAL_INDEX_AUDIT_SAFETY: dict[str, bool] = {
    "mvp_public_scope": True,
    "qaic_private_backend_separated": True,
    "readonly_audit_only": True,
    "patch_plan_only": True,
    "no_index_html_edit": True,
    "no_index_html_generation": True,
    "no_revolutx_real_access": True,
    "no_broker": True,
    "no_order": True,
    "no_cancel": True,
    "no_replace_order": True,
    "no_auto_sizing": True,
    "no_secret_log": True,
    "no_sheet_write": True,
    "no_apps_script_execution": True,
    "no_clasp": True,
    "no_public_deploy": True,
}


INDEX_FILE_NAMES: tuple[str, ...] = (
    "index.html",
    "mvpqaic_index.html",
    "mvpqaic-index.html",
)

SKIP_DIR_NAMES: set[str] = {
    ".git",
    ".venv",
    "__pycache__",
    ".pytest_cache",
    ".ruff_cache",
    "node_modules",
}


def _now_iso(now_utc: str | None = None) -> str:
    if now_utc:
        return now_utc
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def _safe_relative(path: Path, root: Path) -> str:
    try:
        return path.relative_to(root).as_posix()
    except ValueError:
        return path.as_posix()


def _dedupe_key(path: Path) -> str:
    try:
        return str(path.resolve()).casefold()
    except OSError:
        return str(path).casefold()


def _is_index_like(path: Path) -> bool:
    return path.name.casefold() in INDEX_FILE_NAMES


def classify_index_candidate(relative_path: str) -> dict[str, Any]:
    path_cf = relative_path.casefold()
    name_cf = Path(relative_path).name.casefold()

    if "/05_exports/" in f"/{path_cf}/" or path_cf.startswith("05_exports/"):
        return {
            "candidate_role": "generated_export_not_canonical",
            "canonical_score": 0,
            "allowed_to_edit": False,
            "reason": "Generated export artifact, not the validated WebApp shell.",
        }

    if "static_preview" in path_cf or "release_candidate_private_preview" in path_cf:
        return {
            "candidate_role": "local_preview_not_canonical",
            "canonical_score": 0,
            "allowed_to_edit": False,
            "reason": "Local preview/admin artifact, not canonical UI.",
        }

    if "03_dev" in path_cf and ("apps_script" in path_cf or "mirror" in path_cf):
        return {
            "candidate_role": "possible_canonical_apps_script_mirror",
            "canonical_score": 80,
            "allowed_to_edit": False,
            "reason": "Apps Script mirror candidate; read-only audit before any patch plan.",
        }

    if name_cf in {"index.html", "mvpqaic_index.html"}:
        return {
            "candidate_role": "possible_canonical_index",
            "canonical_score": 60,
            "allowed_to_edit": False,
            "reason": "Index-like file outside generated exports; needs human confirmation.",
        }

    return {
        "candidate_role": "unknown_index_like",
        "canonical_score": 10,
        "allowed_to_edit": False,
        "reason": "Index-like file needs review.",
    }


def find_index_candidates(repo_root: str | Path, *, max_files: int = 20000) -> list[dict[str, Any]]:
    root = Path(repo_root)
    seen: set[str] = set()
    candidates: list[dict[str, Any]] = []
    visited = 0

    for path in root.rglob("*"):
        if any(part in SKIP_DIR_NAMES for part in path.parts):
            continue
        if not path.is_file():
            continue

        visited += 1
        if visited > max_files:
            break

        if not _is_index_like(path):
            continue

        key = _dedupe_key(path)
        if key in seen:
            continue
        seen.add(key)

        relative_path = _safe_relative(path, root)
        classification = classify_index_candidate(relative_path)
        candidates.append(
            {
                "relative_path": relative_path,
                "size_bytes": path.stat().st_size,
                "file_name": path.name,
                **classification,
            }
        )

    return sorted(
        candidates,
        key=lambda item: (-int(item["canonical_score"]), item["relative_path"].casefold()),
    )


def build_patch_plan_requirements() -> list[dict[str, Any]]:
    return [
        {
            "requirement_id": "confirm_canonical_index",
            "priority": "P0",
            "action": "Human confirms which Index.html is the validated WebApp shell.",
        },
        {
            "requirement_id": "bind_json_data_packs",
            "priority": "P0",
            "action": "Plan binding of webapp_pack/context_pack/prompt_payload/admin_status to the canonical UI.",
        },
        {
            "requirement_id": "portfolio_modes_visibility",
            "priority": "P1",
            "action": "Show portfolio modes: none, pasted_text, structured, image_capture.",
        },
        {
            "requirement_id": "prompt_benchmark_visibility",
            "priority": "P1",
            "action": "Show quality, public safety, completeness, usefulness, missing_data and blockers.",
        },
        {
            "requirement_id": "admin_monitor_separation",
            "priority": "P1",
            "action": "Keep ADMIN_MONITOR.html internal and separate from public UI shell.",
        },
        {
            "requirement_id": "public_deploy_gate",
            "priority": "P0",
            "action": "Public deployment stays blocked until explicit approval.",
        },
    ]


def build_canonical_index_audit_pack(
    *,
    repo_root: str | Path,
    now_utc: str | None = None,
) -> dict[str, Any]:
    candidates = find_index_candidates(repo_root)
    possible_canonicals = [item for item in candidates if int(item["canonical_score"]) >= 60]

    blockers: list[str] = []
    reviews: list[str] = []

    if not possible_canonicals:
        reviews.append("NO_CONFIRMED_CANONICAL_INDEX_CANDIDATE_FOUND")
    if len(possible_canonicals) > 1:
        reviews.append("MULTIPLE_POSSIBLE_CANONICAL_INDEX_CANDIDATES")

    decision_status = (
        "BLOCKED" if blockers else "REVIEW_REQUIRED" if reviews else "CANONICAL_INDEX_AUDIT_READY"
    )

    return {
        "runtime": "MVP_QAIC_CANONICAL_INDEX_READONLY_AUDIT_PATCH_PLAN",
        "version": "P109_CANONICAL_INDEX_READONLY_AUDIT_PATCH_PLAN_0_1_0",
        "created_at_utc": _now_iso(now_utc),
        "decision_status": decision_status,
        "scope": {
            "mvp": "lexique_webapp_prompts_methods_benchmark_public",
            "qaic_private": "backend_quant_risk_revolutx_execution_locked",
        },
        "candidate_count": len(candidates),
        "possible_canonical_count": len(possible_canonicals),
        "candidates": candidates,
        "requirements": build_patch_plan_requirements(),
        "blockers": blockers,
        "reviews": reviews,
        "allowed_next_actions": [
            "HUMAN_CONFIRM_CANONICAL_INDEX",
            "PREPARE_UI_POLISH_PATCH_PLAN_ONLY",
            "PREPARE_DATA_BINDING_PATCH_AFTER_APPROVAL",
        ],
        "forbidden_next_actions": [
            "EDIT_INDEX_HTML_NOW",
            "OVERWRITE_INDEX_HTML",
            "GENERATE_PUBLIC_INDEX_HTML",
            "CLASP_PUSH",
            "APPS_SCRIPT_EXECUTION",
            "PUBLIC_DEPLOY_WITHOUT_APPROVAL",
            "BROKER_OR_TRADING_EXECUTION",
        ],
        "safety": dict(CANONICAL_INDEX_AUDIT_SAFETY),
        "next": "P110_CANONICAL_INDEX_BINDING_PATCH_PLAN_AFTER_HUMAN_CONFIRMATION",
    }


def render_patch_plan_markdown(audit: dict[str, Any]) -> str:
    candidates = (
        "\n".join(
            "- `{relative_path}` | role=`{candidate_role}` | score=`{canonical_score}` | edit=`{allowed_to_edit}`".format(
                **item
            )
            for item in audit["candidates"]
        )
        or "- No Index-like candidates found in bounded repo audit."
    )

    requirements = "\n".join(
        f"- **{item['priority']} — {item['requirement_id']}**: {item['action']}"
        for item in audit["requirements"]
    )

    allowed = "\n".join(f"- `{item}`" for item in audit["allowed_next_actions"])
    forbidden = "\n".join(f"- `{item}`" for item in audit["forbidden_next_actions"])

    return f"""# P109 — Canonical Index Readonly Audit + UI Polish Patch Plan

## Decision status

`{audit["decision_status"]}`

## Candidates

{candidates}

## Requirements

{requirements}

## Allowed next actions

{allowed}

## Forbidden next actions

{forbidden}

## Safety

- NO_INDEX_HTML_EDIT
- NO_INDEX_HTML_GENERATION
- NO_PUBLIC_DEPLOY
- NO_CLASP
- NO_APPS_SCRIPT_EXECUTION
- NO_SHEET_WRITE
- NO_BROKER_ORDER_SIZING
"""


def summarize_canonical_index_audit(audit: dict[str, Any]) -> dict[str, Any]:
    return {
        "decision_status": audit["decision_status"],
        "candidate_count": audit["candidate_count"],
        "possible_canonical_count": audit["possible_canonical_count"],
        "blocker_count": len(audit["blockers"]),
        "review_count": len(audit["reviews"]),
        "no_index_html_edit": audit["safety"]["no_index_html_edit"],
        "no_public_deploy": audit["safety"]["no_public_deploy"],
        "next": audit["next"],
    }


def write_json(path: str | Path, payload: dict[str, Any]) -> None:
    Path(path).write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
