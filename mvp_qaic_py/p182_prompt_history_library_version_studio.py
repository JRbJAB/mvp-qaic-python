from __future__ import annotations

import argparse
import csv
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


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


def _sha12(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8", errors="replace")).hexdigest()[:12]


def _read_text(path: Path, limit: int = 250_000) -> str:
    try:
        return path.read_text(encoding="utf-8", errors="replace")[:limit]
    except Exception:
        return ""


def _is_prompt_candidate(path: Path, text: str) -> bool:
    lower = (path.name + "\n" + text[:20_000]).lower()
    signals = ["prompt", "gem", "portfolio", "image", "review", "human", "capture"]
    return "prompt" in lower and any(signal in lower for signal in signals)


def _classify_status(path: Path, text: str) -> str:
    lower = (str(path) + "\n" + text[:20_000]).lower()
    if "active_gem_portfolio_image_review" in lower:
        return "ACTIVE_RUNTIME"
    if "mvp qaic — gem portfolio image review" in lower:
        return "ACTIVE_RUNTIME"
    if "p158" in lower or "p159" in lower or "p177" in lower:
        return "REFERENCE_AUDIT"
    if "obsolete" in lower or "deprecated" in lower:
        return "ARCHIVE_OBSOLETE_REVIEW"
    return "HISTORICAL_REFERENCE_ONLY"


def _candidate_paths(root: Path) -> list[Path]:
    candidates: list[Path] = []

    direct = [
        root / "mvp_qaic_py" / "p173_nicegui_private_local_runner.py",
        root / "mvp_qaic_py" / "multimodal_gem_image_prompt_usd_contract.py",
        root / "mvp_qaic_py" / "p177_gem_portfolio_prompt_workflow_usable_smoke.py",
    ]
    candidates.extend(path for path in direct if path.exists())

    exports_root = root / "05_EXPORTS"
    if exports_root.exists():
        for pattern in ["*PROMPT*.md", "*PROMPT*.json", "*prompt*.md", "*prompt*.json"]:
            candidates.extend(exports_root.rglob(pattern))

    unique: dict[str, Path] = {}
    for path in candidates:
        if path.is_file() and path.stat().st_size <= 2_000_000:
            unique[str(path.resolve()).lower()] = path
    return list(unique.values())[:120]


def build_prompt_history_library(
    project_root: str | Path,
    *,
    generated_at: str | None = None,
) -> dict[str, Any]:
    root = Path(project_root)
    generated = generated_at or _utc_now()
    entries: list[dict[str, Any]] = []

    for path in _candidate_paths(root):
        text = _read_text(path)
        if not _is_prompt_candidate(path, text):
            continue

        status = _classify_status(path, text)
        rel = str(path.relative_to(root)) if path.is_relative_to(root) else str(path)
        prompt_id = (
            rel.replace("\\", "/")
            .replace("05_EXPORTS/", "")
            .replace("mvp_qaic_py/", "")
            .replace("/", "__")
        )

        entries.append(
            {
                "prompt_id": prompt_id[:140],
                "status": status,
                "source_path": rel,
                "sha12": _sha12(text),
                "char_count": len(text),
                "has_gem": "gem" in text.lower(),
                "has_portfolio": "portfolio" in text.lower(),
                "has_image": "image" in text.lower() or "capture" in text.lower(),
                "has_review_required": "review_required" in text.lower(),
                "notes": "Auto-classified local prompt candidate; review-only.",
            }
        )

    active_count = sum(1 for row in entries if row["status"] == "ACTIVE_RUNTIME")
    historical_count = sum(1 for row in entries if row["status"] == "HISTORICAL_REFERENCE_ONLY")
    reference_count = sum(1 for row in entries if row["status"] == "REFERENCE_AUDIT")

    blockers: list[str] = []
    if active_count < 1:
        blockers.append("NO_ACTIVE_RUNTIME_PROMPT_FOUND")
    if not entries:
        blockers.append("NO_PROMPT_LIBRARY_ENTRIES_FOUND")

    library_ready = not blockers

    return {
        "STATUS": "OK_P182_PROMPT_HISTORY_LIBRARY_VERSION_STUDIO_READY"
        if library_ready
        else "BLOCKED_P182_PROMPT_HISTORY_LIBRARY_VERSION_STUDIO",
        "generated_at": generated,
        "project_root": str(root),
        "prompt_version_count": len(entries),
        "active_prompt_count": active_count,
        "historical_prompt_count": historical_count,
        "reference_audit_prompt_count": reference_count,
        "library_ready": library_ready,
        "blocker_count": len(blockers),
        "blockers": blockers,
        "entries": entries,
        **SAFETY_FLAGS,
        "recommended_next": "P183_CAPTURE_TO_SESSION_LINK_AND_PROMPT_RUN_WORKFLOW",
    }


def export_prompt_history_library(
    project_root: str | Path,
    *,
    export_dir: str | Path | None = None,
) -> dict[str, Any]:
    root = Path(project_root)
    if export_dir is None:
        stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        export_path = root / "05_EXPORTS" / f"P182_PROMPT_HISTORY_LIBRARY_VERSION_STUDIO_{stamp}"
    else:
        export_path = Path(export_dir)

    export_path.mkdir(parents=True, exist_ok=True)
    payload = build_prompt_history_library(root)
    payload["export_dir"] = str(export_path)

    (export_path / "P182_PROMPT_HISTORY_LIBRARY.json").write_text(
        json.dumps(payload, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )

    summary_keys = [
        "STATUS",
        "generated_at",
        "project_root",
        "export_dir",
        "prompt_version_count",
        "active_prompt_count",
        "historical_prompt_count",
        "reference_audit_prompt_count",
        "library_ready",
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
    (export_path / "P182_SUMMARY.json").write_text(
        json.dumps({key: payload[key] for key in summary_keys}, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )

    csv_path = export_path / "P182_PROMPT_HISTORY_LIBRARY.csv"
    fieldnames = [
        "prompt_id",
        "status",
        "source_path",
        "sha12",
        "char_count",
        "has_gem",
        "has_portfolio",
        "has_image",
        "has_review_required",
        "notes",
    ]
    with csv_path.open("w", encoding="utf-8", newline="") as file_obj:
        writer = csv.DictWriter(file_obj, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(payload["entries"])

    report = [
        "# P182 Prompt History Library And Version Studio",
        "",
        f"- STATUS: {payload['STATUS']}",
        f"- prompt_version_count: {payload['prompt_version_count']}",
        f"- active_prompt_count: {payload['active_prompt_count']}",
        f"- historical_prompt_count: {payload['historical_prompt_count']}",
        f"- reference_audit_prompt_count: {payload['reference_audit_prompt_count']}",
        f"- library_ready: {payload['library_ready']}",
        f"- blocker_count: {payload['blocker_count']}",
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
        "- P183_CAPTURE_TO_SESSION_LINK_AND_PROMPT_RUN_WORKFLOW",
    ]
    (export_path / "P182_PROMPT_HISTORY_LIBRARY_REPORT.md").write_text(
        "\n".join(report) + "\n",
        encoding="utf-8",
    )

    return payload


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="P182 prompt history library.")
    parser.add_argument("--project-root", default=".")
    parser.add_argument("--export-dir", default=None)
    parser.add_argument("--write-export", action="store_true")
    parser.add_argument("--json", action="store_true")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = _build_parser().parse_args(argv)
    if args.write_export:
        payload = export_prompt_history_library(args.project_root, export_dir=args.export_dir)
    else:
        payload = build_prompt_history_library(args.project_root)

    if args.json:
        print(json.dumps(payload, indent=2, ensure_ascii=False))
    else:
        print(payload["STATUS"])
        print(f"LIBRARY_READY={payload['library_ready']}")
        print(f"PROMPT_VERSION_COUNT={payload['prompt_version_count']}")
        print(f"ACTIVE_PROMPT_COUNT={payload['active_prompt_count']}")
        print(f"BLOCKER_COUNT={payload['blocker_count']}")

    return 0 if payload["library_ready"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
