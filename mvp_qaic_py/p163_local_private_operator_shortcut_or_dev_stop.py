"""P163 local private operator shortcut / final dev-stop handoff.

This module is local-only and intentionally conservative:
- no Google Sheets write/read
- no public deploy
- no Apps Script / CLASP
- no broker/order/sizing

It validates P162's sealed local private handoff and creates a small operator
shortcut pack that points to the sealed prompt workflow without triggering live
actions.
"""

from __future__ import annotations

import csv
import json
from dataclasses import asdict, dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

PROMPT_SOURCE_ID = "P132_P133_PORTFOLIO_MULTIMODAL_REVIEW"
MODULE_VERSION = "P163_R2_LOCAL_PRIVATE_OPERATOR_SHORTCUT_DEV_STOP_20260623"
EXPORT_PREFIX = "P163_LOCAL_PRIVATE_OPERATOR_SHORTCUT_OR_DEV_STOP"
P163_STATUS_READY = "P163_LOCAL_PRIVATE_OPERATOR_SHORTCUT_READY_DEV_STOP_NEXT"
STATUS_READY_TO_SEAL = "OK_P163_LOCAL_PRIVATE_OPERATOR_SHORTCUT_OR_DEV_STOP_READY_TO_SEAL"
NEXT_STEP = "MVP_QAIC_LOCAL_PRIVATE_RELEASE_CLOSED_DEV_STOP"

TRUE_VALUES = {"true", "1", "yes", "y", "ok", "ready", "pass"}
FALSE_VALUES = {"false", "0", "no", "n", "ko", "blocked", "fail", ""}


class P163BlockedError(RuntimeError):
    """Raised when P163 cannot be sealed safely."""


def utc_now_iso() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def as_bool(value: Any) -> bool:
    if isinstance(value, bool):
        return value
    if isinstance(value, (int, float)):
        return value != 0
    text = str(value).strip().lower()
    if text in TRUE_VALUES:
        return True
    if text in FALSE_VALUES:
        return False
    return False


def as_int(value: Any, default: int = 0) -> int:
    try:
        return int(value)
    except (TypeError, ValueError):
        return default


def get_any(payload: dict[str, Any], *keys: str, default: Any = None) -> Any:
    for key in keys:
        if key in payload:
            return payload[key]
        lower_key = key.lower()
        if lower_key in payload:
            return payload[lower_key]
    lowered = {str(k).lower(): v for k, v in payload.items()}
    for key in keys:
        if key.lower() in lowered:
            return lowered[key.lower()]
    return default


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8-sig"))


def latest_export_dir(repo_root: Path, prefix: str) -> Path | None:
    exports_root = repo_root / "05_EXPORTS"
    if not exports_root.exists():
        return None
    candidates = [p for p in exports_root.iterdir() if p.is_dir() and p.name.startswith(prefix)]
    if not candidates:
        return None
    return max(candidates, key=lambda p: p.stat().st_mtime)


def find_p162_summary(repo_root: Path) -> tuple[Path, dict[str, Any]]:
    export_dir = latest_export_dir(repo_root, "P162_LOCAL_PRIVATE_OPERATOR_HANDOFF_OR_DEV_STOP")
    if export_dir is None:
        raise P163BlockedError("P162_EXPORT_DIR_NOT_FOUND")
    summary_file = export_dir / "P162_SUMMARY.json"
    if not summary_file.exists():
        raise P163BlockedError("P162_SUMMARY_NOT_FOUND")
    return summary_file, read_json(summary_file)


def validate_p162(summary: dict[str, Any]) -> list[str]:
    blockers: list[str] = []
    p162_status = str(get_any(summary, "P162_STATUS", default=""))
    prompt_source_id = str(get_any(summary, "PROMPT_SOURCE_ID", default=PROMPT_SOURCE_ID))
    next_step = str(get_any(summary, "NEXT", default=""))

    if p162_status != "P162_LOCAL_PRIVATE_OPERATOR_HANDOFF_READY_DEV_STOP_RECOMMENDED":
        blockers.append("P162_STATUS_NOT_HANDOFF_READY_DEV_STOP")
    if prompt_source_id != PROMPT_SOURCE_ID:
        blockers.append("PROMPT_SOURCE_ID_MISMATCH")
    if not as_bool(get_any(summary, "LOCAL_PRIVATE_RELEASE_SEALED", default=False)):
        blockers.append("LOCAL_PRIVATE_RELEASE_NOT_SEALED")
    if not as_bool(get_any(summary, "OPERATOR_HANDOFF_READY", default=False)):
        blockers.append("OPERATOR_HANDOFF_NOT_READY")
    if not as_bool(get_any(summary, "DEV_STOP_RECOMMENDED", default=False)):
        blockers.append("DEV_STOP_NOT_RECOMMENDED")
    if as_bool(get_any(summary, "P160B_REAL_CASE_REVIEW_PACK_REQUIRED", default=True)):
        blockers.append("P160B_REVIEW_PACK_REQUIRED")
    if as_bool(get_any(summary, "PUBLIC_DEPLOY_READY", default=True)):
        blockers.append("PUBLIC_DEPLOY_READY_UNEXPECTED")
    if as_int(get_any(summary, "BLOCKER_COUNT", default=1), default=1) != 0:
        blockers.append("P162_BLOCKER_COUNT_NON_ZERO")
    if as_bool(get_any(summary, "ROLLBACK_REQUIRED", default=True)):
        blockers.append("ROLLBACK_REQUIRED")
    if "MVP_QAIC_LOCAL_PRIVATE_RELEASE_CLOSED_DEV_STOP" not in next_step:
        blockers.append("P162_NEXT_NOT_CLOSE_OR_SHORTCUT")
    return blockers


@dataclass(frozen=True)
class P163Summary:
    STATUS: str
    P163_STATUS: str
    PROMPT_SOURCE_ID: str
    SOURCE_P162_STATUS: str
    SOURCE_P162_DIR: str
    LOCAL_PRIVATE_RELEASE_SEALED: bool
    OPERATOR_SHORTCUT_READY: bool
    OPERATOR_HANDOFF_READY: bool
    DEV_STOP_RECOMMENDED: bool
    FINAL_CLOSE_READY: bool
    PUBLIC_DEPLOY_READY: bool
    GOOGLE_SHEETS_WRITE: bool
    LIVE_GOOGLE_SHEETS_READ: bool
    PUBLIC_DEPLOY: bool
    NO_APPS_SCRIPT_EXECUTION: bool
    NO_CLASP_PUSH: bool
    NO_BROKER: bool
    NO_ORDER: bool
    NO_SIZING: bool
    BLOCKER_COUNT: int
    ROLLBACK_REQUIRED: bool
    SHORTCUT_FILE: str
    EXPORT_DIR: str
    NEXT: str
    created_at_utc: str


def build_summary(repo_root: Path) -> P163Summary:
    p162_summary_file, p162 = find_p162_summary(repo_root)
    blockers = validate_p162(p162)
    if blockers:
        raise P163BlockedError(";".join(blockers))

    return P163Summary(
        STATUS=STATUS_READY_TO_SEAL,
        P163_STATUS=P163_STATUS_READY,
        PROMPT_SOURCE_ID=PROMPT_SOURCE_ID,
        SOURCE_P162_STATUS=str(get_any(p162, "P162_STATUS", default="")),
        SOURCE_P162_DIR=str(p162_summary_file.parent),
        LOCAL_PRIVATE_RELEASE_SEALED=True,
        OPERATOR_SHORTCUT_READY=True,
        OPERATOR_HANDOFF_READY=True,
        DEV_STOP_RECOMMENDED=True,
        FINAL_CLOSE_READY=True,
        PUBLIC_DEPLOY_READY=False,
        GOOGLE_SHEETS_WRITE=False,
        LIVE_GOOGLE_SHEETS_READ=False,
        PUBLIC_DEPLOY=False,
        NO_APPS_SCRIPT_EXECUTION=True,
        NO_CLASP_PUSH=True,
        NO_BROKER=True,
        NO_ORDER=True,
        NO_SIZING=True,
        BLOCKER_COUNT=0,
        ROLLBACK_REQUIRED=False,
        SHORTCUT_FILE="",
        EXPORT_DIR="",
        NEXT=NEXT_STEP,
        created_at_utc=utc_now_iso(),
    )


def write_csv(path: Path, summary: P163Summary) -> None:
    payload = asdict(summary)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(payload.keys()))
        writer.writeheader()
        writer.writerow(payload)


def shortcut_script(repo_root_placeholder: str = "<SET_REPO_PATH>") -> str:
    return f'''$ErrorActionPreference = "Stop"
chcp 65001 | Out-Null
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
$OutputEncoding = [System.Text.Encoding]::UTF8

# P163 local private operator shortcut.
# Safe by construction: no Sheet write/read, no public deploy, no Apps Script/CLASP,
# no broker, no order, no sizing.

$repo = $env:MVP_QAIC_PY_REPO
if (-not $repo) {{ $repo = "{repo_root_placeholder}" }}
if (-not (Test-Path -LiteralPath (Join-Path $repo "pyproject.toml"))) {{
  throw "MVP_QAIC_PY repo introuvable. Set `$env:MVP_QAIC_PY_REPO puis relance."
}}
Set-Location -LiteralPath $repo

Write-Host "============================================================"
Write-Host "MVP_QAIC_PY LOCAL PRIVATE OPERATOR SHORTCUT"
Write-Host "============================================================"
Write-Host "MODE=LOCAL_PRIVATE"
Write-Host "PROMPT_SOURCE_ID=P132_P133_PORTFOLIO_MULTIMODAL_REVIEW"
Write-Host "NO_SHEETS_WRITE=true"
Write-Host "NO_PUBLIC_DEPLOY=true"
Write-Host "NO_APPS_SCRIPT=true"
Write-Host "NO_CLASP=true"
Write-Host "NO_BROKER_ORDER_SIZING=true"
Write-Host ""

$p162 = Get-ChildItem -LiteralPath ".\\05_EXPORTS" -Directory |
  Where-Object {{ $_.Name -like "P162_LOCAL_PRIVATE_OPERATOR_HANDOFF_OR_DEV_STOP*" }} |
  Sort-Object LastWriteTime -Descending |
  Select-Object -First 1
if (-not $p162) {{ throw "P162 handoff introuvable." }}

$handoff = Join-Path $p162.FullName "P162_OPERATOR_HANDOFF.md"
$decision = Join-Path $p162.FullName "P162_DEV_STOP_DECISION.md"
$promptFile = Join-Path (Get-Location).Path "mvp_qaic_py\\multimodal_gem_image_prompt_usd_contract.py"

Write-Host "P162_HANDOFF=$handoff"
Write-Host "P162_DEV_STOP_DECISION=$decision"
Write-Host "PROMPT_SOURCE_FILE=$promptFile"
Write-Host ""
Write-Host "OPERATOR_ACTION=Use the sealed local private prompt workflow."
Write-Host "DEV_STATUS=STOP_RECOMMENDED_AFTER_THIS_SHORTCUT"
Write-Host "============================================================"
'''


def shortcut_markdown(summary: P163Summary) -> str:
    return f"""# P163 — Local Private Operator Shortcut

## Status

`{summary.STATUS}`

## Purpose

This is the final comfort shortcut after P162. It does not unlock public deployment and does not perform any live action.

## Prompt source

`{summary.PROMPT_SOURCE_ID}`

## Operator shortcut

Generated file:

`{summary.SHORTCUT_FILE}`

The shortcut only prints the sealed local private state and key paths for the operator:

- latest P162 operator handoff
- latest P162 dev-stop decision
- patched prompt source file

## Locked safety posture

- Local private only.
- No Google Sheets write.
- No live Google Sheets read.
- No public deploy.
- No Apps Script execution.
- No CLASP push.
- No broker / order / sizing.
- Auto-apply remains out of scope.

## Final next

`{summary.NEXT}`
"""


def final_close_markdown(summary: P163Summary) -> str:
    return f"""# MVP QAIC — Local Private Release Closed / Dev Stop

## Final label

`{summary.NEXT}`

## Closure decision

- Local private release sealed: `{summary.LOCAL_PRIVATE_RELEASE_SEALED}`
- Operator shortcut ready: `{summary.OPERATOR_SHORTCUT_READY}`
- Operator handoff ready: `{summary.OPERATOR_HANDOFF_READY}`
- Dev stop recommended: `{summary.DEV_STOP_RECOMMENDED}`
- Public deploy ready: `{summary.PUBLIC_DEPLOY_READY}`
- Blocker count: `{summary.BLOCKER_COUNT}`
- Rollback required: `{summary.ROLLBACK_REQUIRED}`

## Scope closed

The P152 → P163 prompt chain is closed as a local private operator release.

Any later work must open a new explicit lane, for example public prep, webapp deploy readiness, new real GEM case review, or UI/operator polish.
"""


def build_and_write_export(repo_root: Path) -> P163Summary:
    summary = build_summary(repo_root)
    export_dir = (
        repo_root / "05_EXPORTS" / f"{EXPORT_PREFIX}_{datetime.now(UTC).strftime('%Y%m%d_%H%M%S')}"
    )
    export_dir.mkdir(parents=True, exist_ok=False)
    shortcut_file = export_dir / "P163_LOCAL_PRIVATE_OPERATOR_SHORTCUT.ps1"
    shortcut_file.write_text(shortcut_script(str(repo_root)), encoding="utf-8")

    summary = P163Summary(
        **{
            **asdict(summary),
            "SHORTCUT_FILE": str(shortcut_file),
            "EXPORT_DIR": str(export_dir),
        }
    )

    summary_json = export_dir / "P163_SUMMARY.json"
    summary_json.write_text(
        json.dumps(asdict(summary), ensure_ascii=False, indent=2), encoding="utf-8"
    )
    (export_dir / "P163_OPERATOR_SHORTCUT.md").write_text(
        shortcut_markdown(summary), encoding="utf-8"
    )
    (export_dir / "P163_FINAL_CLOSE_DECISION.md").write_text(
        final_close_markdown(summary), encoding="utf-8"
    )
    write_csv(export_dir / "P163_OPERATOR_SHORTCUT_REPORT.csv", summary)
    (export_dir / "P163_OPERATOR_SHORTCUT_REPORT.json").write_text(
        json.dumps(asdict(summary), ensure_ascii=False, indent=2), encoding="utf-8"
    )
    return summary


def main(argv: list[str] | None = None) -> int:
    import argparse

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-root", default=".")
    args = parser.parse_args(argv)

    repo_root = Path(args.repo_root).resolve()
    summary = build_and_write_export(repo_root)
    print(summary.P163_STATUS)
    print(f"prompt_source_id={summary.PROMPT_SOURCE_ID}")
    print(f"local_private_release_sealed={summary.LOCAL_PRIVATE_RELEASE_SEALED}")
    print(f"operator_shortcut_ready={summary.OPERATOR_SHORTCUT_READY}")
    print(f"operator_handoff_ready={summary.OPERATOR_HANDOFF_READY}")
    print(f"dev_stop_recommended={summary.DEV_STOP_RECOMMENDED}")
    print(f"final_close_ready={summary.FINAL_CLOSE_READY}")
    print(f"public_deploy_ready={summary.PUBLIC_DEPLOY_READY}")
    print(f"blocker_count={summary.BLOCKER_COUNT}")
    print(f"rollback_required={summary.ROLLBACK_REQUIRED}")
    print(f"shortcut_file={summary.SHORTCUT_FILE}")
    print(f"export_dir={summary.EXPORT_DIR}")
    print(f"next={summary.NEXT}")
    return 0


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
