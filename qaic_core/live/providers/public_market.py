from __future__ import annotations

import json
from dataclasses import dataclass, field
from typing import Any, Callable, Mapping
from urllib.request import Request, urlopen

MARKET_PROVIDER_VERSION = "mvp_qaic.public_market_provider_readonly.v1"

READONLY_SAFETY_MARKERS: tuple[str, ...] = (
    "LIVE_READONLY",
    "PUBLIC_MARKET_DATA_ONLY",
    "NO_BROKER",
    "NO_ORDER",
    "NO_SIZING",
    "NO_SECRET",
)

DEFAULT_TIMEOUT_SEC = 5.0
DEFAULT_PROVIDER = "PUBLIC_MARKET_READONLY"

Transport = Callable[[str, float], Mapping[str, Any]]


@dataclass(frozen=True)
class PublicMarketSnapshot:
    provider_version: str = MARKET_PROVIDER_VERSION
    provider: str = DEFAULT_PROVIDER
    asset: str = ""
    symbol: str = ""
    current_price: float | None = None
    quote_currency: str = "USD"
    source_url: str = ""
    status: str = "REVIEW_REQUIRED"
    missing_data: tuple[str, ...] = field(default_factory=tuple)
    blockers: tuple[str, ...] = field(default_factory=tuple)
    live_readonly: bool = True
    network_called: bool = False
    broker_called: bool = False
    order_created: bool = False
    sizing_created: bool = False
    safety_markers: tuple[str, ...] = READONLY_SAFETY_MARKERS
    raw: Mapping[str, Any] = field(default_factory=dict)


def _coerce_price(value: object) -> float | None:
    if isinstance(value, bool) or value is None:
        return None
    try:
        price = float(value)
    except (TypeError, ValueError):
        return None
    if price <= 0:
        return None
    return price


def _asset_to_coingecko_id(asset: str) -> str:
    aliases = {
        "BTC": "bitcoin",
        "XBT": "bitcoin",
        "ETH": "ethereum",
        "SOL": "solana",
        "LINK": "chainlink",
        "NEAR": "near",
    }
    normalized = asset.strip().upper()
    return aliases.get(normalized, asset.strip().lower())


def _build_coingecko_simple_price_url(asset: str, quote_currency: str = "usd") -> str:
    coin_id = _asset_to_coingecko_id(asset)
    quote = quote_currency.strip().lower()
    return f"https://api.coingecko.com/api/v3/simple/price?ids={coin_id}&vs_currencies={quote}"


def _stdlib_json_transport(url: str, timeout_sec: float) -> Mapping[str, Any]:
    request = Request(
        url,
        headers={
            "Accept": "application/json",
            "User-Agent": "MVP-QAIC-Python-Live-Readonly/1.0",
        },
    )
    with urlopen(request, timeout=timeout_sec) as response:  # noqa: S310
        payload = response.read().decode("utf-8")
    loaded = json.loads(payload)
    if not isinstance(loaded, Mapping):
        raise ValueError("provider response must be a JSON object")
    return loaded


def build_public_market_snapshot(
    *,
    asset: str,
    quote_currency: str = "USD",
    provider_payload: Mapping[str, Any],
    source_url: str = "",
    provider: str = DEFAULT_PROVIDER,
    network_called: bool = False,
) -> PublicMarketSnapshot:
    missing: list[str] = []
    blockers: list[str] = []

    asset_clean = asset.strip().upper() if isinstance(asset, str) else ""
    quote_clean = quote_currency.strip().upper() if isinstance(quote_currency, str) else "USD"

    if not asset_clean:
        missing.append("asset")

    coin_id = _asset_to_coingecko_id(asset_clean or "missing")
    quote_key = quote_clean.lower()

    price = None
    if isinstance(provider_payload, Mapping):
        nested = provider_payload.get(coin_id)
        if isinstance(nested, Mapping):
            price = _coerce_price(nested.get(quote_key))
        if price is None:
            price = _coerce_price(provider_payload.get("current_price"))
        if price is None:
            price = _coerce_price(provider_payload.get("price"))

    if price is None:
        missing.append("current_price")

    status = "OK" if not missing and not blockers else "REVIEW_REQUIRED"

    return PublicMarketSnapshot(
        provider=provider,
        asset=asset_clean,
        symbol=asset_clean,
        current_price=price,
        quote_currency=quote_clean,
        source_url=source_url,
        status=status,
        missing_data=tuple(missing),
        blockers=tuple(blockers),
        live_readonly=True,
        network_called=network_called,
        broker_called=False,
        order_created=False,
        sizing_created=False,
        raw=dict(provider_payload),
    )


def fetch_public_market_snapshot(
    *,
    asset: str,
    quote_currency: str = "USD",
    allow_network: bool = False,
    timeout_sec: float = DEFAULT_TIMEOUT_SEC,
    transport: Transport | None = None,
) -> PublicMarketSnapshot:
    """Fetch a public-market snapshot in read-only mode.

    Network access is disabled by default. Passing a fake transport is the
    preferred test path. Real public HTTP access requires allow_network=True and
    never performs broker/order/sizing actions.
    """

    url = _build_coingecko_simple_price_url(asset, quote_currency)

    if transport is None and not allow_network:
        return PublicMarketSnapshot(
            provider=DEFAULT_PROVIDER,
            asset=asset.strip().upper() if isinstance(asset, str) else "",
            symbol=asset.strip().upper() if isinstance(asset, str) else "",
            quote_currency=quote_currency.strip().upper()
            if isinstance(quote_currency, str)
            else "USD",
            source_url=url,
            status="REVIEW_REQUIRED",
            missing_data=("provider_payload",),
            blockers=("NETWORK_DISABLED_BY_DEFAULT",),
            live_readonly=True,
            network_called=False,
            broker_called=False,
            order_created=False,
            sizing_created=False,
            raw={},
        )

    active_transport = transport or _stdlib_json_transport
    payload = active_transport(url, timeout_sec)

    return build_public_market_snapshot(
        asset=asset,
        quote_currency=quote_currency,
        provider_payload=payload,
        source_url=url,
        provider=DEFAULT_PROVIDER,
        network_called=True,
    )


def market_snapshot_to_dict(snapshot: PublicMarketSnapshot) -> dict[str, object]:
    return {
        "provider_version": snapshot.provider_version,
        "provider": snapshot.provider,
        "asset": snapshot.asset,
        "symbol": snapshot.symbol,
        "current_price": snapshot.current_price,
        "quote_currency": snapshot.quote_currency,
        "source_url": snapshot.source_url,
        "status": snapshot.status,
        "missing_data": list(snapshot.missing_data),
        "blockers": list(snapshot.blockers),
        "live_readonly": snapshot.live_readonly,
        "network_called": snapshot.network_called,
        "broker_called": snapshot.broker_called,
        "order_created": snapshot.order_created,
        "sizing_created": snapshot.sizing_created,
        "safety_markers": list(snapshot.safety_markers),
        "raw": dict(snapshot.raw),
    }
