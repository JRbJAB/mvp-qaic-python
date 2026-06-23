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

VERSION = "MVP_QAIC_P143_R1_PREVIEW_ARG_FIX_1.0.0_SAFE"
STATUS_BOUND = "P143_DATA_PREVIEW_BINDING_RENDERED_LOCAL_READONLY"

SAFETY_MARKERS = {
    "source": "LOCAL_CSV_PREVIEW_ONLY",
    "live_google_sheets_read": False,
    "google_sheets_write": False,
    "apps_script_execution": False,
    "clasp_push": False,
    "broker": False,
    "order": False,
    "sizing": False,
    "auto_apply_gem_response": False,
    "public_deploy": False,
    "localhost_only": True,
}


@dataclass(frozen=True)
class BindingRequest:
    p142_spec_path: Path
    source_csv_root: Path
    output_dir: Path
    run_id: str
    generated_at_utc: str
    max_preview_rows: int


def utc_now_iso() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def normalize_name(value: str) -> str:
    value = value.lower()
    value = (
        value.replace("📘", "")
        .replace("🎛️", "")
        .replace("🚀", "")
        .replace("🧩", "")
        .replace("🧠", "")
        .replace("🔗", "")
        .replace("🤖", "")
    )
    value = re.sub(r"[^a-z0-9]+", "_", value).strip("_")
    return value


def read_csv_preview(path: Path, max_rows: int) -> tuple[list[str], list[dict[str, str]], int]:
    rows_read = 0
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        headers = [str(field) for field in (reader.fieldnames or [])]
        rows: list[dict[str, str]] = []
        for row in reader:
            rows_read += 1
            if len(rows) < max_rows:
                rows.append(
                    {str(key): "" if value is None else str(value) for key, value in row.items()}
                )
    return headers, rows, rows_read


def discover_csv_sources(root: Path) -> list[dict[str, Any]]:
    if not root.exists():
        raise FileNotFoundError(f"CSV source root not found: {root}")

    sources: list[dict[str, Any]] = []
    for path in sorted(root.rglob("*.csv")):
        if path.name.lower() == "desktop.ini":
            continue
        title_candidate = path.stem
        sources.append(
            {
                "path": str(path),
                "filename": path.name,
                "stem": path.stem,
                "normalized": normalize_name(title_candidate),
                "size_bytes": path.stat().st_size,
            }
        )
    return sources


def match_source_for_page(
    page: dict[str, Any], sources: list[dict[str, Any]]
) -> dict[str, Any] | None:
    title = str(page.get("title", ""))
    title_norm = normalize_name(title)
    route_norm = normalize_name(str(page.get("route", "")))
    page_id_norm = normalize_name(str(page.get("page_id", "")))

    candidates: list[tuple[int, dict[str, Any]]] = []
    for source in sources:
        src = str(source["normalized"])
        score = 0
        if src == title_norm:
            score += 100
        if title_norm and (title_norm in src or src in title_norm):
            score += 70
        if page_id_norm and (page_id_norm in src or src in page_id_norm):
            score += 40
        if route_norm and (src in route_norm or route_norm in src):
            score += 20
        if score > 0:
            candidates.append((score, source))
    if not candidates:
        return None
    candidates.sort(key=lambda item: (-item[0], str(item[1]["filename"])))
    return candidates[0][1]


def build_binding(
    p142_spec: dict[str, Any], source_csv_root: Path, max_preview_rows: int
) -> dict[str, Any]:
    if p142_spec.get("status") != "P142_UI_FIDELITY_SHELL_RENDERED":
        raise ValueError(f"Invalid P142 spec status: {p142_spec.get('status')}")

    sources = discover_csv_sources(source_csv_root)
    pages = p142_spec.get("pages", [])
    bindings: list[dict[str, Any]] = []

    for page in pages:
        matched = match_source_for_page(page, sources)
        if matched:
            headers, rows, total_rows = read_csv_preview(
                Path(str(matched["path"])), max_rows=max_preview_rows
            )
            bindings.append(
                {
                    "page_id": page.get("page_id"),
                    "title": page.get("title"),
                    "route": page.get("route"),
                    "domain": page.get("domain"),
                    "matched": True,
                    "source_csv": matched["path"],
                    "source_filename": matched["filename"],
                    "source_rows_total": total_rows,
                    "source_headers": headers,
                    "preview_rows": rows,
                    "preview_row_count": len(rows),
                    "missing_source_reason": "",
                }
            )
        else:
            bindings.append(
                {
                    "page_id": page.get("page_id"),
                    "title": page.get("title"),
                    "route": page.get("route"),
                    "domain": page.get("domain"),
                    "matched": False,
                    "source_csv": "",
                    "source_filename": "",
                    "source_rows_total": 0,
                    "source_headers": [],
                    "preview_rows": [],
                    "preview_row_count": 0,
                    "missing_source_reason": "NO_LOCAL_CSV_MATCH",
                }
            )

    matched_count = sum(1 for item in bindings if item["matched"])
    return {
        "status": STATUS_BOUND,
        "version": VERSION,
        "source_p142_status": p142_spec.get("status"),
        "source_csv_root": str(source_csv_root),
        "source_csv_count": len(sources),
        "cockpit_page_count": len(pages),
        "matched_page_count": matched_count,
        "unmatched_page_count": len(bindings) - matched_count,
        "max_preview_rows": max_preview_rows,
        "bindings": bindings,
        "safety": dict(SAFETY_MARKERS),
        "next": "P144_PROMPT_COCKPIT_WORKFLOWS",
    }


def render_preview_app(binding: dict[str, Any]) -> str:
    binding_repr = repr(json.dumps(binding, ensure_ascii=False, indent=2, sort_keys=True))
    lines = [
        "from __future__ import annotations",
        "import json",
        "from nicegui import ui",
        "",
        f"BINDING = json.loads({binding_repr})",
        "",
        "def _badge(text: str):",
        "    ui.badge(text).classes('q-mr-xs')",
        "",
        "@ui.page('/')",
        "def index():",
        "    ui.label('MVP QAIC — Cockpit data preview').classes('text-h4 q-mb-sm')",
        "    ui.label('Local CSV preview only — no Sheet write / no broker / no public deploy').classes('text-caption')",
        "    with ui.row().classes('q-gutter-sm q-mt-md'):",
        "        _badge(f\"pages {BINDING['cockpit_page_count']}\")",
        "        _badge(f\"matched {BINDING['matched_page_count']}\")",
        "        _badge(f\"csv {BINDING['source_csv_count']}\")",
        "    with ui.row().classes('q-gutter-md q-mt-lg'):",
        "        for item in BINDING['bindings']:",
        "            with ui.card().classes('w-96'):",
        "                ui.label(item['title']).classes('text-subtitle1')",
        "                ui.label(item['route']).classes('text-caption')",
        "                _badge('matched' if item['matched'] else 'no csv')",
        "                _badge(str(item['preview_row_count']) + ' preview rows')",
        "                ui.link('open', item['route']).classes('q-mt-sm')",
        "",
        "for item in BINDING['bindings']:",
        "    route = item['route']",
        "    @ui.page(route)",
        "    def page_view(item=item):",
        "        ui.link('← Data preview', '/').classes('q-mb-md')",
        "        ui.label(item['title']).classes('text-h5')",
        "        ui.label(item.get('source_filename') or item.get('missing_source_reason')).classes('text-caption')",
        "        columns = [{'name': h, 'label': h, 'field': h} for h in item.get('source_headers', [])[:20]]",
        "        ui.table(columns=columns, rows=item.get('preview_rows', []), row_key='id').classes('q-mt-md')",
        "",
        "if __name__ in {'__main__', '__mp_main__'}:",
        "    ui.run(host='127.0.0.1', port=8088, reload=False, show=True)",
    ]
    return "\n".join(lines) + "\n"


def write_outputs(binding: dict[str, Any], output_dir: Path) -> dict[str, str]:
    output_dir.mkdir(parents=True, exist_ok=True)
    binding_path = output_dir / "P143_DATA_PREVIEW_BINDING.json"
    app_path = output_dir / "P143_NICEGUI_DATA_PREVIEW_APP.py"
    csv_path = output_dir / "P143_DATA_PREVIEW_BINDING_SUMMARY.csv"
    md_path = output_dir / "P143_DATA_PREVIEW_BINDING.md"
    summary_path = output_dir / "P143_SUMMARY.json"

    binding_path.write_text(
        json.dumps(binding, ensure_ascii=False, indent=2, sort_keys=True), encoding="utf-8"
    )
    app_path.write_text(render_preview_app(binding), encoding="utf-8")

    with csv_path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=[
                "title",
                "route",
                "domain",
                "matched",
                "source_filename",
                "source_rows_total",
                "preview_row_count",
                "missing_source_reason",
            ],
        )
        writer.writeheader()
        for row in binding["bindings"]:
            writer.writerow({field: row.get(field, "") for field in writer.fieldnames})

    lines = [
        "# P143 — Data Preview Binding Local Read-Only",
        "",
        f"- Status: `{binding['status']}`",
        f"- CSV sources: `{binding['source_csv_count']}`",
        f"- Pages: `{binding['cockpit_page_count']}`",
        f"- Matched pages: `{binding['matched_page_count']}`",
        f"- Unmatched pages: `{binding['unmatched_page_count']}`",
        "",
        "## Safety",
        "",
        "- Local CSV preview only",
        "- No live Sheets read",
        "- No Sheet write",
        "- No broker/order/sizing",
        "",
        f"Next: `{binding['next']}`",
        "",
    ]
    md_path.write_text("\n".join(lines), encoding="utf-8")

    summary = {
        "status": binding["status"],
        "source_csv_count": binding["source_csv_count"],
        "cockpit_page_count": binding["cockpit_page_count"],
        "matched_page_count": binding["matched_page_count"],
        "unmatched_page_count": binding["unmatched_page_count"],
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
        "binding_md": str(md_path),
        "summary_json": str(summary_path),
    }


def run_binding(request: BindingRequest) -> dict[str, Any]:
    p142_spec = load_json(request.p142_spec_path)
    binding = build_binding(p142_spec, request.source_csv_root, request.max_preview_rows)
    binding["run_id"] = request.run_id
    binding["generated_at_utc"] = request.generated_at_utc
    binding["source_p142_spec_path"] = str(request.p142_spec_path)
    outputs = write_outputs(binding, request.output_dir)
    binding["output_files"] = outputs
    (request.output_dir / "P143_DATA_PREVIEW_BINDING.json").write_text(
        json.dumps(binding, ensure_ascii=False, indent=2, sort_keys=True),
        encoding="utf-8",
    )
    return binding


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="P143 data preview binding local read-only.")
    parser.add_argument("--p142-spec", required=True)
    parser.add_argument("--source-csv-root", required=True)
    parser.add_argument("--output-dir", required=True)
    parser.add_argument("--run-id", default="P143-DATA-PREVIEW-BINDING")
    parser.add_argument("--generated-at-utc", default=utc_now_iso())
    parser.add_argument("--max-preview-rows", type=int, default=25)
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    binding = run_binding(
        BindingRequest(
            p142_spec_path=Path(args.p142_spec),
            source_csv_root=Path(args.source_csv_root),
            output_dir=Path(args.output_dir),
            run_id=args.run_id,
            generated_at_utc=args.generated_at_utc,
            max_preview_rows=args.max_preview_rows,
        )
    )
    print(binding["status"])
    print(f"source_csv_count={binding['source_csv_count']}")
    print(f"matched_page_count={binding['matched_page_count']}")
    print(f"unmatched_page_count={binding['unmatched_page_count']}")
    print("google_sheets_write=false")
    print("live_google_sheets_read=false")
    print(f"output_dir={args.output_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
