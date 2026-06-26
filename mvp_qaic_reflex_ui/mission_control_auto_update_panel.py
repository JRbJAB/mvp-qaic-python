"""Mission Control panel for local tracker auto-update status."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from mvp_qaic_reflex_ui.tracker_auto_update import build_tracker_auto_update_snapshot

try:
    import reflex as rx
except Exception:  # noqa: BLE001
    rx = None  # type: ignore[assignment]


def _require_reflex() -> Any:
    if rx is None:
        raise RuntimeError("reflex is required to render this panel")
    return rx


def tracker_auto_update_panel(repo_root: str | Path | None = None) -> Any:
    reflex = _require_reflex()
    snapshot = build_tracker_auto_update_snapshot(repo_root or Path.cwd())
    trackers = snapshot.get("trackers", {})

    def row(label: str, key: str) -> Any:
        payload = trackers.get(key, {})
        exists = payload.get("exists")
        path = payload.get("path", "")
        return reflex.hstack(
            reflex.badge(label),
            reflex.text(f"exists={exists}", size="2"),
            reflex.text(str(path), size="2"),
            spacing="3",
            flex_wrap="wrap",
        )

    return reflex.card(
        reflex.vstack(
            reflex.heading("Auto-update Trackers", size="4"),
            reflex.text(
                "Fondation locale : Dev Tracking, CDC Tracker et Migration Tracker "
                "sont lus depuis docs/, 05_EXPORTS/ et CSV CLASP. "
                "Le runtime LocalAppData doit être synchronisé.",
                size="2",
            ),
            reflex.hstack(
                reflex.badge(snapshot.get("status", "LOCAL_FILES")),
                reflex.badge(snapshot.get("sync_state", "SYNC_REQUIRED")),
                spacing="3",
                flex_wrap="wrap",
            ),
            row("Dev Tracking", "dev_tracking"),
            row("CDC Tracker", "cdc_tracker"),
            row("Migration Tracker", "migration_tracker"),
            row("CLASP CSV", "clasp_imports"),
            reflex.link(reflex.button("Ouvrir le panneau détaillé"), href="/trackers/auto-update"),
            spacing="3",
        ),
        width="100%",
    )
