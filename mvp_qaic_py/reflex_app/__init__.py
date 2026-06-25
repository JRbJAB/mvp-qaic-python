"""MVP QAIC Reflex global webapp shell foundation.

Local-only foundation. No live provider, broker, Sheet writes, data warehouse writes, CLASP or public deploy action.
"""

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
]
