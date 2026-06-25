"""Reflex app entrypoint for MVP QAIC global shell.

The module imports without requiring Reflex to be installed.
When Reflex is available, `app` is built as a local-only shell.
"""

from __future__ import annotations

from .registry import ARCHITECTURE_ASSET, DOCS_REGISTRY, PAGES, SAFETY_FLAGS

try:
    import reflex as rx  # type: ignore
except Exception:  # pragma: no cover - depends on local environment
    rx = None  # type: ignore

REFLEX_AVAILABLE = rx is not None
REFLEX_BUILD_ERROR = ""


def page_registry_payload() -> dict[str, object]:
    return {
        "title": "MVP QAIC Global WebApp Shell",
        "route_count": len(PAGES),
        "page_count": len(PAGES),
        "architecture_asset": ARCHITECTURE_ASSET.as_posix(),
        "docs": DOCS_REGISTRY,
        "safety_flags": SAFETY_FLAGS,
        "pages": [
            {
                "page_id": page.page_id,
                "route": page.route,
                "title": page.title,
                "group": page.group,
                "purpose": page.purpose,
            }
            for page in PAGES
        ],
    }


def index():
    if rx is None:
        return page_registry_payload()
    return rx.vstack(
        rx.heading("🛠️ MVP QAIC — Global WebApp Shell", size="7"),
        rx.text("Reflex shell foundation — local, read-only, human-review only."),
        rx.text(f"Architecture asset: {ARCHITECTURE_ASSET.as_posix()}"),
        rx.divider(),
        rx.foreach([p.title for p in PAGES], lambda title: rx.text(title)),
        spacing="4",
        align="start",
        padding="2rem",
    )


def build_app():
    if rx is None:
        return None
    local_app = rx.App()
    local_app.add_page(index, route="/", title="MVP QAIC")
    return local_app


try:
    app = build_app()
except Exception as exc:  # pragma: no cover - defensive for Reflex API drift
    app = None
    REFLEX_BUILD_ERROR = repr(exc)
