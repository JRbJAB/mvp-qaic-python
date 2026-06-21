from __future__ import annotations

import csv
import io
import json
from dataclasses import asdict, is_dataclass
from typing import Any, Mapping, Sequence


SCHEMA_VERSION = "MVP_QAIC_BENCHMARK_EXPORT_REPORT_0.1.0"

SAFETY_MARKERS = (
    "HUMAN_REVIEW_ONLY",
    "NO_BROKER",
    "NO_ORDER",
    "NO_SIZING",
    "NO_GOOGLE_LIVE_WRITE",
    "DRY_RUN_DEFAULT",
    "LOCAL_FILES_ONLY",
)


def _as_mapping(record: Any) -> Mapping[str, Any]:
    if is_dataclass(record):
        data = asdict(record)
        if isinstance(data, Mapping):
            return data
    if isinstance(record, Mapping):
        return record
    if hasattr(record, "model_dump"):
        dumped = record.model_dump()
        if isinstance(dumped, Mapping):
            return dumped
    raise TypeError("benchmark export records must be mappings or dataclasses")


def _normalize_value(value: Any) -> str | int | float | bool | None:
    if value is None or isinstance(value, str | int | float | bool):
        return value
    if is_dataclass(value):
        return json.dumps(asdict(value), ensure_ascii=False, sort_keys=True)
    if isinstance(value, Mapping):
        normalized = {str(k): _normalize_value(v) for k, v in value.items()}
        return json.dumps(normalized, ensure_ascii=False, sort_keys=True)
    if isinstance(value, Sequence) and not isinstance(value, str | bytes | bytearray):
        normalized_items = [_normalize_value(item) for item in value]
        return json.dumps(normalized_items, ensure_ascii=False, sort_keys=True)
    return str(value)


def normalize_benchmark_record(record: Any) -> dict[str, str | int | float | bool | None]:
    raw = _as_mapping(record)
    return {str(key): _normalize_value(value) for key, value in raw.items()}


def build_benchmark_export_payload(
    records: Sequence[Any],
    *,
    run_id: str = "LOCAL_BENCHMARK_EXPORT",
    generated_at: str = "LOCAL_EXPORT_UNSPECIFIED_TIME",
    source: str = "local",
) -> dict[str, Any]:
    normalized_records = [normalize_benchmark_record(record) for record in records]
    field_names = sorted({key for record in normalized_records for key in record})

    return {
        "schema_version": SCHEMA_VERSION,
        "run_id": run_id,
        "generated_at": generated_at,
        "source": source,
        "safety": {
            "human_review_only": True,
            "no_broker": True,
            "no_order": True,
            "no_sizing": True,
            "no_google_live_write": True,
            "dry_run_default": True,
            "local_files_only": True,
            "markers": list(SAFETY_MARKERS),
        },
        "summary": {
            "record_count": len(normalized_records),
            "field_count": len(field_names),
            "fields": field_names,
        },
        "records": normalized_records,
    }


def benchmark_payload_to_json(payload: Mapping[str, Any]) -> str:
    return json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n"


def benchmark_payload_to_csv_rows(payload: Mapping[str, Any]) -> list[dict[str, str]]:
    run_id = str(payload.get("run_id", ""))
    records = payload.get("records", [])
    summary = payload.get("summary", {})
    fields = list(summary.get("fields", []))

    rows: list[dict[str, str]] = []
    for index, record in enumerate(records):
        if not isinstance(record, Mapping):
            raise TypeError("payload records must be mappings")
        row = {"run_id": run_id, "record_index": str(index)}
        for field in fields:
            value = record.get(field)
            row[str(field)] = "" if value is None else str(value)
        rows.append(row)
    return rows


def benchmark_payload_to_csv(payload: Mapping[str, Any]) -> str:
    rows = benchmark_payload_to_csv_rows(payload)
    fields = list(payload.get("summary", {}).get("fields", []))
    fieldnames = ["run_id", "record_index", *[str(field) for field in fields]]

    output = io.StringIO()
    writer = csv.DictWriter(output, fieldnames=fieldnames, lineterminator="\n")
    writer.writeheader()
    writer.writerows(rows)
    return output.getvalue()


def _markdown_escape(value: Any) -> str:
    text = "" if value is None else str(value)
    return text.replace("|", "\\|").replace("\n", " ")


def benchmark_payload_to_markdown(payload: Mapping[str, Any]) -> str:
    summary = payload.get("summary", {})
    fields = [str(field) for field in summary.get("fields", [])]
    records = payload.get("records", [])
    safety = payload.get("safety", {})

    lines = [
        "# MVP QAIC Benchmark Export Report",
        "",
        f"- schema_version: `{payload.get('schema_version', '')}`",
        f"- run_id: `{payload.get('run_id', '')}`",
        f"- generated_at: `{payload.get('generated_at', '')}`",
        f"- source: `{payload.get('source', '')}`",
        f"- record_count: `{summary.get('record_count', 0)}`",
        f"- field_count: `{summary.get('field_count', 0)}`",
        "",
        "## Safety",
        "",
    ]

    for marker in safety.get("markers", []):
        lines.append(f"- `{marker}`")

    lines.extend(["", "## Records", ""])

    if not records:
        lines.append("_No records._")
        return "\n".join(lines) + "\n"

    header = ["record_index", *fields]
    lines.append("| " + " | ".join(header) + " |")
    lines.append("| " + " | ".join(["---"] * len(header)) + " |")

    for index, record in enumerate(records):
        if not isinstance(record, Mapping):
            raise TypeError("payload records must be mappings")
        row = [str(index), *[_markdown_escape(record.get(field)) for field in fields]]
        lines.append("| " + " | ".join(row) + " |")

    return "\n".join(lines) + "\n"


def build_benchmark_export_bundle(
    records: Sequence[Any],
    *,
    run_id: str = "LOCAL_BENCHMARK_EXPORT",
    generated_at: str = "LOCAL_EXPORT_UNSPECIFIED_TIME",
    source: str = "local",
) -> dict[str, str]:
    payload = build_benchmark_export_payload(
        records,
        run_id=run_id,
        generated_at=generated_at,
        source=source,
    )
    return {
        "json": benchmark_payload_to_json(payload),
        "csv": benchmark_payload_to_csv(payload),
        "markdown": benchmark_payload_to_markdown(payload),
    }
