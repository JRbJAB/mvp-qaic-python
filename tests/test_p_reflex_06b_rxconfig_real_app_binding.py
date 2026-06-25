import importlib

import reflex as rx

import rxconfig
from mvp_qaic_reflex_ui.mvp_qaic_reflex_ui import (
    app,
    gem_portfolio,
    index,
    lexique_knowledge,
    qaic_bridge,
)


def test_rxconfig_exists_and_targets_real_app():
    assert rxconfig.config.app_name == "mvp_qaic_reflex_ui"


def test_reflex_import_and_app_object_exist():
    assert rx is not None
    assert app is not None


def test_reflex_pages_return_components():
    assert index() is not None
    assert lexique_knowledge() is not None
    assert gem_portfolio() is not None
    assert qaic_bridge() is not None


def test_reflex_app_module_is_importable_by_name():
    module = importlib.import_module("mvp_qaic_reflex_ui.mvp_qaic_reflex_ui")
    assert hasattr(module, "app")
