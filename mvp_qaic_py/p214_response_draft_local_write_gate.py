from __future__ import annotations

from pathlib import Path
from typing import Any

from mvp_qaic_py.p211_prompt_history_response_save_draft import (
    build_response_draft_payload,
)

DENIED_ROOT_NAMES = (".git", "__pycache__", ".pytest_cache", ".ruff_cache")


def _resolve(path: str | Path) -> Path:
    return Path(path).expanduser().resolve(strict=False)


def _is_inside(child: Path, parent: Path) -> bool:
    try:
        child.relative_to(parent)
    except ValueError:
        return False
    return True


def _relative_or_abs(path: Path, root: Path) -> str:
    try:
        return path.relative_to(root).as_posix()
    except ValueError:
        return path.as_posix()


def _has_denied_part(path: Path) -> bool:
    return any(part in DENIED_ROOT_NAMES for part in path.parts)


def build_response_draft_local_write_gate(
    project_root: str | Path,
    output_dir: str | Path,
    *,
    gem_response_text: str,
    card_id: str | None = None,
    query: str = "",
    generated_at: str | None = None,
) -> dict[str, Any]:
    root = _resolve(project_root)
    output = _resolve(output_dir)

    draft = build_response_draft_payload(
        root,
        card_id=card_id,
        query=query,
        gem_response_text=gem_response_text,
        generated_at=generated_at,
    )

    blockers = list(draft.get("blockers", []))

    output_inside_project = _is_inside(output, root)
    output_is_project_root = output == root
    output_denied_part = _has_denied_part(output)

    if not output_inside_project:
        blockers.append("OUTPUT_DIR_OUTSIDE_PROJECT_ROOT")
    if output_is_project_root:
        blockers.append("OUTPUT_DIR_IS_PROJECT_ROOT")
    if output_denied_part:
        blockers.append("OUTPUT_DIR_DENIED_SYSTEM_PATH")
    if draft.get("write_plan", {}).get("auto_apply_gem_response") is not False:
        blockers.append("AUTO_APPLY_GEM_RESPONSE_NOT_ALLOWED")
    if draft.get("write_plan", {}).get("requires_human_review") is not True:
        blockers.append("HUMAN_REVIEW_REQUIRED_FLAG_MISSING")

    write_allowed = len(blockers) == 0

    status = "OK_P214_RESPONSE_DRAFT_LOCAL_WRITE_GATE_READY"
    if not write_allowed:
        status = "REVIEW_P214_RESPONSE_DRAFT_LOCAL_WRITE_GATE"

    write_plan = draft.get("write_plan", {})
    json_filename = str(write_plan.get("json_filename") or "")
    md_filename = str(write_plan.get("md_filename") or "")

    return {
        "STATUS": status,
        "write_allowed": write_allowed,
        "blocker_count": len(blockers),
        "blockers": blockers,
        "generated_at": draft.get("generated_at"),
        "project_root": str(root),
        "output_dir": str(output),
        "output_dir_relative": _relative_or_abs(output, root),
        "output_inside_project": output_inside_project,
        "output_is_project_root": output_is_project_root,
        "output_denied_part": output_denied_part,
        "draft_id": draft.get("draft_id"),
        "source_prompt_path": draft.get("source_prompt_path"),
        "response_text_present": draft.get("response_text_present", False),
        "planned_files": {
            "json_path": str(output / json_filename) if json_filename else None,
            "md_path": str(output / md_filename) if md_filename else None,
            "json_filename": json_filename,
            "md_filename": md_filename,
        },
        "draft_payload": draft,
        "files_written": False,
        "local_only": True,
        "review_only": True,
        "server_started": False,
        "browser_started": False,
        "gem_call_executed": False,
        "provider_call_executed": False,
        "auto_apply_gem_response": False,
        "google_sheets_write": False,
        "apps_script_execution": False,
        "broker": False,
        "order": False,
        "sizing": False,
        "recommended_next": "P215_RESPONSE_DRAFT_LOCAL_EXPORT_RUNTIME_FAST_FUSE",
    }


def build_response_draft_local_write_gate_summary(
    gate_payload: dict[str, Any],
) -> dict[str, Any]:
    return {
        "STATUS": "OK_P214_RESPONSE_DRAFT_LOCAL_WRITE_GATE_SUMMARY_READY",
        "write_allowed": gate_payload.get("write_allowed", False),
        "blocker_count": gate_payload.get("blocker_count", 0),
        "output_dir_relative": gate_payload.get("output_dir_relative"),
        "source_prompt_path": gate_payload.get("source_prompt_path"),
        "response_text_present": gate_payload.get("response_text_present", False),
        "files_written": False,
        "review_only": True,
        "auto_apply_gem_response": False,
        "server_started": False,
        "browser_started": False,
        "broker": False,
        "order": False,
        "sizing": False,
    }


def main() -> None:
    import argparse
    import json

    parser = argparse.ArgumentParser()
    parser.add_argument("--project-root", default=".")
    parser.add_argument("--output-dir", required=True)
    parser.add_argument("--gem-response-text", required=True)
    parser.add_argument("--card-id", default=None)
    parser.add_argument("--query", default="")
    parser.add_argument("--generated-at", default=None)
    args = parser.parse_args()

    payload = build_response_draft_local_write_gate(
        args.project_root,
        args.output_dir,
        gem_response_text=args.gem_response_text,
        card_id=args.card_id,
        query=args.query,
        generated_at=args.generated_at,
    )
    print(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
