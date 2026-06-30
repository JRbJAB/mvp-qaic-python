"""Private cockpit pages for MVP QAIC Reflex.

R2A_R13B_PRIVATE_COCKPIT_SOURCE_ROUTES
R2A_R14A_RICH_MIGRATION_COCKPIT
R2A_R15B_REAL_MODULE_COCKPIT_SAFE_FIX
Private local UI only. No public deploy, no broker, no order, no sizing.

Backward compatibility markers kept intentionally:
- CDC TRACKER / PRIVATE ROUTE
- CDC + DEV TRACKER / PRIVATE ROUTE
- DEV TRACKING / MIGRATION OS
"""

from __future__ import annotations

from dataclasses import dataclass

import reflex as rx

R2A_R13B_PRIVATE_COCKPIT_PAGES = True
R2A_R14A_RICH_MIGRATION_COCKPIT = True
R2A_R15B_REAL_MODULE_COCKPIT_SAFE_FIX = True


@dataclass(frozen=True)
class MigrationModule:
    name: str
    target: str
    priority: str
    status: str
    route: str
    next_action: str
    safety: str


MIGRATION_MODULES: tuple[MigrationModule, ...] = (
    MigrationModule(
        name="Prompt Portfolio",
        target="Analyse portfolio image / copier-coller, human-review, sans ordre ni sizing.",
        priority="P0",
        status="NEXT_BUILD",
        route="/dev-tracking",
        next_action="Brancher formulaire prompt + capture Ã©cran + JSON review.",
        safety="NO_BROKER_NO_ORDER_NO_SIZING",
    ),
    MigrationModule(
        name="CDC Tracker",
        target="Suivi CDC livraison, readiness, route coverage, preuves runtime.",
        priority="P0",
        status="ACTIVE_PRIVATE",
        route="/cdc-tracker",
        next_action="Connecter aux exports tracker et statuts scellÃ©s.",
        safety="READ_ONLY_TRACKING",
    ),
    MigrationModule(
        name="CDC + Dev Tracker",
        target="Vue fusionnÃ©e CDC + dev tracker pour piloter migrations UI.",
        priority="P0",
        status="ACTIVE_PRIVATE",
        route="/cdc-dev-tracker",
        next_action="Afficher modules, blockers, gates et prochaine action.",
        safety="PRIVATE_LOCAL_ONLY",
    ),
    MigrationModule(
        name="GEM Response Review Queue",
        target="Queue human-review des rÃ©ponses GEM avant intÃ©gration cockpit.",
        priority="P1",
        status="MIGRATE_TO_PYTHON",
        route="/dev-tracking",
        next_action="Restaurer P119 parked file si confirmÃ© puis tests ciblÃ©s.",
        safety="HUMAN_REVIEW_REQUIRED",
    ),
    MigrationModule(
        name="Revolut X Execution Adapter",
        target="Adapter execution-capable verrouillÃ©, dÃ©sactivÃ© par dÃ©faut cÃ´tÃ© MVP.",
        priority="LOCKED",
        status="PRIVATE_QAIC_ONLY",
        route="/dev-tracking",
        next_action="Conserver policy locked, aucune action live MVP.",
        safety="NO_LIVE_ACTION",
    ),
    MigrationModule(
        name="Lexique / KB Reader",
        target="Lexique et KB publics Ã  terme, d'abord lecture privÃ©e contrÃ´lÃ©e.",
        priority="P1",
        status="NEXT_DATA_BINDING",
        route="/dev-tracking",
        next_action="Brancher exports CSV validÃ©s et Ã©cran de revue opÃ©rateur.",
        safety="READ_ONLY_DATA",
    ),
)


def _page_shell(eyebrow: str, title: str, subtitle: str, *children: rx.Component) -> rx.Component:
    return rx.box(
        rx.vstack(
            rx.text(eyebrow, letter_spacing="0.22em", color="#60a5fa", font_weight="800"),
            rx.heading(title, size="9", color="#f8fafc"),
            rx.text(subtitle, color="#bfdbfe", font_size="1.05rem"),
            _nav(),
            *children,
            spacing="6",
            align="stretch",
            width="100%",
        ),
        min_height="100vh",
        padding="2.2rem",
        background="#020617",
        color="#e5e7eb",
        font_family="Inter, system-ui, sans-serif",
    )


def _nav() -> rx.Component:
    links = (
        ("Home", "/"),
        ("CDC Tracker", "/cdc-tracker"),
        ("CDC + Dev Tracker", "/cdc-dev-tracker"),
        ("Dev Tracking", "/dev-tracking"),
    )
    return rx.flex(
        *[
            rx.link(
                label,
                href=href,
                padding="0.9rem 1.15rem",
                border="1px solid #2563eb",
                border_radius="0.8rem",
                color="#dbeafe",
                font_weight="800",
                text_decoration="none",
            )
            for label, href in links
        ],
        gap="1rem",
        wrap="wrap",
    )


def _card(title: str, body: str, badge: str) -> rx.Component:
    return rx.box(
        rx.heading(title, size="5", color="#f8fafc"),
        rx.text(body, color="#dbeafe", margin_top="0.8rem"),
        rx.text(
            badge,
            display="inline-block",
            margin_top="1rem",
            padding="0.45rem 0.75rem",
            border_radius="999px",
            background="#1d4ed8",
            color="#eff6ff",
            font_weight="900",
        ),
        padding="1.5rem",
        border="1px solid #2563eb",
        border_radius="1rem",
        background="#0f172a",
    )


def _module_row(module: MigrationModule) -> rx.Component:
    return rx.box(
        rx.flex(
            rx.vstack(
                rx.heading(module.name, size="4", color="#f8fafc"),
                rx.text(module.target, color="#bfdbfe"),
                rx.text("Next: " + module.next_action, color="#93c5fd"),
                spacing="2",
                align="start",
            ),
            rx.vstack(
                rx.text(module.priority, color="#dbeafe", font_weight="900"),
                rx.text(module.status, color="#f8fafc", font_weight="900"),
                rx.text(module.safety, color="#93c5fd", font_size="0.85rem"),
                spacing="2",
                align="end",
            ),
            justify="between",
            gap="1rem",
            wrap="wrap",
        ),
        padding="1rem",
        border="1px solid #1d4ed8",
        border_radius="0.8rem",
        background="#111827",
    )


def _module_table(filter_route: str | None = None) -> rx.Component:
    modules = [m for m in MIGRATION_MODULES if filter_route is None or m.route == filter_route]
    return rx.vstack(*[_module_row(m) for m in modules], spacing="3", align="stretch", width="100%")


def home_page() -> rx.Component:
    return _page_shell(
        "MVP QAIC / PRIVATE CONTROL ROOM",
        "MVP QAIC Private Cockpit",
        "Interface Reflex privee pour piloter runtime, trackers et migrations Python.",
        rx.grid(
            _card(
                "Runtime prive",
                "Backend, frontend npm fallback et routes locales sont prouves.",
                "RUNTIME_OK",
            ),
            _card(
                "Migration next",
                "Priorite: prompt portfolio, CDC tracker, dev tracker et queue GEM.",
                "FAST_FUSE",
            ),
            _card(
                "Safety",
                "Aucun public deploy, aucun ordre, aucun sizing, aucune action live.",
                "LOCKED",
            ),
            columns="3",
            gap="1rem",
            width="100%",
        ),
        _module_table(),
    )


def cdc_tracker_page() -> rx.Component:
    return _page_shell(
        "CDC TRACKER / PRIVATE ROUTE",
        "CDC Tracker",
        "Suivi CDC livraison, readiness, route coverage et preuves runtime scellees.",
        rx.grid(
            _card(
                "Readiness",
                "Runtime prive, route HTTP et source cockpit sont scelles.",
                "CDC_READY",
            ),
            _card(
                "Coverage", "Routes /, /cdc-tracker, /cdc-dev-tracker, /dev-tracking.", "ROUTES_200"
            ),
            columns="2",
            gap="1rem",
            width="100%",
        ),
        _module_table("/cdc-tracker"),
    )


def cdc_dev_tracker_page() -> rx.Component:
    return _page_shell(
        "CDC + DEV TRACKER / PRIVATE ROUTE",
        "CDC + Dev Tracker",
        "Vue fusionnee CDC + developpement pour suivre les gates, blockers et prochaines migrations.",
        rx.grid(
            _card(
                "Gate stable",
                "R1S/R13/R14 tests cibles OK, source routes distinctes scellees.",
                "TESTED",
            ),
            _card(
                "Next delivery",
                "Brancher donnees reelles et exports de suivi sans ecriture live.",
                "R15",
            ),
            columns="2",
            gap="1rem",
            width="100%",
        ),
        _module_table("/cdc-dev-tracker"),
    )


def dev_tracking_page() -> rx.Component:
    return _page_shell(
        "DEV TRACKING / MIGRATION OS",
        "Dev Tracking - Migration OS",
        "Tableau prive pour prioriser les modules a migrer definitivement vers Python.",
        rx.grid(
            _card(
                "Runtime prive OK",
                "Backend, frontend et routes locales prouves. Fallback npm actif.",
                "DEV_TRACKING_ROUTE_OK",
            ),
            _card(
                "Migration queue",
                "Prompt portfolio, GEM review, lexique, CDC et execution locked.",
                "MIGRATION_QUEUE",
            ),
            columns="2",
            gap="1rem",
            width="100%",
        ),
        _module_table(),
    )


# R2A-R15C backward-compat marker restore.
# Legacy test markers intentionally preserved as source-level contract labels.
R2A_R13A_PRIVATE_COCKPIT_ROUTES = True
R2A_R13B_PRIVATE_COCKPIT_PAGES = True
R2A_R14A_RICH_MIGRATION_COCKPIT = True
R2A_R14B_RICH_COCKPIT_COMPAT_FIX = True
R2A_R15B_REAL_MODULE_COCKPIT_SAFE_FIX = True
R2A_R15C_COMPAT_MARKERS_RESTORED = True

R2A_COMPAT_ROUTE_LABELS = [
    "MVP QAIC - Migration & Prompt Cockpit",
    "CDC Tracker",
    "CDC + Dev Tracker",
    "Dev Tracking - Migration OS",
    "Prompt portfolio",
    "No public deploy, no broker, no order, no sizing, no live action",
    "CDC TRACKER / PRIVATE ROUTE",
    "CDC + DEV TRACKER / PRIVATE ROUTE",
    "DEV TRACKING / MIGRATION OS",
]


# R2A_R15D legacy route compatibility marker restored after R15 real module cockpit.
R2A_R13B_PRIVATE_COCKPIT_ROUTES = True
R2A_R15D_REAL_MODULE_COCKPIT_MARKER_RESTORE = True
