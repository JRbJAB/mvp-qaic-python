from __future__ import annotations

from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

from mvp_qaic_py.p207_prompt_history_library import build_prompt_history_library

MAX_UI_CARDS = 50


@dataclass(frozen=True)
class PromptHistoryCard:
    card_id: str
    title: str
    path: str
    source_root: str
    extension: str
    size_bytes: int
    preview: str
    actions: tuple[str, ...]


def _normalize(text: str) -> str:
    return " ".join(str(text).lower().split())


def _matches_query(entry: dict[str, Any], query: str) -> bool:
    normalized_query = _normalize(query)
    if not normalized_query:
        return True

    haystack = _normalize(
        " ".join(
            [
                str(entry.get("prompt_id", "")),
                str(entry.get("title", "")),
                str(entry.get("path", "")),
                str(entry.get("preview", "")),
                str(entry.get("source_root", "")),
            ]
        )
    )
    return normalized_query in haystack


def _build_counters(entries: list[dict[str, Any]]) -> dict[str, Any]:
    by_source_root: dict[str, int] = {}
    by_extension: dict[str, int] = {}

    for entry in entries:
        source_root = str(entry.get("source_root") or "UNKNOWN")
        extension = str(entry.get("extension") or "UNKNOWN")
        by_source_root[source_root] = by_source_root.get(source_root, 0) + 1
        by_extension[extension] = by_extension.get(extension, 0) + 1

    return {
        "total_entries": len(entries),
        "by_source_root": dict(sorted(by_source_root.items())),
        "by_extension": dict(sorted(by_extension.items())),
    }


def _to_card(entry: dict[str, Any]) -> PromptHistoryCard:
    return PromptHistoryCard(
        card_id=str(entry.get("prompt_id") or entry.get("path") or "UNKNOWN"),
        title=str(entry.get("title") or "Untitled prompt"),
        path=str(entry.get("path") or ""),
        source_root=str(entry.get("source_root") or "UNKNOWN"),
        extension=str(entry.get("extension") or ""),
        size_bytes=int(entry.get("size_bytes") or 0),
        preview=str(entry.get("preview") or ""),
        actions=(
            "Copier le prompt",
            "Ouvrir source locale",
            "Sauver réponse GEM localement",
            "Créer session review-only",
        ),
    )


def build_prompt_history_ui_binding(
    project_root: str | Path,
    *,
    query: str = "",
    generated_at: str | None = None,
    max_cards: int = MAX_UI_CARDS,
) -> dict[str, Any]:
    library = build_prompt_history_library(
        project_root,
        generated_at=generated_at,
    )

    entries = list(library.get("entries", []))
    filtered_entries = [entry for entry in entries if _matches_query(entry, query)]
    cards = [_to_card(entry) for entry in filtered_entries[:max_cards]]

    status = "OK_P208_PROMPT_HISTORY_UI_BINDING_READY"
    if not entries:
        status = "REVIEW_P208_PROMPT_HISTORY_UI_BINDING_EMPTY_LIBRARY"
    elif query and not filtered_entries:
        status = "REVIEW_P208_PROMPT_HISTORY_UI_BINDING_NO_QUERY_RESULT"

    return {
        "STATUS": status,
        "generated_at": library.get("generated_at"),
        "project_root": library.get("project_root"),
        "query": query,
        "library_entry_count": len(entries),
        "filtered_entry_count": len(filtered_entries),
        "card_count": len(cards),
        "counters": _build_counters(entries),
        "ui": {
            "title": "Prompt History Library",
            "subtitle": "Historique local des prompts, captures et réponses GEM",
            "search_placeholder": "Rechercher prompt, GEM, capture, session...",
            "tabs": [
                "Tous",
                "Prompt GEM",
                "Captures",
                "Sessions",
                "Réponses",
                "Review-only",
            ],
            "primary_actions": [
                "Copier le prompt",
                "Sauver réponse GEM localement",
                "Créer session review-only",
            ],
        },
        "cards": [asdict(card) for card in cards],
        "local_only": True,
        "review_only": True,
        "server_started": False,
        "browser_started": False,
        "gem_call_executed": False,
        "auto_apply_gem_response": False,
        "google_sheets_write": False,
        "apps_script_execution": False,
        "broker": False,
        "order": False,
        "sizing": False,
        "recommended_next": "P209_PROMPT_HISTORY_PRIVATE_COCKPIT_WIRING_FAST_FUSE",
    }


def build_prompt_history_ui_markdown(payload: dict[str, Any]) -> str:
    lines = [
        "# Prompt History Library",
        "",
        f"Status: `{payload['STATUS']}`",
        f"Query: `{payload.get('query', '')}`",
        f"Cards: `{payload.get('card_count', 0)}`",
        "",
        "## Cards",
        "",
    ]

    cards = payload.get("cards", [])
    if not cards:
        lines.append("- Aucun résultat.")
    else:
        for card in cards:
            lines.append(f"- **{card['title']}** — `{card['path']}`")

    return "\n".join(lines) + "\n"


def main() -> None:
    import argparse
    import json

    parser = argparse.ArgumentParser()
    parser.add_argument("--project-root", default=".")
    parser.add_argument("--query", default="")
    parser.add_argument("--generated-at", default=None)
    args = parser.parse_args()

    payload = build_prompt_history_ui_binding(
        args.project_root,
        query=args.query,
        generated_at=args.generated_at,
    )
    print(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
