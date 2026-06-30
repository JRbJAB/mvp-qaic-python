from __future__ import annotations

import reflex as rx

R2A_R13A_PRIVATE_COCKPIT_ROUTES = True
R2A_R13B_PRIVATE_COCKPIT_ROUTES = True

ACCENT = "#60a5fa"
BG = "#020617"
CARD = "#0f172a"
BORDER = "#2563eb"
TEXT = "#e5e7eb"
MUTED = "#93a4c7"


def _pill(label: str) -> rx.Component:
    return rx.box(
        label,
        padding="0.45rem 0.8rem",
        border_radius="999px",
        background="#1d4ed8",
        color="#eff6ff",
        font_weight="800",
        border=f"1px solid {BORDER}",
    )


def _card(title: str, body: str, status: str, pct: int) -> rx.Component:
    return rx.box(
        rx.vstack(
            rx.heading(title, size="5", color=TEXT),
            rx.box(
                rx.box(
                    width=f"{pct}%",
                    height="0.55rem",
                    background="#3b82f6",
                    border_radius="999px",
                ),
                width="100%",
                background="#1e293b",
                border_radius="999px",
                overflow="hidden",
            ),
            rx.text(body, color=MUTED, font_size="1rem", line_height="1.45"),
            _pill(status),
            align="start",
            spacing="4",
        ),
        padding="1.35rem",
        border=f"1px solid {BORDER}",
        border_radius="1.15rem",
        background=CARD,
        min_height="13rem",
    )


def _nav() -> rx.Component:
    return rx.hstack(
        rx.link("Home", href="/", color="#bfdbfe", font_weight="800"),
        rx.link("CDC Tracker", href="/cdc-tracker", color="#bfdbfe", font_weight="800"),
        rx.link("CDC + Dev Tracker", href="/cdc-dev-tracker", color="#bfdbfe", font_weight="800"),
        rx.link("Dev Tracking", href="/dev-tracking", color="#bfdbfe", font_weight="800"),
        spacing="5",
        wrap="wrap",
    )


def _shell(
    kicker: str,
    title: str,
    subtitle: str,
    card_a: rx.Component,
    card_b: rx.Component,
    card_c: rx.Component,
    card_d: rx.Component,
) -> rx.Component:
    return rx.box(
        rx.vstack(
            rx.text(kicker, color=ACCENT, font_weight="900", letter_spacing="0.16em"),
            rx.heading(title, size="8", color=TEXT),
            rx.text(subtitle, color=MUTED, font_size="1.05rem", max_width="78rem"),
            _nav(),
            rx.grid(card_a, card_b, card_c, card_d, columns="2", spacing="5", width="100%"),
            align="start",
            spacing="5",
            width="100%",
        ),
        min_height="100vh",
        background=BG,
        padding="2.2rem",
        color=TEXT,
        font_family="Inter, system-ui, sans-serif",
    )


def home_page() -> rx.Component:
    return _shell(
        "MVP QAIC / PRIVATE REFLEX COCKPIT",
        "MVP QAIC - Migration & Prompt Cockpit",
        "Interface privee locale pour piloter les migrations Python, les trackers CDC/Dev et les prochains modules prompt/portfolio. Runtime local uniquement.",
        _card(
            "Runtime prive",
            "Backend et frontend locaux valides. Fallback npm actif tant que Bun Windows bloque.",
            "RUNTIME_OK",
            100,
        ),
        _card(
            "Priorite court terme",
            "Rendre le cockpit utile pour suivre les migrations et preparer le module prompt portfolio.",
            "HUMAN_REVIEW_ONLY",
            72,
        ),
        _card(
            "Securite",
            "No public deploy, no broker, no order, no sizing, no live action.",
            "SAFETY_OK",
            100,
        ),
        _card(
            "Next",
            "Brancher les donnees reelles de migration et reduire les shims visuels generes.",
            "NEXT_R14",
            45,
        ),
    )


def cdc_tracker_page() -> rx.Component:
    return _shell(
        "CDC TRACKER / PRIVATE ROUTE",
        "CDC Tracker",
        "Vue dediee au suivi CDC : readiness, couverture routes, artefacts et points bloquants a transformer en migration actionnable.",
        _card(
            "CDC readiness",
            "Route dediee distincte validee. Prochaine etape : donnees reelles au lieu de smoke values.",
            "CDC_ROUTE_OK",
            86,
        ),
        _card(
            "Contrats",
            "docs/FINAL reste source canonique. Les residus legacy ne pilotent pas la suite.",
            "DOCS_FINAL_OK",
            100,
        ),
        _card(
            "Risques",
            "Bun Windows reste contourne par npm fallback prive, sans impact source metier.",
            "BUN_FALLBACK",
            62,
        ),
        _card("Action", "Identifier exports/CSV a connecter au cockpit CDC.", "MIGRATION_NEXT", 50),
    )


def cdc_dev_tracker_page() -> rx.Component:
    return _shell(
        "CDC + DEV TRACKER / PRIVATE ROUTE",
        "CDC + Dev Tracker",
        "Cockpit combine CDC et developpement pour prioriser les migrations, suivre les gates et afficher le statut operateur.",
        _card(
            "Dev readiness",
            "Stable gate R1K/R1M/R1P/R1Q/R1R/R1S valide avant runtime.",
            "DEV_GATE_OK",
            74,
        ),
        _card(
            "Runtime evidence",
            "Backend-only, full runtime, route HTTP validation et keepalive prives prouves.",
            "EVIDENCE_OK",
            100,
        ),
        _card(
            "A migrer",
            "Prompt portfolio, module image/capture, matrices migration, CDC exports.",
            "QUEUE",
            38,
        ),
        _card(
            "Decision",
            "On passe des shims au vrai cockpit lisible par lots R14/R15.",
            "FAST_FUSE",
            55,
        ),
    )


def dev_tracking_page() -> rx.Component:
    return _shell(
        "DEV TRACKING / MIGRATION OS",
        "Dev Tracking - Migration OS",
        "Tableau prive pour suivre les modules a migrer definitivement vers Python et organiser le prochain Batch Fast & Fuse.",
        _card(
            "Prompt portfolio",
            "Priorite MVP : analyse capture/coller portefeuille, human review, sans ordre ni sizing.",
            "PRIORITY_1",
            70,
        ),
        _card(
            "Migration modules",
            "Lister source Apps Script / Sheets / CSV puis decider KEEP, MIGRATE, ARCHIVE_REVIEW.",
            "PRIORITY_2",
            60,
        ),
        _card(
            "UI cockpit",
            "Remplacer les placeholders par tableaux reels, filtres, badges et preuves.",
            "PRIORITY_3",
            50,
        ),
        _card(
            "Seal",
            "Apres validation visuelle, commit/tag/push et memo de reprise final.",
            "SEAL_NEXT",
            40,
        ),
    )
