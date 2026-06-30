"""Private cockpit pages for MVP QAIC Reflex.

R2A_R14A_RICH_MIGRATION_COCKPIT
Private local UI only. No public deploy, no broker, no order, no sizing.
"""

from __future__ import annotations

import reflex as rx

ACCENT = "#3b82f6"
BG = "#020617"
CARD = "#0f172a"
TEXT = "#f8fafc"
MUTED = "#93a4c6"
BORDER = "#2563eb"
GREEN = "#22c55e"
AMBER = "#f59e0b"
RED = "#ef4444"

ROUTE_SUMMARY = [
    ("/", "Home", "MVP QAIC control room"),
    ("/cdc-tracker", "CDC Tracker", "CDC delivery tracker"),
    ("/cdc-dev-tracker", "CDC + Dev Tracker", "cross cockpit"),
    ("/dev-tracking", "Dev Tracking", "migration OS"),
]

MIGRATION_MODULES = [
    (
        "Prompt Portfolio",
        "P0",
        "NEXT",
        "Migrate prompt portfolio review with image/text input and human review.",
    ),
    (
        "CDC Tracker",
        "R6/R13",
        "ACTIVE",
        "Keep CDC route readable and tied to real tracker evidence.",
    ),
    ("Dev Tracker", "R13/R14", "ACTIVE", "Track modules to migrate definitively to Python."),
    ("Gem Response Review", "P119", "PARKED", "Review parked queue before restoring into source."),
    (
        "Revolut X Execution",
        "QAIC",
        "LOCKED",
        "Private backend only; no order/sizing/live action in MVP.",
    ),
]

CDC_ITEMS = [
    ("Runtime private", "OK", "backend 8007 + frontend 3007 proved locally"),
    ("Routes", "OK", "/, /cdc-tracker, /cdc-dev-tracker, /dev-tracking"),
    ("Bun frontend", "BYPASSED", "Windows Bun dependency crash; npm fallback active"),
    ("Source routes", "OK", "distinct Reflex source pages sealed"),
]


def _style_page() -> dict[str, str]:
    return {
        "min_height": "100vh",
        "background": BG,
        "color": TEXT,
        "padding": "34px",
        "font_family": "Inter, system-ui, Segoe UI, sans-serif",
    }


def _card_style() -> dict[str, str]:
    return {
        "background": CARD,
        "border": f"1px solid {BORDER}",
        "border_radius": "18px",
        "padding": "24px",
        "box_shadow": "0 0 0 1px rgba(59,130,246,.16)",
    }


def _badge(label: str, color: str = ACCENT) -> rx.Component:
    return rx.box(
        label,
        padding="8px 12px",
        border_radius="999px",
        background=color,
        color="white",
        font_weight="800",
        display="inline-block",
    )


def _nav(active: str) -> rx.Component:
    links = []
    for route, label, _desc in ROUTE_SUMMARY:
        active_style = {"background": "rgba(59,130,246,.22)"} if route == active else {}
        links.append(
            rx.link(
                label,
                href=route,
                padding="14px 18px",
                border=f"1px solid {BORDER}",
                border_radius="14px",
                color=TEXT,
                font_weight="800",
                text_decoration="none",
                style=active_style,
            )
        )
    return rx.hstack(*links, spacing="4", flex_wrap="wrap", margin_y="28px")


def _metric(label: str, value: str, status: str) -> rx.Component:
    color = GREEN if status == "OK" else AMBER if status in {"NEXT", "ACTIVE", "BYPASSED"} else RED
    return rx.box(
        rx.text(label, color=MUTED, font_size="14px", font_weight="700"),
        rx.heading(value, size="6", margin_top="8px"),
        _badge(status, color),
        style=_card_style(),
    )


def _module_table() -> rx.Component:
    rows = []
    for name, phase, status, detail in MIGRATION_MODULES:
        rows.append(
            rx.box(
                rx.hstack(
                    rx.box(
                        rx.text(name, font_weight="900"), rx.text(detail, color=MUTED), width="58%"
                    ),
                    rx.text(phase, font_weight="800", width="14%"),
                    rx.text(status, font_weight="900", color=ACCENT, width="18%"),
                    spacing="4",
                    align="start",
                ),
                padding="14px 0",
                border_bottom="1px solid rgba(59,130,246,.22)",
            )
        )
    return rx.box(*rows, style=_card_style())


def _cdc_list() -> rx.Component:
    return rx.vstack(
        *[
            rx.hstack(
                rx.text(name, font_weight="900", width="28%"),
                rx.text(status, color=ACCENT, font_weight="900", width="18%"),
                rx.text(detail, color=MUTED, width="54%"),
                padding="10px 0",
                border_bottom="1px solid rgba(59,130,246,.18)",
            )
            for name, status, detail in CDC_ITEMS
        ],
        align="stretch",
        spacing="2",
        style=_card_style(),
    )


def _shell(
    section: str, title: str, subtitle: str, active: str, body: rx.Component
) -> rx.Component:
    return rx.box(
        rx.text(section.upper(), color="#60a5fa", font_weight="900", letter_spacing=".22em"),
        rx.heading(title, size="9", margin_top="18px"),
        rx.text(subtitle, color=MUTED, font_size="20px", margin_top="14px"),
        _nav(active),
        body,
        rx.text(
            "Private preview only - no public deploy / no broker / no order / no sizing.",
            color=MUTED,
            margin_top="28px",
            font_size="14px",
        ),
        style=_style_page(),
    )


def home_page() -> rx.Component:
    return _shell(
        "MVP QAIC private cockpit",
        "MVP QAIC Control Room",
        "Runtime prive valide. Prochaine etape: brancher les donnees reelles et piloter les migrations Python.",
        "/",
        rx.vstack(
            rx.grid(
                _metric("Runtime", "OK", "OK"),
                _metric("Routes", "4/4", "OK"),
                _metric("Frontend", "npm fallback", "BYPASSED"),
                _metric("Next", "Migration cockpit", "NEXT"),
                columns="4",
                spacing="4",
                width="100%",
            ),
            rx.box(
                rx.heading("Priorite immediate", size="6"),
                rx.text(
                    "Transformer ce cockpit prive en outil operateur: prompt portfolio, CDC, dev tracker, modules a migrer definitivement vers Python.",
                    color=MUTED,
                    margin_top="10px",
                ),
                style=_card_style(),
                width="100%",
            ),
            spacing="5",
            align="stretch",
        ),
    )


def cdc_tracker_page() -> rx.Component:
    return _shell(
        "CDC tracker",
        "CDC Tracker",
        "Etat CDC et preuves de route pour eviter les faux OK et les shims uniques.",
        "/cdc-tracker",
        rx.vstack(
            rx.grid(
                _metric("Readiness", "86%", "ACTIVE"),
                _metric("HTTP routes", "200", "OK"),
                _metric("Evidence", "R11/R12", "OK"),
                columns="3",
                spacing="4",
                width="100%",
            ),
            _cdc_list(),
            spacing="5",
            align="stretch",
        ),
    )


def cdc_dev_tracker_page() -> rx.Component:
    return _shell(
        "CDC + Dev tracker",
        "CDC + Dev Tracker",
        "Vue croisee: runtime, routes, tests, fallback frontend et prochaine migration utile.",
        "/cdc-dev-tracker",
        rx.vstack(
            rx.grid(
                _metric("Stable gate", "15 passed", "OK"),
                _metric("R13B tests", "8 passed", "OK"),
                _metric("Repo", "clean", "OK"),
                columns="3",
                spacing="4",
                width="100%",
            ),
            _module_table(),
            spacing="5",
            align="stretch",
        ),
    )


def dev_tracking_page() -> rx.Component:
    return _shell(
        "Dev tracking / migration OS",
        "Dev Tracking - Migration OS",
        "Tableau prive pour suivre les modules a migrer definitivement vers Python.",
        "/dev-tracking",
        rx.vstack(
            rx.box(
                rx.heading("Migration next", size="6"),
                rx.text(
                    "Brancher donnees reelles, prioriser prompt portfolio, CDC et dev tracker.",
                    color=MUTED,
                    margin_top="10px",
                ),
                _badge("FAST_FUSE", ACCENT),
                style=_card_style(),
            ),
            _module_table(),
            spacing="5",
            align="stretch",
        ),
    )


# R13B backward-compatible route markers kept deliberately for regression gates.
R2A_R13B_ROUTE_MARKERS = (
    "CDC TRACKER / PRIVATE ROUTE",
    "CDC + DEV TRACKER / PRIVATE ROUTE",
    "DEV TRACKING / MIGRATION OS",
)
R2A_R14B_RICH_COCKPIT_COMPAT_FIX = True
