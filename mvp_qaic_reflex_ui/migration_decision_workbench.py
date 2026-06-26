from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ALLOWED_DECISION_STATUSES = {
    "MIGRATE_NOW",
    "MIGRATE_LATER",
    "PYTHON_REWRITE",
    "KEEP_AS_EXPORT_SOURCE",
    "KEEP_SHEETS_MANUAL",
    "BIGQUERY_FUTURE_CANDIDATE",
    "REVIEW_REQUIRED",
    "RETIRE_NO_VALUE",
    "NO_MIGRATION_NEEDED",
    "REFLEX_UI_BINDING",
    "STRUCTURE_READY",
    "PARTIAL",
    "TO_MIGRATE",
    "PRIVATE_READY",
    "ACTIVE",
    "TO_BIND",
}

DEFAULT_REVIEW_STATUSES = {
    "MIGRATE_NOW",
    "MIGRATE_LATER",
    "PYTHON_REWRITE",
    "BIGQUERY_FUTURE_CANDIDATE",
    "REVIEW_REQUIRED",
    "KEEP_AS_EXPORT_SOURCE",
    "KEEP_SHEETS_MANUAL",
}

OVERLAY_VERSION = "0.2.0"
DECISION_OVERLAY_REL = "docs/MIGRATION_DECISION_OVERLAY.json"
LIVE_PAYLOAD_REL = "docs/MIGRATION_OS_LIVE_PAYLOAD.json"
DECISION_QUEUE_REL = "docs/MIGRATION_DECISION_QUEUE.json"


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def repo_path(repo_root: str | Path, rel: str) -> Path:
    return Path(repo_root).resolve() / rel


def read_json(path: Path, default: Any) -> Any:
    if not path.exists():
        return default
    return json.loads(path.read_text(encoding="utf-8-sig"))


def write_json_atomic(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    tmp.replace(path)


def load_decision_overlay(repo_root: str | Path = ".") -> dict[str, Any]:
    path = repo_path(repo_root, DECISION_OVERLAY_REL)
    overlay = read_json(path, {"version": OVERLAY_VERSION, "decisions": []})
    if not isinstance(overlay, dict):
        overlay = {"version": OVERLAY_VERSION, "decisions": []}
    overlay.setdefault("version", OVERLAY_VERSION)
    overlay.setdefault("decisions", [])
    if not isinstance(overlay["decisions"], list):
        overlay["decisions"] = []
    return overlay


def save_decision_overlay(repo_root: str | Path, overlay: dict[str, Any]) -> None:
    overlay["version"] = str(overlay.get("version") or OVERLAY_VERSION)
    overlay["updated_at_utc"] = utc_now()
    write_json_atomic(repo_path(repo_root, DECISION_OVERLAY_REL), overlay)


def normalize_source(value: Any) -> str:
    return str(value or "").strip()


def row_source(row: dict[str, Any]) -> str:
    return normalize_source(
        row.get("source") or row.get("Source") or row.get("name") or row.get("Name")
    )


def row_status(row: dict[str, Any]) -> str:
    return str(row.get("status") or row.get("Statut") or row.get("decision_status") or "").strip()


def overlay_by_source(overlay: dict[str, Any]) -> dict[str, dict[str, Any]]:
    out: dict[str, dict[str, Any]] = {}
    for entry in overlay.get("decisions", []):
        if not isinstance(entry, dict):
            continue
        source = normalize_source(entry.get("source"))
        if source:
            out[source] = entry
    return out


def normalize_decision_entry(
    *,
    source: str,
    decision_status: str,
    target: str = "",
    note: str = "",
    reviewer: str = "operator",
) -> dict[str, Any]:
    source = normalize_source(source)
    status = str(decision_status or "").strip().upper()
    if not source:
        raise ValueError("source is required")
    if status not in ALLOWED_DECISION_STATUSES:
        raise ValueError(f"decision_status not allowed: {status}")
    return {
        "source": source,
        "decision_status": status,
        "target": str(target or "").strip(),
        "note": str(note or "").strip(),
        "reviewer": str(reviewer or "operator").strip(),
        "updated_at_utc": utc_now(),
    }


def upsert_decision(
    repo_root: str | Path,
    *,
    source: str,
    decision_status: str,
    target: str = "",
    note: str = "",
    reviewer: str = "operator",
) -> dict[str, Any]:
    overlay = load_decision_overlay(repo_root)
    entry = normalize_decision_entry(
        source=source,
        decision_status=decision_status,
        target=target,
        note=note,
        reviewer=reviewer,
    )
    decisions = [
        d
        for d in overlay.get("decisions", [])
        if isinstance(d, dict) and normalize_source(d.get("source")) != entry["source"]
    ]
    decisions.append(entry)
    decisions.sort(key=lambda item: normalize_source(item.get("source")).casefold())
    overlay["decisions"] = decisions
    save_decision_overlay(repo_root, overlay)
    return entry


def load_live_payload(repo_root: str | Path = ".") -> dict[str, Any]:
    path = repo_path(repo_root, LIVE_PAYLOAD_REL)
    payload = read_json(path, {})
    if isinstance(payload, dict) and payload.get("rows"):
        return payload
    from mvp_qaic_reflex_ui.migration_os import build_migration_tracker_payload

    built = build_migration_tracker_payload()
    return built if isinstance(built, dict) else {"rows": []}


def apply_overlay_to_rows(
    rows: list[dict[str, Any]], overlay: dict[str, Any]
) -> list[dict[str, Any]]:
    by_source = overlay_by_source(overlay)
    merged: list[dict[str, Any]] = []
    for row in rows:
        if not isinstance(row, dict):
            continue
        copied = dict(row)
        source = row_source(copied)
        decision = by_source.get(source)
        if decision:
            copied["decision_override"] = True
            copied["decision_status"] = decision.get("decision_status")
            copied["decision_note"] = decision.get("note", "")
            copied["decision_reviewer"] = decision.get("reviewer", "")
            copied["decision_updated_at_utc"] = decision.get("updated_at_utc", "")
            if decision.get("target"):
                copied["target"] = decision.get("target")
                copied["cible"] = decision.get("target")
            copied["status"] = decision.get("decision_status")
            copied["Statut"] = decision.get("decision_status")
        else:
            copied.setdefault("decision_override", False)
        merged.append(copied)
    return merged


def build_decision_queue(
    repo_root: str | Path = ".",
    *,
    statuses: set[str] | None = None,
    limit: int = 200,
) -> dict[str, Any]:
    payload = load_live_payload(repo_root)
    overlay = load_decision_overlay(repo_root)
    rows = payload.get("rows", [])
    if not isinstance(rows, list):
        rows = []
    merged_rows = apply_overlay_to_rows([r for r in rows if isinstance(r, dict)], overlay)
    allowed_statuses = statuses or DEFAULT_REVIEW_STATUSES
    queue = [row for row in merged_rows if row_status(row) in allowed_statuses]
    queue = queue[: max(0, int(limit))]
    return {
        "version": "0.1.0",
        "generated_at_utc": utc_now(),
        "source_live_hash": payload.get("data_hash")
        or payload.get("live_meta", {}).get("data_hash"),
        "queue_count": len(queue),
        "overlay_decision_count": len(overlay.get("decisions", [])),
        "allowed_statuses": sorted(allowed_statuses),
        "rows": queue,
    }


def export_decision_queue(repo_root: str | Path = ".", *, limit: int = 200) -> dict[str, Any]:
    queue = build_decision_queue(repo_root, limit=limit)
    write_json_atomic(repo_path(repo_root, DECISION_QUEUE_REL), queue)
    return queue


# P_REFLEX_12H1B_BEGIN_UI_COMPONENTS
try:
    import reflex as rx
except Exception:  # noqa: BLE001
    rx = None  # type: ignore[assignment]


MIGRATION_DECISION_WORKBENCH_ROUTE = "/migration/decisions"


def _require_reflex() -> Any:
    if rx is None:
        raise RuntimeError("reflex is required to render migration decision workbench")
    return rx


def _safe_text(value: Any, default: str = "-") -> str:
    text = str(value or "").strip()
    return text or default


def _decision_row_card(row: dict[str, Any]) -> Any:
    reflex = _require_reflex()
    source = _safe_text(row.get("source") or row.get("Source") or row.get("name"))
    status = _safe_text(row.get("decision_status") or row.get("status") or row.get("Statut"))
    target = _safe_text(row.get("target") or row.get("cible") or row.get("Cible"))
    note = _safe_text(row.get("decision_note") or row.get("note"), "")

    return reflex.card(
        reflex.vstack(
            reflex.hstack(
                reflex.badge(status),
                reflex.text(source, size="2", weight="bold"),
                spacing="2",
                flex_wrap="wrap",
            ),
            reflex.text(f"Cible: {target}", size="2"),
            reflex.cond(note != "", reflex.text(note, size="1"), reflex.text("", size="1")),
            spacing="2",
            width="100%",
        ),
        width="100%",
    )


def migration_decision_workbench_compact_panel(limit: int = 6) -> Any:
    reflex = _require_reflex()
    queue = build_decision_queue(".", limit=limit)
    rows = [row for row in queue.get("rows", []) if isinstance(row, dict)][:limit]
    cards = [_decision_row_card(row) for row in rows]

    return reflex.card(
        reflex.vstack(
            reflex.hstack(
                reflex.heading("Migration Decision Workbench", size="4"),
                reflex.badge(f"queue={queue.get('queue_count', 0)}"),
                reflex.badge(f"overlay={queue.get('overlay_decision_count', 0)}"),
                spacing="2",
                flex_wrap="wrap",
            ),
            reflex.text(
                "Revue humaine des lignes à migrer. Écritures via overlay JSON, aucun ordre, aucun broker.",
                size="2",
            ),
            *cards,
            reflex.hstack(
                reflex.link(
                    reflex.button("Ouvrir le workbench"),
                    href=MIGRATION_DECISION_WORKBENCH_ROUTE,
                ),
                reflex.link(
                    reflex.button("Migration globale"),
                    href="/migration/global",
                ),
                spacing="3",
                flex_wrap="wrap",
            ),
            spacing="3",
            width="100%",
        ),
        width="100%",
    )


def migration_decision_workbench_page() -> Any:
    reflex = _require_reflex()
    queue = build_decision_queue(".", limit=40)
    rows = [row for row in queue.get("rows", []) if isinstance(row, dict)][:40]
    cards = [_decision_row_card(row) for row in rows]

    return reflex.container(
        reflex.vstack(
            reflex.heading("Migration Decision Workbench", size="6"),
            reflex.text(
                "Queue de décision migration alimentée par MIGRATION_OS_LIVE_PAYLOAD.json et MIGRATION_DECISION_OVERLAY.json.",
                size="2",
            ),
            reflex.hstack(
                reflex.badge(f"queue={queue.get('queue_count', 0)}"),
                reflex.badge(f"overlay={queue.get('overlay_decision_count', 0)}"),
                reflex.badge(f"hash={queue.get('source_live_hash', '-')}"),
                spacing="3",
                flex_wrap="wrap",
            ),
            *cards,
            reflex.link(reflex.button("Retour Mission Control"), href="/"),
            spacing="4",
            width="100%",
        ),
        size="4",
        padding_y="1.5rem",
    )


# P_REFLEX_12H1B_END_UI_COMPONENTS
