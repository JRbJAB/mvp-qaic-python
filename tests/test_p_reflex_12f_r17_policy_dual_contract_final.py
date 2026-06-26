from __future__ import annotations

from mvp_qaic_reflex_ui.migration_os import ESSENTIAL_ONLY_POLICY
from mvp_qaic_reflex_ui.migration_os import build_migration_tracker_payload


def test_r17_policy_satisfies_r11_and_r14_contracts() -> None:
    assert ESSENTIAL_ONLY_POLICY == "LEGACY_15_PLUS_LIVE_ESSENTIALS_TABLE_UX"
    assert "Mission Control: uniquement" in ESSENTIAL_ONLY_POLICY


def test_r17_payload_contract_is_still_stable() -> None:
    payload = build_migration_tracker_payload()
    assert payload["legacy_row_count"] == 15
    assert payload["table_ux_with_percentages"] is True
    assert payload["show_only_essential"] is True
    assert payload["row_count"] < 150
    assert payload["function_index_count"] >= 2738
    sources = [row["source"] for row in payload["rows"]]
    assert len(sources) == len(set(sources))
