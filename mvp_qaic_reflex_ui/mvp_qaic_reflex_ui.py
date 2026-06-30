"""MVP QAIC local private Reflex UI."""

from __future__ import annotations

import reflex as rx

from mvp_qaic_reflex_ui.private_cockpit_pages import (
    cdc_dev_tracker_page,
    cdc_tracker_page,
    dev_tracking_page,
    home_page,
)

R2A_R13B_PRIVATE_COCKPIT_APP_ENTRYPOINT = True
R2A_R14A_RICH_MIGRATION_COCKPIT = True
R2A_R15B_REAL_MODULE_COCKPIT_SAFE_FIX = True

app = rx.App()
app.add_page(home_page, route="/", title="MVP QAIC Private Cockpit")
app.add_page(cdc_tracker_page, route="/cdc-tracker", title="CDC Tracker")
app.add_page(cdc_dev_tracker_page, route="/cdc-dev-tracker", title="CDC + Dev Tracker")
app.add_page(dev_tracking_page, route="/dev-tracking", title="Dev Tracking / Migration OS")

# Backward-compatible alias used by older cockpit tests and launcher contracts.
cdc_dev_tracker_reflex_page = cdc_dev_tracker_page

# R2A-R15C backward-compat marker restore.
# Keep previous route/source contracts alive while richer migration cockpit evolves.
R2A_R13B_PRIVATE_COCKPIT_APP_ENTRYPOINT = True
R2A_R14B_RICH_COCKPIT_COMPAT_FIX = True
R2A_R15C_COMPAT_MARKERS_RESTORED = True

# R2A_R13B_BEGIN_PRIVATE_COCKPIT_SOURCE_ROUTES
# R2A_R14A_RICH_MIGRATION_COCKPIT_ROUTE_BINDINGS
# route="/"
# route="/cdc-tracker"
# route="/cdc-dev-tracker"
# route="/dev-tracking"
# R2A_R13B_END_PRIVATE_COCKPIT_SOURCE_ROUTES

# R2A_R15D final compatibility seal marker.
R2A_R15D_REAL_MODULE_COCKPIT_MARKER_RESTORE = True
