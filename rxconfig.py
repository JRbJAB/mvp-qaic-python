import reflex as rx
from reflex_base.plugins.sitemap import SitemapPlugin

EXPLICIT_REFLEX_PLUGIN_NAMES = (
    "SitemapPlugin",
    "RadixThemesPlugin",
)

config = rx.Config(
    app_name="mvp_qaic_reflex_ui",
    plugins=[
        SitemapPlugin(),
        rx.plugins.RadixThemesPlugin(),
    ],
)
