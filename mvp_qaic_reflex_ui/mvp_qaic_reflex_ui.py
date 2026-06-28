from mvp_qaic_reflex_ui.cdc_dev_tracker_reflex_page import cdc_dev_tracker_reflex_page
"""MVP QAIC local private Reflex UI."""

from __future__ import annotations

import reflex as rx

from .pages_admin import (
    admin_center,
    admin_data_binding,
    admin_routes,
    admin_runtime,
    admin_safety,
    admin_theme,
)
from .pages_landing import (
    architecture_registry,
    architecture_web,
    web_sitemap,
    cdc_tracker,
    dev_tracking,
    documentation_registry,
    gem_portfolio,
    home,
    lexique_knowledge,
    mission_control,
    prompt_lab,
    qaic_bridge,
    settings_safety,
)
from .migration_decision_workbench import (
    MIGRATION_DECISION_WORKBENCH_ROUTE,
    migration_decision_workbench_page,
)

index = home

app = rx.App(
    theme=rx.theme(
        appearance="inherit",
        accent_color="blue",
        gray_color="slate",
        panel_background="solid",
        radius="large",
        scaling="100%",
    )
)
app.add_page(index, route="/", title="MVP QAIC — Mission Control")
app.add_page(mission_control, route="/mission-control", title="Mission Control")
app.add_page(dev_tracking, route="/dev-tracking", title="Dev Tracking")
app.add_page(cdc_tracker, route="/cdc-tracker", title="CDC Tracker")
app.add_page(architecture_web, route="/architecture-web", title="Architecture Web")
app.add_page(web_sitemap, route="/sitemap", title="MVP QAIC — Visual Sitemap")
app.add_page(
    documentation_registry, route="/documentation-registry", title="Documentation Registry"
)
app.add_page(architecture_registry, route="/architecture-registry", title="Architecture & Registry")
app.add_page(admin_center, route="/admin", title="Admin Center")
app.add_page(admin_runtime, route="/admin/runtime", title="Admin Runtime")
app.add_page(admin_theme, route="/admin/theme", title="Admin Theme")
app.add_page(admin_safety, route="/admin/safety", title="Admin Safety")
app.add_page(admin_routes, route="/admin/routes", title="Admin Routes")
app.add_page(admin_data_binding, route="/admin/data-binding", title="Admin Data Binding")
app.add_page(lexique_knowledge, route="/lexique-knowledge", title="Lexique Knowledge")
app.add_page(prompt_lab, route="/prompt-lab", title="Prompt Lab")
app.add_page(gem_portfolio, route="/gem-portfolio", title="GEM Portfolio")
app.add_page(qaic_bridge, route="/qaic-bridge", title="QAIC Bridge")
app.add_page(settings_safety, route="/settings-safety", title="Settings Safety")
app.add_page(
    migration_decision_workbench_page,
    route=MIGRATION_DECISION_WORKBENCH_ROUTE,
    title="Migration Decision Workbench",
)


# P_REFLEX_12E_R2D_BEGIN_SAFE_ROUTE_WIRING
def _p12e_r2d_register_safe_routes() -> None:
    try:
        _schema_mod = __import__(
            "mvp_qaic_reflex_ui.svg_schema_viewer",
            fromlist=["schema_large_page"],
        )
        _trackers_mod = __import__(
            "mvp_qaic_reflex_ui.auto_update_trackers_page",
            fromlist=["auto_update_trackers_page"],
        )
        app.add_page(
            _schema_mod.schema_large_page,
            route="/architecture-web/schema",
            title="Architecture Web Schema",
        )
        app.add_page(
            _trackers_mod.auto_update_trackers_page,
            route="/trackers/auto-update",
            title="Auto-update Trackers",
        )
    except Exception:  # noqa: BLE001
        pass


_p12e_r2d_register_safe_routes()
# P_REFLEX_12E_R2D_END_SAFE_ROUTE_WIRING

# P_REFLEX_12F_BEGIN_GLOBAL_MIGRATION_ROUTE
try:
    from mvp_qaic_reflex_ui.global_migration_page import global_migration_page

    app.add_page(global_migration_page, route="/migration/global", title="Migration globale")
except Exception:
    pass
# P_REFLEX_12F_END_GLOBAL_MIGRATION_ROUTE

# MVP UI CDC + Dev Tracker route
app.add_page(cdc_dev_tracker_reflex_page, route="/cdc-dev-tracker", title="CDC + Dev Tracker")
