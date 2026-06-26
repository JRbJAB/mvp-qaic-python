from __future__ import annotations

from mvp_qaic_reflex_ui.svg_schema_viewer import (
    SCHEMA_ROUTE,
    SVG_ASSET_CANDIDATES,
    SVG_FIT_STYLE,
    SVG_LARGE_FIT_STYLE,
    schema_svg_asset_src,
)


def test_svg_schema_viewer_contract() -> None:
    assert SCHEMA_ROUTE == "/architecture-web/schema"
    assert SVG_ASSET_CANDIDATES
    assert schema_svg_asset_src().startswith("/")
    assert SVG_FIT_STYLE["width"] == "100%"
    assert SVG_FIT_STYLE["object_fit"] == "contain"
    assert SVG_LARGE_FIT_STYLE["object_fit"] == "contain"
