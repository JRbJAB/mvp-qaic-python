"""Private local page for auto-update tracker status."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from mvp_qaic_reflex_ui.mission_control_auto_update_panel import tracker_auto_update_panel
from mvp_qaic_reflex_ui.tracker_auto_update import build_tracker_auto_update_snapshot

try:
    import reflex as rx
except Exception:  # noqa: BLE001
    rx = None  # type: ignore[assignment]

TRACKERS_ROUTE = "/trackers/auto-update"


def _require_reflex() -> Any:
    if rx is None:
        raise RuntimeError("reflex is required to render this page")
    return rx


def auto_update_trackers_page() -> Any:
    reflex = _require_reflex()
    snapshot = build_tracker_auto_update_snapshot(Path.cwd())
    legend = snapshot.get("legend", {})
    return reflex.container(
        reflex.vstack(
            reflex.heading("Auto-update Trackers", size="6"),
            reflex.text(
                "Lecture locale uniquement. Le serveur permanent doit synchroniser "
                "le repo Drive vers le runtime LocalAppData.",
                size="2",
            ),
            tracker_auto_update_panel(Path.cwd()),
            reflex.card(
                reflex.vstack(
                    reflex.heading("Différences", size="4"),
                    reflex.text(f"Dev Tracking — {legend.get('dev_tracking')}", size="2"),
                    reflex.text(f"CDC Tracker — {legend.get('cdc_tracker')}", size="2"),
                    reflex.text(f"Migration Tracker — {legend.get('migration_tracker')}", size="2"),
                    spacing="2",
                ),
                width="100%",
            ),
            reflex.hstack(
                reflex.link(reflex.button("Retour Mission Control"), href="/"),
                reflex.link(
                    reflex.button("Snapshot JSON"),
                    href="/TRACKER_AUTO_UPDATE_SNAPSHOT.json",
                    is_external=True,
                ),
                spacing="3",
                flex_wrap="wrap",
            ),
            spacing="4",
            width="100%",
        ),
        size="4",
        padding_y="1.5rem",
    )
