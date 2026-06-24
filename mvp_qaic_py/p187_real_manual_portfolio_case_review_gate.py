from __future__ import annotations

import argparse
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from mvp_qaic_py.p184_real_gem_session_review_response_parser import (
    parse_gem_response_text,
)


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


CAPTURE_EXTENSIONS = {".png", ".jpg", ".jpeg", ".webp", ".gif", ".bmp"}
RESPONSE_EXTENSIONS = {".json", ".md", ".txt"}


def _utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def _stamp() -> str:
    return datetime.now().strftime("%Y%m%d_%H%M%S")


def _sha12(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()[:12]


def _is_ignored_runtime_file(path: Path) -> bool:
    name = path.name.lower()
    if name == "desktop.ini":
        return True
    if name.startswith("p186_smoke_"):
        return True
    if name.startswith("."):
        return True
    return False


def _capture_dir(root: Path) -> Path:
    folder = root / "00_OPERATOR_EXPORTS" / "P181_CAPTURE_INBOX"
    folder.mkdir(parents=True, exist_ok=True)
    return folder


def _response_dir(root: Path) -> Path:
    folder = root / "00_OPERATOR_EXPORTS" / "P181_GEM_RESPONSES"
    folder.mkdir(parents=True, exist_ok=True)
    return folder


def _latest_real_files(folder: Path, extensions: set[str]) -> list[Path]:
    files: list[Path] = []
    for path in folder.glob("*"):
        if not path.is_file():
            continue
        if _is_ignored_runtime_file(path):
            continue
        if path.suffix.lower() not in extensions:
            continue
        files.append(path)
    return sorted(files, key=lambda item: item.stat().st_mtime, reverse=True)


def build_manual_portfolio_case_review_gate(project_root: str | Path) -> dict[str, Any]:
    root = Path(project_root)
    captures = _latest_real_files(_capture_dir(root), CAPTURE_EXTENSIONS)
    responses = _latest_real_files(_response_dir(root), RESPONSE_EXTENSIONS)

    selected_capture = captures[0] if captures else None
    selected_response = responses[0] if responses else None

    parsed_response: dict[str, Any] | None = None
    if selected_response is not None:
        parsed_response = parse_gem_response_text(
            selected_response.read_text(encoding="utf-8", errors="replace"),
            source_name=selected_response.name,
        )

    blockers: list[str] = []
    if selected_capture is None:
        blockers.append("WAITING_REAL_OPERATOR_CAPTURE")
    if selected_response is None:
        blockers.append("WAITING_REAL_GEM_RESPONSE_PASTE")
    if parsed_response is not None and parsed_response["blocker_count"] != 0:
        blockers.append("REAL_GEM_RESPONSE_SAFETY_BLOCKERS")

    real_case_ready = len(blockers) == 0
    status = (
        "OK_P187_REAL_MANUAL_PORTFOLIO_CASE_READY_FOR_HUMAN_REVIEW"
        if real_case_ready
        else "WAITING_P187_REAL_MANUAL_PORTFOLIO_CASE_INPUTS"
    )

    return {
        "STATUS": status,
        "generated_at": _utc_now(),
        "project_root": str(root),
        "real_case_ready": real_case_ready,
        "human_review_required": True,
        "apply_allowed": False,
        "capture_count": len(captures),
        "response_count": len(responses),
        "selected_capture": {
            "file": selected_capture.name,
            "sha12": _sha12(selected_capture),
            "size_bytes": selected_capture.stat().st_size,
        }
        if selected_capture
        else None,
        "selected_response": {
            "file": selected_response.name,
            "sha12": _sha12(selected_response),
            "size_bytes": selected_response.stat().st_size,
        }
        if selected_response
        else None,
        "parsed_response": parsed_response,
        "parsed_response_status": parsed_response["review_status"] if parsed_response else None,
        "parsed_response_blocker_count": parsed_response["blocker_count"]
        if parsed_response
        else None,
        "blocker_count": len(blockers),
        "blockers": blockers,
        "ignored_smoke_files": True,
        **SAFETY_FLAGS,
        "recommended_next": "P188_REAL_CASE_UI_OPERATOR_DECISION_SEAL_OR_WAIT",
    }


def export_manual_portfolio_case_review_gate(
    project_root: str | Path,
    *,
    export_dir: str | Path | None = None,
) -> dict[str, Any]:
    root = Path(project_root)
    export_path = (
        Path(export_dir)
        if export_dir is not None
        else root / "05_EXPORTS" / f"P187_REAL_MANUAL_PORTFOLIO_CASE_REVIEW_GATE_{_stamp()}"
    )
    export_path.mkdir(parents=True, exist_ok=True)

    payload = build_manual_portfolio_case_review_gate(root)
    payload["export_dir"] = str(export_path)

    (export_path / "P187_REAL_MANUAL_CASE_GATE.json").write_text(
        json.dumps(payload, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )

    summary_keys = [
        "STATUS",
        "generated_at",
        "project_root",
        "export_dir",
        "real_case_ready",
        "human_review_required",
        "apply_allowed",
        "capture_count",
        "response_count",
        "selected_capture",
        "selected_response",
        "parsed_response_status",
        "parsed_response_blocker_count",
        "blocker_count",
        "blockers",
        "ignored_smoke_files",
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
    summary = {key: payload.get(key) for key in summary_keys}
    (export_path / "P187_SUMMARY.json").write_text(
        json.dumps(summary, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )

    report = [
        "# P187 Real Manual Portfolio Case Review Gate",
        "",
        f"- STATUS: {payload['STATUS']}",
        f"- real_case_ready: {payload['real_case_ready']}",
        f"- capture_count: {payload['capture_count']}",
        f"- response_count: {payload['response_count']}",
        f"- blocker_count: {payload['blocker_count']}",
        "",
        "Gate:",
        "- Ignore P186 controlled smoke files.",
        "- Wait for real operator capture and pasted GEM response.",
        "- Parse response locally through P184 parser.",
        "- Human review remains mandatory.",
        "- No auto-apply.",
        "",
        "Safety:",
        "- GEM_CALL_EXECUTED=False",
        "- AUTO_APPLY_GEM_RESPONSE=False",
        "- GOOGLE_SHEETS_WRITE=False",
        "- PUBLIC_SERVE=False",
        "- BROKER=False",
        "- ORDER=False",
        "- SIZING=False",
        "",
        "Next:",
        "- P188_REAL_CASE_UI_OPERATOR_DECISION_SEAL_OR_WAIT",
    ]
    (export_path / "P187_REAL_MANUAL_CASE_GATE_REPORT.md").write_text(
        "\n".join(report) + "\n",
        encoding="utf-8",
    )

    return payload


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="P187 real manual case review gate.")
    parser.add_argument("--project-root", default=".")
    parser.add_argument("--export-dir", default=None)
    parser.add_argument("--write-export", action="store_true")
    parser.add_argument("--json", action="store_true")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = _build_parser().parse_args(argv)
    payload = (
        export_manual_portfolio_case_review_gate(args.project_root, export_dir=args.export_dir)
        if args.write_export
        else build_manual_portfolio_case_review_gate(args.project_root)
    )

    if args.json:
        print(json.dumps(payload, indent=2, ensure_ascii=False))
    else:
        print(payload["STATUS"])
        print(f"REAL_CASE_READY={payload['real_case_ready']}")
        print(f"CAPTURE_COUNT={payload['capture_count']}")
        print(f"RESPONSE_COUNT={payload['response_count']}")
        print(f"BLOCKER_COUNT={payload['blocker_count']}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
