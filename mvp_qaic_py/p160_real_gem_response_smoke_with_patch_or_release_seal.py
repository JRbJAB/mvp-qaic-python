from __future__ import annotations

import csv
import importlib
import json
from dataclasses import asdict, dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

STEP_ID = "P160_REAL_GEM_RESPONSE_SMOKE_WITH_PATCH_OR_RELEASE_SEAL"
PROMPT_SOURCE_ID = "P132_P133_PORTFOLIO_MULTIMODAL_REVIEW"
PATCH_MARKER = "P158_R5_PROMPT_PATCH_APPLIED_20260623"
PROMPT_MODULE_NAME = "mvp_qaic_py.multimodal_gem_image_prompt_usd_contract"
PROMPT_SOURCE_REL = Path("mvp_qaic_py") / "multimodal_gem_image_prompt_usd_contract.py"

P152_PREFIX = "P152_REAL_GEM_RESPONSE_IMPORT_OR_STOP_"
P159_PREFIX = "P159_PROMPT_PATCH_RUNTIME_SMOKE_OR_ROLLBACK_GATE_"
P160_PREFIX = "P160_REAL_GEM_RESPONSE_SMOKE_WITH_PATCH_OR_RELEASE_SEAL_"

UNSAFE_RUNTIME_MARKERS = (
    "AUTO_APPLY_GEM_RESPONSE=true",
    "GOOGLE_SHEETS_WRITE=true",
    "LIVE_GOOGLE_SHEETS_READ=true",
    "PUBLIC_DEPLOY=true",
    "NO_APPS_SCRIPT_EXECUTION=false",
    "NO_CLASP_PUSH=false",
    "NO_BROKER=false",
    "NO_ORDER=false",
    "NO_SIZING=false",
    "REAL_ORDER_ALLOWED=true",
    "AUTO_ORDER_ALLOWED=true",
    "AUTO_SIZING_ALLOWED=true",
    "POST_ORDER_ALLOWED=true",
    "place_real_order(",
    "execute_real_order(",
    "broker.place_order(",
)


class P160BlockedError(RuntimeError):
    """Raised when the real GEM smoke/release seal cannot safely pass."""


@dataclass(frozen=True)
class P160Summary:
    STATUS: str
    P160_STATUS: str
    PROMPT_SOURCE_ID: str
    SOURCE_P152_DIR: str
    SOURCE_P159_DIR: str
    SOURCE_PROMPT_FILE_REL: str
    PATCH_MARKER: str
    P152_REAL_GEM_RESPONSE_OK: bool
    P159_RUNTIME_SMOKE_OK: bool
    PATCH_MARKER_FOUND: bool
    SOURCE_IMPORT_OK: bool
    REAL_GEM_SUMMARY_READ_OK: bool
    REAL_CASE_SMOKE_OK: bool
    RELEASE_SEAL_READY: bool
    UNSAFE_RUNTIME_MARKER_COUNT: int
    BLOCKER_COUNT: int
    ROLLBACK_REQUIRED: bool
    APPLY_ALLOWED: bool
    PROMPT_SOURCE_MODIFIED: bool
    AUTO_APPLY_GEM_RESPONSE: bool
    GOOGLE_SHEETS_WRITE: bool
    LIVE_GOOGLE_SHEETS_READ: bool
    PUBLIC_DEPLOY: bool
    NO_APPS_SCRIPT_EXECUTION: bool
    NO_CLASP_PUSH: bool
    NO_BROKER: bool
    NO_ORDER: bool
    NO_SIZING: bool
    EXPORT_DIR: str
    NEXT: str
    created_at_utc: str


def utc_now_iso() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8-sig"))


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def find_latest_export_dir(repo_root: Path, prefix: str) -> Path:
    exports_root = repo_root / "05_EXPORTS"
    if not exports_root.exists():
        raise P160BlockedError(f"EXPORTS_ROOT_NOT_FOUND:{exports_root}")
    candidates = [p for p in exports_root.iterdir() if p.is_dir() and p.name.startswith(prefix)]
    if not candidates:
        raise P160BlockedError(f"EXPORT_DIR_NOT_FOUND:{prefix}")
    return max(candidates, key=lambda p: p.stat().st_mtime)


def find_summary_json(export_dir: Path, prefix: str | None = None) -> Path:
    candidates = sorted(export_dir.glob("*SUMMARY*.json"))
    if prefix:
        exact = [p for p in candidates if p.name.startswith(prefix)]
        if exact:
            return exact[0]
    if candidates:
        return candidates[0]
    raise P160BlockedError(f"SUMMARY_JSON_NOT_FOUND:{export_dir}")


def ci_get(payload: dict[str, Any], key: str, default: Any = None) -> Any:
    if key in payload:
        return payload[key]
    key_lower = key.lower()
    for current_key, value in payload.items():
        if str(current_key).lower() == key_lower:
            return value
    for value in payload.values():
        if isinstance(value, dict):
            nested = ci_get(value, key, default=None)
            if nested is not None:
                return nested
    return default


def as_bool(value: Any) -> bool:
    if isinstance(value, bool):
        return value
    if isinstance(value, (int, float)):
        return bool(value)
    if isinstance(value, str):
        return value.strip().lower() in {"true", "yes", "1", "ok"}
    return False


def as_int(value: Any, default: int = 0) -> int:
    try:
        return int(value)
    except (TypeError, ValueError):
        return default


def validate_p152_summary(summary: dict[str, Any]) -> list[str]:
    blockers: list[str] = []
    status = str(ci_get(summary, "STATUS", ""))
    p152_status = str(ci_get(summary, "P152_STATUS", ""))
    validation_status = str(ci_get(summary, "VALIDATION_STATUS", ""))
    json_detected = as_bool(
        ci_get(summary, "JSON_PAYLOAD_DETECTED", ci_get(summary, "JSON_DETECTED", False))
    )
    blocker_count = as_int(ci_get(summary, "BLOCKER_COUNT", 0))
    human_review_required = as_bool(ci_get(summary, "HUMAN_REVIEW_REQUIRED", True))

    expected_runtime_status = "P152_REAL_GEM_RESPONSE_IMPORTED_LOCAL_REVIEW"
    status_blob = " ".join(
        str(value)
        for value in (
            status,
            p152_status,
            validation_status,
            ci_get(summary, "IMPORT_STATUS", ""),
            ci_get(summary, "REAL_GEM_RESPONSE_STATUS", ""),
            ci_get(summary, "P152_IMPORT_STATUS", ""),
        )
        if value is not None
    )
    sealed_global_status_ok = "OK_P152_REAL_GEM_RESPONSE_IMPORT_OR_STOP" in status_blob
    runtime_status_ok = expected_runtime_status in status_blob
    proof_status_ok = "P152_REAL_GEM_RESPONSE_IMPORTED" in status_blob

    validation_ok = validation_status in {
        "VALIDATED_FOR_HUMAN_REVIEW",
        "OK_VALIDATED_FOR_HUMAN_REVIEW",
    }
    real_gem_proof_ok = (
        validation_ok and json_detected and blocker_count == 0 and human_review_required
    )

    # R3 repair: the real P152 export may use a sealed/global STATUS and omit or vary
    # P152_STATUS. Do not block when the actual import evidence is complete.
    if not (runtime_status_ok or sealed_global_status_ok or proof_status_ok or real_gem_proof_ok):
        blockers.append("P152_STATUS_NOT_IMPORTED_LOCAL_REVIEW")
    if not validation_ok:
        blockers.append("P152_VALIDATION_NOT_HUMAN_REVIEW_VALIDATED")
    if not json_detected:
        blockers.append("P152_JSON_PAYLOAD_NOT_DETECTED")
    if blocker_count != 0:
        blockers.append("P152_BLOCKERS_PRESENT")
    if not human_review_required:
        blockers.append("P152_HUMAN_REVIEW_REQUIRED_NOT_TRUE")
    return blockers


def validate_p159_summary(summary: dict[str, Any]) -> list[str]:
    blockers: list[str] = []
    status = str(ci_get(summary, "STATUS", ""))
    p159_status = str(ci_get(summary, "P159_STATUS", ""))
    marker_found = as_bool(ci_get(summary, "PATCH_MARKER_FOUND", False))
    source_import_ok = as_bool(ci_get(summary, "SOURCE_IMPORT_OK", False))
    runtime_smoke_ok = as_bool(ci_get(summary, "RUNTIME_SMOKE_OK", False))
    unsafe_count = as_int(ci_get(summary, "UNSAFE_RUNTIME_MARKER_COUNT", 0))
    blocker_count = as_int(ci_get(summary, "BLOCKER_COUNT", 0))
    rollback_required = as_bool(ci_get(summary, "ROLLBACK_REQUIRED", True))

    if not status.startswith("OK_P159"):
        blockers.append("P159_GLOBAL_STATUS_NOT_OK")
    if p159_status != "P159_PROMPT_PATCH_RUNTIME_SMOKE_OK_REVIEW_ONLY":
        blockers.append("P159_STATUS_NOT_RUNTIME_SMOKE_OK")
    if not marker_found:
        blockers.append("P159_PATCH_MARKER_NOT_FOUND")
    if not source_import_ok:
        blockers.append("P159_SOURCE_IMPORT_NOT_OK")
    if not runtime_smoke_ok:
        blockers.append("P159_RUNTIME_SMOKE_NOT_OK")
    if unsafe_count != 0:
        blockers.append("P159_UNSAFE_RUNTIME_MARKERS_PRESENT")
    if blocker_count != 0:
        blockers.append("P159_BLOCKERS_PRESENT")
    if rollback_required:
        blockers.append("P159_ROLLBACK_REQUIRED")
    return blockers


def count_unsafe_markers(text: str) -> int:
    haystack = text.lower()
    return sum(1 for marker in UNSAFE_RUNTIME_MARKERS if marker.lower() in haystack)


def import_prompt_module() -> bool:
    importlib.invalidate_caches()
    importlib.import_module(PROMPT_MODULE_NAME)
    return True


def build_and_write_export(repo_root: Path) -> P160Summary:
    repo_root = repo_root.resolve()
    p152_dir = find_latest_export_dir(repo_root, P152_PREFIX)
    p159_dir = find_latest_export_dir(repo_root, P159_PREFIX)

    p152_summary = read_json(find_summary_json(p152_dir, "P152"))
    p159_summary = read_json(find_summary_json(p159_dir, "P159"))

    blockers: list[str] = []
    blockers.extend(validate_p152_summary(p152_summary))
    blockers.extend(validate_p159_summary(p159_summary))

    prompt_file = repo_root / PROMPT_SOURCE_REL
    if not prompt_file.exists():
        blockers.append("PROMPT_SOURCE_FILE_NOT_FOUND")
        prompt_text = ""
    else:
        prompt_text = prompt_file.read_text(encoding="utf-8")

    patch_marker_found = PATCH_MARKER in prompt_text
    if not patch_marker_found:
        blockers.append("PATCH_MARKER_NOT_FOUND_IN_PROMPT_SOURCE")

    unsafe_count = count_unsafe_markers(prompt_text)
    if unsafe_count:
        blockers.append("UNSAFE_RUNTIME_MARKERS_FOUND_IN_PROMPT_SOURCE")

    source_import_ok = False
    try:
        source_import_ok = import_prompt_module()
    except Exception as exc:  # pragma: no cover - defensive runtime report path
        blockers.append(f"PROMPT_SOURCE_IMPORT_FAILED:{type(exc).__name__}")

    real_gem_summary_read_ok = bool(p152_summary)
    real_case_smoke_ok = (
        real_gem_summary_read_ok
        and patch_marker_found
        and source_import_ok
        and unsafe_count == 0
        and not blockers
    )

    release_seal_ready = real_case_smoke_ok
    rollback_required = not real_case_smoke_ok
    status = (
        "OK_P160_REAL_GEM_RESPONSE_SMOKE_WITH_PATCH_RELEASE_SEAL_READY"
        if release_seal_ready
        else "BLOCKED_P160_REAL_GEM_RESPONSE_SMOKE_WITH_PATCH_REVIEW_REQUIRED"
    )
    p160_status = (
        "P160_REAL_GEM_RESPONSE_SMOKE_WITH_PATCH_OK_RELEASE_SEAL_READY"
        if release_seal_ready
        else "P160_REAL_GEM_RESPONSE_SMOKE_WITH_PATCH_BLOCKED_REVIEW_REQUIRED"
    )

    export_dir = (
        repo_root / "05_EXPORTS" / f"{P160_PREFIX}{datetime.now(UTC).strftime('%Y%m%d_%H%M%S')}"
    )
    export_dir.mkdir(parents=True, exist_ok=True)

    summary = P160Summary(
        STATUS=status,
        P160_STATUS=p160_status,
        PROMPT_SOURCE_ID=PROMPT_SOURCE_ID,
        SOURCE_P152_DIR=str(p152_dir),
        SOURCE_P159_DIR=str(p159_dir),
        SOURCE_PROMPT_FILE_REL=str(PROMPT_SOURCE_REL),
        PATCH_MARKER=PATCH_MARKER,
        P152_REAL_GEM_RESPONSE_OK=not validate_p152_summary(p152_summary),
        P159_RUNTIME_SMOKE_OK=not validate_p159_summary(p159_summary),
        PATCH_MARKER_FOUND=patch_marker_found,
        SOURCE_IMPORT_OK=source_import_ok,
        REAL_GEM_SUMMARY_READ_OK=real_gem_summary_read_ok,
        REAL_CASE_SMOKE_OK=real_case_smoke_ok,
        RELEASE_SEAL_READY=release_seal_ready,
        UNSAFE_RUNTIME_MARKER_COUNT=unsafe_count,
        BLOCKER_COUNT=len(blockers),
        ROLLBACK_REQUIRED=rollback_required,
        APPLY_ALLOWED=False,
        PROMPT_SOURCE_MODIFIED=False,
        AUTO_APPLY_GEM_RESPONSE=False,
        GOOGLE_SHEETS_WRITE=False,
        LIVE_GOOGLE_SHEETS_READ=False,
        PUBLIC_DEPLOY=False,
        NO_APPS_SCRIPT_EXECUTION=True,
        NO_CLASP_PUSH=True,
        NO_BROKER=True,
        NO_ORDER=True,
        NO_SIZING=True,
        EXPORT_DIR=str(export_dir),
        NEXT="P161_RELEASE_SEAL_OR_P160B_REAL_CASE_REVIEW_PACK",
        created_at_utc=utc_now_iso(),
    )

    summary_payload = asdict(summary)
    summary_payload["BLOCKERS"] = blockers
    summary_payload["P152_SUMMARY_FILE"] = str(find_summary_json(p152_dir, "P152"))
    summary_payload["P159_SUMMARY_FILE"] = str(find_summary_json(p159_dir, "P159"))

    write_json(export_dir / "P160_SUMMARY.json", summary_payload)
    write_json(export_dir / "P160_REAL_GEM_RESPONSE_SMOKE_WITH_PATCH_REPORT.json", summary_payload)

    with (export_dir / "P160_REAL_GEM_RESPONSE_SMOKE_WITH_PATCH_REPORT.csv").open(
        "w", newline="", encoding="utf-8"
    ) as handle:
        writer = csv.DictWriter(handle, fieldnames=list(summary_payload.keys()))
        writer.writeheader()
        writer.writerow(summary_payload)

    (export_dir / "P160_RELEASE_SEAL_DECISION.md").write_text(
        "\n".join(
            [
                "# P160 Real GEM Response Smoke With Patch — Release Seal Decision",
                "",
                f"- Status: `{summary.STATUS}`",
                f"- P160 status: `{summary.P160_STATUS}`",
                f"- Patch marker found: `{summary.PATCH_MARKER_FOUND}`",
                f"- Source import OK: `{summary.SOURCE_IMPORT_OK}`",
                f"- Real GEM summary read OK: `{summary.REAL_GEM_SUMMARY_READ_OK}`",
                f"- Real case smoke OK: `{summary.REAL_CASE_SMOKE_OK}`",
                f"- Release seal ready: `{summary.RELEASE_SEAL_READY}`",
                f"- Rollback required: `{summary.ROLLBACK_REQUIRED}`",
                f"- Blocker count: `{summary.BLOCKER_COUNT}`",
                "",
                "Safety gates:",
                "",
                f"- Auto-apply GEM response: `{summary.AUTO_APPLY_GEM_RESPONSE}`",
                f"- Google Sheets write: `{summary.GOOGLE_SHEETS_WRITE}`",
                f"- Public deploy: `{summary.PUBLIC_DEPLOY}`",
                f"- Broker/order/sizing disabled: `{summary.NO_BROKER}` / `{summary.NO_ORDER}` / `{summary.NO_SIZING}`",
                "",
                "No live action was performed.",
            ]
        )
        + "\n",
        encoding="utf-8",
    )

    (export_dir / "P160_HANDOFF.md").write_text(
        "\n".join(
            [
                "# P160 Handoff",
                "",
                f"Next: `{summary.NEXT}`",
                "",
                "Use this only after confirming the P160 summary is OK and rollback is false.",
            ]
        )
        + "\n",
        encoding="utf-8",
    )

    if blockers:
        raise P160BlockedError(";".join(blockers))

    return summary


def main(argv: list[str] | None = None) -> int:
    repo_root = Path.cwd()
    summary = build_and_write_export(repo_root)
    print(summary.P160_STATUS)
    print(f"prompt_source_id={summary.PROMPT_SOURCE_ID}")
    print(f"p152_real_gem_response_ok={str(summary.P152_REAL_GEM_RESPONSE_OK).lower()}")
    print(f"p159_runtime_smoke_ok={str(summary.P159_RUNTIME_SMOKE_OK).lower()}")
    print(f"patch_marker_found={str(summary.PATCH_MARKER_FOUND).lower()}")
    print(f"source_import_ok={str(summary.SOURCE_IMPORT_OK).lower()}")
    print(f"real_case_smoke_ok={str(summary.REAL_CASE_SMOKE_OK).lower()}")
    print(f"release_seal_ready={str(summary.RELEASE_SEAL_READY).lower()}")
    print(f"unsafe_runtime_marker_count={summary.UNSAFE_RUNTIME_MARKER_COUNT}")
    print(f"blocker_count={summary.BLOCKER_COUNT}")
    print(f"rollback_required={str(summary.ROLLBACK_REQUIRED).lower()}")
    print(f"output_dir={summary.EXPORT_DIR}")
    print(f"next={summary.NEXT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
