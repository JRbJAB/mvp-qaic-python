"""P161 release seal or P160B review pack selector for MVP_QAIC_PY.

Local/private release seal only. No Google Sheets, no public deploy, no Apps Script,
no CLASP, no broker, no order, no sizing.
"""

from __future__ import annotations

import csv
import json
from dataclasses import asdict, dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

STEP = "P161_RELEASE_SEAL_OR_P160B_REAL_CASE_REVIEW_PACK"
PROMPT_SOURCE_ID = "P132_P133_PORTFOLIO_MULTIMODAL_REVIEW"
P160_READY_STATUS = "P160_REAL_GEM_RESPONSE_SMOKE_WITH_PATCH_OK_RELEASE_SEAL_READY"
P161_READY_STATUS = "P161_LOCAL_PRIVATE_RELEASE_SEAL_READY"
P161_GLOBAL_STATUS = "OK_P161_RELEASE_SEAL_LOCAL_PRIVATE_READY"

SAFETY_FLAGS = {
    "AUTO_APPLY_GEM_RESPONSE": False,
    "GOOGLE_SHEETS_WRITE": False,
    "LIVE_GOOGLE_SHEETS_READ": False,
    "PUBLIC_DEPLOY": False,
    "APPS_SCRIPT_EXECUTION": False,
    "CLASP_PUSH": False,
    "BROKER_ACTION": False,
    "ORDER_ACTION": False,
    "SIZING_ACTION": False,
}

REQUIRED_TRUE_FLAGS = (
    "P152_REAL_GEM_RESPONSE_OK",
    "P159_RUNTIME_SMOKE_OK",
    "PATCH_MARKER_FOUND",
    "SOURCE_IMPORT_OK",
    "REAL_CASE_SMOKE_OK",
    "RELEASE_SEAL_READY",
)

REQUIRED_ZERO_FLAGS = ("UNSAFE_RUNTIME_MARKER_COUNT", "BLOCKER_COUNT")


def utc_stamp() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def export_stamp() -> str:
    return datetime.now(UTC).strftime("%Y%m%d_%H%M%S")


def _norm_key(key: str) -> str:
    return "".join(ch for ch in str(key).lower() if ch.isalnum())


def get_any(data: dict[str, Any], *keys: str, default: Any = None) -> Any:
    if not data:
        return default
    normalized = {_norm_key(k): v for k, v in data.items()}
    for key in keys:
        n = _norm_key(key)
        if n in normalized:
            return normalized[n]
    return default


def as_bool(value: Any) -> bool:
    if isinstance(value, bool):
        return value
    if isinstance(value, (int, float)):
        return bool(value)
    text = str(value).strip().lower()
    return text in {"true", "1", "yes", "y", "ok", "pass", "passed"}


def as_int(value: Any, default: int = 0) -> int:
    if isinstance(value, bool):
        return int(value)
    if isinstance(value, int):
        return value
    if isinstance(value, float):
        return int(value)
    try:
        return int(str(value).strip())
    except Exception:
        return default


def repo_root_from(start: Path | None = None) -> Path:
    start = (start or Path.cwd()).resolve()
    for candidate in (start, *start.parents):
        if (candidate / "pyproject.toml").exists() and (candidate / "mvp_qaic_py").exists():
            return candidate
    raise FileNotFoundError("MVP_QAIC_PY repo root not found from current path")


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8-sig"))


def latest_export_dir(repo_root: Path, prefix: str) -> Path | None:
    exports = repo_root / "05_EXPORTS"
    if not exports.exists():
        return None
    candidates = [p for p in exports.iterdir() if p.is_dir() and p.name.startswith(prefix)]
    if not candidates:
        return None
    return sorted(candidates, key=lambda p: p.stat().st_mtime, reverse=True)[0]


def find_summary_file(export_dir: Path, exact_name: str | None = None) -> Path | None:
    if exact_name:
        candidate = export_dir / exact_name
        if candidate.exists():
            return candidate
    summaries = sorted(
        export_dir.glob("*SUMMARY*.json"), key=lambda p: p.stat().st_mtime, reverse=True
    )
    return summaries[0] if summaries else None


def find_latest_p160_summary(repo_root: Path) -> tuple[Path, dict[str, Any]]:
    export_dir = latest_export_dir(
        repo_root, "P160_REAL_GEM_RESPONSE_SMOKE_WITH_PATCH_OR_RELEASE_SEAL_"
    )
    if not export_dir:
        raise FileNotFoundError("P160 export directory not found")
    summary_path = find_summary_file(export_dir, "P160_SUMMARY.json")
    if not summary_path:
        raise FileNotFoundError(f"P160 summary not found in {export_dir}")
    return summary_path, load_json(summary_path)


@dataclass(frozen=True)
class P161Summary:
    STATUS: str
    P161_STATUS: str
    PROMPT_SOURCE_ID: str
    P160_STATUS: str
    P160_SUMMARY_FILE: str
    P160_EXPORT_DIR: str
    P160_RELEASE_SEAL_READY: bool
    P152_REAL_GEM_RESPONSE_OK: bool
    P159_RUNTIME_SMOKE_OK: bool
    PATCH_MARKER_FOUND: bool
    SOURCE_IMPORT_OK: bool
    REAL_CASE_SMOKE_OK: bool
    RELEASE_SEAL_READY: bool
    AUTO_APPLY_GEM_RESPONSE: bool
    GOOGLE_SHEETS_WRITE: bool
    LIVE_GOOGLE_SHEETS_READ: bool
    PUBLIC_DEPLOY: bool
    NO_APPS_SCRIPT_EXECUTION: bool
    NO_CLASP_PUSH: bool
    NO_BROKER: bool
    NO_ORDER: bool
    NO_SIZING: bool
    UNSAFE_RUNTIME_MARKER_COUNT: int
    BLOCKER_COUNT: int
    ROLLBACK_REQUIRED: bool
    RELEASE_DECISION: str
    P160B_REAL_CASE_REVIEW_PACK_REQUIRED: bool
    EXPORT_DIR: str
    NEXT: str
    created_at_utc: str


def validate_p160_release_ready(p160: dict[str, Any]) -> list[str]:
    blockers: list[str] = []
    p160_status = str(get_any(p160, "P160_STATUS", "p160_status", default=""))
    status = str(get_any(p160, "STATUS", "status", default=""))
    if p160_status != P160_READY_STATUS and not status.startswith("OK_P160"):
        blockers.append("P160_STATUS_NOT_RELEASE_READY")

    prompt_source_id = str(
        get_any(p160, "PROMPT_SOURCE_ID", "prompt_source_id", default=PROMPT_SOURCE_ID)
    )
    if prompt_source_id != PROMPT_SOURCE_ID:
        blockers.append("PROMPT_SOURCE_ID_MISMATCH")

    for key in REQUIRED_TRUE_FLAGS:
        if not as_bool(get_any(p160, key, key.lower(), default=False)):
            blockers.append(f"{key}_NOT_TRUE")

    for key in REQUIRED_ZERO_FLAGS:
        if as_int(get_any(p160, key, key.lower(), default=999), default=999) != 0:
            blockers.append(f"{key}_NOT_ZERO")

    if as_bool(get_any(p160, "ROLLBACK_REQUIRED", "rollback_required", default=True)):
        blockers.append("ROLLBACK_REQUIRED_TRUE")

    return blockers


def build_summary(repo_root: Path, export_dir: Path) -> P161Summary:
    p160_summary_file, p160 = find_latest_p160_summary(repo_root)
    blockers = validate_p160_release_ready(p160)
    p160_status = str(get_any(p160, "P160_STATUS", "p160_status", default=""))

    if blockers:
        return P161Summary(
            STATUS="BLOCKED_P161_RELEASE_SEAL_LOCAL_PRIVATE",
            P161_STATUS="P161_BLOCKED_P160B_REAL_CASE_REVIEW_PACK_REQUIRED",
            PROMPT_SOURCE_ID=PROMPT_SOURCE_ID,
            P160_STATUS=p160_status,
            P160_SUMMARY_FILE=str(p160_summary_file),
            P160_EXPORT_DIR=str(p160_summary_file.parent),
            P160_RELEASE_SEAL_READY=False,
            P152_REAL_GEM_RESPONSE_OK=as_bool(
                get_any(p160, "P152_REAL_GEM_RESPONSE_OK", default=False)
            ),
            P159_RUNTIME_SMOKE_OK=as_bool(get_any(p160, "P159_RUNTIME_SMOKE_OK", default=False)),
            PATCH_MARKER_FOUND=as_bool(get_any(p160, "PATCH_MARKER_FOUND", default=False)),
            SOURCE_IMPORT_OK=as_bool(get_any(p160, "SOURCE_IMPORT_OK", default=False)),
            REAL_CASE_SMOKE_OK=as_bool(get_any(p160, "REAL_CASE_SMOKE_OK", default=False)),
            RELEASE_SEAL_READY=as_bool(get_any(p160, "RELEASE_SEAL_READY", default=False)),
            AUTO_APPLY_GEM_RESPONSE=False,
            GOOGLE_SHEETS_WRITE=False,
            LIVE_GOOGLE_SHEETS_READ=False,
            PUBLIC_DEPLOY=False,
            NO_APPS_SCRIPT_EXECUTION=True,
            NO_CLASP_PUSH=True,
            NO_BROKER=True,
            NO_ORDER=True,
            NO_SIZING=True,
            UNSAFE_RUNTIME_MARKER_COUNT=as_int(
                get_any(p160, "UNSAFE_RUNTIME_MARKER_COUNT", default=999), 999
            ),
            BLOCKER_COUNT=len(blockers),
            ROLLBACK_REQUIRED=True,
            RELEASE_DECISION="BLOCKED_ROUTE_TO_P160B_REAL_CASE_REVIEW_PACK",
            P160B_REAL_CASE_REVIEW_PACK_REQUIRED=True,
            EXPORT_DIR=str(export_dir),
            NEXT="P160B_REAL_CASE_REVIEW_PACK_REQUIRED",
            created_at_utc=utc_stamp(),
        )

    return P161Summary(
        STATUS=P161_GLOBAL_STATUS,
        P161_STATUS=P161_READY_STATUS,
        PROMPT_SOURCE_ID=PROMPT_SOURCE_ID,
        P160_STATUS=p160_status or P160_READY_STATUS,
        P160_SUMMARY_FILE=str(p160_summary_file),
        P160_EXPORT_DIR=str(p160_summary_file.parent),
        P160_RELEASE_SEAL_READY=True,
        P152_REAL_GEM_RESPONSE_OK=True,
        P159_RUNTIME_SMOKE_OK=True,
        PATCH_MARKER_FOUND=True,
        SOURCE_IMPORT_OK=True,
        REAL_CASE_SMOKE_OK=True,
        RELEASE_SEAL_READY=True,
        AUTO_APPLY_GEM_RESPONSE=False,
        GOOGLE_SHEETS_WRITE=False,
        LIVE_GOOGLE_SHEETS_READ=False,
        PUBLIC_DEPLOY=False,
        NO_APPS_SCRIPT_EXECUTION=True,
        NO_CLASP_PUSH=True,
        NO_BROKER=True,
        NO_ORDER=True,
        NO_SIZING=True,
        UNSAFE_RUNTIME_MARKER_COUNT=0,
        BLOCKER_COUNT=0,
        ROLLBACK_REQUIRED=False,
        RELEASE_DECISION="LOCAL_PRIVATE_RELEASE_SEALED",
        P160B_REAL_CASE_REVIEW_PACK_REQUIRED=False,
        EXPORT_DIR=str(export_dir),
        NEXT="P162_LOCAL_PRIVATE_OPERATOR_HANDOFF_OR_DEV_STOP",
        created_at_utc=utc_stamp(),
    )


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def write_csv(path: Path, payload: dict[str, Any]) -> None:
    with path.open("w", encoding="utf-8", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=list(payload.keys()))
        writer.writeheader()
        writer.writerow(payload)


def write_md(path: Path, title: str, summary: P161Summary) -> None:
    payload = asdict(summary)
    lines = [f"# {title}", "", "## Résultat", ""]
    for key in (
        "STATUS",
        "P161_STATUS",
        "PROMPT_SOURCE_ID",
        "P160_STATUS",
        "P152_REAL_GEM_RESPONSE_OK",
        "P159_RUNTIME_SMOKE_OK",
        "PATCH_MARKER_FOUND",
        "SOURCE_IMPORT_OK",
        "REAL_CASE_SMOKE_OK",
        "RELEASE_SEAL_READY",
        "RELEASE_DECISION",
        "BLOCKER_COUNT",
        "ROLLBACK_REQUIRED",
        "NEXT",
    ):
        lines.append(f"- **{key}**: `{payload[key]}`")
    lines.extend(
        [
            "",
            "## Sécurité",
            "",
            "- No Google Sheets write/read live.",
            "- No Apps Script / CLASP.",
            "- No public deploy.",
            "- No broker/order/sizing.",
            "- No auto-apply GEM response.",
            "",
            "## Source validée",
            "",
            f"- P160 summary: `{summary.P160_SUMMARY_FILE}`",
        ]
    )
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def build_and_write_export(repo_root: Path | None = None) -> P161Summary:
    repo_root = repo_root_from(repo_root or Path.cwd())
    export_dir = (
        repo_root
        / "05_EXPORTS"
        / f"P161_RELEASE_SEAL_OR_P160B_REAL_CASE_REVIEW_PACK_{export_stamp()}"
    )
    export_dir.mkdir(parents=True, exist_ok=True)
    summary = build_summary(repo_root, export_dir)
    payload = asdict(summary)

    write_json(export_dir / "P161_SUMMARY.json", payload)
    write_json(export_dir / "P161_RELEASE_SEAL_REPORT.json", payload)
    write_csv(export_dir / "P161_RELEASE_SEAL_REPORT.csv", payload)
    write_md(export_dir / "P161_RELEASE_SEAL_DECISION.md", "P161 Release Seal Decision", summary)
    write_md(export_dir / "P161_HANDOFF.md", "P161 Local Private Release Handoff", summary)

    if summary.BLOCKER_COUNT:
        raise RuntimeError(";".join(["P161_RELEASE_SEAL_BLOCKED", summary.RELEASE_DECISION]))
    return summary


def main() -> int:
    repo_root = repo_root_from(Path.cwd())
    summary = build_and_write_export(repo_root)
    payload = asdict(summary)
    print(summary.P161_STATUS)
    for key in (
        "PROMPT_SOURCE_ID",
        "P160_STATUS",
        "P160_RELEASE_SEAL_READY",
        "P152_REAL_GEM_RESPONSE_OK",
        "P159_RUNTIME_SMOKE_OK",
        "PATCH_MARKER_FOUND",
        "SOURCE_IMPORT_OK",
        "REAL_CASE_SMOKE_OK",
        "RELEASE_SEAL_READY",
        "RELEASE_DECISION",
        "BLOCKER_COUNT",
        "ROLLBACK_REQUIRED",
        "EXPORT_DIR",
        "NEXT",
    ):
        print(f"{key.lower()}={payload[key]}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
