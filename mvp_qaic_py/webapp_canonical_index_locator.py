from __future__ import annotations

import csv
import json
from datetime import UTC, datetime
from pathlib import Path
from typing import Any


CANONICAL_INDEX_LOCATOR_SAFETY: dict[str, bool] = {
    "mvp_public_scope": True,
    "qaic_private_backend_separated": True,
    "bounded_local_readonly_locator": True,
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
    ".trash",
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


def normalize_locator_roots(roots: list[dict[str, str]] | None) -> list[dict[str, str]]:
    normalized: list[dict[str, str]] = []
    for index, root in enumerate(roots or [], start=1):
        path = str(root.get("path", "")).strip()
        if not path:
            continue
        normalized.append(
            {
                "root_id": root.get("root_id") or f"root_{index:02d}",
                "path": path,
                "role": root.get("role") or "candidate_root",
            }
        )
    return normalized


def score_locator_candidate(relative_path: str, root_role: str) -> dict[str, Any]:
    path_cf = relative_path.casefold()
    name_cf = Path(relative_path).name.casefold()
    root_role_cf = root_role.casefold()

    if "mvp_qaic_py/05_exports" in path_cf or path_cf.startswith("05_exports/"):
        return {
            "candidate_role": "python_generated_export_not_canonical",
            "canonical_score": 0,
            "reason": "Python generated export, not validated WebApp source.",
        }

    if "static_preview" in path_cf or "release_candidate_private_preview" in path_cf:
        return {
            "candidate_role": "local_preview_not_canonical",
            "canonical_score": 0,
            "reason": "Preview/admin artifact, not canonical WebApp source.",
        }

    if "03_dev" in path_cf and ("apps_script" in path_cf or "mirror" in path_cf):
        return {
            "candidate_role": "probable_canonical_apps_script_mirror",
            "canonical_score": 95,
            "reason": "Apps Script mirror in DEV area; strongest local candidate for validated WebApp shell.",
        }

    if "scripts" in path_cf and name_cf in {"index.html", "mvpqaic_index.html"}:
        return {
            "candidate_role": "probable_script_source_index",
            "canonical_score": 85,
            "reason": "Index-like file under scripts/source area.",
        }

    if "source" in path_cf and name_cf in {"index.html", "mvpqaic_index.html"}:
        return {
            "candidate_role": "probable_source_index",
            "canonical_score": 80,
            "reason": "Index-like file under source area.",
        }

    if "03_exports" in path_cf or "backup" in path_cf or "sauvegarde" in path_cf:
        return {
            "candidate_role": "historical_export_or_backup_evidence",
            "canonical_score": 40,
            "reason": "Historical export/backup evidence; useful for comparison, not canonical by itself.",
        }

    if "mvp qaic" in root_role_cf and name_cf in {"index.html", "mvpqaic_index.html"}:
        return {
            "candidate_role": "possible_mvp_root_index",
            "canonical_score": 70,
            "reason": "Index-like file in MVP root scan; needs human confirmation.",
        }

    return {
        "candidate_role": "index_like_review_required",
        "canonical_score": 50,
        "reason": "Index-like file discovered; needs review.",
    }


def locate_index_candidates(
    roots: list[dict[str, str]],
    *,
    max_files_per_root: int = 40000,
) -> list[dict[str, Any]]:
    normalized_roots = normalize_locator_roots(roots)
    seen: set[str] = set()
    candidates: list[dict[str, Any]] = []

    for root_info in normalized_roots:
        root_path = Path(root_info["path"])
        if not root_path.exists():
            continue

        visited = 0
        for path in root_path.rglob("*"):
            if any(part in SKIP_DIR_NAMES for part in path.parts):
                continue
            if not path.is_file():
                continue

            visited += 1
            if visited > max_files_per_root:
                break

            if not _is_index_like(path):
                continue

            key = _dedupe_key(path)
            if key in seen:
                continue
            seen.add(key)

            relative_path = _safe_relative(path, root_path)
            scoring = score_locator_candidate(relative_path, root_info["role"])
            candidates.append(
                {
                    "root_id": root_info["root_id"],
                    "root_role": root_info["role"],
                    "root_path": root_info["path"],
                    "relative_path": relative_path,
                    "full_path": str(path),
                    "file_name": path.name,
                    "size_bytes": path.stat().st_size,
                    "allowed_to_edit": False,
                    **scoring,
                }
            )

    return sorted(
        candidates,
        key=lambda item: (
            -int(item["canonical_score"]),
            item["root_id"],
            item["relative_path"].casefold(),
        ),
    )


def build_locator_audit(
    *,
    roots: list[dict[str, str]],
    now_utc: str | None = None,
) -> dict[str, Any]:
    candidates = locate_index_candidates(roots)
    probable = [item for item in candidates if int(item["canonical_score"]) >= 80]
    possible = [item for item in candidates if int(item["canonical_score"]) >= 70]

    blockers: list[str] = []
    reviews: list[str] = []

    if not possible:
        reviews.append("NO_POSSIBLE_CANONICAL_INDEX_FOUND_IN_BOUNDED_ROOTS")
    if len(possible) > 1:
        reviews.append("MULTIPLE_POSSIBLE_CANONICAL_INDEX_CANDIDATES")

    decision_status = (
        "BLOCKED"
        if blockers
        else "REVIEW_REQUIRED"
        if reviews
        else "CANONICAL_INDEX_CANDIDATE_FOUND_REVIEW_REQUIRED"
    )

    return {
        "runtime": "MVP_QAIC_CANONICAL_WEBAPP_INDEX_LOCATOR_READONLY",
        "version": "P110A_CANONICAL_WEBAPP_INDEX_LOCATOR_READONLY_0_1_0",
        "created_at_utc": _now_iso(now_utc),
        "decision_status": decision_status,
        "scope": {
            "mvp": "lexique_webapp_prompts_methods_benchmark_public",
            "qaic_private": "backend_quant_risk_revolutx_execution_locked",
        },
        "root_count": len(normalize_locator_roots(roots)),
        "candidate_count": len(candidates),
        "probable_canonical_count": len(probable),
        "possible_canonical_count": len(possible),
        "top_candidate": candidates[0] if candidates else None,
        "candidates": candidates,
        "blockers": blockers,
        "reviews": reviews,
        "allowed_next_actions": [
            "HUMAN_CONFIRM_TOP_INDEX_CANDIDATE",
            "PREPARE_BINDING_PATCH_PLAN_ONLY",
            "COMPARE_VALIDATED_UI_SHELL_TO_DATA_PACK_REQUIREMENTS",
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
        "safety": dict(CANONICAL_INDEX_LOCATOR_SAFETY),
        "next": "P110B_HUMAN_CONFIRM_CANONICAL_INDEX_OR_PATCH_PLAN",
    }


def render_locator_review_markdown(audit: dict[str, Any]) -> str:
    rows = []
    for item in audit["candidates"][:25]:
        rows.append(
            "- score=`{canonical_score}` role=`{candidate_role}` root=`{root_id}` path=`{relative_path}`".format(
                **item
            )
        )
    candidates_md = "\n".join(rows) or "- No candidates found."

    top = audit.get("top_candidate")
    top_md = (
        f"`{top['full_path']}` | score=`{top['canonical_score']}` | role=`{top['candidate_role']}`"
        if top
        else "`NONE`"
    )

    return f"""# P110A — Canonical WebApp Index Locator Readonly

## Decision status

`{audit["decision_status"]}`

## Top candidate

{top_md}

## Candidate counts

- total: `{audit["candidate_count"]}`
- probable canonical: `{audit["probable_canonical_count"]}`
- possible canonical: `{audit["possible_canonical_count"]}`

## Candidates

{candidates_md}

## Allowed next actions

{chr(10).join(f"- `{item}`" for item in audit["allowed_next_actions"])}

## Forbidden next actions

{chr(10).join(f"- `{item}`" for item in audit["forbidden_next_actions"])}

## Safety

- NO_INDEX_HTML_EDIT
- NO_INDEX_HTML_GENERATION
- NO_PUBLIC_DEPLOY
- NO_CLASP
- NO_APPS_SCRIPT_EXECUTION
- NO_SHEET_WRITE
- NO_BROKER_ORDER_SIZING
"""


def write_candidates_csv(path: str | Path, candidates: list[dict[str, Any]]) -> None:
    fieldnames = [
        "canonical_score",
        "candidate_role",
        "root_id",
        "root_role",
        "relative_path",
        "full_path",
        "size_bytes",
        "allowed_to_edit",
        "reason",
    ]
    with Path(path).open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for item in candidates:
            writer.writerow({key: item.get(key, "") for key in fieldnames})


def write_json(path: str | Path, payload: dict[str, Any]) -> None:
    Path(path).write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
