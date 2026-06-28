from __future__ import annotations

import json
import subprocess
from pathlib import Path
from typing import Any

try:
    import reflex as rx
except Exception:  # pragma: no cover - Reflex optional in unit tests
    rx = None  # type: ignore[assignment]


REPO_ROOT = Path(__file__).resolve().parents[1]
TRACKER_JSON = REPO_ROOT / "docs" / "dev_tracking" / "DEV_LIFECYCLE_TRACKER.json"
STATUS_READY = "READY_AUTO_LIVE_CDC_DEV_TRACKER"


def _git(args: list[str]) -> str:
    try:
        cp = subprocess.run(
            ["git", *args],
            cwd=str(REPO_ROOT),
            text=True,
            capture_output=True,
            encoding="utf-8",
            errors="replace",
            timeout=8,
            check=False,
        )
    except Exception as exc:  # pragma: no cover - defensive local shell fallback
        return f"GIT_ERROR:{exc.__class__.__name__}"
    if cp.returncode != 0:
        return (cp.stderr or cp.stdout or "").strip()
    return cp.stdout.strip()


def _git_lines(args: list[str]) -> list[str]:
    return [line.strip() for line in _git(args).splitlines() if line.strip()]


def _load_contract() -> dict[str, Any]:
    if not TRACKER_JSON.exists():
        return {
            "schema_version": "MISSING_DEV_LIFECYCLE_TRACKER_JSON",
            "status": "MISSING_DEV_LIFECYCLE_TRACKER_JSON",
            "policy": "missing local tracker contract",
            "phases": [],
            "views": {},
            "required_coverage": [],
        }
    return json.loads(TRACKER_JSON.read_text(encoding="utf-8"))


def _live_git_state() -> dict[str, Any]:
    status_lines = _git_lines(["status", "--short"])
    return {
        "head": _git(["rev-parse", "--short=12", "HEAD"]),
        "branch": _git(["rev-parse", "--abbrev-ref", "HEAD"]),
        "subject": _git(["log", "-1", "--pretty=%s"]),
        "last_tag": _git(["describe", "--tags", "--abbrev=0"]),
        "dirty_count": len(status_lines),
        "dirty_files": status_lines,
        "recent_commits": _git_lines(["log", "--oneline", "-8"]),
    }


def build_dev_lifecycle_model() -> dict[str, Any]:
    contract = _load_contract()
    phases = list(contract.get("phases", []))
    done = [row for row in phases if row.get("status") == "DONE"]
    active = [row for row in phases if row.get("status") == "ACTIVE"]
    next_rows = [row for row in phases if row.get("status") == "NEXT"]
    blocked = [row for row in phases if row.get("status") in {"BLOCKED", "PARKED"}]
    git = _live_git_state()
    return {
        "status": contract.get("status", STATUS_READY),
        "schema_version": contract.get("schema_version", ""),
        "policy": contract.get("policy", ""),
        "views": contract.get("views", {}),
        "required_coverage": contract.get("required_coverage", []),
        "git": git,
        "phases": phases,
        "done_phase_ids": [row.get("phase_id", "") for row in done],
        "active_phase_ids": [row.get("phase_id", "") for row in active],
        "next_phase_ids": [row.get("phase_id", "") for row in next_rows],
        "blocked_or_parked_phase_ids": [row.get("phase_id", "") for row in blocked],
        "counts": {
            "total": len(phases),
            "done": len(done),
            "active": len(active),
            "next": len(next_rows),
            "blocked_or_parked": len(blocked),
        },
    }


def _plain_card(title: str, detail: str) -> dict[str, str]:
    return {"title": title, "detail": detail}


def _metric(label: str, value: object) -> Any:
    if rx is None:
        return _plain_card(label, str(value))
    return rx.box(
        rx.text(label, font_size="12px", opacity="0.72"),
        rx.heading(str(value), size="4"),
        padding="0.75em",
        border="1px solid #e5e7eb",
        border_radius="12px",
        min_width="140px",
    )


def _phase_card(row: dict[str, Any]) -> Any:
    title = f"{row.get('phase_id', '')} · {row.get('status', '')} · {row.get('title', '')}"
    details = (
        f"HEAD={row.get('head', '')} · TAG={row.get('tag', '')} · "
        f"TESTS={row.get('tests', '')}"
    )
    evidence = str(row.get("evidence", ""))
    next_action = str(row.get("next_action", ""))
    if rx is None:
        return {"title": title, "details": details, "evidence": evidence, "next_action": next_action}
    return rx.box(
        rx.text(title, font_weight="700"),
        rx.text(details, font_size="12px", opacity="0.78"),
        rx.text(evidence, font_size="13px"),
        rx.text(f"Next: {next_action}", font_size="12px", opacity="0.78"),
        padding="0.75em",
        border="1px solid #e5e7eb",
        border_radius="12px",
        width="100%",
    )


def dev_lifecycle_tracker_panel(compact: bool = False) -> Any:
    model = build_dev_lifecycle_model()
    if rx is None:
        return model
    git = model["git"]
    counts = model["counts"]
    phases = model["phases"] if not compact else model["phases"][:6]
    return rx.box(
        rx.vstack(
            rx.heading("Auto-live Dev Lifecycle Tracker", size="4"),
            rx.text(model["policy"], font_size="12px", opacity="0.75"),
            rx.hstack(
                _metric("Live HEAD", git["head"]),
                _metric("Branch", git["branch"]),
                _metric("Dirty", git["dirty_count"]),
                _metric("Done", counts["done"]),
                _metric("Active", counts["active"]),
                _metric("Next", counts["next"]),
                flex_wrap="wrap",
                spacing="3",
            ),
            rx.text(f"Last commit: {git['subject']}", font_size="13px", opacity="0.82"),
            rx.heading("Past / active / future phases", size="3"),
            *[_phase_card(row) for row in phases],
            spacing="3",
            align="stretch",
        ),
        padding="1em",
        border="1px solid #e5e7eb",
        border_radius="14px",
        width="100%",
    )


def dev_lifecycle_tracker_page() -> Any:
    if rx is None:
        return build_dev_lifecycle_model()
    return rx.box(
        rx.vstack(
            rx.heading("Dev Tracking", size="6"),
            rx.text("Vue auto-live des phases passées, actives et futures, alimentée par Git et le contrat local versionné."),
            dev_lifecycle_tracker_panel(compact=False),
            spacing="4",
            align="stretch",
        ),
        padding="1em",
        width="100%",
    )
