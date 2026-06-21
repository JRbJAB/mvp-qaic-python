from __future__ import annotations

import json

from qaic_core.live.cache import (
    CACHE_SAFETY_MARKERS,
    build_snapshot_cache_record,
    cache_write_result_to_dict,
    canonical_json_line,
    write_snapshot_jsonl,
)
from qaic_core.live.smoke import (
    SMOKE_SAFETY_MARKERS,
    live_provider_smoke_result_to_dict,
    run_public_market_provider_smoke,
)


def test_smoke_without_transport_keeps_network_disabled() -> None:
    result = run_public_market_provider_smoke(asset="BTC")
    payload = live_provider_smoke_result_to_dict(result)

    assert payload["status"] == "REVIEW_REQUIRED"
    assert "NETWORK_DISABLED_BY_DEFAULT" in payload["blockers"]
    assert payload["network_called"] is False
    assert payload["cache_written"] is False
    assert payload["broker_called"] is False
    assert payload["order_created"] is False
    assert payload["sizing_created"] is False


def test_smoke_with_fake_transport_returns_ok_without_broker_or_order() -> None:
    def fake_transport(url: str, timeout_sec: float) -> dict[str, object]:
        return {"bitcoin": {"usd": 68200}}

    result = run_public_market_provider_smoke(asset="BTC", transport=fake_transport)
    payload = live_provider_smoke_result_to_dict(result)

    assert payload["status"] == "OK"
    assert payload["snapshot"]["current_price"] == 68200.0
    assert payload["network_called"] is True
    assert payload["broker_called"] is False
    assert payload["order_created"] is False
    assert payload["sizing_created"] is False
    assert payload["cache_written"] is False


def test_smoke_cache_write_requires_explicit_path() -> None:
    def fake_transport(url: str, timeout_sec: float) -> dict[str, object]:
        return {"ethereum": {"usd": 3600}}

    result = run_public_market_provider_smoke(
        asset="ETH",
        transport=fake_transport,
        write_cache=True,
    )
    payload = live_provider_smoke_result_to_dict(result)

    assert payload["status"] == "REVIEW_REQUIRED"
    assert "CACHE_PATH_REQUIRED" in payload["blockers"]
    assert payload["cache_written"] is False


def test_smoke_writes_cache_only_to_explicit_tmp_path(tmp_path) -> None:
    def fake_transport(url: str, timeout_sec: float) -> dict[str, object]:
        return {"solana": {"usd": 145.5}}

    result = run_public_market_provider_smoke(
        asset="SOL",
        transport=fake_transport,
        write_cache=True,
        snapshot_dir=tmp_path,
        run_id="P65-SOL",
    )
    payload = live_provider_smoke_result_to_dict(result)

    assert payload["status"] == "OK"
    assert payload["cache_written"] is True
    assert payload["cache"] is not None
    cache_path = tmp_path / "P65-SOL.jsonl"
    assert cache_path.exists()
    loaded = json.loads(cache_path.read_text(encoding="utf-8"))
    assert loaded["run_id"] == "P65-SOL"
    assert loaded["snapshot"]["asset"] == "SOL"


def test_cache_record_is_canonical_and_deterministic() -> None:
    snapshot = {"asset": "BTC", "current_price": 68000}
    first = build_snapshot_cache_record(
        snapshot=snapshot,
        run_id="RUN-1",
        generated_at="2026-06-21T00:00:00+00:00",
    )
    second = build_snapshot_cache_record(
        snapshot=snapshot,
        run_id="RUN-1",
        generated_at="2026-06-21T00:00:00+00:00",
    )

    assert canonical_json_line(first) == canonical_json_line(second)


def test_write_snapshot_jsonl_result_has_hash_and_one_line(tmp_path) -> None:
    result = write_snapshot_jsonl(
        snapshot={"asset": "BTC", "current_price": 68000},
        snapshot_dir=tmp_path,
        run_id="RUN-HASH",
        generated_at="2026-06-21T00:00:00+00:00",
    )
    payload = cache_write_result_to_dict(result)

    assert payload["wrote_file"] is True
    assert payload["line_count"] == 1
    assert isinstance(payload["sha256"], str)
    assert len(payload["sha256"]) == 64
    assert (tmp_path / "RUN-HASH.jsonl").exists()


def test_smoke_safety_markers_are_explicit() -> None:
    assert SMOKE_SAFETY_MARKERS == (
        "LIVE_READONLY",
        "PUBLIC_MARKET_DATA_ONLY",
        "NO_BROKER",
        "NO_ORDER",
        "NO_SIZING",
        "NO_SECRET",
        "NETWORK_DISABLED_BY_DEFAULT",
        "CACHE_DISABLED_BY_DEFAULT",
    )


def test_cache_safety_markers_are_explicit() -> None:
    assert CACHE_SAFETY_MARKERS == (
        "LOCAL_CACHE_ONLY",
        "EXPLICIT_PATH_REQUIRED",
        "NO_BROKER",
        "NO_ORDER",
        "NO_SIZING",
        "NO_SECRET",
    )
