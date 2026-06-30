from __future__ import annotations

import reflex as rx

RESTORED_RENDER_MARKER = "RESTORED_REFLEX_INITIAL_RENDER_R16F2G1"
ROUTE_ITEMS = [('/', 'Mission Control'), ('/mission-control', 'Mission Control'), ('/dev-tracking', 'Dev Tracking'), ('/cdc-tracker', 'Cdc Tracker'), ('/cdc-dev-tracker', 'Cdc Dev Tracker'), ('/architecture-web', 'Architecture Web'), ('/architecture-web/schema', 'Architecture Web / Schema'), ('/sitemap', 'Sitemap'), ('/documentation-registry', 'Documentation Registry'), ('/architecture-registry', 'Architecture Registry'), ('/admin', 'Admin'), ('/admin/runtime', 'Admin / Runtime'), ('/admin/theme', 'Admin / Theme'), ('/admin/safety', 'Admin / Safety'), ('/admin/routes', 'Admin / Routes'), ('/admin/data-binding', 'Admin / Data Binding'), ('/prompt-lab', 'Prompt Lab'), ('/gem-portfolio', 'Gem Portfolio'), ('/qaic-bridge', 'Qaic Bridge'), ('/lexique-knowledge', 'Lexique Knowledge'), ('/settings-safety', 'Settings Safety'), ('/migration/global', 'Migration / Global'), ('/migration/decisions', 'Migration / Decisions'), ('/trackers/auto-update', 'Trackers / Auto Update'), ('/architecture', 'Architecture'), ('/audit-runs', 'Audit Runs'), ('/base-python', 'Base Python'), ('/configuration', 'Configuration'), ('/documents', 'Documents'), ('/google-sheets', 'Google Sheets'), ('/prompt', 'Prompt'), ('/responses', 'Responses'), ('/workflow', 'Workflow')]


def _nav_item(route: str, label: str):
    return rx.link(
        rx.box(
            rx.text(label, font_size="13px", font_weight="600"),
            rx.text(route, font_size="10px", color="#8aa0c7"),
            padding="10px 12px",
            border_radius="12px",
            border="1px solid rgba(148,163,184,.18)",
            background="rgba(15,23,42,.72)",
            _hover={"background": "rgba(37,99,235,.22)", "border_color": "rgba(96,165,250,.55)"},
            width="100%",
        ),
        href=route,
        text_decoration="none",
        width="100%",
    )


def _metric(label: str, value: str, detail: str):
    return rx.box(
        rx.text(label, color="#93a4c7", font_size="12px", font_weight="700"),
        rx.heading(value, size="6", color="#f8fafc"),
        rx.text(detail, color="#a8b7d6", font_size="12px"),
        padding="16px",
        border="1px solid rgba(148,163,184,.18)",
        border_radius="18px",
        background="linear-gradient(135deg, rgba(15,23,42,.96), rgba(30,41,59,.82))",
        box_shadow="0 14px 40px rgba(0,0,0,.24)",
        min_width="180px",
        flex="1",
    )


def _panel(title: str, body: str, accent: str):
    return rx.box(
        rx.hstack(
            rx.box(width="10px", height="10px", border_radius="99px", background=accent),
            rx.heading(title, size="4", color="#f8fafc"),
            align="center",
            spacing="3",
        ),
        rx.text(body, color="#b7c5df", font_size="14px", margin_top="10px", line_height="1.6"),
        padding="18px",
        border="1px solid rgba(148,163,184,.18)",
        border_radius="20px",
        background="rgba(15,23,42,.72)",
        box_shadow="0 12px 34px rgba(0,0,0,.22)",
    )


def make_restored_initial_route_page(route: str = "/", title: str | None = None):
    page_title = title or route
    nav = rx.vstack(
        rx.box(
            rx.text("JRb Trading OS", color="#93c5fd", font_size="12px", font_weight="800"),
            rx.heading("MVP QAIC", size="6", color="#f8fafc"),
            rx.text("Reflex restored runtime", color="#94a3b8", font_size="12px"),
            margin_bottom="16px",
        ),
        *[_nav_item(r, lbl) for r, lbl in ROUTE_ITEMS[:24]],
        spacing="2",
        align="stretch",
        width="100%",
    )
    return rx.box(
        rx.hstack(
            rx.box(
                nav,
                width="292px",
                min_width="292px",
                min_height="100vh",
                padding="22px",
                background="linear-gradient(180deg, #050816 0%, #0f172a 55%, #111827 100%)",
                border_right="1px solid rgba(148,163,184,.18)",
                overflow_y="auto",
                position="sticky",
                top="0",
            ),
            rx.box(
                rx.vstack(
                    rx.box(
                        rx.text(RESTORED_RENDER_MARKER, color="#60a5fa", font_size="11px", font_weight="800"),
                        rx.heading(page_title, size="8", color="#f8fafc", margin_top="8px"),
                        rx.text("Route active: " + route, color="#a8b7d6", font_size="14px", margin_top="6px"),
                        padding="22px",
                        border="1px solid rgba(96,165,250,.28)",
                        border_radius="24px",
                        background="radial-gradient(circle at top left, rgba(37,99,235,.34), rgba(15,23,42,.82) 42%, rgba(2,6,23,.96))",
                        box_shadow="0 22px 70px rgba(0,0,0,.33)",
                        width="100%",
                    ),
                    rx.hstack(
                        _metric("Runtime", "Docker pinned", "Python 3.12 / Node 22 / Reflex 0.9.6.post1"),
                        _metric("Routes", "Critical gate", "Mission Control, CDC, Prompt Lab, GEM Portfolio"),
                        _metric("Safety", "Human review", "No broker, no order, no sizing, no public deploy"),
                        spacing="4",
                        width="100%",
                    ),
                    rx.grid(
                        _panel("Mission Control", "Cockpit central restauré pour reprendre le pilotage MVP QAIC avec navigation verticale, statuts et preuves runtime.", "#38bdf8"),
                        _panel("CDC / Dev Tracker", "Suivi des contrats, routes critiques, trackers et décisions de migration dans le même shell Reflex.", "#22c55e"),
                        _panel("Prompt Lab", "Espace de travail pour prompts GEM portfolio, historique et réponses en human-review.", "#a78bfa"),
                        _panel("GEM Portfolio", "Module opérateur privé, sans exécution broker, sans sizing, sans action live.", "#f59e0b"),
                        columns="2",
                        spacing="4",
                        width="100%",
                    ),
                    rx.box(
                        rx.heading("Routes disponibles", size="4", color="#f8fafc"),
                        rx.text(", ".join([r for r, _ in ROUTE_ITEMS]), color="#b7c5df", font_size="12px", margin_top="8px"),
                        padding="16px",
                        border="1px solid rgba(148,163,184,.16)",
                        border_radius="18px",
                        background="rgba(15,23,42,.58)",
                        width="100%",
                    ),
                    spacing="5",
                    align="stretch",
                    width="100%",
                ),
                flex="1",
                padding="28px",
                min_height="100vh",
                background="linear-gradient(135deg, #020617 0%, #0b1220 46%, #111827 100%)",
            ),
            align="start",
            spacing="0",
            width="100%",
        ),
        min_height="100vh",
        background="#020617",
        color="#e5e7eb",
        font_family="Inter, Segoe UI, Arial, sans-serif",
    )
