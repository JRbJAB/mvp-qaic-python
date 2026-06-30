"""MVP QAIC local private Reflex UI.

R2A-R13B: clean source entrypoint for private local cockpit routes.
"""

from __future__ import annotations

import reflex as rx

from mvp_qaic_reflex_ui.private_cockpit_pages import (
    cdc_dev_tracker_page,
    cdc_tracker_page,
    dev_tracking_page,
    home_page,
)

R2A_R13B_PRIVATE_COCKPIT_APP_ENTRYPOINT = True

app = rx.App()

# R2A_R13B_BEGIN_PRIVATE_COCKPIT_SOURCE_ROUTES
app.add_page(home_page, route="/", title="MVP QAIC Cockpit")
app.add_page(cdc_tracker_page, route="/cdc-tracker", title="CDC Tracker")
app.add_page(cdc_dev_tracker_page, route="/cdc-dev-tracker", title="CDC + Dev Tracker")
app.add_page(dev_tracking_page, route="/dev-tracking", title="Dev Tracking")
# R2A_R13B_END_PRIVATE_COCKPIT_SOURCE_ROUTES
