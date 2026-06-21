from __future__ import annotations

from qaic_core.live.providers.public_market import (
    READONLY_SAFETY_MARKERS,
    build_public_market_snapshot,
    fetch_public_market_snapshot,
    market_snapshot_to_dict,
)


def test_build_public_market_snapshot_from_payload() -> None:
    snapshot = build_public_market_snapshot(
        asset="BTC",
        quote_currency="USD",
        provider_payload={"bitcoin": {"usd": 68000}},
        source_url="https://example.test/price",
    )
    payload = market_snapshot_to_dict(snapshot)

    assert payload["status"] == "OK"
    assert payload["asset"] == "BTC"
    assert payload["current_price"] == 68000.0
    assert payload["live_readonly"] is True
    assert payload["broker_called"] is False
    assert payload["order_created"] is False
    assert payload["sizing_created"] is False


def test_network_is_disabled_by_default_without_transport() -> None:
    snapshot = fetch_public_market_snapshot(asset="BTC")
    payload = market_snapshot_to_dict(snapshot)

    assert payload["status"] == "REVIEW_REQUIRED"
    assert "NETWORK_DISABLED_BY_DEFAULT" in payload["blockers"]
    assert payload["network_called"] is False
    assert payload["broker_called"] is False
    assert payload["order_created"] is False
    assert payload["sizing_created"] is False


def test_fake_transport_enables_readonly_market_snapshot_without_real_network() -> None:
    calls: list[tuple[str, float]] = []

    def fake_transport(url: str, timeout_sec: float) -> dict[str, object]:
        calls.append((url, timeout_sec))
        return {"bitcoin": {"usd": 68123.45}}

    snapshot = fetch_public_market_snapshot(
        asset="BTC",
        quote_currency="USD",
        transport=fake_transport,
    )
    payload = market_snapshot_to_dict(snapshot)

    assert calls
    assert "coingecko" in calls[0][0]
    assert payload["status"] == "OK"
    assert payload["current_price"] == 68123.45
    assert payload["network_called"] is True
    assert payload["broker_called"] is False
    assert payload["order_created"] is False
    assert payload["sizing_created"] is False


def test_missing_price_returns_review_required() -> None:
    snapshot = build_public_market_snapshot(
        asset="ETH",
        provider_payload={"ethereum": {}},
    )
    payload = market_snapshot_to_dict(snapshot)

    assert payload["status"] == "REVIEW_REQUIRED"
    assert "current_price" in payload["missing_data"]


def test_missing_asset_returns_review_required() -> None:
    snapshot = build_public_market_snapshot(
        asset="",
        provider_payload={"current_price": 100},
    )
    payload = market_snapshot_to_dict(snapshot)

    assert payload["status"] == "REVIEW_REQUIRED"
    assert "asset" in payload["missing_data"]


def test_safety_markers_are_readonly_only() -> None:
    assert READONLY_SAFETY_MARKERS == (
        "LIVE_READONLY",
        "PUBLIC_MARKET_DATA_ONLY",
        "NO_BROKER",
        "NO_ORDER",
        "NO_SIZING",
        "NO_SECRET",
    )


def test_provider_payload_can_use_flat_current_price() -> None:
    snapshot = build_public_market_snapshot(
        asset="SOL",
        provider_payload={"current_price": "145.5"},
    )
    payload = market_snapshot_to_dict(snapshot)

    assert payload["status"] == "OK"
    assert payload["current_price"] == 145.5


def test_negative_price_is_rejected_as_missing() -> None:
    snapshot = build_public_market_snapshot(
        asset="BTC",
        provider_payload={"bitcoin": {"usd": -1}},
    )
    payload = market_snapshot_to_dict(snapshot)

    assert payload["status"] == "REVIEW_REQUIRED"
    assert "current_price" in payload["missing_data"]
