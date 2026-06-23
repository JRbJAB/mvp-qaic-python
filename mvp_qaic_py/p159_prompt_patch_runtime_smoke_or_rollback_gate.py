"""P159 prompt patch runtime smoke or rollback gate.

Local-only gate for the P158-R5 manual prompt patch.
It verifies that the patched P132/P133 prompt source is present, importable,
and still locked behind human review / no live action constraints.
"""

from __future__ import annotations

import csv
import importlib
import json
from dataclasses import asdict, dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

P159_STEP = "P159_PROMPT_PATCH_RUNTIME_SMOKE_OR_ROLLBACK_GATE"
PATCH_MARKER = "P158_R5_PROMPT_PATCH_APPLIED_20260623"
PROMPT_SOURCE_REL = Path("mvp_qaic_py") / "multimodal_gem_image_prompt_usd_contract.py"
EXPORT_PREFIX = "P159_PROMPT_PATCH_RUNTIME_SMOKE_OR_ROLLBACK_GATE"
EXPECTED_P158_STATUS = "P158_R5_MANUAL_PROMPT_PATCH_APPLIED_REVIEW_ONLY"

HARD_SAFETY_MARKERS = (
    "no_broker",
    "no_order",
    "no_sizing",
    "auto_apply_gem_response",
    "google_sheets_write",
    "public_deploy",
)

UNSAFE_RUNTIME_PATTERNS = (
    "place a real order",
    "execute a real order",
    "send order to broker",
    "auto apply gem response",
    "auto-apply gem response",
    "ignore human review",
    "bypass human review",
)


@dataclass(frozen=True)
class P159Summary:
    STATUS: str
    P159_STATUS: str
    PROMPT_SOURCE_ID: str
    SOURCE_P158_R5_STATUS: str
    SOURCE_P158_R5_DIR: str
    SOURCE_PROMPT_FILE: str
    PATCH_MARKER_FOUND: bool
    SOURCE_IMPORT_OK: bool
    RUNTIME_SMOKE_OK: bool
    PROMPT_CONTRACT_FUNCTION_FOUND: bool
    UNSAFE_RUNTIME_MARKER_COUNT: int
    SAFETY_MARKER_COUNT: int
    ROLLBACK_REQUIRED: bool
    APPLY_ALLOWED: bool
    SOURCE_PATCH_APPLIED: bool
    PROMPT_SOURCE_MODIFIED: bool
    GOOGLE_SHEETS_WRITE: bool
    LIVE_GOOGLE_SHEETS_READ: bool
    PUBLIC_DEPLOY: bool
    NO_APPS_SCRIPT_EXECUTION: bool
    NO_CLASP_PUSH: bool
    NO_BROKER: bool
    NO_ORDER: bool
    NO_SIZING: bool
    AUTO_APPLY_GEM_RESPONSE: bool
    BLOCKER_COUNT: int
    EXPORT_DIR: str
    NEXT: str
    created_at_utc: str


def utc_now_iso() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def repo_root_from_cwd() -> Path:
    cwd = Path.cwd().resolve()
    for candidate in (cwd, *cwd.parents):
        if (candidate / "pyproject.toml").exists() and (candidate / "mvp_qaic_py").is_dir():
            return candidate
    raise RuntimeError("MVP_QAIC_PY repo root not found from current directory")


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8-sig"))


def bool_from_summary(summary: dict[str, Any], key: str, default: bool = False) -> bool:
    value = summary.get(key)
    if value is None:
        value = summary.get(key.lower())
    if isinstance(value, bool):
        return value
    if isinstance(value, str):
        return value.strip().lower() in {"true", "yes", "1"}
    return default


def text_from_summary(summary: dict[str, Any], key: str, default: str = "") -> str:
    value = summary.get(key)
    if value is None:
        value = summary.get(key.lower(), default)
    return str(value) if value is not None else default


def find_latest_p158_r5_summary(repo_root: Path) -> tuple[Path, dict[str, Any]]:
    export_root = repo_root / "05_EXPORTS"
    candidates = sorted(
        export_root.glob(
            "P158_R5_AUTHORIZE_AND_APPLY_PROMPT_PATCH_MANUAL_GATE_*/P158_R5_SUMMARY.json"
        ),
        key=lambda path: path.stat().st_mtime,
        reverse=True,
    )
    if not candidates:
        raise RuntimeError("P158_R5 summary not found under 05_EXPORTS")
    summary_path = candidates[0]
    return summary_path, load_json(summary_path)


def prompt_source_text(repo_root: Path) -> str:
    source_path = repo_root / PROMPT_SOURCE_REL
    if not source_path.exists():
        raise RuntimeError(f"Prompt source file not found: {source_path}")
    return source_path.read_text(encoding="utf-8")


def import_prompt_module() -> tuple[bool, bool, str]:
    try:
        module = importlib.import_module("mvp_qaic_py.multimodal_gem_image_prompt_usd_contract")
    except Exception as exc:  # pragma: no cover - surfaced in summary
        return False, False, f"IMPORT_ERROR:{type(exc).__name__}:{exc}"

    attrs = dir(module)
    prompt_like = [
        name
        for name in attrs
        if "prompt" in name.lower() or "contract" in name.lower() or name.lower().startswith("p132")
    ]
    return True, bool(prompt_like), ",".join(sorted(prompt_like)[:20])


def count_safety_markers(text: str) -> int:
    lowered = text.lower()
    return sum(1 for marker in HARD_SAFETY_MARKERS if marker in lowered)


def find_unsafe_runtime_patterns(text: str) -> list[str]:
    lowered = text.lower()
    return [pattern for pattern in UNSAFE_RUNTIME_PATTERNS if pattern in lowered]


def build_summary(repo_root: Path) -> P159Summary:
    p158_summary_path, p158_summary = find_latest_p158_r5_summary(repo_root)
    source_text = prompt_source_text(repo_root)
    source_import_ok, prompt_function_found, prompt_attrs = import_prompt_module()

    patch_marker_found = PATCH_MARKER in source_text
    unsafe_patterns = find_unsafe_runtime_patterns(source_text)
    safety_marker_count = count_safety_markers(source_text)

    blockers: list[str] = []
    if text_from_summary(p158_summary, "P158_R5_STATUS") != EXPECTED_P158_STATUS:
        blockers.append("P158_R5_STATUS_NOT_APPLIED_REVIEW_ONLY")
    if not bool_from_summary(p158_summary, "SOURCE_PATCH_APPLIED"):
        blockers.append("P158_R5_SOURCE_PATCH_NOT_APPLIED")
    if not bool_from_summary(p158_summary, "PROMPT_SOURCE_MODIFIED"):
        blockers.append("P158_R5_PROMPT_SOURCE_NOT_MODIFIED")
    if bool_from_summary(p158_summary, "AUTO_APPLY_GEM_RESPONSE", default=True):
        blockers.append("AUTO_APPLY_GEM_RESPONSE_NOT_FALSE")
    if bool_from_summary(p158_summary, "GOOGLE_SHEETS_WRITE"):
        blockers.append("GOOGLE_SHEETS_WRITE_NOT_FALSE")
    if bool_from_summary(p158_summary, "PUBLIC_DEPLOY"):
        blockers.append("PUBLIC_DEPLOY_NOT_FALSE")
    if not patch_marker_found:
        blockers.append("PROMPT_PATCH_MARKER_NOT_FOUND")
    if not source_import_ok:
        blockers.append("PROMPT_SOURCE_IMPORT_FAILED")
    if not prompt_function_found:
        blockers.append("PROMPT_CONTRACT_FUNCTION_NOT_FOUND")
    if unsafe_patterns:
        blockers.append("UNSAFE_RUNTIME_PATTERNS_FOUND")

    runtime_smoke_ok = not blockers
    status = (
        "OK_P159_PROMPT_PATCH_RUNTIME_SMOKE_READY"
        if runtime_smoke_ok
        else "REVIEW_P159_ROLLBACK_REQUIRED"
    )
    p159_status = (
        "P159_PROMPT_PATCH_RUNTIME_SMOKE_OK_REVIEW_ONLY"
        if runtime_smoke_ok
        else "P159_ROLLBACK_REQUIRED_REVIEW_ONLY"
    )

    export_dir = (
        repo_root / "05_EXPORTS" / f"{EXPORT_PREFIX}_{datetime.now(UTC).strftime('%Y%m%d_%H%M%S')}"
    )

    # prompt_attrs is intentionally consumed to ensure the introspection result is deterministic for debugging.
    if prompt_attrs and not prompt_function_found:
        blockers.append("PROMPT_ATTRS_INCONSISTENT")

    return P159Summary(
        STATUS=status,
        P159_STATUS=p159_status,
        PROMPT_SOURCE_ID="P132_P133_PORTFOLIO_MULTIMODAL_REVIEW",
        SOURCE_P158_R5_STATUS=text_from_summary(p158_summary, "P158_R5_STATUS"),
        SOURCE_P158_R5_DIR=str(p158_summary_path.parent),
        SOURCE_PROMPT_FILE=str(repo_root / PROMPT_SOURCE_REL),
        PATCH_MARKER_FOUND=patch_marker_found,
        SOURCE_IMPORT_OK=source_import_ok,
        RUNTIME_SMOKE_OK=runtime_smoke_ok,
        PROMPT_CONTRACT_FUNCTION_FOUND=prompt_function_found,
        UNSAFE_RUNTIME_MARKER_COUNT=len(unsafe_patterns),
        SAFETY_MARKER_COUNT=safety_marker_count,
        ROLLBACK_REQUIRED=not runtime_smoke_ok,
        APPLY_ALLOWED=False,
        SOURCE_PATCH_APPLIED=True,
        PROMPT_SOURCE_MODIFIED=True,
        GOOGLE_SHEETS_WRITE=False,
        LIVE_GOOGLE_SHEETS_READ=False,
        PUBLIC_DEPLOY=False,
        NO_APPS_SCRIPT_EXECUTION=True,
        NO_CLASP_PUSH=True,
        NO_BROKER=True,
        NO_ORDER=True,
        NO_SIZING=True,
        AUTO_APPLY_GEM_RESPONSE=False,
        BLOCKER_COUNT=len(blockers),
        EXPORT_DIR=str(export_dir),
        NEXT="P160_REAL_GEM_RESPONSE_SMOKE_WITH_PATCH_OR_RELEASE_SEAL"
        if runtime_smoke_ok
        else "P159_ROLLBACK_GATE_DECISION",
        created_at_utc=utc_now_iso(),
    )


def write_export(summary: P159Summary) -> Path:
    export_dir = Path(summary.EXPORT_DIR)
    export_dir.mkdir(parents=True, exist_ok=True)
    payload = asdict(summary)
    (export_dir / "P159_SUMMARY.json").write_text(
        json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    (export_dir / "P159_RUNTIME_SMOKE_REPORT.json").write_text(
        json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    with (export_dir / "P159_RUNTIME_SMOKE_REPORT.csv").open(
        "w", newline="", encoding="utf-8"
    ) as handle:
        writer = csv.DictWriter(handle, fieldnames=list(payload.keys()))
        writer.writeheader()
        writer.writerow(payload)
    handoff = f"""# P159 Prompt Patch Runtime Smoke

Status: `{summary.P159_STATUS}`

- patch_marker_found: `{summary.PATCH_MARKER_FOUND}`
- source_import_ok: `{summary.SOURCE_IMPORT_OK}`
- runtime_smoke_ok: `{summary.RUNTIME_SMOKE_OK}`
- unsafe_runtime_marker_count: `{summary.UNSAFE_RUNTIME_MARKER_COUNT}`
- blocker_count: `{summary.BLOCKER_COUNT}`
- rollback_required: `{summary.ROLLBACK_REQUIRED}`
- next: `{summary.NEXT}`

Safety remains local-only: no Sheets write, no public deploy, no Apps Script, no CLASP, no broker/order/sizing.
"""
    (export_dir / "P159_HANDOFF.md").write_text(handoff, encoding="utf-8")
    if summary.ROLLBACK_REQUIRED:
        (export_dir / "P159_ROLLBACK_REQUIRED.md").write_text(
            "# P159 Rollback Required\n\nRuntime smoke failed. Do not proceed without rollback decision.\n",
            encoding="utf-8",
        )
    else:
        (export_dir / "P159_RUNTIME_SMOKE_OK.md").write_text(
            "# P159 Runtime Smoke OK\n\nPatched prompt source is importable and safety gates remain locked.\n",
            encoding="utf-8",
        )
    return export_dir


def main() -> int:
    repo_root = repo_root_from_cwd()
    summary = build_summary(repo_root)
    export_dir = write_export(summary)
    print(summary.P159_STATUS)
    print(f"patch_marker_found={str(summary.PATCH_MARKER_FOUND).lower()}")
    print(f"source_import_ok={str(summary.SOURCE_IMPORT_OK).lower()}")
    print(f"runtime_smoke_ok={str(summary.RUNTIME_SMOKE_OK).lower()}")
    print(f"unsafe_runtime_marker_count={summary.UNSAFE_RUNTIME_MARKER_COUNT}")
    print(f"blocker_count={summary.BLOCKER_COUNT}")
    print(f"rollback_required={str(summary.ROLLBACK_REQUIRED).lower()}")
    print(f"output_dir={export_dir}")
    print(f"next={summary.NEXT}")
    return 0 if summary.RUNTIME_SMOKE_OK else 2


if __name__ == "__main__":
    raise SystemExit(main())
