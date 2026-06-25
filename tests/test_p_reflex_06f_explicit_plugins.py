import rxconfig


def test_rxconfig_targets_real_reflex_app():
    assert rxconfig.config.app_name == "mvp_qaic_reflex_ui"


def test_sitemap_plugin_is_explicitly_enabled():
    assert "SitemapPlugin" in rxconfig.EXPLICIT_REFLEX_PLUGIN_NAMES
    plugin_names = {plugin.__class__.__name__ for plugin in rxconfig.config.plugins}
    assert "SitemapPlugin" in plugin_names


def test_radix_themes_plugin_is_explicitly_enabled():
    assert "RadixThemesPlugin" in rxconfig.EXPLICIT_REFLEX_PLUGIN_NAMES
    plugin_names = {plugin.__class__.__name__ for plugin in rxconfig.config.plugins}
    assert "RadixThemesPlugin" in plugin_names
