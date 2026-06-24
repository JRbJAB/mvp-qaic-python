from __future__ import annotations

from dataclasses import asdict, dataclass
from datetime import UTC, datetime
from html import escape
from pathlib import Path
import re
from typing import Any

from mvp_qaic_py.p219a_document_management_ui_foundation import (
    build_document_management_ui_payload,
)

SCAN_EXTENSIONS = {".py", ".html", ".md", ".json", ".svg", ".csv"}
IGNORE_DIR_NAMES = {".git", ".venv", "__pycache__", ".pytest_cache", ".ruff_cache"}

SOURCE_FIRST_SCAN_ROOTS = (
    "mvp_qaic_py",
    "tests",
    "docs",
    "01_OPERATOR_INPUTS",
    "05_EXPORTS",
    "03_EXPORTS",
    "08_LEGACY_REFERENCE",
)

UI_SIGNAL_PATTERNS = (
    "nicegui",
    "ui.page",
    "ui.run",
    "ui.left_drawer",
    "ui.tabs",
    "ui.tab_panels",
    "ui.html",
    "ui.markdown",
    "ui.table",
    "ui.card",
    "ui.expansion",
    "cockpit",
    "prompt",
    "document",
    "architecture",
    "config",
    "audit",
)

SAFETY_FLAGS = {
    "HUMAN_REVIEW_ONLY": True,
    "NO_AUTO_APPLY": True,
    "NO_PROVIDER_CALL": True,
    "NO_GEM_CALL_FROM_ADMIN": True,
    "NO_BROKER": True,
    "NO_ORDER": True,
    "NO_SIZING": True,
    "PRIVATE_ADMIN_ONLY": True,
}


@dataclass(frozen=True)
class UiCandidate:
    path: str
    name: str
    extension: str
    layer: str
    score: int
    routes: list[str]
    functions: list[str]
    has_nicegui: bool
    has_menu_signal: bool
    has_prompt_signal: bool
    has_document_signal: bool
    has_config_signal: bool
    has_audit_signal: bool


def _now_iso() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def _safe_read(path: Path) -> str:
    for encoding in ("utf-8", "utf-8-sig", "cp1252"):
        try:
            return path.read_text(encoding=encoding)
        except Exception:
            continue
    return ""


def _should_skip(path: Path) -> bool:
    return bool(set(path.parts) & IGNORE_DIR_NAMES)


def _classify_layer(rel_path: str, text: str) -> str:
    low = (rel_path + "\n" + text).lower()
    if "p219a_document_management_ui_foundation" in low:
        return "document_ui_foundation"
    if "p219b_core_admin_registry" in low:
        return "core_admin_registry"
    if "p219c_core_admin_shell_wiring" in low:
        return "core_admin_shell_wiring"
    if "p217_nicegui_private_cockpit_ui_wiring" in low:
        return "private_cockpit_wiring"
    if "p216_private_cockpit_runtime_bundle" in low:
        return "private_cockpit_runtime_core"
    if "nicegui" in low and "cockpit" in low:
        return "nicegui_private_cockpit"
    if "nicegui" in low:
        return "nicegui_ui"
    if "prompt" in low and "history" in low:
        return "prompt_history"
    if "response" in low and "draft" in low:
        return "response_draft"
    if "document" in low or "architecture" in low or "svg" in low:
        return "document_architecture"
    if "config" in low or "registry" in low:
        return "config_registry"
    if "audit" in low or "run_log" in low:
        return "audit_run"
    return "other"


def _iter_source_first_files(root: Path) -> list[Path]:
    seen: set[Path] = set()
    paths: list[Path] = []

    for rel_root in SOURCE_FIRST_SCAN_ROOTS:
        base = root / rel_root
        if not base.exists():
            continue
        for path in sorted(base.rglob("*")):
            if path in seen:
                continue
            seen.add(path)
            paths.append(path)

    for path in sorted(root.rglob("*")):
        if path in seen:
            continue
        seen.add(path)
        paths.append(path)

    return paths


def scan_ui_foundation(project_root: str | Path, *, max_files: int = 700) -> list[dict[str, Any]]:
    root = Path(project_root)
    candidates: list[UiCandidate] = []

    for path in _iter_source_first_files(root):
        if len(candidates) >= max_files:
            break
        if _should_skip(path) or not path.is_file():
            continue
        if path.name.lower() == "desktop.ini":
            continue
        if path.suffix.lower() not in SCAN_EXTENSIONS:
            continue

        text = _safe_read(path)
        if not text:
            continue

        rel = path.relative_to(root).as_posix()
        low = (rel + "\n" + text).lower()
        score = sum(1 for pattern in UI_SIGNAL_PATTERNS if pattern.lower() in low)
        routes = re.findall(r"@ui\.page\(['\"]([^'\"]+)['\"]\)", text)
        functions = re.findall(r"^def\s+([a-zA-Z0-9_]+)\(", text, flags=re.MULTILINE)

        has_nicegui = "nicegui" in low or "ui." in low
        has_menu = any(
            token in low for token in ("menu", "drawer", "tabs", "navigation", "sidebar")
        )
        has_prompt = "prompt" in low or "gem" in low
        has_document = "document" in low or "svg" in low or "architecture" in low
        has_config = "config" in low or "registry" in low
        has_audit = "audit" in low or "run_log" in low or "status" in low

        if score == 0 and not (
            has_nicegui or has_prompt or has_document or has_config or has_audit
        ):
            continue

        candidates.append(
            UiCandidate(
                path=rel,
                name=path.name,
                extension=path.suffix.lower(),
                layer=_classify_layer(rel, text),
                score=score,
                routes=routes,
                functions=functions[:30],
                has_nicegui=has_nicegui,
                has_menu_signal=has_menu,
                has_prompt_signal=has_prompt,
                has_document_signal=has_document,
                has_config_signal=has_config,
                has_audit_signal=has_audit,
            )
        )

    return [asdict(item) for item in sorted(candidates, key=lambda c: (-c.score, c.path))]


def build_core_admin_registry(
    project_root: str | Path,
    *,
    generated_at: str | None = None,
    max_files: int = 700,
) -> dict[str, Any]:
    generated = generated_at or _now_iso()
    ui_candidates = scan_ui_foundation(project_root, max_files=max_files)
    document_payload = build_document_management_ui_payload(project_root, max_files=max_files)

    layer_counts: dict[str, int] = {}
    route_registry: list[dict[str, Any]] = []
    component_registry: list[dict[str, Any]] = []

    for candidate in ui_candidates:
        layer = str(candidate["layer"])
        layer_counts[layer] = layer_counts.get(layer, 0) + 1

        for route in candidate.get("routes", []):
            route_registry.append(
                {
                    "route": route,
                    "source_path": candidate["path"],
                    "layer": layer,
                    "status": "DISCOVERED",
                }
            )

        for fn in candidate.get("functions", []):
            component_registry.append(
                {
                    "name": fn,
                    "source_path": candidate["path"],
                    "layer": layer,
                    "status": "DISCOVERED",
                }
            )

    target_routes = [
        {"route": "/", "label": "Dashboard", "target_layer": "dashboard"},
        {"route": "/prompt", "label": "Prompt Cockpit", "target_layer": "prompt"},
        {"route": "/responses", "label": "Responses / Drafts", "target_layer": "response_draft"},
        {"route": "/documents", "label": "Documents", "target_layer": "document_ui_foundation"},
        {
            "route": "/architecture",
            "label": "Architecture Map",
            "target_layer": "document_architecture",
        },
        {"route": "/config", "label": "Configuration", "target_layer": "config_registry"},
        {"route": "/audit", "label": "Runs / Audit", "target_layer": "audit_run"},
    ]

    admin_sections = [
        {
            "id": "core",
            "label": "Noyau",
            "items": ["route_registry", "component_registry", "safety_registry"],
        },
        {
            "id": "workflow",
            "label": "Workflow",
            "items": ["prompt", "responses", "documents", "architecture"],
        },
        {
            "id": "governance",
            "label": "Gouvernance",
            "items": ["config", "audit", "run_logs", "safety"],
        },
    ]

    status = "OK_P219B_CORE_ADMIN_REGISTRY_READY"
    blockers: list[str] = []
    if not ui_candidates:
        status = "REVIEW_P219B_CORE_ADMIN_NO_UI_CANDIDATE"
        blockers.append("NO_UI_CANDIDATE")
    if not document_payload.get("documents"):
        status = "REVIEW_P219B_CORE_ADMIN_NO_DOCUMENTS"
        blockers.append("NO_DOCUMENTS")

    return {
        "STATUS": status,
        "generated_at": generated,
        "project_root": str(Path(project_root)),
        "blocker_count": len(blockers),
        "blockers": blockers,
        "ui_candidate_count": len(ui_candidates),
        "nicegui_candidate_count": sum(1 for item in ui_candidates if item["has_nicegui"]),
        "route_candidate_count": len(route_registry),
        "component_candidate_count": len(component_registry),
        "layer_counts": dict(sorted(layer_counts.items())),
        "target_routes": target_routes,
        "discovered_routes": route_registry,
        "component_registry": component_registry[:250],
        "ui_candidates": ui_candidates[:250],
        "document_registry_summary": {
            "document_count": document_payload.get("document_count", 0),
            "group_count": document_payload.get("group_count", 0),
            "ui_related_count": document_payload.get("ui_related_count", 0),
            "groups": document_payload.get("groups", {}),
        },
        "admin_sections": admin_sections,
        "safety_registry": SAFETY_FLAGS,
        "local_only": True,
        "review_only": True,
        "server_started": False,
        "browser_started": False,
        "provider_call_executed": False,
        "gem_call_executed": False,
        "auto_apply_gem_response": False,
        "broker": False,
        "order": False,
        "sizing": False,
        "recommended_next": "P219D_PATCH_SELECTED_SOURCE_NICEGUI_SHELL_MENU_WITH_CORE_ADMIN",
    }


def build_core_admin_html(payload: dict[str, Any]) -> str:
    target_rows = "\n".join(
        "<tr>"
        f"<td>{escape(str(item.get('route', '')))}</td>"
        f"<td>{escape(str(item.get('label', '')))}</td>"
        f"<td>{escape(str(item.get('target_layer', '')))}</td>"
        "</tr>"
        for item in payload.get("target_routes", [])
    )
    layer_rows = "\n".join(
        f"<tr><td>{escape(str(layer))}</td><td>{count}</td></tr>"
        for layer, count in payload.get("layer_counts", {}).items()
    )
    candidate_rows = "\n".join(
        "<tr>"
        f"<td>{escape(str(item.get('path', '')))}</td>"
        f"<td>{escape(str(item.get('layer', '')))}</td>"
        f"<td>{escape(str(item.get('score', '')))}</td>"
        f"<td>{escape(str(item.get('has_nicegui', False)))}</td>"
        "</tr>"
        for item in payload.get("ui_candidates", [])[:80]
    )
    safety_rows = "\n".join(
        f"<tr><td>{escape(str(flag))}</td><td>{escape(str(value))}</td></tr>"
        for flag, value in payload.get("safety_registry", {}).items()
    )

    return "\n".join(
        [
            "<section class='core-admin'>",
            "<h1>Noyau d'administration MVP QAIC</h1>",
            f"<p>Status: <strong>{escape(str(payload.get('STATUS', '')))}</strong></p>",
            "<div class='metrics'>",
            f"<p>UI candidates: {payload.get('ui_candidate_count', 0)}</p>",
            f"<p>NiceGUI candidates: {payload.get('nicegui_candidate_count', 0)}</p>",
            f"<p>Routes discovered: {payload.get('route_candidate_count', 0)}</p>",
            f"<p>Components discovered: {payload.get('component_candidate_count', 0)}</p>",
            "</div>",
            "<h2>Routes cibles du cockpit</h2>",
            "<table><thead><tr><th>Route</th><th>Label</th><th>Layer</th></tr></thead><tbody>",
            target_rows,
            "</tbody></table>",
            "<h2>Layers détectés</h2>",
            "<table><thead><tr><th>Layer</th><th>Count</th></tr></thead><tbody>",
            layer_rows,
            "</tbody></table>",
            "<h2>Candidats UI existants</h2>",
            "<table><thead><tr><th>Path</th><th>Layer</th><th>Score</th><th>NiceGUI</th></tr></thead><tbody>",
            candidate_rows,
            "</tbody></table>",
            "<h2>Safety registry</h2>",
            "<table><thead><tr><th>Flag</th><th>Value</th></tr></thead><tbody>",
            safety_rows,
            "</tbody></table>",
            "</section>",
        ]
    )


def render_core_admin_nicegui(ui: Any, payload: dict[str, Any]) -> dict[str, Any]:
    html = build_core_admin_html(payload)
    summary = (
        "## Noyau d'administration\n\n"
        f"- UI candidates: {payload.get('ui_candidate_count', 0)}\n"
        f"- NiceGUI candidates: {payload.get('nicegui_candidate_count', 0)}\n"
        f"- Routes découvertes: {payload.get('route_candidate_count', 0)}\n"
        f"- Components découverts: {payload.get('component_candidate_count', 0)}\n"
        "- Safety: HUMAN_REVIEW_ONLY / NO_AUTO_APPLY / NO_BROKER / NO_ORDER / NO_SIZING\n"
    )

    rendered: list[dict[str, str]] = []
    if hasattr(ui, "html"):
        ui.html(html)
        rendered.append({"type": "html", "content": "core_admin_html"})
    if hasattr(ui, "markdown"):
        ui.markdown(summary)
        rendered.append({"type": "markdown", "content": "core_admin_summary"})

    return {
        "STATUS": "OK_P219B_CORE_ADMIN_NICEGUI_RENDERED",
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


def build_core_admin_audit_markdown(payload: dict[str, Any]) -> str:
    lines = [
        "# P219B/P219C-R3 — Core Admin Source-First UI Foundation",
        "",
        "## Status",
        "",
        f"- STATUS: {payload.get('STATUS')}",
        f"- UI candidates: {payload.get('ui_candidate_count')}",
        f"- NiceGUI candidates: {payload.get('nicegui_candidate_count')}",
        f"- Routes discovered: {payload.get('route_candidate_count')}",
        f"- Components discovered: {payload.get('component_candidate_count')}",
        "",
        "## Target architecture",
        "",
        "```text",
        "NiceGUI Private Admin Cockpit",
        "├─ Dashboard",
        "├─ Prompt Cockpit",
        "├─ Responses / Drafts",
        "├─ Documents",
        "├─ Architecture Map",
        "├─ Configuration",
        "└─ Runs / Audit",
        "```",
        "",
        "## Layer counts",
        "",
    ]
    for layer, count in payload.get("layer_counts", {}).items():
        lines.append(f"- {layer}: {count}")
    lines.extend(["", "## Safety registry", ""])
    for flag, value in payload.get("safety_registry", {}).items():
        lines.append(f"- {flag}: {value}")
    lines.extend(
        ["", "## Recommended next", "", "P219D: patch selected source NiceGUI shell/menu."]
    )
    return "\n".join(lines)


def main() -> None:
    import argparse
    import json

    parser = argparse.ArgumentParser()
    parser.add_argument("--project-root", default=".")
    parser.add_argument("--generated-at", default=None)
    parser.add_argument("--max-files", type=int, default=700)
    args = parser.parse_args()

    payload = build_core_admin_registry(
        args.project_root,
        generated_at=args.generated_at,
        max_files=args.max_files,
    )
    print(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
