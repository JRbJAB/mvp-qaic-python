"""MVP QAIC local private Reflex UI."""

from __future__ import annotations

import reflex as rx

from .pages_landing import (
    architecture_registry,
    architecture_web,
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

index = home

app = rx.App()
app.add_page(index, route="/", title="MVP QAIC — Mission Control")
app.add_page(mission_control, route="/mission-control", title="Mission Control")
app.add_page(dev_tracking, route="/dev-tracking", title="Dev Tracking")
app.add_page(cdc_tracker, route="/cdc-tracker", title="CDC Tracker")
app.add_page(architecture_web, route="/architecture-web", title="Architecture Web")
app.add_page(
    documentation_registry, route="/documentation-registry", title="Documentation Registry"
)
app.add_page(architecture_registry, route="/architecture-registry", title="Architecture & Registry")
app.add_page(lexique_knowledge, route="/lexique-knowledge", title="Lexique Knowledge")
app.add_page(prompt_lab, route="/prompt-lab", title="Prompt Lab")
app.add_page(gem_portfolio, route="/gem-portfolio", title="GEM Portfolio")
app.add_page(qaic_bridge, route="/qaic-bridge", title="QAIC Bridge")
app.add_page(settings_safety, route="/settings-safety", title="Settings Safety")
