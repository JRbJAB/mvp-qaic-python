"""Local read-only data binding for the MVP QAIC Reflex shell."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from .registry import DOCS_REGISTRY, REPO_ROOT, SAFETY_FLAGS


@dataclass(frozen=True)
class LocalDataSource:
    source_id: str
    title: str
    path: str
    kind: str
    exists: bool
    status: str


def _exists(relative_path: str) -> bool:
    return (REPO_ROOT / Path(relative_path)).exists()


def docs_registry_sources() -> list[LocalDataSource]:
    sources: list[LocalDataSource] = []
    for doc in DOCS_REGISTRY:
        path = str(doc["path"])
        sources.append(
            LocalDataSource(
                source_id=str(doc["doc_id"]),
                title=str(doc["title"]),
                path=path,
                kind=str(doc["kind"]),
                exists=_exists(path),
                status=str(doc["status"]),
            )
        )
    return sources


def export_evidence_sources(limit: int = 12) -> list[LocalDataSource]:
    export_root = REPO_ROOT / "05_EXPORTS"
    if not export_root.exists():
        return []

    dirs = sorted(
        [path for path in export_root.iterdir() if path.is_dir()],
        key=lambda path: path.stat().st_mtime,
        reverse=True,
    )[:limit]

    return [
        LocalDataSource(
            source_id=path.name,
            title=path.name,
            path=path.relative_to(REPO_ROOT).as_posix(),
            kind="export_dir",
            exists=True,
            status="LOCAL_READONLY",
        )
        for path in dirs
    ]


def build_local_data_binding_payload() -> dict[str, object]:
    docs = docs_registry_sources()
    exports = export_evidence_sources()

    missing_docs = [source.source_id for source in docs if not source.exists]

    return {
        "binding_mode": "LOCAL_READONLY",
        "server_required": False,
        "browser_required": False,
        "public_deploy_required": False,
        "live_action_required": False,
        "sheet_write_allowed": False,
        "bigquery_write_allowed": False,
        "broker_action_allowed": False,
        "safety_flags": SAFETY_FLAGS,
        "docs_source_count": len(docs),
        "export_source_count": len(exports),
        "missing_doc_sources": missing_docs,
        "docs_sources": [source.__dict__ for source in docs],
        "export_sources": [source.__dict__ for source in exports],
    }
