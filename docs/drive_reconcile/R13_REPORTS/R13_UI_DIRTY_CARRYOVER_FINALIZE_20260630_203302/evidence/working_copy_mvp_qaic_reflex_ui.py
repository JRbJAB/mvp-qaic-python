from __future__ import annotations

import re
import reflex as rx

from .restored_initial_render import make_restored_initial_route_page

# R16F2G1_SOURCE_REFLEX_RENDER_REPAIR_ONLY
app = rx.App()

ROUTES = [('/', 'Mission Control'), ('/mission-control', 'Mission Control'), ('/dev-tracking', 'Dev Tracking'), ('/cdc-tracker', 'Cdc Tracker'), ('/cdc-dev-tracker', 'Cdc Dev Tracker'), ('/architecture-web', 'Architecture Web'), ('/architecture-web/schema', 'Architecture Web / Schema'), ('/sitemap', 'Sitemap'), ('/documentation-registry', 'Documentation Registry'), ('/architecture-registry', 'Architecture Registry'), ('/admin', 'Admin'), ('/admin/runtime', 'Admin / Runtime'), ('/admin/theme', 'Admin / Theme'), ('/admin/safety', 'Admin / Safety'), ('/admin/routes', 'Admin / Routes'), ('/admin/data-binding', 'Admin / Data Binding'), ('/prompt-lab', 'Prompt Lab'), ('/gem-portfolio', 'Gem Portfolio'), ('/qaic-bridge', 'Qaic Bridge'), ('/lexique-knowledge', 'Lexique Knowledge'), ('/settings-safety', 'Settings Safety'), ('/migration/global', 'Migration / Global'), ('/migration/decisions', 'Migration / Decisions'), ('/trackers/auto-update', 'Trackers / Auto Update'), ('/architecture', 'Architecture'), ('/audit-runs', 'Audit Runs'), ('/base-python', 'Base Python'), ('/configuration', 'Configuration'), ('/documents', 'Documents'), ('/google-sheets', 'Google Sheets'), ('/prompt', 'Prompt'), ('/responses', 'Responses'), ('/workflow', 'Workflow')]


def _page_name(route: str) -> str:
    if route == "/":
        return "page_index"
    return "page_" + re.sub(r"[^a-zA-Z0-9_]+", "_", route.strip("/")).strip("_")


def _make_page(route: str, title: str):
    def page():
        return make_restored_initial_route_page(route, title)
    page.__name__ = _page_name(route)
    return page


_seen = set()
for _route, _title in ROUTES:
    if _route in _seen:
        continue
    _seen.add(_route)
    app.add_page(_make_page(_route, _title), route=_route, title="MVP QAIC — " + _title)
