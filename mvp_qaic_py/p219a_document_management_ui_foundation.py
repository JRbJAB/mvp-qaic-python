from __future__ import annotations

from datetime import UTC, datetime
from html import escape
from pathlib import Path
from typing import Any

DOC_EXTENSIONS = {".md", ".txt", ".json", ".csv", ".html", ".svg", ".py"}
UI_KEYWORDS = ("nicegui", "cockpit", "ui", "view_model", "visual", "document", "html", "svg")
SCAN_ROOTS = (
    "01_OPERATOR_INPUTS",
    "05_EXPORTS",
    "docs",
    "mvp_qaic_py",
    "tests",
    "08_LEGACY_REFERENCE",
)


def _now_iso() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def _group(rel_path: str) -> str:
    first = rel_path.split("/", 1)[0]
    return {
        "01_OPERATOR_INPUTS": "operator_inputs",
        "05_EXPORTS": "exports",
        "docs": "docs",
        "mvp_qaic_py": "python_ui_modules",
        "tests": "tests",
        "08_LEGACY_REFERENCE": "legacy_reference",
    }.get(first, "other")


def _is_ui(rel_path: str) -> bool:
    low = rel_path.lower()
    return any(keyword in low for keyword in UI_KEYWORDS)


def scan_document_registry(
    project_root: str | Path, *, max_files: int = 350
) -> list[dict[str, Any]]:
    root = Path(project_root)
    docs: list[dict[str, Any]] = []

    for scan_root in SCAN_ROOTS:
        base = root / scan_root
        if not base.exists():
            continue

        for path in sorted(base.rglob("*")):
            if len(docs) >= max_files:
                break
            if not path.is_file() or path.name.lower() == "desktop.ini":
                continue
            if path.suffix.lower() not in DOC_EXTENSIONS:
                continue

            rel = path.relative_to(root).as_posix()
            docs.append(
                {
                    "path": rel,
                    "name": path.name,
                    "extension": path.suffix.lower(),
                    "group": _group(rel),
                    "size_bytes": path.stat().st_size,
                    "is_ui_related": _is_ui(rel),
                }
            )

    return docs


def build_document_management_ui_payload(
    project_root: str | Path,
    *,
    generated_at: str | None = None,
    max_files: int = 350,
) -> dict[str, Any]:
    docs = scan_document_registry(project_root, max_files=max_files)
    groups: dict[str, int] = {}
    for doc in docs:
        groups[str(doc["group"])] = groups.get(str(doc["group"]), 0) + 1

    tree = {
        "id": "mvp_qaic_tool",
        "label": "MVP QAIC Tool",
        "children": [
            {
                "id": "documents",
                "label": "Gestion documentaire",
                "children": [
                    {
                        "id": group,
                        "label": group.replace("_", " ").title(),
                        "count": count,
                    }
                    for group, count in sorted(groups.items())
                ],
            },
            {
                "id": "interface",
                "label": "Interface MVP",
                "children": [
                    {"id": "prompt_history", "label": "Prompt History"},
                    {"id": "response_draft", "label": "Response Draft"},
                    {"id": "local_export", "label": "Local Export"},
                    {"id": "document_ui", "label": "Document Management UI"},
                    {"id": "svg_schema", "label": "Auto SVG Schema"},
                ],
            },
        ],
    }

    generated = generated_at or _now_iso()
    ui_related_count = sum(1 for doc in docs if doc["is_ui_related"])
    svg = build_mvp_interface_svg(
        generated_at=generated,
        document_count=len(docs),
        ui_related_count=ui_related_count,
        groups=groups,
    )

    status = "OK_P219A_DOCUMENT_MANAGEMENT_UI_PAYLOAD_READY"
    if not docs:
        status = "REVIEW_P219A_DOCUMENT_MANAGEMENT_UI_EMPTY_REGISTRY"

    return {
        "STATUS": status,
        "generated_at": generated,
        "project_root": str(Path(project_root)),
        "document_count": len(docs),
        "group_count": len(groups),
        "ui_related_count": ui_related_count,
        "groups": dict(sorted(groups.items())),
        "documents": docs,
        "tree": tree,
        "svg_schema": svg,
        "svg_schema_bytes": len(svg.encode("utf-8")),
        "html_strategy": {
            "primary": "ui.html",
            "secondary": "ui.markdown",
            "tree_adapter": "inline_svg",
            "auto_update": "rebuild payload by rescanning project roots",
        },
        "local_only": True,
        "review_only": True,
        "server_started": False,
        "browser_started": False,
        "provider_call_executed": False,
        "gem_call_executed": False,
        "broker": False,
        "order": False,
        "sizing": False,
        "recommended_next": "P219B_NICEGUI_DOCUMENT_UI_REAL_PAGE_WIRING_FAST_FUSE",
    }


def build_mvp_interface_svg(
    *,
    generated_at: str,
    document_count: int,
    ui_related_count: int,
    groups: dict[str, int],
) -> str:
    rows = list(groups.items())
    height = max(360, 240 + 42 * len(rows))

    def box(x: int, y: int, w: int, h: int, title: str, sub: str) -> str:
        return (
            f"<rect x='{x}' y='{y}' width='{w}' height='{h}' rx='16' fill='#fff' stroke='#d1d5db'/>"
            f"<text x='{x + 16}' y='{y + 28}' font-size='15' font-weight='700' fill='#111827'>{escape(title)}</text>"
            f"<text x='{x + 16}' y='{y + 52}' font-size='12' fill='#4b5563'>{escape(sub)}</text>"
        )

    group_svg = []
    y = 205
    for group, count in rows:
        group_svg.append(box(760, y, 340, 34, group.replace("_", " ").title(), f"{count} item(s)"))
        group_svg.append(f"<line x1='670' y1='146' x2='760' y2='{y + 17}' stroke='#9ca3af'/>")
        y += 42

    return "\n".join(
        [
            f"<svg xmlns='http://www.w3.org/2000/svg' width='1180' height='{height}' viewBox='0 0 1180 {height}'>",
            "<rect width='100%' height='100%' fill='#f6f7fb'/>",
            "<text x='40' y='46' font-size='24' font-weight='800' fill='#111827'>MVP QAIC — Interface & Documentation Map</text>",
            f"<text x='40' y='76' font-size='13' fill='#4b5563'>Generated: {escape(generated_at)}</text>",
            box(40, 110, 270, 72, "MVP QAIC Tool", f"{document_count} documents tracked"),
            box(405, 110, 270, 72, "HTML / NiceGUI UI", f"{ui_related_count} UI-related artifacts"),
            box(760, 110, 340, 72, "Documentation Registry", f"{len(rows)} groups auto-scanned"),
            "<line x1='310' y1='146' x2='405' y2='146' stroke='#6b7280' stroke-width='2'/>",
            "<line x1='675' y1='146' x2='760' y2='146' stroke='#6b7280' stroke-width='2'/>",
            *group_svg,
            "</svg>",
        ]
    )


def build_document_management_html(payload: dict[str, Any]) -> str:
    group_rows = "\n".join(
        f"<tr><td>{escape(str(group))}</td><td>{count}</td></tr>"
        for group, count in payload.get("groups", {}).items()
    )
    doc_rows = "\n".join(
        "<tr>"
        f"<td>{escape(str(doc.get('name', '')))}</td>"
        f"<td>{escape(str(doc.get('group', '')))}</td>"
        f"<td>{escape(str(doc.get('path', '')))}</td>"
        f"<td>{escape(str(doc.get('is_ui_related', False)))}</td>"
        "</tr>"
        for doc in payload.get("documents", [])[:80]
    )

    return "\n".join(
        [
            "<section class='doc-ui'>",
            "<h1>Gestion documentaire MVP QAIC</h1>",
            f"<p>Status: <strong>{escape(str(payload.get('STATUS')))}</strong></p>",
            f"<p>Documents: {payload.get('document_count')} | UI-related: {payload.get('ui_related_count')}</p>",
            "<div class='schema'>",
            payload["svg_schema"],
            "</div>",
            "<h2>Groupes documentaires</h2>",
            "<table><thead><tr><th>Groupe</th><th>Count</th></tr></thead><tbody>",
            group_rows,
            "</tbody></table>",
            "<h2>Documents suivis</h2>",
            "<table><thead><tr><th>Nom</th><th>Groupe</th><th>Chemin</th><th>UI</th></tr></thead><tbody>",
            doc_rows,
            "</tbody></table>",
            "</section>",
        ]
    )


def render_document_management_nicegui(ui: Any, payload: dict[str, Any]) -> dict[str, Any]:
    html = build_document_management_html(payload)
    markdown = (
        "## Suivi interface MVP\n\n"
        f"- Documents suivis : {payload.get('document_count')}\n"
        f"- Groupes : {payload.get('group_count')}\n"
        f"- UI-related : {payload.get('ui_related_count')}\n"
        "- Mise à jour : scan projet à chaque refresh payload\n"
    )

    rendered = []
    ui.html(html)
    rendered.append({"type": "html", "content": "document_management_html"})
    ui.markdown(markdown)
    rendered.append({"type": "markdown", "content": "document_management_summary"})

    return {
        "STATUS": "OK_P219A_DOCUMENT_MANAGEMENT_NICEGUI_RENDERED",
        "rendered_count": len(rendered),
        "rendered": rendered,
        "server_started": False,
        "browser_started": False,
        "provider_call_executed": False,
        "gem_call_executed": False,
        "broker": False,
        "order": False,
        "sizing": False,
    }


def main() -> None:
    import argparse
    import json

    parser = argparse.ArgumentParser()
    parser.add_argument("--project-root", default=".")
    parser.add_argument("--generated-at", default=None)
    parser.add_argument("--max-files", type=int, default=350)
    args = parser.parse_args()

    payload = build_document_management_ui_payload(
        args.project_root,
        generated_at=args.generated_at,
        max_files=args.max_files,
    )
    print(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
