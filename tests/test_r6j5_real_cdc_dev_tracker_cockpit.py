from __future__ import annotations

from pathlib import Path

from mvp_qaic_reflex_ui.v25_cdc_delivery_tracker_static import (
    DETAIL_ROWS,
    GLOBAL_META,
    REAL_COCKPIT_MARKER,
    SUMMARY_ROWS,
    cdc_kpis,
)

ROOT = Path(__file__).resolve().parents[1]
PAGE = ROOT / "mvp_qaic_reflex_ui" / "cdc_dev_tracker_reflex_page.py"
PAGES_LANDING = ROOT / "mvp_qaic_reflex_ui" / "pages_landing.py"


def test_real_v25_payload_present() -> None:
    assert REAL_COCKPIT_MARKER == "V25_CDC_DELIVERY_TRACKER_COCKPIT"
    assert GLOBAL_META["global_status"] == "REVIEW"
    assert GLOBAL_META["realized_pct"] == "73.25%"
    assert len(SUMMARY_ROWS) >= 14
    assert len(DETAIL_ROWS) >= 80
    assert any(row["phase_id"] == "P10" for row in SUMMARY_ROWS)
    assert any(row["module_id"] == "PMT-0001" for row in DETAIL_ROWS)


def test_page_is_not_stub_and_uses_real_cockpit() -> None:
    text = PAGE.read_text(encoding="utf-8")
    assert "V25_CDC_DELIVERY_TRACKER_COCKPIT" in text
    assert "📊 V25 CDC Delivery Tracker" in text
    assert "progression" in text.lower() or "Progress" in text
    assert "CDC-001" not in text
    assert "DEV-001" not in text
    assert "runtime smoke unique" not in text


def test_landing_routes_are_real_cockpit_not_placeholder() -> None:
    text = PAGES_LANDING.read_text(encoding="utf-8")
    assert "cdc_tracker_reflex_page" in text
    assert "dev_tracking_reflex_page" in text
    dev_block = text[text.index("def dev_tracking") : text.index("def cdc_tracker")]
    cdc_block = text[text.index("def cdc_tracker") : text.index("def architecture_web")]
    assert "placeholder_body" not in dev_block
    assert "placeholder_body" not in cdc_block
    assert "dev_tracking_reflex_page()" in dev_block
    assert "cdc_tracker_reflex_page()" in cdc_block


def test_kpi_contract() -> None:
    kpis = cdc_kpis()
    assert kpis["status"] == "REVIEW"
    assert int(kpis["realized_num"]) == 73
    assert kpis["blocked"] == "1"
    assert kpis["at_risk"] == "50"
