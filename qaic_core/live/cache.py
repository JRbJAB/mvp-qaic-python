from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Mapping, Any

CACHE_VERSION = "mvp_qaic.live_snapshot_cache.v1"

CACHE_SAFETY_MARKERS: tuple[str, ...] = (
    "LOCAL_CACHE_ONLY",
    "EXPLICIT_PATH_REQUIRED",
    "NO_BROKER",
    "NO_ORDER",
    "NO_SIZING",
    "NO_SECRET",
)


@dataclass(frozen=True)
class CacheWriteResult:
    cache_version: str
    wrote_file: bool
    path: str
    sha256: str
    bytes_written: int
    line_count: int
    safety_markers: tuple[str, ...] = CACHE_SAFETY_MARKERS


def canonical_json_line(record: Mapping[str, Any]) -> str:
    return json.dumps(record, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def build_snapshot_cache_record(
    *,
    snapshot: Mapping[str, Any],
    run_id: str,
    source: str = "PUBLIC_MARKET_READONLY",
    generated_at: str | None = None,
) -> dict[str, object]:
    timestamp = generated_at or datetime.now(UTC).replace(microsecond=0).isoformat()
    record = {
        "cache_version": CACHE_VERSION,
        "run_id": run_id,
        "source": source,
        "generated_at": timestamp,
        "safety_markers": list(CACHE_SAFETY_MARKERS),
        "snapshot": dict(snapshot),
    }
    return record


def write_snapshot_jsonl(
    *,
    snapshot: Mapping[str, Any],
    snapshot_dir: str | Path,
    run_id: str,
    source: str = "PUBLIC_MARKET_READONLY",
    generated_at: str | None = None,
) -> CacheWriteResult:
    target_dir = Path(snapshot_dir)
    target_dir.mkdir(parents=True, exist_ok=True)

    record = build_snapshot_cache_record(
        snapshot=snapshot,
        run_id=run_id,
        source=source,
        generated_at=generated_at,
    )
    line = canonical_json_line(record) + "\n"
    digest = hashlib.sha256(line.encode("utf-8")).hexdigest()
    path = target_dir / f"{run_id}.jsonl"
    path.write_text(line, encoding="utf-8")

    return CacheWriteResult(
        cache_version=CACHE_VERSION,
        wrote_file=True,
        path=str(path),
        sha256=digest,
        bytes_written=len(line.encode("utf-8")),
        line_count=1,
    )


def cache_write_result_to_dict(result: CacheWriteResult) -> dict[str, object]:
    return {
        "cache_version": result.cache_version,
        "wrote_file": result.wrote_file,
        "path": result.path,
        "sha256": result.sha256,
        "bytes_written": result.bytes_written,
        "line_count": result.line_count,
        "safety_markers": list(result.safety_markers),
    }
