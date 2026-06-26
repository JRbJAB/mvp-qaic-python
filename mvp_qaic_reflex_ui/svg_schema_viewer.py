"""Responsive SVG schema viewer for the private Reflex WebApp."""

from __future__ import annotations

from typing import Any

try:  # Reflex is available in the app runtime; tests can still import constants without rendering.
    import reflex as rx
except Exception:  # noqa: BLE001
    rx = None  # type: ignore[assignment]

SCHEMA_ROUTE = "/architecture-web/schema"
ARCHITECTURE_ROUTE = "/architecture-web"
SVG_ASSET_CANDIDATES: tuple[str, ...] = (
    "web_architecture_sitemap.svg",
    "MVPQAIC_WEB_ARCHITECTURE_SITEMAP.svg",
    "architecture_web_sitemap.svg",
    "architecture-web-sitemap.svg",
    "schema_architecture_web.svg",
)
SVG_FIT_STYLE: dict[str, str] = {
    "width": "100%",
    "max_width": "100%",
    "max_height": "520px",
    "object_fit": "contain",
}
SVG_LARGE_FIT_STYLE: dict[str, str] = {
    "width": "100%",
    "max_width": "100%",
    "max_height": "calc(100vh - 180px)",
    "object_fit": "contain",
}


def schema_svg_asset_src(primary: str | None = None) -> str:
    asset = primary or SVG_ASSET_CANDIDATES[0]
    return asset if asset.startswith("/") else f"/{asset}"


def _require_reflex() -> Any:
    if rx is None:
        raise RuntimeError("reflex is required to render this page")
    return rx


def schema_viewer_link_card() -> Any:
    reflex = _require_reflex()
    return reflex.card(
        reflex.vstack(
            reflex.heading("Schéma architecture web", size="4"),
            reflex.text(
                "Le SVG est contraint à la largeur disponible. "
                "La vue grand format reste locale et privée.",
                size="2",
            ),
            reflex.hstack(
                reflex.link(reflex.button("Voir le schéma en grand"), href=SCHEMA_ROUTE),
                reflex.link(
                    reflex.button("Ouvrir SVG brut"),
                    href=schema_svg_asset_src(),
                    is_external=True,
                ),
                spacing="3",
                flex_wrap="wrap",
            ),
            spacing="3",
        ),
        width="100%",
    )


def schema_large_page() -> Any:
    reflex = _require_reflex()
    src = schema_svg_asset_src()
    return reflex.container(
        reflex.vstack(
            reflex.heading("Architecture Web — Schéma grand format", size="6"),
            reflex.text(
                "Preview locale privée. Aucun déploiement public, "
                "aucune action live, aucun ordre, aucun sizing.",
                size="2",
            ),
            reflex.hstack(
                reflex.link(reflex.button("Retour architecture web"), href=ARCHITECTURE_ROUTE),
                reflex.link(reflex.button("Ouvrir SVG brut"), href=src, is_external=True),
                spacing="3",
                flex_wrap="wrap",
            ),
            reflex.box(
                reflex.image(
                    src=src,
                    alt="MVP QAIC Web Architecture Sitemap",
                    width="100%",
                    max_width="100%",
                    max_height="calc(100vh - 180px)",
                    object_fit="contain",
                ),
                width="100%",
                overflow="auto",
                border="1px solid var(--gray-a5)",
                border_radius="12px",
                padding="1rem",
            ),
            spacing="4",
            width="100%",
        ),
        size="4",
        padding_y="1.5rem",
    )
