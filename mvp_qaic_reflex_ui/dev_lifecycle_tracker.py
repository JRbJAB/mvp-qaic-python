from __future__ import annotations

import json
import subprocess
from collections import Counter
from pathlib import Path
from typing import Any

try:
    import reflex as rx
except Exception:  # pragma: no cover - Reflex optional for tests/static smoke
    rx = None  # type: ignore[assignment]


REPO_ROOT = Path(__file__).resolve().parents[1]
TRACKER_JSON = REPO_ROOT / "docs" / "dev_tracking" / "DEV_LIFECYCLE_TRACKER.json"
STATUS_READY = "ACTIVE"


def _git(args: list[str]) -> str:
    try:
        cp = subprocess.run(
            ["git", *args],
            cwd=REPO_ROOT,
            text=True,
            capture_output=True,
            encoding="utf-8",
            errors="replace",
            check=False,
        )
        if cp.returncode != 0:
            return ""
        return cp.stdout.strip()
    except Exception:
        return ""


def _live_git() -> dict[str, Any]:
    status_lines = [line for line in _git(["status", "--short"]).splitlines() if line.strip()]
    commits = [line for line in _git(["log", "--oneline", "-8"]).splitlines() if line.strip()]
    return {
        "head": _git(["rev-parse", "--short=12", "HEAD"]),
        "branch": _git(["rev-parse", "--abbrev-ref", "HEAD"]),
        "subject": _git(["log", "-1", "--pretty=%s"]),
        "latest_tag": _git(["describe", "--tags", "--abbrev=0"]),
        "dirty_count": len(status_lines),
        "dirty_files": status_lines,
        "recent_commits": commits,
    }


def _load_contract() -> dict[str, Any]:
    payload = json.loads(TRACKER_JSON.read_text(encoding="utf-8"))
    phases = sorted(payload.get("phases", []), key=lambda row: int(row.get("order", 0)))
    payload["phases"] = phases
    return payload


def build_dev_lifecycle_model() -> dict[str, Any]:
    payload = _load_contract()
    phases = payload["phases"]
    git = _live_git()
    counts = Counter(str(row.get("status", "UNKNOWN")) for row in phases)
    done = [row for row in phases if row.get("status") == "DONE"]
    active = [row for row in phases if row.get("status") == "ACTIVE"]
    next_rows = [row for row in phases if row.get("status") == "NEXT"]
    future = [row for row in phases if row.get("status") == "FUTURE"]
    blocked_or_parked = [row for row in phases if row.get("status") in {"BLOCKED", "PARKED"}]
    done_weight = counts.get("DONE", 0)
    active_weight = 0.5 * counts.get("ACTIVE", 0)
    progress = round(((done_weight + active_weight) / max(len(phases), 1)) * 100, 1)
    return {
        "status": STATUS_READY,
        "schema_version": payload.get("schema_version", ""),
        "ui_contract": payload.get("ui_contract", "VERTICAL_MIGRATION_TRACKER_STYLE"),
        "update_policy": payload.get(
            "update_policy", "automatic_on_batch_commit_plus_git_live_on_render"
        ),
        "policy": payload.get("update_policy", "automatic_on_batch_commit_plus_git_live_on_render"),
        "quality_gate": payload.get("quality_gate", "vertical lifecycle tracker"),
        "views": payload.get("views", {}),
        "required_coverage": payload.get("required_coverage", []),
        "git": git,
        "phases": phases,
        "phase_count": len(phases),
        "status_counts": dict(counts),
        "counts": {
            "total": len(phases),
            "done": len(done),
            "active": len(active),
            "next": len(next_rows) + len(future),
            "blocked_or_parked": len(blocked_or_parked),
        },
        "progress_percent": progress,
        "done_phase_ids": [row["phase_id"] for row in done],
        "active_phase_ids": [row["phase_id"] for row in active],
        "next_phase_ids": [row["phase_id"] for row in [*next_rows, *future]],
        "blocked_or_parked_phase_ids": [row["phase_id"] for row in blocked_or_parked],
    }


def _status_label(status: str) -> str:
    return {
        "DONE": "Terminé",
        "ACTIVE": "En cours",
        "NEXT": "À venir",
        "FUTURE": "Futur",
        "BLOCKED": "Bloqué",
        "PARKED": "Parké",
    }.get(status, status)


def _status_style(status: str) -> dict[str, str]:
    styles = {
        "DONE": {"bg": "#dcfce7", "fg": "#166534", "bar": "#2563eb"},
        "ACTIVE": {"bg": "#dbeafe", "fg": "#1d4ed8", "bar": "#2563eb"},
        "NEXT": {"bg": "#fef3c7", "fg": "#92400e", "bar": "#93c5fd"},
        "FUTURE": {"bg": "#f3f4f6", "fg": "#374151", "bar": "#bfdbfe"},
        "BLOCKED": {"bg": "#fee2e2", "fg": "#991b1b", "bar": "#ef4444"},
        "PARKED": {"bg": "#ede9fe", "fg": "#5b21b6", "bar": "#8b5cf6"},
    }
    return styles.get(status, {"bg": "#f3f4f6", "fg": "#374151", "bar": "#93c5fd"})


def _plain_phase(row: dict[str, Any]) -> dict[str, Any]:
    return {
        "phase_id": row.get("phase_id"),
        "status": row.get("status"),
        "title": row.get("title"),
        "goal": row.get("goal"),
        "progress_percent": row.get("progress_percent"),
        "evidence": row.get("evidence"),
        "tests": row.get("tests"),
        "head": row.get("head"),
        "tag": row.get("tag"),
        "next_action": row.get("next_action"),
    }


def _phase_card(row: dict[str, Any], compact: bool) -> Any:
    if rx is None:
        return _plain_phase(row)
    status = str(row.get("status", "UNKNOWN"))
    style = _status_style(status)
    progress = int(row.get("progress_percent", 0) or 0)
    return rx.box(
        rx.vstack(
            rx.hstack(
                rx.badge(_status_label(status), background_color=style["bg"], color=style["fg"]),
                rx.text(str(row.get("phase_id", "")), font_weight="700", color="#111827"),
                rx.spacer(),
                rx.text(f"{progress}%", font_size="12px", color="#2563eb", font_weight="700"),
                width="100%",
                align="center",
            ),
            rx.heading(str(row.get("title", "")), size="3"),
            rx.box(
                rx.box(
                    height="8px",
                    width=f"{progress}%",
                    background_color=style["bar"],
                    border_radius="999px",
                ),
                height="8px",
                width="100%",
                background_color="#e5e7eb",
                border_radius="999px",
            ),
            rx.text(str(row.get("track", "")), font_size="12px", color="#4b5563"),
            rx.text(str(row.get("goal", "")), font_size="13px", color="#1f2937"),
            rx.text(str(row.get("evidence", "")), font_size="13px", color="#111827"),
            rx.cond(
                compact,
                rx.fragment(),
                rx.vstack(
                    rx.text(
                        "Tests · " + str(row.get("tests", "")), font_size="12px", color="#374151"
                    ),
                    rx.text(
                        "Next · " + str(row.get("next_action", "")),
                        font_size="12px",
                        color="#374151",
                    ),
                    rx.text(
                        "HEAD/TAG · " + str(row.get("head", "")) + " · " + str(row.get("tag", "")),
                        font_size="11px",
                        color="#6b7280",
                    ),
                    spacing="1",
                    align="stretch",
                ),
            ),
            spacing="2",
            align="stretch",
        ),
        padding="0.85em",
        border="1px solid #e5e7eb",
        border_left=f"6px solid {style['bar']}",
        border_radius="14px",
        background_color="white",
        box_shadow="0 1px 2px rgba(15, 23, 42, 0.06)",
        width="100%",
    )


def dev_lifecycle_tracker_panel(compact: bool = False, context: str = "dev") -> Any:
    model = build_dev_lifecycle_model()
    if rx is None:
        return model
    git = model["git"]
    subtitle = (
        "CDC + Dev Tracker · timeline verticale style Migration Tracker · "
        "passé, en cours, à venir, futur · mise à jour Git live"
    )
    return rx.box(
        rx.vstack(
            rx.hstack(
                rx.vstack(
                    rx.heading("CDC + Dev Lifecycle Tracker", size="4"),
                    rx.text(subtitle, font_size="12px", color="#4b5563"),
                    spacing="1",
                    align="start",
                ),
                rx.spacer(),
                rx.badge(model["status"], background_color="#dbeafe", color="#1d4ed8"),
                width="100%",
                align="center",
            ),
            rx.hstack(
                rx.text("Progression globale", font_weight="600", color="#111827"),
                rx.spacer(),
                rx.text(str(model["progress_percent"]) + "%", color="#2563eb", font_weight="700"),
                width="100%",
            ),
            rx.box(
                rx.box(
                    height="10px",
                    width=str(model["progress_percent"]) + "%",
                    background_color="#2563eb",
                    border_radius="999px",
                ),
                height="10px",
                width="100%",
                background_color="#e5e7eb",
                border_radius="999px",
            ),
            rx.hstack(
                rx.badge(
                    "DONE " + str(len(model["done_phase_ids"])),
                    background_color="#dcfce7",
                    color="#166534",
                ),
                rx.badge(
                    "ACTIVE " + ",".join(model["active_phase_ids"]),
                    background_color="#dbeafe",
                    color="#1d4ed8",
                ),
                rx.badge(
                    "NEXT/FUTURE " + str(len(model["next_phase_ids"])),
                    background_color="#fef3c7",
                    color="#92400e",
                ),
                flex_wrap="wrap",
                spacing="2",
            ),
            rx.text(
                "Git live · HEAD "
                + str(git.get("head", ""))
                + " · branch "
                + str(git.get("branch", ""))
                + " · dirty "
                + str(git.get("dirty_count", 0))
                + " · tag "
                + str(git.get("latest_tag", "")),
                font_size="12px",
                color="#374151",
            ),
            rx.vstack(
                *[_phase_card(row, compact=compact) for row in model["phases"]],
                spacing="3",
                align="stretch",
                width="100%",
            ),
            spacing="3",
            align="stretch",
        ),
        padding="1em",
        border="1px solid #e5e7eb",
        border_radius="16px",
        background_color="#f8fafc",
        width="100%",
    )


# Compatibility aliases used by previous batches/tests.
def dev_tracker_lifecycle_panel(compact: bool = False) -> Any:
    return dev_lifecycle_tracker_panel(compact=compact, context="dev")


def cdc_lifecycle_tracker_panel(compact: bool = False) -> Any:
    return dev_lifecycle_tracker_panel(compact=compact, context="cdc")


def dev_lifecycle_tracker_page() -> Any:
    if rx is None:
        return build_dev_lifecycle_model()
    return rx.box(
        dev_lifecycle_tracker_panel(compact=False, context="dev"),
        padding="1em",
        width="100%",
    )
