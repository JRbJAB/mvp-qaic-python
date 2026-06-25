"""MVP QAIC Reflex shell package."""

from __future__ import annotations

from .data_binding import build_local_data_binding_payload
from .navigation import (
    build_navigation_groups,
    safety_banner_payload,
    ui_shell_payload,
)
from .registry import (
    ARCHITECTURE_ASSET,
    CURRENT_CDC,
    DOCS_REGISTRY,
    PAGES,
    SAFETY_FLAGS,
    get_page,
    list_routes,
)

__all__ = [
    "ARCHITECTURE_ASSET",
    "CURRENT_CDC",
    "DOCS_REGISTRY",
    "PAGES",
    "SAFETY_FLAGS",
    "get_page",
    "list_routes",
    "build_navigation_groups",
    "safety_banner_payload",
    "ui_shell_payload",
    "build_local_data_binding_payload",
]
