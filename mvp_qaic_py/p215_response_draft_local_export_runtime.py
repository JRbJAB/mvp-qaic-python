from __future__ import annotations

from pathlib import Path
from typing import Any

from mvp_qaic_py.p211_prompt_history_response_save_draft import (
    write_response_draft_files,
)
from mvp_qaic_py.p214_response_draft_local_write_gate import (
    build_response_draft_local_write_gate,
)


def run_response_draft_local_export(
    project_root: str | Path,
    output_dir: str | Path,
    *,
    gem_response_text: str,
    card_id: str | None = None,
    query: str = "",
    generated_at: str | None = None,
    execute_write: bool = False,
) -> dict[str, Any]:
    gate = build_response_draft_local_write_gate(
        project_root,
        output_dir,
        gem_response_text=gem_response_text,
        card_id=card_id,
        query=query,
        generated_at=generated_at,
    )

    if not gate["write_allowed"]:
        return {
            "STATUS": "REVIEW_P215_RESPONSE_DRAFT_LOCAL_EXPORT_RUNTIME",
            "export_allowed": False,
            "execute_write": execute_write,
            "files_written": False,
            "json_path": None,
            "md_path": None,
            "gate": gate,
            "blocker_count": gate["blocker_count"],
            "blockers": gate["blockers"],
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
            "recommended_next": "P216_PRIVATE_COCKPIT_RUNTIME_BUNDLE_FAST_FUSE",
        }

    if not execute_write:
        return {
            "STATUS": "OK_P215_RESPONSE_DRAFT_LOCAL_EXPORT_PLAN_READY",
            "export_allowed": True,
            "execute_write": False,
            "files_written": False,
            "json_path": gate["planned_files"]["json_path"],
            "md_path": gate["planned_files"]["md_path"],
            "gate": gate,
            "blocker_count": 0,
            "blockers": [],
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
            "recommended_next": "P216_PRIVATE_COCKPIT_RUNTIME_BUNDLE_FAST_FUSE",
        }

    written = write_response_draft_files(gate["draft_payload"], output_dir)

    return {
        "STATUS": "OK_P215_RESPONSE_DRAFT_LOCAL_EXPORT_RUNTIME_EXPORTED",
        "export_allowed": True,
        "execute_write": True,
        "files_written": True,
        "json_path": written["json_path"],
        "md_path": written["md_path"],
        "gate": gate,
        "draft_payload": written,
        "blocker_count": 0,
        "blockers": [],
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
        "recommended_next": "P216_PRIVATE_COCKPIT_RUNTIME_BUNDLE_FAST_FUSE",
    }


def build_response_draft_local_export_summary(payload: dict[str, Any]) -> dict[str, Any]:
    return {
        "STATUS": "OK_P215_RESPONSE_DRAFT_LOCAL_EXPORT_SUMMARY_READY",
        "export_allowed": payload.get("export_allowed", False),
        "execute_write": payload.get("execute_write", False),
        "files_written": payload.get("files_written", False),
        "json_path": payload.get("json_path"),
        "md_path": payload.get("md_path"),
        "blocker_count": payload.get("blocker_count", 0),
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
    parser.add_argument("--execute-write", action="store_true")
    args = parser.parse_args()

    payload = run_response_draft_local_export(
        args.project_root,
        args.output_dir,
        gem_response_text=args.gem_response_text,
        card_id=args.card_id,
        query=args.query,
        generated_at=args.generated_at,
        execute_write=args.execute_write,
    )
    print(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
