"""Navigation model for the MVP QAIC Reflex shell.

Local-only UI payload builder. No server, browser, provider, broker,
public deploy, order, sizing or live action.
"""

from __future__ import annotations

from dataclasses import dataclass

from .registry import PAGES, SAFETY_FLAGS


@dataclass(frozen=True)
class NavItem:
    page_id: str
    route: str
    title: str
    group: str
    purpose: str


@dataclass(frozen=True)
class NavGroup:
    group_id: str
    title: str
    description: str
    items: tuple[NavItem, ...]


GROUP_ORDER = {
    "core": (
        "Core cockpit",
        "Home, dev tracking, CDC, architecture and documentation.",
        (
            "home",
            "dev_tracking",
            "cdc_tracker",
            "architecture_web",
            "docs_registry",
            "architecture_registry",
        ),
    ),
    "knowledge": (
        "Knowledge base",
        "Lexique, knowledge terms and methods library.",
        ("lexique_knowledge", "methods_library"),
    ),
    "prompt": (
        "Prompt and review",
        "Prompt lab, GEM portfolio workflow and response review.",
        ("prompt_lab", "gem_portfolio", "responses_review"),
    ),
    "bridge": (
        "QAIC bridge",
        "Read-only liaison with the private QAIC backend.",
        ("qaic_bridge",),
    ),
    "gateways": (
        "Specialized gateways",
        "Panel and Gradio placeholders outside the main shell runtime.",
        ("panel_gateway", "gradio_gateway"),
    ),
    "safety": (
        "Safety and archives",
        "Human-review safety, no-live policy and audit archives.",
        ("settings_safety", "audit_archives"),
    ),
}


def _page_by_id() -> dict[str, object]:
    return {page.page_id: page for page in PAGES}


def build_navigation_groups() -> list[NavGroup]:
    pages = _page_by_id()
    groups: list[NavGroup] = []

    for group_id, (title, description, page_ids) in GROUP_ORDER.items():
        items: list[NavItem] = []
        for page_id in page_ids:
            page = pages[page_id]
            items.append(
                NavItem(
                    page_id=page.page_id,
                    route=page.route,
                    title=page.title,
                    group=page.group,
                    purpose=page.purpose,
                )
            )
        groups.append(
            NavGroup(
                group_id=group_id,
                title=title,
                description=description,
                items=tuple(items),
            )
        )

    return groups


def safety_banner_payload() -> dict[str, object]:
    locked_flags = sorted(flag for flag, value in SAFETY_FLAGS.items() if value is True)
    unlocked_flags = sorted(flag for flag, value in SAFETY_FLAGS.items() if value is not True)

    return {
        "status": "LOCKED",
        "human_review_only": SAFETY_FLAGS.get("HUMAN_REVIEW_ONLY") is True,
        "no_live_action": all(SAFETY_FLAGS.values()),
        "locked_flags": locked_flags,
        "unlocked_flags": unlocked_flags,
        "summary": (
            "Human review only. No order, no sizing, no broker execution, no public deploy."
        ),
    }


def ui_shell_payload() -> dict[str, object]:
    groups = build_navigation_groups()
    covered_page_ids = [item.page_id for group in groups for item in group.items]

    return {
        "shell_title": "MVP QAIC Global WebApp Shell",
        "shell_mode": "LOCAL_PRIVATE_OPERATOR_PREVIEW",
        "layout": "left_menu_top_status_content_area",
        "navigation_group_count": len(groups),
        "navigation_item_count": len(covered_page_ids),
        "covered_page_ids": covered_page_ids,
        "groups": [
            {
                "group_id": group.group_id,
                "title": group.title,
                "description": group.description,
                "items": [
                    {
                        "page_id": item.page_id,
                        "route": item.route,
                        "title": item.title,
                        "purpose": item.purpose,
                    }
                    for item in group.items
                ],
            }
            for group in groups
        ],
        "safety_banner": safety_banner_payload(),
    }
