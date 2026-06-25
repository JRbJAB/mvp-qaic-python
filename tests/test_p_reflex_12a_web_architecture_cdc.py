import json
from pathlib import Path

from mvp_qaic_reflex_ui import mvp_qaic_reflex_ui as ui
from mvp_qaic_reflex_ui.pages_landing import architecture_web, web_sitemap
from mvp_qaic_reflex_ui.web_architecture_cdc import (
    CDC_TRACKER_ROWS,
    COCKPIT_REGISTRY_ROWS,
    SITEMAP_NODES,
    WEB_ARCHITECTURE_DOCS,
    WEB_ARCHITECTURE_SCHEMA_ASSET,
    architecture_docs_panel,
    architecture_schema_panel,
    architecture_summary_metrics,
    architecture_web_cdc_body,
    cdc_progress_average,
    cdc_tracker_table,
    cockpit_registry_grid,
    sitemap_page_body,
)


def test_p12a_architecture_source_artifacts_exist():
    assert Path("docs/WEB_ARCHITECTURE_CDC.md").exists()
    assert Path("docs/WEB_ARCHITECTURE_SITEMAP.json").exists()
    assert Path("docs/WEB_ARCHITECTURE_SCHEMA.svg").exists()
    assert Path("assets/mvp_qaic_web_architecture_schema.svg").exists()


def test_p12a_sitemap_json_contract_is_stable():
    payload = json.loads(Path("docs/WEB_ARCHITECTURE_SITEMAP.json").read_text(encoding="utf-8"))

    assert payload["schema_version"] == "web_architecture_sitemap.v1"
    assert payload["base"] == "P11D_BROWSER_LOCALSTORAGE_THEME_PERSISTENCE"
    assert payload["reflex_sitemap_plugin"] == "EXPLICIT_ENABLED"
    assert payload["architecture_web_route"] == "/architecture-web"
    assert payload["sitemap_route"] == "/sitemap"
    assert payload["safety"]["public_deploy"] is False
    assert len(payload["nodes"]) >= 17
    assert len(payload["cdc_rows"]) >= 15
    assert len(payload["cockpits"]) >= 8


def test_p12a_cdc_rows_have_routes_progress_and_cockpits():
    assert len(CDC_TRACKER_ROWS) >= 15
    assert len(SITEMAP_NODES) >= 17
    assert len(COCKPIT_REGISTRY_ROWS) >= 8
    assert WEB_ARCHITECTURE_SCHEMA_ASSET == "/mvp_qaic_web_architecture_schema.svg"

    for row in CDC_TRACKER_ROWS:
        assert row["route"].startswith("/")
        assert row["cockpit"]
        assert 0 <= row["progress_percent"] <= 100


def test_p12a_average_and_metrics_are_valid():
    average = cdc_progress_average()
    metrics = architecture_summary_metrics()

    assert average > 0
    assert average <= 100
    assert len(metrics) == 4
    assert any(metric["label"] == "CDC progress" for metric in metrics)


def test_p12a_components_render():
    assert architecture_schema_panel() is not None
    assert cdc_tracker_table() is not None
    assert cockpit_registry_grid() is not None
    assert architecture_docs_panel() is not None
    assert architecture_web_cdc_body() is not None
    assert sitemap_page_body() is not None
    assert architecture_web() is not None
    assert web_sitemap() is not None


def test_p12a_reflex_routes_are_registered_in_app_source():
    source = Path("mvp_qaic_reflex_ui/mvp_qaic_reflex_ui.py").read_text(encoding="utf-8")

    assert 'route="/architecture-web"' in source
    assert 'route="/sitemap"' in source
    assert "web_sitemap" in source
    assert ui.architecture_web() is not None
    assert ui.web_sitemap() is not None


def test_p12a_sitemap_plugin_remains_enabled():
    rxconfig = Path("rxconfig.py").read_text(encoding="utf-8")

    assert "SitemapPlugin" in rxconfig
    assert "RadixThemesPlugin" in rxconfig


def test_p12a_docs_contract_mentions_cdc_and_cockpits():
    cdc_doc = Path(WEB_ARCHITECTURE_DOCS["cdc"]).read_text(encoding="utf-8")

    assert "Web Architecture CDC" in cdc_doc
    assert "CDC tracker" in cdc_doc
    assert "Essential cockpits" in cdc_doc
    assert "/architecture-web" in cdc_doc
    assert "/sitemap" in cdc_doc
