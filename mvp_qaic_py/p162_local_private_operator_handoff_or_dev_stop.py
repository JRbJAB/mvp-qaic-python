"""P162 local private operator handoff or dev-stop gate.

Local-only MVP QAIC release closure helper.
No Google Sheets writes, no public deploy, no Apps Script, no CLASP, no broker.
"""

from __future__ import annotations

import csv
import json
from dataclasses import asdict, dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

PROMPT_SOURCE_ID = "P132_P133_PORTFOLIO_MULTIMODAL_REVIEW"
MODULE_VERSION = "P162_LOCAL_PRIVATE_OPERATOR_HANDOFF_OR_DEV_STOP_20260623"
EXPORT_PREFIX = "P162_LOCAL_PRIVATE_OPERATOR_HANDOFF_OR_DEV_STOP"
P162_STATUS_READY = "P162_LOCAL_PRIVATE_OPERATOR_HANDOFF_READY_DEV_STOP_RECOMMENDED"
STATUS_READY_TO_SEAL = "OK_P162_LOCAL_PRIVATE_OPERATOR_HANDOFF_OR_DEV_STOP_READY_TO_SEAL"
NEXT_STEP = "MVP_QAIC_LOCAL_PRIVATE_RELEASE_CLOSED_DEV_STOP_OR_P163_OPERATOR_SHORTCUT"

TRUE_VALUES = {"true", "1", "yes", "y", "ok", "ready", "pass"}
FALSE_VALUES = {"false", "0", "no", "n", "ko", "blocked", "fail", ""}


class P162BlockedError(RuntimeError):
    """Raised when P162 cannot be sealed safely."""


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


def find_p161_summary(repo_root: Path) -> tuple[Path, dict[str, Any]]:
    export_dir = latest_export_dir(repo_root, "P161_RELEASE_SEAL_OR_P160B_REAL_CASE_REVIEW_PACK")
    if export_dir is None:
        raise P162BlockedError("P161_EXPORT_DIR_NOT_FOUND")
    summary_file = export_dir / "P161_SUMMARY.json"
    if not summary_file.exists():
        raise P162BlockedError("P161_SUMMARY_NOT_FOUND")
    return summary_file, read_json(summary_file)


def validate_p161(summary: dict[str, Any]) -> list[str]:
    blockers: list[str] = []
    p161_status = str(get_any(summary, "P161_STATUS", default=""))
    release_decision = str(get_any(summary, "RELEASE_DECISION", default=""))
    prompt_source_id = str(get_any(summary, "PROMPT_SOURCE_ID", default=PROMPT_SOURCE_ID))

    if p161_status != "P161_LOCAL_PRIVATE_RELEASE_SEAL_READY":
        blockers.append("P161_STATUS_NOT_RELEASE_SEAL_READY")
    if release_decision != "LOCAL_PRIVATE_RELEASE_SEALED":
        blockers.append("P161_RELEASE_DECISION_NOT_SEALED")
    if prompt_source_id != PROMPT_SOURCE_ID:
        blockers.append("PROMPT_SOURCE_ID_MISMATCH")
    if not as_bool(get_any(summary, "P160_RELEASE_SEAL_READY", default=False)):
        blockers.append("P160_RELEASE_SEAL_NOT_READY")
    if as_bool(get_any(summary, "P160B_REAL_CASE_REVIEW_PACK_REQUIRED", default=True)):
        blockers.append("P160B_REVIEW_PACK_REQUIRED")
    if as_int(get_any(summary, "BLOCKER_COUNT", default=1), default=1) != 0:
        blockers.append("P161_BLOCKER_COUNT_NON_ZERO")
    if as_bool(get_any(summary, "ROLLBACK_REQUIRED", default=True)):
        blockers.append("ROLLBACK_REQUIRED")
    return blockers


@dataclass(frozen=True)
class P162Summary:
    STATUS: str
    P162_STATUS: str
    PROMPT_SOURCE_ID: str
    SOURCE_P161_STATUS: str
    SOURCE_P161_RELEASE_DECISION: str
    SOURCE_P161_DIR: str
    LOCAL_PRIVATE_RELEASE_SEALED: bool
    OPERATOR_HANDOFF_READY: bool
    DEV_STOP_RECOMMENDED: bool
    P160B_REAL_CASE_REVIEW_PACK_REQUIRED: bool
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
    EXPORT_DIR: str
    NEXT: str
    created_at_utc: str


def build_summary(repo_root: Path) -> P162Summary:
    p161_summary_file, p161 = find_p161_summary(repo_root)
    blockers = validate_p161(p161)
    if blockers:
        raise P162BlockedError(";".join(blockers))

    p161_dir = p161_summary_file.parent
    return P162Summary(
        STATUS=STATUS_READY_TO_SEAL,
        P162_STATUS=P162_STATUS_READY,
        PROMPT_SOURCE_ID=PROMPT_SOURCE_ID,
        SOURCE_P161_STATUS=str(get_any(p161, "P161_STATUS", default="")),
        SOURCE_P161_RELEASE_DECISION=str(get_any(p161, "RELEASE_DECISION", default="")),
        SOURCE_P161_DIR=str(p161_dir),
        LOCAL_PRIVATE_RELEASE_SEALED=True,
        OPERATOR_HANDOFF_READY=True,
        DEV_STOP_RECOMMENDED=True,
        P160B_REAL_CASE_REVIEW_PACK_REQUIRED=False,
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
        EXPORT_DIR="",
        NEXT=NEXT_STEP,
        created_at_utc=utc_now_iso(),
    )


def write_csv(path: Path, summary: P162Summary) -> None:
    payload = asdict(summary)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(payload.keys()))
        writer.writeheader()
        writer.writerow(payload)


def handoff_markdown(summary: P162Summary) -> str:
    return f"""# P162 — Local Private Operator Handoff / Dev Stop

## Status

`{summary.STATUS}`

## Decision

- P162 status: `{summary.P162_STATUS}`
- Release decision: `LOCAL_PRIVATE_RELEASE_SEALED`
- Operator handoff ready: `{summary.OPERATOR_HANDOFF_READY}`
- Dev stop recommended: `{summary.DEV_STOP_RECOMMENDED}`
- P160B real-case review pack required: `{summary.P160B_REAL_CASE_REVIEW_PACK_REQUIRED}`
- Rollback required: `{summary.ROLLBACK_REQUIRED}`
- Blocker count: `{summary.BLOCKER_COUNT}`

## Scope locked

- Prompt source: `{summary.PROMPT_SOURCE_ID}`
- Local/private release only.
- No Google Sheets write.
- No live Google Sheets read.
- No public deploy.
- No Apps Script execution.
- No CLASP push.
- No broker/order/sizing.

## Operator next use

Use the local private prompt/operator flow already validated by P152 → P161. Any future public access, Sheets write, or deployed webapp route must start as a separate authorization gate.

## Next

`{summary.NEXT}`
"""


def dev_stop_markdown(summary: P162Summary) -> str:
    return f"""# P162 — Dev Stop Decision

MVP QAIC local private prompt patch chain is sealed.

## Stop recommendation

`DEV_STOP_RECOMMENDED=True`

Reason: P161 sealed the local private release after the real GEM case smoke and patched prompt runtime validation. No P160B review pack is required. No rollback is required.

## Allowed after this point

- Manual operator use of the local private prompt workflow.
- New batch only if it has a new explicit objective, such as public prep, operator shortcut, UI polish, or next real GEM case review.

## Not allowed in this sealed lane

- No automatic GEM response apply.
- No Google Sheets write.
- No public deploy.
- No Apps Script / CLASP.
- No broker / order / sizing.

## Final status

`{summary.STATUS}`
"""


def build_and_write_export(repo_root: Path) -> P162Summary:
    summary = build_summary(repo_root)
    export_dir = (
        repo_root / "05_EXPORTS" / f"{EXPORT_PREFIX}_{datetime.now(UTC).strftime('%Y%m%d_%H%M%S')}"
    )
    export_dir.mkdir(parents=True, exist_ok=False)
    summary = P162Summary(**{**asdict(summary), "EXPORT_DIR": str(export_dir)})

    payload = asdict(summary)
    (export_dir / "P162_SUMMARY.json").write_text(
        json.dumps(payload, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    (export_dir / "P162_OPERATOR_HANDOFF.md").write_text(
        handoff_markdown(summary), encoding="utf-8"
    )
    (export_dir / "P162_DEV_STOP_DECISION.md").write_text(
        dev_stop_markdown(summary), encoding="utf-8"
    )
    (export_dir / "P162_OPERATOR_HANDOFF_REPORT.json").write_text(
        json.dumps(payload, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    write_csv(export_dir / "P162_OPERATOR_HANDOFF_REPORT.csv", summary)
    return summary


def main(argv: list[str] | None = None) -> int:
    import argparse

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-root", default=".")
    args = parser.parse_args(argv)

    repo_root = Path(args.repo_root).resolve()
    summary = build_and_write_export(repo_root)
    print(summary.P162_STATUS)
    print(f"prompt_source_id={summary.PROMPT_SOURCE_ID}")
    print(f"local_private_release_sealed={summary.LOCAL_PRIVATE_RELEASE_SEALED}")
    print(f"operator_handoff_ready={summary.OPERATOR_HANDOFF_READY}")
    print(f"dev_stop_recommended={summary.DEV_STOP_RECOMMENDED}")
    print(f"p160b_real_case_review_pack_required={summary.P160B_REAL_CASE_REVIEW_PACK_REQUIRED}")
    print(f"public_deploy_ready={summary.PUBLIC_DEPLOY_READY}")
    print(f"blocker_count={summary.BLOCKER_COUNT}")
    print(f"rollback_required={summary.ROLLBACK_REQUIRED}")
    print(f"export_dir={summary.EXPORT_DIR}")
    print(f"next={summary.NEXT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
