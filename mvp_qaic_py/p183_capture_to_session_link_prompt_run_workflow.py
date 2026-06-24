from __future__ import annotations

import argparse
import csv
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from mvp_qaic_py.p182_prompt_history_library_version_studio import build_prompt_history_library


SAFETY_FLAGS: dict[str, bool] = {
    "gem_call_executed": False,
    "google_sheets_write": False,
    "live_google_api_call_from_python": False,
    "apps_script_execution": False,
    "clasp_push": False,
    "public_serve": False,
    "broker": False,
    "order": False,
    "sizing": False,
    "auto_apply_gem_response": False,
    "source_prompt_modified": False,
}


def _utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def _stamp() -> str:
    return datetime.now().strftime("%Y%m%d_%H%M%S")


def _sha12_bytes(path: Path) -> str:
    try:
        return hashlib.sha256(path.read_bytes()).hexdigest()[:12]
    except Exception:
        return "UNREADABLE"


def _ensure_dirs(root: Path) -> dict[str, Path]:
    dirs = {
        "capture_dir": root / "00_OPERATOR_EXPORTS" / "P181_CAPTURE_INBOX",
        "response_dir": root / "00_OPERATOR_EXPORTS" / "P181_GEM_RESPONSES",
        "session_dir": root / "00_OPERATOR_EXPORTS" / "P181_SESSION_LOG",
    }
    for folder in dirs.values():
        folder.mkdir(parents=True, exist_ok=True)
    return dirs


CAPTURE_EXTENSIONS = {".png", ".jpg", ".jpeg", ".webp", ".gif", ".bmp"}
RESPONSE_EXTENSIONS = {".json", ".md", ".txt"}


def _is_desktop_ini(path: Path) -> bool:
    return path.name.lower() == "desktop.ini"


def _latest_files(
    folder: Path,
    limit: int = 20,
    *,
    allowed_extensions: set[str] | None = None,
) -> list[Path]:
    files: list[Path] = []
    for path in folder.glob("*"):
        if not path.is_file():
            continue
        if _is_desktop_ini(path):
            continue
        if allowed_extensions is not None and path.suffix.lower() not in allowed_extensions:
            continue
        files.append(path)
    return sorted(files, key=lambda path: path.stat().st_mtime, reverse=True)[:limit]


def build_capture_prompt_session_workflow(
    project_root: str | Path,
    *,
    generated_at: str | None = None,
) -> dict[str, Any]:
    root = Path(project_root)
    dirs = _ensure_dirs(root)
    prompt_library = build_prompt_history_library(root)

    active_prompts = [
        row for row in prompt_library.get("entries", []) if row.get("status") == "ACTIVE_RUNTIME"
    ]
    captures = _latest_files(dirs["capture_dir"], allowed_extensions=CAPTURE_EXTENSIONS)
    responses = _latest_files(dirs["response_dir"], allowed_extensions=RESPONSE_EXTENSIONS)

    blockers: list[str] = []
    if not prompt_library.get("library_ready"):
        blockers.append("PROMPT_LIBRARY_NOT_READY")
    if not active_prompts:
        blockers.append("NO_ACTIVE_PROMPT_FOR_SESSION_WORKFLOW")

    workflow_ready = not blockers

    return {
        "STATUS": "OK_P183_CAPTURE_TO_SESSION_LINK_WORKFLOW_READY"
        if workflow_ready
        else "BLOCKED_P183_CAPTURE_TO_SESSION_LINK_WORKFLOW",
        "generated_at": generated_at or _utc_now(),
        "project_root": str(root),
        "capture_dir": str(dirs["capture_dir"]),
        "response_dir": str(dirs["response_dir"]),
        "session_dir": str(dirs["session_dir"]),
        "active_prompt_count": len(active_prompts),
        "capture_count": len(captures),
        "gem_response_count": len(responses),
        "workflow_ready": workflow_ready,
        "blocker_count": len(blockers),
        "blockers": blockers,
        "active_prompts": active_prompts[:5],
        "latest_captures": [
            {"file": path.name, "sha12": _sha12_bytes(path), "size_bytes": path.stat().st_size}
            for path in captures
        ],
        "latest_gem_responses": [
            {"file": path.name, "sha12": _sha12_bytes(path), "size_bytes": path.stat().st_size}
            for path in responses
        ],
        **SAFETY_FLAGS,
        "recommended_next": "P184_REAL_GEM_SESSION_REVIEW_AND_RESPONSE_PARSER",
    }


def create_review_only_session(
    project_root: str | Path,
    *,
    capture_file: str | None = None,
    response_file: str | None = None,
    prompt_id: str | None = None,
) -> dict[str, Any]:
    root = Path(project_root)
    dirs = _ensure_dirs(root)
    workflow = build_capture_prompt_session_workflow(root)

    captures = _latest_files(dirs["capture_dir"], allowed_extensions=CAPTURE_EXTENSIONS)
    responses = _latest_files(dirs["response_dir"], allowed_extensions=RESPONSE_EXTENSIONS)

    selected_capture = (
        dirs["capture_dir"] / capture_file if capture_file else (captures[0] if captures else None)
    )
    selected_response = (
        dirs["response_dir"] / response_file
        if response_file
        else (responses[0] if responses else None)
    )

    active_prompt = workflow["active_prompts"][0] if workflow["active_prompts"] else {}
    session_id = "GEMSESSION-" + _stamp()

    session = {
        "session_id": session_id,
        "created_at": _utc_now(),
        "status": "SESSION_READY_FOR_HUMAN_REVIEW",
        "workflow_status": workflow["STATUS"],
        "prompt_id": prompt_id or active_prompt.get("prompt_id", "ACTIVE_PROMPT_NOT_FOUND"),
        "prompt_sha12": active_prompt.get("sha12", "UNKNOWN"),
        "capture_file": selected_capture.name if selected_capture else "",
        "capture_sha12": _sha12_bytes(selected_capture) if selected_capture else "",
        "gem_response_file": selected_response.name if selected_response else "",
        "gem_response_sha12": _sha12_bytes(selected_response) if selected_response else "",
        "human_review_required": True,
        "apply_allowed": False,
        "auto_apply_gem_response": False,
        "notes": "Local review-only session link. Missing files are allowed for pre-session planning.",
        **SAFETY_FLAGS,
    }

    target = dirs["session_dir"] / f"{session_id}.json"
    target.write_text(json.dumps(session, indent=2, ensure_ascii=False), encoding="utf-8")
    session["session_path"] = str(target)
    return session


def export_capture_session_workflow(
    project_root: str | Path,
    *,
    export_dir: str | Path | None = None,
    create_session: bool = False,
) -> dict[str, Any]:
    root = Path(project_root)
    if export_dir is None:
        export_path = root / "05_EXPORTS" / f"P183_CAPTURE_TO_SESSION_LINK_WORKFLOW_{_stamp()}"
    else:
        export_path = Path(export_dir)

    export_path.mkdir(parents=True, exist_ok=True)
    workflow = build_capture_prompt_session_workflow(root)
    session = create_review_only_session(root) if create_session else None

    payload = {
        **workflow,
        "export_dir": str(export_path),
        "session_created": session is not None,
        "session": session,
    }

    (export_path / "P183_CAPTURE_SESSION_WORKFLOW.json").write_text(
        json.dumps(payload, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )

    summary_keys = [
        "STATUS",
        "generated_at",
        "project_root",
        "export_dir",
        "active_prompt_count",
        "capture_count",
        "gem_response_count",
        "workflow_ready",
        "session_created",
        "blocker_count",
        "blockers",
        "gem_call_executed",
        "google_sheets_write",
        "live_google_api_call_from_python",
        "apps_script_execution",
        "clasp_push",
        "public_serve",
        "broker",
        "order",
        "sizing",
        "auto_apply_gem_response",
        "source_prompt_modified",
        "recommended_next",
    ]
    (export_path / "P183_SUMMARY.json").write_text(
        json.dumps({key: payload.get(key) for key in summary_keys}, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )

    csv_path = export_path / "P183_SESSION_LINK_INDEX.csv"
    with csv_path.open("w", encoding="utf-8", newline="") as file_obj:
        fieldnames = ["type", "file", "sha12", "size_bytes"]
        writer = csv.DictWriter(file_obj, fieldnames=fieldnames)
        writer.writeheader()
        for row in workflow["latest_captures"]:
            writer.writerow({"type": "capture", **row})
        for row in workflow["latest_gem_responses"]:
            writer.writerow({"type": "gem_response", **row})

    report = [
        "# P183 Capture To Session Link And Prompt Run Workflow",
        "",
        f"- STATUS: {payload['STATUS']}",
        f"- workflow_ready: {payload['workflow_ready']}",
        f"- active_prompt_count: {payload['active_prompt_count']}",
        f"- capture_count: {payload['capture_count']}",
        f"- gem_response_count: {payload['gem_response_count']}",
        f"- session_created: {payload['session_created']}",
        f"- blocker_count: {payload['blocker_count']}",
        "",
        "Workflow:",
        "1. Upload capture portfolio locally.",
        "2. Use active prompt from Prompt Studio.",
        "3. Query GEM manually outside Python.",
        "4. Paste/save GEM response locally.",
        "5. Create review-only session link.",
        "6. Human review required before any next action.",
        "",
        "Safety:",
        "- GEM_CALL_EXECUTED=False",
        "- AUTO_APPLY_GEM_RESPONSE=False",
        "- SOURCE_PROMPT_MODIFIED=False",
        "- GOOGLE_SHEETS_WRITE=False",
        "- LIVE_GOOGLE_API_CALL_FROM_PYTHON=False",
        "- APPS_SCRIPT_EXECUTION=False",
        "- CLASP_PUSH=False",
        "- PUBLIC_SERVE=False",
        "- BROKER=False",
        "- ORDER=False",
        "- SIZING=False",
        "",
        "Next:",
        "- P184_REAL_GEM_SESSION_REVIEW_AND_RESPONSE_PARSER",
    ]
    (export_path / "P183_CAPTURE_SESSION_WORKFLOW_REPORT.md").write_text(
        "\n".join(report) + "\n",
        encoding="utf-8",
    )

    return payload


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="P183 capture to session link workflow.")
    parser.add_argument("--project-root", default=".")
    parser.add_argument("--export-dir", default=None)
    parser.add_argument("--write-export", action="store_true")
    parser.add_argument("--create-session", action="store_true")
    parser.add_argument("--json", action="store_true")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = _build_parser().parse_args(argv)
    if args.write_export:
        payload = export_capture_session_workflow(
            args.project_root,
            export_dir=args.export_dir,
            create_session=args.create_session,
        )
    else:
        payload = build_capture_prompt_session_workflow(args.project_root)

    if args.json:
        print(json.dumps(payload, indent=2, ensure_ascii=False))
    else:
        print(payload["STATUS"])
        print(f"WORKFLOW_READY={payload['workflow_ready']}")
        print(f"ACTIVE_PROMPT_COUNT={payload['active_prompt_count']}")
        print(f"BLOCKER_COUNT={payload['blocker_count']}")

    return 0 if payload["workflow_ready"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
