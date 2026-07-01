"""Static registry for the MVP QAIC global Reflex webapp shell."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from mvp_qaic_reflex_ui.qaic_bridge_operator_binding import (
    build_qaic_bridge_operator_card,
)

PROJECT = "MVP_QAIC"
SHELL_ID = "P_REFLEX_01_MVP_GLOBAL_WEBAPP_SHELL_FOUNDATION"
DOCS_CANONICAL_FORMAT = "markdown_md_with_emoji"
REFLEX_SCOPE = "global_mvp_qaic_webapp_shell"
PANEL_SCOPE = "specialized_gateway_placeholder"
GRADIO_SCOPE = "specialized_gateway_placeholder"
QAIC_SCOPE = "read_only_private_liaison_future"
QAIT_OUT_OF_SCOPE = True

REPO_ROOT = Path(__file__).resolve().parents[2]
CURRENT_CDC = Path(
    "docs/FINAL/WEBAPP_ARCHITECTURE_CDC/CURRENT/CDC_MVP_QAIC_WEBAPP_ARCHITECTURE_QAIC_LIAISON_v0_1_2.md"
)
ARCHITECTURE_ASSET = Path(
    "docs/FINAL/WEBAPP_ARCHITECTURE_CDC/CURRENT/CDC_MVP_QAIC_WEBAPP_ARCHITECTURE_SCHEMA_PRO_v0_1_2.png"
)
ZIP_PACK = Path(
    "docs/FINAL/WEBAPP_ARCHITECTURE_CDC/CURRENT/MVP_QAIC_WEBAPP_ARCHITECTURE_CDC_v0_1_2_PRO_PACK_REPAIRED.zip"
)

SAFETY_FLAGS = {
    "HUMAN_REVIEW_ONLY": True,
    "NO_AUTO_ORDER": True,
    "NO_AUTO_SIZING": True,
    "NO_BROKER_EXECUTION": True,
    "NO_REAL_ORDER": True,
    "NO_APPS_SCRIPT_EXECUTION": True,
    "NO_CLASP_PUSH": True,
    "NO_SHEET_WRITE": True,
    "NO_BIGQUERY_WRITE": True,
    "NO_PUBLIC_PUBLISH": True,
    "NO_QAIT": True,
}


@dataclass(frozen=True)
class PageSpec:
    page_id: str
    route: str
    title: str
    group: str
    purpose: str


PAGES = [
    PageSpec("home", "/", "🏠 Home / Mission Control", "global", "Global MVP QAIC cockpit shell."),
    PageSpec(
        "dev_tracking",
        "/dev-tracking",
        "🧭 Dev Tracking",
        "priority",
        "Local development and batch tracking.",
    ),
    PageSpec(
        "cdc_tracker",
        "/cdc-tracker",
        "📘 CDC Tracker",
        "priority",
        "Current CDC status, role and next action.",
    ),
    PageSpec(
        "architecture_web",
        "/architecture-web",
        "🧱 Architecture Web",
        "priority",
        "Architecture schema and MVP/QAIC liaison.",
    ),
    PageSpec(
        "docs_registry",
        "/docs-registry",
        "📚 Documentation Registry",
        "priority",
        "Canonical markdown documents and assets.",
    ),
    PageSpec(
        "architecture_registry",
        "/architecture-registry",
        "🗂️ Architecture & Registry",
        "priority",
        "Components, routes, registries and boundaries.",
    ),
    PageSpec(
        "lexique_knowledge",
        "/lexique-knowledge",
        "📚 Lexique & Knowledge",
        "global",
        "Lexique, search cockpit and knowledge base.",
    ),
    PageSpec(
        "methods_library",
        "/methods-library",
        "🧪 Methods Library",
        "global",
        "Methods, workflows and reusable decision methods.",
    ),
    PageSpec("prompt_lab", "/prompt-lab", "🧠 Prompt Lab", "global", "Prompt workflow gateway."),
    PageSpec(
        "gem_portfolio",
        "/gem-portfolio",
        "💎 GEM Portfolio",
        "global",
        "Portfolio image/text review gateway.",
    ),
    PageSpec(
        "responses_review",
        "/responses-review",
        "🧾 Responses Review",
        "global",
        "GPT/GEM response intake and human review.",
    ),
    PageSpec(
        "qaic_bridge",
        "/qaic-bridge",
        "🔗 QAIC Bridge",
        "bridge",
        "Read-only future liaison with private QAIC backend.",
    ),
    PageSpec(
        "panel_gateway",
        "/panel-gateway",
        "📊 Panel Analytics Gateway",
        "gateway",
        "Placeholder for specialized Panel analytics.",
    ),
    PageSpec(
        "gradio_gateway",
        "/gradio-gateway",
        "🖼️ Gradio Prompt Gateway",
        "gateway",
        "Placeholder for specialized Gradio prompt/image tools.",
    ),
    PageSpec(
        "settings_safety",
        "/settings-safety",
        "🛡️ Settings & Safety",
        "priority",
        "Safety flags and local-only policy.",
    ),
    PageSpec(
        "audit_archives",
        "/audit-archives",
        "🗄️ Audit & Archives",
        "priority",
        "Audit trails, archived packs and superseded docs.",
    ),
]

DOCS_REGISTRY = [
    {
        "doc_id": "webapp_architecture_cdc",
        "title": "🧱 CDC MVP QAIC WebApp Architecture QAIC Liaison v0.1.2",
        "path": CURRENT_CDC.as_posix(),
        "kind": "markdown",
        "status": "CURRENT",
    },
    {
        "doc_id": "webapp_architecture_schema_png",
        "title": "🗺️ MVP QAIC WebApp Architecture Schema PRO v0.1.2",
        "path": ARCHITECTURE_ASSET.as_posix(),
        "kind": "png",
        "status": "CURRENT",
    },
    {
        "doc_id": "webapp_architecture_pack",
        "title": "📦 MVP QAIC WebApp Architecture CDC Pack v0.1.2",
        "path": ZIP_PACK.as_posix(),
        "kind": "zip",
        "status": "CURRENT",
    },
]

QAIC_BRIDGE_OPERATOR_CARD = build_qaic_bridge_operator_card()


def list_routes() -> list[str]:
    return [page.route for page in PAGES]


def get_page(page_id: str) -> PageSpec:
    for page in PAGES:
        if page.page_id == page_id:
            return page
    raise KeyError(page_id)


def required_sections_present() -> bool:
    expected = {
        "home",
        "dev_tracking",
        "cdc_tracker",
        "architecture_web",
        "docs_registry",
        "architecture_registry",
        "lexique_knowledge",
        "methods_library",
        "prompt_lab",
        "gem_portfolio",
        "responses_review",
        "qaic_bridge",
        "panel_gateway",
        "gradio_gateway",
        "settings_safety",
        "audit_archives",
    }
    return expected.issubset({page.page_id for page in PAGES})


def resolve_repo_path(path: Path) -> Path:
    return REPO_ROOT / path


def architecture_asset_exists() -> bool:
    return resolve_repo_path(ARCHITECTURE_ASSET).exists()


def current_cdc_exists() -> bool:
    return resolve_repo_path(CURRENT_CDC).exists()


def no_live_action_policy() -> bool:
    return all(SAFETY_FLAGS.values())


def qaic_bridge_operator_card() -> dict[str, object]:
    return dict(QAIC_BRIDGE_OPERATOR_CARD)
