from __future__ import annotations

import argparse
import csv
import json
import re
import sys
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

VERSION = "MVP_QAIC_P143B_DATA_PREVIEW_SOURCE_EXPANSION_1.0.0_SAFE"
STATUS_BOUND = "P143B_DATA_PREVIEW_SOURCE_EXPANSION_RENDERED_LOCAL_READONLY"

SAFETY_MARKERS = {
    "source": "LOCAL_EXPORTS_RECURSIVE_CSV_METADATA_FALLBACK",
    "live_google_sheets_read": False,
    "google_sheets_write": False,
    "apps_script_execution": False,
    "clasp_push": False,
    "broker": False,
    "order": False,
    "sizing": False,
    "auto_apply_gem_response": False,
    "public_deploy": False,
}


@dataclass(frozen=True)
class SourceExpansionRequest:
    p142_spec_path: Path
    source_root: Path
    output_dir: Path
    run_id: str
    generated_at_utc: str
    max_preview_rows: int
    max_sources: int


def utc_now_iso() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def normalize(value: str) -> str:
    value = value.lower()
    value = (
        value.replace("📘", " ")
        .replace("🎛️", " ")
        .replace("🚀", " ")
        .replace("🧩", " ")
        .replace("🧠", " ")
        .replace("🔗", " ")
        .replace("🤖", " ")
    )
    return re.sub(r"[^a-z0-9]+", "_", value).strip("_")


def token_set(value: str) -> set[str]:
    return {token for token in normalize(value).split("_") if len(token) >= 3}


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def read_csv(path: Path, max_rows: int) -> tuple[list[str], list[dict[str, str]], int]:
    total = 0
    try:
        with path.open("r", encoding="utf-8-sig", newline="") as handle:
            reader = csv.DictReader(handle)
            headers = [str(field) for field in (reader.fieldnames or [])]
            rows: list[dict[str, str]] = []
            for row in reader:
                total += 1
                if len(rows) < max_rows:
                    rows.append({str(k): "" if v is None else str(v) for k, v in row.items()})
            return headers, rows, total
    except UnicodeDecodeError:
        with path.open("r", encoding="cp1252", newline="") as handle:
            reader = csv.DictReader(handle)
            headers = [str(field) for field in (reader.fieldnames or [])]
            rows = []
            for row in reader:
                total += 1
                if len(rows) < max_rows:
                    rows.append({str(k): "" if v is None else str(v) for k, v in row.items()})
            return headers, rows, total


def discover_sources(root: Path, max_sources: int) -> list[dict[str, Any]]:
    if not root.exists():
        raise FileNotFoundError(f"source_root not found: {root}")

    sources: list[dict[str, Any]] = []
    for path in sorted(root.rglob("*.csv")):
        if path.name.lower() == "desktop.ini":
            continue
        rel = path.relative_to(root).as_posix()
        # Ignore smoke/summary outputs unless they carry likely cockpit names.
        lower = path.name.lower()
        if "route_smoke" in lower or "summary" in lower:
            continue
        headers, rows, total = read_csv(path, max_rows=3)
        src_text = " ".join([path.stem, rel, " ".join(headers)])
        sources.append(
            {
                "path": str(path),
                "relative_path": rel,
                "filename": path.name,
                "stem": path.stem,
                "normalized": normalize(src_text),
                "tokens": sorted(token_set(src_text)),
                "headers": headers,
                "sample_rows": rows,
                "total_rows": total,
                "size_bytes": path.stat().st_size,
            }
        )
        if len(sources) >= max_sources:
            break
    return sources


def score_source(page: dict[str, Any], source: dict[str, Any]) -> int:
    page_text = " ".join(
        [
            str(page.get("title", "")),
            str(page.get("route", "")),
            str(page.get("page_id", "")),
            " ".join(str(c) for c in page.get("primary_columns", [])),
        ]
    )
    page_tokens = token_set(page_text)
    source_tokens = set(source.get("tokens", []))
    if not page_tokens:
        return 0

    overlap = len(page_tokens & source_tokens)
    score = overlap * 10

    title_norm = normalize(str(page.get("title", "")))
    src_norm = str(source.get("normalized", ""))
    if title_norm and title_norm in src_norm:
        score += 80
    if "prompt_library" in title_norm and "prompt_library" in src_norm:
        score += 120
    if "runtime" in title_norm and "runtime" in src_norm:
        score += 60
    if "queue" in title_norm and "queue" in src_norm:
        score += 60

    page_cols = {normalize(str(c)) for c in page.get("primary_columns", [])}
    src_headers = {normalize(str(c)) for c in source.get("headers", [])}
    score += len(page_cols & src_headers) * 15
    return score


def best_source(
    page: dict[str, Any], sources: list[dict[str, Any]]
) -> tuple[dict[str, Any] | None, int]:
    scored = [(score_source(page, source), source) for source in sources]
    scored = [(score, source) for score, source in scored if score > 0]
    if not scored:
        return None, 0
    scored.sort(key=lambda item: (-item[0], item[1]["relative_path"]))
    return scored[0][1], scored[0][0]


def metadata_fallback_rows(page: dict[str, Any]) -> tuple[list[str], list[dict[str, str]]]:
    columns = [str(c) for c in page.get("primary_columns", [])]
    if not columns:
        columns = ["page_id", "title", "route", "domain"]
    row = {col: "" for col in columns}
    for key in ("page_id", "title", "route", "domain"):
        if key in row:
            row[key] = str(page.get(key, ""))
    return columns, [row]


def build_expanded_binding(
    p142_spec: dict[str, Any], source_root: Path, max_preview_rows: int, max_sources: int
) -> dict[str, Any]:
    if p142_spec.get("status") != "P142_UI_FIDELITY_SHELL_RENDERED":
        raise ValueError(f"Invalid P142 status: {p142_spec.get('status')}")
    sources = discover_sources(source_root, max_sources=max_sources)
    bindings: list[dict[str, Any]] = []

    for page in p142_spec.get("pages", []):
        source, score = best_source(page, sources)
        if source:
            headers, rows, total = read_csv(Path(str(source["path"])), max_rows=max_preview_rows)
            mode = "csv_match"
            reason = ""
            source_path = source["path"]
            source_file = source["filename"]
        else:
            headers, rows = metadata_fallback_rows(page)
            total = len(rows)
            mode = "metadata_fallback"
            reason = "NO_LOCAL_CSV_MATCH"
            source_path = ""
            source_file = ""
        bindings.append(
            {
                "page_id": page.get("page_id"),
                "title": page.get("title"),
                "route": page.get("route"),
                "domain": page.get("domain"),
                "binding_mode": mode,
                "match_score": score,
                "source_csv": source_path,
                "source_filename": source_file,
                "source_rows_total": total,
                "source_headers": headers,
                "preview_rows": rows[:max_preview_rows],
                "preview_row_count": min(len(rows), max_preview_rows),
                "missing_source_reason": reason,
            }
        )

    csv_match_count = sum(1 for item in bindings if item["binding_mode"] == "csv_match")
    fallback_count = sum(1 for item in bindings if item["binding_mode"] == "metadata_fallback")
    return {
        "status": STATUS_BOUND,
        "version": VERSION,
        "source_p142_status": p142_spec.get("status"),
        "source_root": str(source_root),
        "source_csv_count": len(sources),
        "cockpit_page_count": len(bindings),
        "csv_match_page_count": csv_match_count,
        "metadata_fallback_page_count": fallback_count,
        "bound_page_count": len(bindings),
        "max_preview_rows": max_preview_rows,
        "bindings": bindings,
        "safety": dict(SAFETY_MARKERS),
        "next": "P144_PROMPT_COCKPIT_WORKFLOWS",
    }


def render_app(binding: dict[str, Any]) -> str:
    binding_repr = repr(json.dumps(binding, ensure_ascii=False, indent=2, sort_keys=True))
    return "\n".join(
        [
            "from __future__ import annotations",
            "import json",
            "from nicegui import ui",
            f"BINDING = json.loads({binding_repr})",
            "",
            "@ui.page('/')",
            "def index():",
            "    ui.label('MVP QAIC — Data preview binding').classes('text-h4')",
            "    ui.label('Local read-only preview. No Sheet write / no broker / no public deploy.').classes('text-caption')",
            "    with ui.row().classes('q-gutter-sm q-mt-md'):",
            "        ui.badge(f\"pages {BINDING['cockpit_page_count']}\")",
            "        ui.badge(f\"csv matches {BINDING['csv_match_page_count']}\")",
            "        ui.badge(f\"fallback {BINDING['metadata_fallback_page_count']}\")",
            "    for item in BINDING['bindings']:",
            "        with ui.card().classes('q-mt-md'):",
            "            ui.label(item['title']).classes('text-subtitle1')",
            "            ui.label(item['route']).classes('text-caption')",
            "            ui.badge(item['binding_mode'])",
            "            columns = [{'name': h, 'label': h, 'field': h} for h in item.get('source_headers', [])[:20]]",
            "            ui.table(columns=columns, rows=item.get('preview_rows', []), row_key='id').classes('q-mt-sm')",
            "",
            "if __name__ in {'__main__', '__mp_main__'}:",
            "    ui.run(host='127.0.0.1', port=8088, reload=False, show=True)",
            "",
        ]
    )


def write_outputs(binding: dict[str, Any], output_dir: Path) -> dict[str, str]:
    output_dir.mkdir(parents=True, exist_ok=True)
    binding_path = output_dir / "P143B_DATA_PREVIEW_EXPANDED_BINDING.json"
    app_path = output_dir / "P143B_NICEGUI_DATA_PREVIEW_APP.py"
    csv_path = output_dir / "P143B_BINDING_SUMMARY.csv"
    md_path = output_dir / "P143B_DATA_PREVIEW_SOURCE_EXPANSION.md"
    summary_path = output_dir / "P143B_SUMMARY.json"

    binding_path.write_text(
        json.dumps(binding, ensure_ascii=False, indent=2, sort_keys=True), encoding="utf-8"
    )
    app_path.write_text(render_app(binding), encoding="utf-8")
    with csv_path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=[
                "title",
                "route",
                "binding_mode",
                "match_score",
                "source_filename",
                "preview_row_count",
                "missing_source_reason",
            ],
        )
        writer.writeheader()
        for item in binding["bindings"]:
            writer.writerow({field: item.get(field, "") for field in writer.fieldnames})

    md_path.write_text(
        "\n".join(
            [
                "# P143B — Data Preview Source Expansion",
                "",
                f"- Status: `{binding['status']}`",
                f"- CSV sources scanned: `{binding['source_csv_count']}`",
                f"- Bound pages: `{binding['bound_page_count']}`",
                f"- CSV matches: `{binding['csv_match_page_count']}`",
                f"- Metadata fallback: `{binding['metadata_fallback_page_count']}`",
                "",
                "Safety: local only, no live Sheets read, no Sheet write, no broker/order/sizing, no public deploy.",
                "",
                f"Next: `{binding['next']}`",
                "",
            ]
        ),
        encoding="utf-8",
    )

    summary = {
        "status": binding["status"],
        "source_csv_count": binding["source_csv_count"],
        "cockpit_page_count": binding["cockpit_page_count"],
        "csv_match_page_count": binding["csv_match_page_count"],
        "metadata_fallback_page_count": binding["metadata_fallback_page_count"],
        "bound_page_count": binding["bound_page_count"],
        "google_sheets_write": False,
        "live_google_sheets_read": False,
        "public_deploy": False,
        "output_dir": str(output_dir),
        "next": binding["next"],
    }
    summary_path.write_text(
        json.dumps(summary, ensure_ascii=False, indent=2, sort_keys=True), encoding="utf-8"
    )
    return {
        "binding_json": str(binding_path),
        "preview_app_py": str(app_path),
        "summary_csv": str(csv_path),
        "markdown": str(md_path),
        "summary_json": str(summary_path),
    }


def run_expansion(request: SourceExpansionRequest) -> dict[str, Any]:
    spec = load_json(request.p142_spec_path)
    binding = build_expanded_binding(
        spec, request.source_root, request.max_preview_rows, request.max_sources
    )
    binding["run_id"] = request.run_id
    binding["generated_at_utc"] = request.generated_at_utc
    binding["source_p142_spec_path"] = str(request.p142_spec_path)
    outputs = write_outputs(binding, request.output_dir)
    binding["output_files"] = outputs
    (request.output_dir / "P143B_DATA_PREVIEW_EXPANDED_BINDING.json").write_text(
        json.dumps(binding, ensure_ascii=False, indent=2, sort_keys=True),
        encoding="utf-8",
    )
    return binding


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="P143B data preview source expansion.")
    parser.add_argument("--p142-spec", required=True)
    parser.add_argument("--source-root", required=True)
    parser.add_argument("--output-dir", required=True)
    parser.add_argument("--run-id", default="P143B-DATA-PREVIEW-SOURCE-EXPANSION")
    parser.add_argument("--generated-at-utc", default=utc_now_iso())
    parser.add_argument("--max-preview-rows", type=int, default=25)
    parser.add_argument("--max-sources", type=int, default=500)
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    binding = run_expansion(
        SourceExpansionRequest(
            p142_spec_path=Path(args.p142_spec),
            source_root=Path(args.source_root),
            output_dir=Path(args.output_dir),
            run_id=args.run_id,
            generated_at_utc=args.generated_at_utc,
            max_preview_rows=args.max_preview_rows,
            max_sources=args.max_sources,
        )
    )
    print(binding["status"])
    print(f"source_csv_count={binding['source_csv_count']}")
    print(f"bound_page_count={binding['bound_page_count']}")
    print(f"csv_match_page_count={binding['csv_match_page_count']}")
    print(f"metadata_fallback_page_count={binding['metadata_fallback_page_count']}")
    print("google_sheets_write=false")
    print("live_google_sheets_read=false")
    print(f"output_dir={args.output_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
