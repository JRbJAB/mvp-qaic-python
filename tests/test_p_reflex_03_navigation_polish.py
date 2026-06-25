from mvp_qaic_py.reflex_app import registry
from mvp_qaic_py.reflex_app.app import page_registry_payload
from mvp_qaic_py.reflex_app.navigation import (
    GROUP_ORDER,
    build_navigation_groups,
    safety_banner_payload,
    ui_shell_payload,
)


def test_navigation_groups_cover_every_registered_page_once():
    groups = build_navigation_groups()
    covered = [item.page_id for group in groups for item in group.items]
    expected = [page.page_id for page in registry.PAGES]

    assert len(groups) == 6
    assert set(GROUP_ORDER) == {
        "core",
        "knowledge",
        "prompt",
        "bridge",
        "gateways",
        "safety",
    }
    assert sorted(covered) == sorted(expected)
    assert len(covered) == len(set(covered))


def test_navigation_group_routes_are_operator_ready():
    payload = ui_shell_payload()

    assert payload["layout"] == "left_menu_top_status_content_area"
    assert payload["navigation_group_count"] == 6
    assert payload["navigation_item_count"] >= 16

    group_ids = {group["group_id"] for group in payload["groups"]}
    assert "core" in group_ids
    assert "knowledge" in group_ids
    assert "prompt" in group_ids
    assert "bridge" in group_ids
    assert "gateways" in group_ids
    assert "safety" in group_ids


def test_safety_banner_is_locked_and_no_live():
    banner = safety_banner_payload()

    assert banner["status"] == "LOCKED"
    assert banner["human_review_only"] is True
    assert banner["no_live_action"] is True
    assert banner["unlocked_flags"] == []
    assert "NO_BIGQUERY_WRITE" in banner["locked_flags"]
    assert "NO_QAIT" in banner["locked_flags"]


def test_app_payload_includes_ui_shell():
    payload = page_registry_payload()

    assert "ui_shell" in payload
    assert payload["ui_shell"]["navigation_group_count"] == 6
    assert payload["ui_shell"]["safety_banner"]["status"] == "LOCKED"
