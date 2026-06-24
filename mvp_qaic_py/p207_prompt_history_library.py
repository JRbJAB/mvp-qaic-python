from __future__ import annotations

from dataclasses import asdict, dataclass
from datetime import datetime, timezone
import json
from pathlib import Path
from typing import Any

SCAN_ROOTS = ("01_OPERATOR_INPUTS", "mvp_qaic_py", "docs/INDEX")
PROMPT_KEYWORDS = ("prompt", "gem", "capture", "session", "response")
TEXT_EXTENSIONS = (".md", ".txt", ".json", ".py")
MAX_FILES_PER_ROOT = 80
MAX_PREVIEW_BYTES = 6000
MAX_PREVIEW_CHARS = 900


@dataclass(frozen=True)
class PromptHistoryEntry:
    prompt_id: str
    source_root: str
    path: str
    title: str
    extension: str
    size_bytes: int
    preview: str


def _utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def _safe_relative(path: Path, root: Path) -> str:
    try:
        return path.relative_to(root).as_posix()
    except ValueError:
        return path.as_posix()


def _looks_prompt_related(path: Path) -> bool:
    name = path.name.lower()
    return any(keyword in name for keyword in PROMPT_KEYWORDS)


def _read_preview(path: Path) -> str:
    try:
        with path.open("rb") as handle:
            raw = handle.read(MAX_PREVIEW_BYTES)
    except OSError:
        return ""

    text = raw.decode("utf-8", errors="replace")
    return " ".join(text.split())[:MAX_PREVIEW_CHARS]


def _iter_prompt_files(root: Path, scan_root: str, max_files: int) -> list[Path]:
    base = root / scan_root
    if not base.exists():
        return []

    files: list[Path] = []
    for path in base.rglob("*"):
        if len(files) >= max_files:
            break
        if not path.is_file():
            continue
        if path.suffix.lower() not in TEXT_EXTENSIONS:
            continue
        if not _looks_prompt_related(path):
            continue
        files.append(path)

    return sorted(files, key=lambda item: item.as_posix().lower())


def build_prompt_history_library(
    project_root: str | Path,
    *,
    generated_at: str | None = None,
    max_files_per_root: int = MAX_FILES_PER_ROOT,
) -> dict[str, Any]:
    root = Path(project_root).resolve()
    entries: list[PromptHistoryEntry] = []

    for scan_root in SCAN_ROOTS:
        for path in _iter_prompt_files(root, scan_root, max_files_per_root):
            try:
                size_bytes = path.stat().st_size
            except OSError:
                size_bytes = 0

            relative_path = _safe_relative(path, root)
            prompt_id = relative_path.replace("/", "__").replace("\\", "__")

            entries.append(
                PromptHistoryEntry(
                    prompt_id=prompt_id,
                    source_root=scan_root,
                    path=relative_path,
                    title=path.stem,
                    extension=path.suffix.lower(),
                    size_bytes=size_bytes,
                    preview=_read_preview(path),
                )
            )

    status = "OK_P207_PROMPT_HISTORY_LIBRARY_READY"
    if not entries:
        status = "REVIEW_P207_PROMPT_HISTORY_LIBRARY_EMPTY"

    return {
        "STATUS": status,
        "generated_at": generated_at or _utc_now(),
        "project_root": str(root),
        "scan_roots": list(SCAN_ROOTS),
        "entry_count": len(entries),
        "entries": [asdict(entry) for entry in entries],
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
        "recommended_next": "P208_PROMPT_HISTORY_UI_BINDING_FAST_FUSE",
    }


def write_prompt_history_library(
    project_root: str | Path,
    output_dir: str | Path,
    *,
    generated_at: str | None = None,
) -> dict[str, Any]:
    output = Path(output_dir)
    output.mkdir(parents=True, exist_ok=True)

    payload = build_prompt_history_library(project_root, generated_at=generated_at)
    json_path = output / "P207_PROMPT_HISTORY_LIBRARY.json"
    md_path = output / "P207_PROMPT_HISTORY_LIBRARY.md"

    json_path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True),
        encoding="utf-8",
    )

    lines = [
        "# P207 — Prompt History Library",
        "",
        f"- Status: `{payload['STATUS']}`",
        f"- Entry count: `{payload['entry_count']}`",
        "- Local only: `true`",
        "- Review only: `true`",
        "",
        "## Entries",
        "",
    ]

    for entry in payload["entries"]:
        lines.append(f"- `{entry['path']}` — `{entry['title']}`")

    if not payload["entries"]:
        lines.append("- No prompt-related local files detected.")

    md_path.write_text("\n".join(lines) + "\n", encoding="utf-8")

    return {
        **payload,
        "json_path": str(json_path),
        "md_path": str(md_path),
    }


def main() -> None:
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--project-root", default=".")
    parser.add_argument("--output-dir", required=True)
    parser.add_argument("--generated-at", default=None)
    args = parser.parse_args()

    payload = write_prompt_history_library(
        args.project_root,
        args.output_dir,
        generated_at=args.generated_at,
    )
    print(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
