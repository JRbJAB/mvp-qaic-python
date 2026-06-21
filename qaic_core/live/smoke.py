from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Mapping, Any

from qaic_core.live.cache import (
    CacheWriteResult,
    cache_write_result_to_dict,
    write_snapshot_jsonl,
)
from qaic_core.live.providers.public_market import (
    Transport,
    fetch_public_market_snapshot,
    market_snapshot_to_dict,
)

SMOKE_VERSION = "mvp_qaic.live_provider_smoke.v1"

SMOKE_SAFETY_MARKERS: tuple[str, ...] = (
    "LIVE_READONLY",
    "PUBLIC_MARKET_DATA_ONLY",
    "NO_BROKER",
    "NO_ORDER",
    "NO_SIZING",
    "NO_SECRET",
    "NETWORK_DISABLED_BY_DEFAULT",
    "CACHE_DISABLED_BY_DEFAULT",
)


@dataclass(frozen=True)
class LiveProviderSmokeResult:
    smoke_version: str = SMOKE_VERSION
    asset: str = ""
    status: str = "REVIEW_REQUIRED"
    snapshot: Mapping[str, Any] = field(default_factory=dict)
    cache: Mapping[str, Any] | None = None
    blockers: tuple[str, ...] = field(default_factory=tuple)
    missing_data: tuple[str, ...] = field(default_factory=tuple)
    live_readonly: bool = True
    network_called: bool = False
    cache_written: bool = False
    broker_called: bool = False
    order_created: bool = False
    sizing_created: bool = False
    safety_markers: tuple[str, ...] = SMOKE_SAFETY_MARKERS


def run_public_market_provider_smoke(
    *,
    asset: str,
    quote_currency: str = "USD",
    allow_network: bool = False,
    transport: Transport | None = None,
    snapshot_dir: str | Path | None = None,
    write_cache: bool = False,
    run_id: str = "P65-SMOKE",
) -> LiveProviderSmokeResult:
    snapshot = fetch_public_market_snapshot(
        asset=asset,
        quote_currency=quote_currency,
        allow_network=allow_network,
        transport=transport,
    )
    snapshot_payload = market_snapshot_to_dict(snapshot)

    blockers = list(snapshot.blockers)
    if snapshot.status != "OK" and not blockers:
        blockers.append("PROVIDER_REVIEW_REQUIRED")

    cache_payload: dict[str, object] | None = None
    cache_written = False

    if write_cache:
        if snapshot_dir is None:
            blockers.append("CACHE_PATH_REQUIRED")
        else:
            cache_result: CacheWriteResult = write_snapshot_jsonl(
                snapshot=snapshot_payload,
                snapshot_dir=snapshot_dir,
                run_id=run_id,
            )
            cache_payload = cache_write_result_to_dict(cache_result)
            cache_written = cache_result.wrote_file

    status = "OK" if snapshot.status == "OK" and not blockers else "REVIEW_REQUIRED"

    return LiveProviderSmokeResult(
        asset=asset.strip().upper() if isinstance(asset, str) else "",
        status=status,
        snapshot=snapshot_payload,
        cache=cache_payload,
        blockers=tuple(dict.fromkeys(blockers)),
        missing_data=tuple(snapshot.missing_data),
        live_readonly=True,
        network_called=bool(snapshot.network_called),
        cache_written=cache_written,
        broker_called=False,
        order_created=False,
        sizing_created=False,
    )


def live_provider_smoke_result_to_dict(result: LiveProviderSmokeResult) -> dict[str, object]:
    return {
        "smoke_version": result.smoke_version,
        "asset": result.asset,
        "status": result.status,
        "snapshot": dict(result.snapshot),
        "cache": dict(result.cache) if result.cache is not None else None,
        "blockers": list(result.blockers),
        "missing_data": list(result.missing_data),
        "live_readonly": result.live_readonly,
        "network_called": result.network_called,
        "cache_written": result.cache_written,
        "broker_called": result.broker_called,
        "order_created": result.order_created,
        "sizing_created": result.sizing_created,
        "safety_markers": list(result.safety_markers),
    }
