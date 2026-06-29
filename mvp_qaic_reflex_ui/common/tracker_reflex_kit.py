from __future__ import annotations

from collections import defaultdict
from collections.abc import Iterable, Mapping, Sequence
from typing import Any

import reflex as rx

from .tracker_ui_kit import (
    COCKPIT_RENDER_BINDINGS,
    REFERENCE_RENDER_TYPES,
    TrackerItem,
    normalize_percent,
)

BLUE = "#2563eb"
BLUE_SOFT = "#dbeafe"
LINE = "#dbe4f0"
INK = "#172033"
MUTED = "#64748b"

STATUS_STYLES: dict[str, dict[str, str]] = {
    "DONE": {"bg": "#dcfce7", "fg": "#166534", "bar": BLUE},
    "ACTIVE": {"bg": BLUE_SOFT, "fg": "#1d4ed8", "bar": BLUE},
    "NEXT": {"bg": BLUE_SOFT, "fg": "#1d4ed8", "bar": "#60a5fa"},
    "REVIEW": {"bg": "#fff7ed", "fg": "#c2410c", "bar": "#60a5fa"},
    "MISSING": {"bg": "#fee2e2", "fg": "#991b1b", "bar": "#ef4444"},
    "BLOCKED": {"bg": "#fee2e2", "fg": "#991b1b", "bar": "#ef4444"},
    "PLANNED": {"bg": BLUE_SOFT, "fg": "#1d4ed8", "bar": "#93c5fd"},
    "PARKED": {"bg": "#ede9fe", "fg": "#5b21b6", "bar": "#8b5cf6"},
    "FUTURE": {"bg": "#f3f4f6", "fg": "#374151", "bar": "#bfdbfe"},
    "ON_TRACK": {"bg": "#dcfce7", "fg": "#166534", "bar": BLUE},
    "WATCH": {"bg": "#fff7ed", "fg": "#c2410c", "bar": "#d97706"},
}


def status_badge(status: object) -> rx.Component:
    label = str(status or "REVIEW").upper()
    style = STATUS_STYLES.get(label, STATUS_STYLES["FUTURE"])
    return rx.badge(
        label,
        background_color=style["bg"],
        color=style["fg"],
        border=f"1px solid {style['bg']}",
        font_weight="700",
    )


def progress_bar(percent: object, *, width: str = "100%") -> rx.Component:
    value = normalize_percent(percent)
    return rx.vstack(
        rx.hstack(
            rx.text("Progress", font_size="12px", color=MUTED),
            rx.spacer(),
            rx.text(f"{value}%", font_size="12px", color=BLUE, font_weight="800"),
            width="100%",
            align="center",
        ),
        rx.box(
            rx.box(
                height="10px",
                width=f"{value}%",
                background_color=BLUE,
                border_radius="999px",
            ),
            height="10px",
            width=width,
            background_color=BLUE_SOFT,
            border_radius="999px",
            overflow="hidden",
        ),
        spacing="1",
        align="stretch",
        width=width,
    )


def tracker_item_card(item: TrackerItem, *, reference_type: str) -> rx.Component:
    route = item.route or ""
    return rx.box(
        rx.vstack(
            rx.hstack(
                status_badge(item.status),
                rx.spacer(),
                rx.text(item.item_id, font_size="12px", color=BLUE, font_weight="800"),
                width="100%",
                align="center",
            ),
            rx.heading(item.title, size="3", color=INK),
            progress_bar(item.percent),
            rx.text(item.description, font_size="13px", color="#1f2937"),
            rx.hstack(
                rx.badge(
                    item.priority or "P2",
                    background_color="#f8fafc",
                    color="#334155",
                    border=f"1px solid {LINE}",
                ),
                rx.link(route, href=route, color=BLUE, font_size="12px")
                if route
                else rx.fragment(),
                rx.spacer(),
                rx.text(reference_type, font_size="11px", color=MUTED),
                width="100%",
                align="center",
            ),
            spacing="2",
            align="stretch",
        ),
        padding="0.9rem",
        border=f"1px solid {LINE}",
        border_left=f"5px solid {BLUE}",
        border_radius="8px",
        background_color="white",
        box_shadow="0 1px 3px rgba(15, 23, 42, 0.08)",
        width="100%",
    )


def tracker_section(
    title: str,
    subtitle: str,
    render_type: str,
    items: Sequence[TrackerItem],
    *,
    route: str,
    group_by_priority: bool = False,
) -> rx.Component:
    sections: dict[str, list[TrackerItem]] = defaultdict(list)
    if group_by_priority:
        for item in items:
            sections[item.priority or "P2"].append(item)
    else:
        sections["All"] = list(items)

    groups = []
    for group, group_items in sections.items():
        groups.append(
            rx.vstack(
                rx.heading(group if group_by_priority else "Readiness", size="3", color=INK),
                rx.grid(
                    *[tracker_item_card(item, reference_type=render_type) for item in group_items],
                    columns="repeat(auto-fit, minmax(250px, 1fr))",
                    spacing="3",
                    width="100%",
                ),
                spacing="3",
                align="stretch",
                width="100%",
            )
        )

    return rx.box(
        rx.vstack(
            rx.hstack(
                rx.vstack(
                    rx.heading(title, size="5", color=INK),
                    rx.text(subtitle, font_size="13px", color=MUTED),
                    spacing="1",
                    align="start",
                ),
                rx.spacer(),
                rx.link(route, href=route, color=BLUE, font_weight="800"),
                status_badge(render_type),
                width="100%",
                align="center",
            ),
            *groups,
            spacing="4",
            align="stretch",
            width="100%",
        ),
        data_render_type=render_type,
        border=f"1px solid {LINE}",
        border_radius="8px",
        background_color="#f8fbff",
        padding="1rem",
        width="100%",
    )


def reference_gallery() -> rx.Component:
    return rx.box(
        rx.vstack(
            rx.heading("Reference rendering types", size="4", color=INK),
            rx.grid(
                *[
                    rx.box(
                        rx.vstack(
                            rx.text(ref_id, font_size="12px", color=BLUE, font_weight="800"),
                            rx.heading(str(ref["title"]), size="3", color=INK),
                            rx.text(str(ref["purpose"]), font_size="13px", color=MUTED),
                            spacing="2",
                            align="stretch",
                        ),
                        id=f"render-type-{ref_id}",
                        border=f"1px solid {LINE}",
                        border_radius="8px",
                        background_color="white",
                        padding="0.85rem",
                    )
                    for ref_id, ref in REFERENCE_RENDER_TYPES.items()
                ],
                columns="repeat(auto-fit, minmax(230px, 1fr))",
                spacing="3",
                width="100%",
            ),
            spacing="3",
            align="stretch",
            width="100%",
        ),
        border=f"1px solid {LINE}",
        border_radius="8px",
        background_color="white",
        padding="1rem",
        width="100%",
    )


def cockpit_mapping() -> rx.Component:
    return rx.box(
        rx.vstack(
            rx.heading("Cockpit mapping", size="4", color=INK),
            rx.vstack(
                *[
                    rx.hstack(
                        rx.text(binding["cockpit"], font_weight="700", color=INK),
                        rx.link(binding["route"], href=binding["route"], color=BLUE),
                        rx.link(
                            binding["render_type"],
                            href=f"#render-type-{binding['render_type']}",
                            color=BLUE,
                            font_weight="700",
                        ),
                        rx.text(binding["role"], color=MUTED, font_size="13px"),
                        spacing="3",
                        align="center",
                        width="100%",
                        flex_wrap="wrap",
                    )
                    for binding in COCKPIT_RENDER_BINDINGS
                ],
                spacing="2",
                align="stretch",
                width="100%",
            ),
            spacing="3",
            align="stretch",
            width="100%",
        ),
        border=f"1px solid {LINE}",
        border_radius="8px",
        background_color="white",
        padding="1rem",
        width="100%",
    )


def tracker_body(
    *,
    cdc_items: Sequence[TrackerItem],
    dev_items: Sequence[TrackerItem],
    source_label: str,
    source_detail: str,
    view: str = "combined",
) -> rx.Component:
    show_cdc = view in {"combined", "cdc"}
    show_dev = view in {"combined", "dev"}
    return rx.vstack(
        rx.box(
            rx.vstack(
                rx.hstack(
                    rx.vstack(
                        rx.heading("CDC + Dev Tracker", size="6", color=INK),
                        rx.text(source_label, color=MUTED),
                        rx.text(source_detail, font_size="12px", color=MUTED),
                        spacing="1",
                        align="start",
                    ),
                    rx.spacer(),
                    status_badge("ACTIVE"),
                    width="100%",
                    align="center",
                ),
                progress_bar(_average_percent([*cdc_items, *dev_items]), width="260px"),
                spacing="3",
                align="stretch",
                width="100%",
            ),
            border=f"1px solid {LINE}",
            border_radius="8px",
            background_color="white",
            padding="1rem",
            width="100%",
        ),
        reference_gallery() if view == "combined" else rx.fragment(),
        cockpit_mapping() if view == "combined" else rx.fragment(),
        tracker_section(
            "CDC Tracker",
            "CDC delivery tracker view with route, source, readiness, and cockpit coverage.",
            "cdc_dev_tracker" if view == "combined" else "cdc_tracker",
            cdc_items,
            route="/cdc-tracker",
        )
        if show_cdc
        else rx.fragment(),
        tracker_section(
            "Dev Tracker",
            "Development priorities grouped by priority/readiness with blue progress language.",
            "dev_tracker",
            dev_items,
            route="/dev-tracking",
            group_by_priority=True,
        )
        if show_dev
        else rx.fragment(),
        spacing="4",
        align="stretch",
        width="100%",
    )


def tracker_items_from_rows(
    rows: Iterable[Mapping[str, Any]],
    *,
    id_keys: Sequence[str],
    title_keys: Sequence[str],
    percent_keys: Sequence[str],
    status_key: str,
    description_keys: Sequence[str],
    route: str = "",
    default_priority: str = "P2",
) -> list[TrackerItem]:
    return [
        TrackerItem(
            item_id=_first(row, id_keys, f"item_{index}"),
            title=_first(row, title_keys, f"Tracker item {index}"),
            status=_status_from_row(row, status_key),
            percent=normalize_percent(_first(row, percent_keys, "0")),
            description=_first(row, description_keys, ""),
            route=route,
            priority=_first(row, ("priority", "prio"), default_priority),
        )
        for index, row in enumerate(rows, 1)
    ]


def _first(row: Mapping[str, Any], keys: Sequence[str], fallback: str) -> str:
    for key in keys:
        value = row.get(key)
        if value not in (None, ""):
            return str(value)
    return fallback


def _status_from_row(row: Mapping[str, Any], status_key: str) -> str:
    value = str(row.get(status_key) or "").upper()
    if value:
        return value
    remaining = str(row.get("remaining_h") or row.get("remaining_effort_hours") or "").replace(
        ",", "."
    )
    if remaining in {"0", "0.0", "0.00"}:
        return "DONE"
    blocked = str(row.get("blocked") or "").replace(",", ".")
    if blocked not in {"", "0", "0.0", "0.00", "0.0%"}:
        return "BLOCKED"
    return "REVIEW"


def _average_percent(items: Sequence[TrackerItem]) -> int:
    if not items:
        return 0
    return normalize_percent(sum(item.percent for item in items) / len(items))
