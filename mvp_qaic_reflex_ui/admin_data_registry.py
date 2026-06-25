"""Admin data registry for MVP QAIC Reflex."""

from __future__ import annotations

from mvp_qaic_py.reflex_app.data_binding import build_local_data_binding_payload

from .theme import ADMIN_SECTIONS, LANDING_SECTIONS, SECONDARY_ROUTES, get_all_routes


REGISTRY_DOMAINS = (
    {
        "domain_id": "runtime",
        "title": "Runtime",
        "status": "ACTIVE",
        "description": "Local Reflex frontend/backend runtime and plugin config.",
    },
    {
        "domain_id": "navigation",
        "title": "Navigation",
        "status": "ACTIVE",
        "description": "Landing, admin and module routes.",
    },
    {
        "domain_id": "docs_exports",
        "title": "Docs & Exports",
        "status": "LOCAL_READONLY",
        "description": "Documentation and local export sources surfaced in admin.",
    },
    {
        "domain_id": "theme",
        "title": "Theme",
        "status": "READY_INTERACTIVE_LOCAL",
        "description": "Light/dark/system, accent, density and panel background.",
    },
    {
        "domain_id": "safety",
        "title": "Safety",
        "status": "LOCKED",
        "description": "No broker, no order, no sizing, no public deploy.",
    },
)


def build_admin_data_registry_payload() -> dict[str, object]:
    data_binding = build_local_data_binding_payload()
    routes = get_all_routes()

    return {
        "registry_status": "READY_LOCAL_READONLY",
        "domain_count": len(REGISTRY_DOMAINS),
        "route_count": len(routes),
        "landing_section_count": len(LANDING_SECTIONS),
        "admin_section_count": len(ADMIN_SECTIONS),
        "secondary_route_count": len(SECONDARY_ROUTES),
        "docs_source_count": data_binding["docs_source_count"],
        "export_source_count": data_binding["export_source_count"],
        "binding_mode": data_binding["binding_mode"],
        "write_allowed": False,
        "live_action": False,
        "domains": [dict(domain) for domain in REGISTRY_DOMAINS],
        "routes": routes,
    }


def admin_registry_summary_rows() -> dict[str, object]:
    payload = build_admin_data_registry_payload()
    return {
        "registry_status": payload["registry_status"],
        "domain_count": payload["domain_count"],
        "route_count": payload["route_count"],
        "landing_section_count": payload["landing_section_count"],
        "admin_section_count": payload["admin_section_count"],
        "docs_source_count": payload["docs_source_count"],
        "export_source_count": payload["export_source_count"],
        "binding_mode": payload["binding_mode"],
        "write_allowed": payload["write_allowed"],
    }


def registry_domain_rows() -> dict[str, str]:
    return {
        domain["domain_id"]: f"{domain['title']} — {domain['status']}"
        for domain in REGISTRY_DOMAINS
    }
