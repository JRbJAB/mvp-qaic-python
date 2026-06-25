from __future__ import annotations

from dataclasses import asdict, dataclass


@dataclass(frozen=True)
class AdminNavItem:
    id: str
    label: str
    route: str
    icon: str
    group: str
    purpose: str
    safety_level: str = "LOCAL_REVIEW_ONLY"


ADMIN_NAVIGATION: tuple[AdminNavItem, ...] = (
    AdminNavItem(
        id="dashboard",
        label="Dashboard",
        route="/",
        icon="dashboard",
        group="core",
        purpose="Vue synthèse du cockpit privé MVP QAIC.",
    ),
    AdminNavItem(
        id="base_python",
        label="Base Python",
        route="/base-python",
        icon="terminal",
        group="foundation",
        purpose="Accès visuel aux modules Python, noyau, registres et état repo.",
    ),
    AdminNavItem(
        id="google_sheets",
        label="Google Sheets",
        route="/google-sheets",
        icon="table_view",
        group="foundation",
        purpose="Vue cockpit/export Google Sheets, sans écriture live par défaut.",
    ),
    AdminNavItem(
        id="prompt",
        label="Prompt Cockpit",
        route="/prompt",
        icon="psychology",
        group="workflow",
        purpose="Prompts, templates, historique, qualité et review humaine.",
    ),
    AdminNavItem(
        id="responses",
        label="Réponses GEM",
        route="/responses",
        icon="rate_review",
        group="workflow",
        purpose="Brouillons, réponses GEM, review humaine et exports locaux.",
    ),
    AdminNavItem(
        id="documents",
        label="Documents",
        route="/documents",
        icon="folder",
        group="knowledge",
        purpose="Registry documentaire, méthodes, lexique et sources MVP.",
    ),
    AdminNavItem(
        id="architecture",
        label="Architecture",
        route="/architecture",
        icon="account_tree",
        group="governance",
        purpose="Schéma SVG, arborescence, routes, modules et frontières MVP/QAIC.",
    ),
    AdminNavItem(
        id="configuration",
        label="Configuration",
        route="/configuration",
        icon="settings",
        group="governance",
        purpose="Paths, modes, flags safety et paramètres UI.",
    ),
    AdminNavItem(
        id="audit_runs",
        label="Audit / Runs",
        route="/audit-runs",
        icon="fact_check",
        group="governance",
        purpose="Gates, tests, tags, logs et preuves de validation.",
    ),
)


def get_admin_navigation() -> list[dict[str, str]]:
    return [asdict(item) for item in ADMIN_NAVIGATION]


def get_navigation_groups() -> dict[str, list[dict[str, str]]]:
    groups: dict[str, list[dict[str, str]]] = {}
    for item in get_admin_navigation():
        groups.setdefault(item["group"], []).append(item)
    return groups


def get_route_index() -> dict[str, dict[str, str]]:
    return {item["route"]: item for item in get_admin_navigation()}
