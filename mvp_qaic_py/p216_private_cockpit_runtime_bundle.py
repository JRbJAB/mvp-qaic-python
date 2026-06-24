from __future__ import annotations

from pathlib import Path
from typing import Any

from mvp_qaic_py.p209_prompt_history_private_cockpit_wiring import (
    build_private_cockpit_prompt_history_sections,
)
from mvp_qaic_py.p213_response_draft_private_cockpit_wiring import (
    build_response_draft_private_cockpit_panel,
)
from mvp_qaic_py.p215_response_draft_local_export_runtime import (
    run_response_draft_local_export,
)


def _status_rank(status: str) -> int:
    if status.startswith("BLOCKED_"):
        return 3
    if status.startswith("REVIEW_"):
        return 2
    if status.startswith("OK_"):
        return 1
    return 2


def _rollup_status(statuses: list[str]) -> str:
    if any(status.startswith("BLOCKED_") for status in statuses):
        return "BLOCKED_P216_PRIVATE_COCKPIT_RUNTIME_BUNDLE"
    if any(status.startswith("REVIEW_") for status in statuses):
        return "REVIEW_P216_PRIVATE_COCKPIT_RUNTIME_BUNDLE"
    return "OK_P216_PRIVATE_COCKPIT_RUNTIME_BUNDLE_READY"


def build_private_cockpit_runtime_bundle(
    project_root: str | Path,
    output_dir: str | Path,
    *,
    gem_response_text: str,
    card_id: str | None = None,
    query: str = "",
    generated_at: str | None = None,
    execute_export: bool = False,
) -> dict[str, Any]:
    prompt_history = build_private_cockpit_prompt_history_sections(
        project_root,
        generated_at=generated_at,
    )
    response_draft_panel = build_response_draft_private_cockpit_panel(
        project_root,
        gem_response_text=gem_response_text,
        card_id=card_id,
        query=query,
        generated_at=generated_at,
    )
    export_runtime = run_response_draft_local_export(
        project_root,
        output_dir,
        gem_response_text=gem_response_text,
        card_id=card_id,
        query=query,
        generated_at=generated_at,
        execute_write=execute_export,
    )

    component_statuses = [
        prompt_history["STATUS"],
        response_draft_panel["STATUS"],
        export_runtime["STATUS"],
    ]
    status = _rollup_status(component_statuses)

    blocker_lists = [
        response_draft_panel.get("blockers", []),
        export_runtime.get("blockers", []),
    ]
    blockers = sorted({str(item) for sublist in blocker_lists for item in sublist})

    return {
        "STATUS": status,
        "generated_at": generated_at,
        "project_root": str(Path(project_root)),
        "output_dir": str(Path(output_dir)),
        "component_statuses": {
            "prompt_history": prompt_history["STATUS"],
            "response_draft_panel": response_draft_panel["STATUS"],
            "export_runtime": export_runtime["STATUS"],
        },
        "component_rank": max(_status_rank(item) for item in component_statuses),
        "blocker_count": len(blockers),
        "blockers": blockers,
        "cockpit": {
            "title": "MVP QAIC Private Prompt Cockpit",
            "subtitle": "Historique prompts, réponse GEM, brouillon local review-only",
            "runtime_mode": "LOCAL_PRIVATE_REVIEW_ONLY",
            "route_hints": [
                "/prompt-history",
                "/response-draft",
                "/local-export",
            ],
            "primary_actions": [
                "select_prompt",
                "preview_response_draft",
                "save_response_draft_local",
                "review_only_mark",
            ],
        },
        "prompt_history": prompt_history,
        "response_draft_panel": response_draft_panel,
        "export_runtime": export_runtime,
        "decision_header": {
            "prompt_history_status": prompt_history["STATUS"],
            "response_draft_status": response_draft_panel["STATUS"],
            "export_status": export_runtime["STATUS"],
            "export_allowed": export_runtime.get("export_allowed", False),
            "execute_export": execute_export,
            "files_written": export_runtime.get("files_written", False),
            "next_action": "P217_NICEGUI_PRIVATE_COCKPIT_UI_WIRING_FAST_FUSE",
        },
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
        "recommended_next": "P217_NICEGUI_PRIVATE_COCKPIT_UI_WIRING_FAST_FUSE",
    }


def build_private_cockpit_runtime_summary(bundle: dict[str, Any]) -> dict[str, Any]:
    decision = bundle.get("decision_header", {})
    return {
        "STATUS": "OK_P216_PRIVATE_COCKPIT_RUNTIME_SUMMARY_READY",
        "bundle_status": bundle.get("STATUS"),
        "blocker_count": bundle.get("blocker_count", 0),
        "prompt_history_status": decision.get("prompt_history_status"),
        "response_draft_status": decision.get("response_draft_status"),
        "export_status": decision.get("export_status"),
        "export_allowed": decision.get("export_allowed", False),
        "execute_export": decision.get("execute_export", False),
        "files_written": decision.get("files_written", False),
        "review_only": True,
        "server_started": False,
        "browser_started": False,
        "gem_call_executed": False,
        "provider_call_executed": False,
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
    parser.add_argument("--execute-export", action="store_true")
    args = parser.parse_args()

    payload = build_private_cockpit_runtime_bundle(
        args.project_root,
        args.output_dir,
        gem_response_text=args.gem_response_text,
        card_id=args.card_id,
        query=args.query,
        generated_at=args.generated_at,
        execute_export=args.execute_export,
    )
    print(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
