from __future__ import annotations

from html import escape
from pathlib import Path
from typing import Any

from mvp_qaic_py.p219b_core_admin_registry import (
    build_core_admin_registry,
)


TARGET_ADMIN_NAVIGATION = [
    {
        "id": "dashboard",
        "label": "Dashboard",
        "route": "/",
        "purpose": "Vue synthèse du cockpit privé",
    },
    {
        "id": "prompt",
        "label": "Prompt Cockpit",
        "route": "/prompt",
        "purpose": "Prompts, templates, historique et qualité",
    },
    {
        "id": "responses",
        "label": "Réponses GEM",
        "route": "/responses",
        "purpose": "Brouillons, review humaine et exports locaux",
    },
    {
        "id": "documents",
        "label": "Documents",
        "route": "/documents",
        "purpose": "Registry documentaire et sources du MVP",
    },
    {
        "id": "architecture",
        "label": "Architecture",
        "route": "/architecture",
        "purpose": "Carte SVG, modules, routes, dépendances",
    },
    {
        "id": "config",
        "label": "Configuration",
        "route": "/config",
        "purpose": "Paths, modes, registry et flags safety",
    },
    {
        "id": "audit",
        "label": "Audit / Runs",
        "route": "/audit",
        "purpose": "Gates, tests, logs, tags et preuves",
    },
]


PREFERRED_SHELL_LAYERS = (
    "private_cockpit_wiring",
    "nicegui_private_cockpit",
    "nicegui_ui",
)

SOURCE_SHELL_PREFIXES = ("mvp_qaic_py/",)
NON_SOURCE_SHELL_PREFIXES = (
    "05_EXPORTS/",
    "03_EXPORTS/",
    "exports/",
    "reports/",
    "docs/",
    "tests/",
    "01_OPERATOR_INPUTS/",
    "08_LEGACY_REFERENCE/",
)


def is_source_shell_candidate(candidate: dict[str, Any]) -> bool:
    path = str(candidate.get("path", "")).replace("\\", "/")
    if not candidate.get("has_nicegui"):
        return False
    if any(path.startswith(prefix) for prefix in NON_SOURCE_SHELL_PREFIXES):
        return False
    return any(path.startswith(prefix) for prefix in SOURCE_SHELL_PREFIXES)


def _candidate_rank(candidate: dict[str, Any]) -> tuple[int, int, int, int, int, str]:
    layer = str(candidate.get("layer", ""))
    score = int(candidate.get("score", 0))
    source_bonus = 500 if is_source_shell_candidate(candidate) else 0
    layer_bonus = 100 if layer in PREFERRED_SHELL_LAYERS else 0
    menu_bonus = 30 if candidate.get("has_menu_signal") else 0
    route_bonus = 20 if candidate.get("routes") else 0
    nicegui_bonus = 15 if candidate.get("has_nicegui") else 0
    return (
        source_bonus + layer_bonus + menu_bonus + route_bonus + nicegui_bonus + score,
        source_bonus,
        layer_bonus,
        menu_bonus,
        route_bonus,
        str(candidate.get("path", "")),
    )


def select_primary_nicegui_shell(core_registry: dict[str, Any]) -> dict[str, Any]:
    all_nicegui = [
        item for item in core_registry.get("ui_candidates", []) if item.get("has_nicegui")
    ]
    source_candidates = [item for item in all_nicegui if is_source_shell_candidate(item)]

    if source_candidates:
        selected = sorted(source_candidates, key=_candidate_rank, reverse=True)[0]
        return {
            "STATUS": "OK_P219C_PRIMARY_SOURCE_NICEGUI_SHELL_SELECTED",
            "selected": selected,
            "reason": "SOURCE_SHELL_PRIORITY_LAYER_MENU_ROUTE_SELECTION",
            "fallback_used": False,
            "ignored_non_source_nicegui_count": len(all_nicegui) - len(source_candidates),
        }

    if all_nicegui:
        selected = sorted(all_nicegui, key=_candidate_rank, reverse=True)[0]
        return {
            "STATUS": "REVIEW_P219C_ONLY_NON_SOURCE_NICEGUI_SHELL_FOUND",
            "selected": selected,
            "reason": "NO_SOURCE_SHELL_FOUND_FALLBACK_FOR_REVIEW_ONLY",
            "fallback_used": True,
            "ignored_non_source_nicegui_count": 0,
        }

    return {
        "STATUS": "REVIEW_P219C_NO_NICEGUI_SHELL_CANDIDATE",
        "selected": None,
        "reason": "NO_NICEGUI_CANDIDATE_FOUND",
        "fallback_used": False,
        "ignored_non_source_nicegui_count": 0,
    }


def build_core_admin_shell_payload(
    project_root: str | Path,
    *,
    generated_at: str | None = None,
    max_files: int = 700,
) -> dict[str, Any]:
    core = build_core_admin_registry(
        project_root,
        generated_at=generated_at,
        max_files=max_files,
    )
    selection = select_primary_nicegui_shell(core)

    status = "OK_P219C_CORE_ADMIN_SHELL_PAYLOAD_READY"
    blockers: list[str] = []
    if selection["STATUS"].startswith("REVIEW_"):
        status = "REVIEW_P219C_CORE_ADMIN_SHELL_NEEDS_SOURCE_UI_CONFIRMATION"
        blockers.append(str(selection.get("reason", "UNKNOWN_SELECTION_REVIEW")))

    navigation = [
        {
            **item,
            "enabled": True,
            "source": "TARGET_ADMIN_NAVIGATION",
            "wiring_status": "TARGET_DEFINED",
        }
        for item in TARGET_ADMIN_NAVIGATION
    ]

    selected = selection.get("selected") or {}

    return {
        "STATUS": status,
        "blocker_count": len(blockers),
        "blockers": blockers,
        "core_registry_status": core.get("STATUS"),
        "primary_shell_selection": selection,
        "navigation": navigation,
        "navigation_count": len(navigation),
        "core_registry": core,
        "shell_strategy": {
            "mode": "SOURCE_SHELL_ADAPTER_FIRST_NO_DESTRUCTIVE_PATCH",
            "next_patch": "wire render_core_admin_shell_nicegui into selected source shell/menu",
            "selected_shell_path": selected.get("path"),
            "selected_shell_is_source": is_source_shell_candidate(selected) if selected else False,
            "reason": (
                "Conserve existing source cockpit shell; add admin sections through a safe adapter layer."
            ),
        },
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


def build_core_admin_shell_html(payload: dict[str, Any]) -> str:
    selected = payload.get("primary_shell_selection", {}).get("selected") or {}
    nav_rows = "\n".join(
        "<tr>"
        f"<td>{escape(str(item.get('route', '')))}</td>"
        f"<td>{escape(str(item.get('label', '')))}</td>"
        f"<td>{escape(str(item.get('purpose', '')))}</td>"
        f"<td>{escape(str(item.get('wiring_status', '')))}</td>"
        "</tr>"
        for item in payload.get("navigation", [])
    )
    layer_rows = "\n".join(
        f"<tr><td>{escape(str(layer))}</td><td>{count}</td></tr>"
        for layer, count in payload.get("core_registry", {}).get("layer_counts", {}).items()
    )

    return "\n".join(
        [
            "<section class='core-admin-shell'>",
            "<h1>Noyau MVP QAIC — Shell d'administration</h1>",
            f"<p>Status: <strong>{escape(str(payload.get('STATUS', '')))}</strong></p>",
            "<h2>Shell NiceGUI source sélectionné</h2>",
            "<ul>",
            f"<li>Path: <code>{escape(str(selected.get('path', '-')))}</code></li>",
            f"<li>Layer: <strong>{escape(str(selected.get('layer', '-')))}</strong></li>",
            f"<li>Score: {escape(str(selected.get('score', '-')))}</li>",
            f"<li>Is source: {escape(str(payload.get('shell_strategy', {}).get('selected_shell_is_source', False)))}</li>",
            f"<li>Reason: {escape(str(payload.get('primary_shell_selection', {}).get('reason', '-')))}</li>",
            "</ul>",
            "<h2>Navigation cible admin</h2>",
            "<table><thead><tr><th>Route</th><th>Page</th><th>Purpose</th><th>Status</th></tr></thead><tbody>",
            nav_rows,
            "</tbody></table>",
            "<h2>Layers UI détectés</h2>",
            "<table><thead><tr><th>Layer</th><th>Count</th></tr></thead><tbody>",
            layer_rows,
            "</tbody></table>",
            "</section>",
        ]
    )


def render_core_admin_shell_nicegui(ui: Any, payload: dict[str, Any]) -> dict[str, Any]:
    html = build_core_admin_shell_html(payload)
    markdown = (
        "## Shell admin MVP QAIC\n\n"
        f"- Status: {payload.get('STATUS')}\n"
        f"- Navigation count: {payload.get('navigation_count')}\n"
        f"- Selected shell: {payload.get('shell_strategy', {}).get('selected_shell_path')}\n"
        f"- Selected shell is source: {payload.get('shell_strategy', {}).get('selected_shell_is_source')}\n"
        "- Mode: source-shell adapter-first, no destructive patch\n"
    )

    rendered: list[dict[str, str]] = []
    if hasattr(ui, "html"):
        ui.html(html)
        rendered.append({"type": "html", "content": "core_admin_shell_html"})
    if hasattr(ui, "markdown"):
        ui.markdown(markdown)
        rendered.append({"type": "markdown", "content": "core_admin_shell_summary"})

    return {
        "STATUS": "OK_P219C_CORE_ADMIN_SHELL_NICEGUI_RENDERED",
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


def build_shell_wiring_markdown(payload: dict[str, Any]) -> str:
    selected = payload.get("primary_shell_selection", {}).get("selected") or {}
    lines = [
        "# P219C-R3 — Source-First Scan Visual Gate",
        "",
        f"- STATUS: {payload.get('STATUS')}",
        f"- Selected shell: `{selected.get('path', '-')}`",
        f"- Selected layer: `{selected.get('layer', '-')}`",
        f"- Selected shell is source: {payload.get('shell_strategy', {}).get('selected_shell_is_source')}",
        f"- Navigation count: {payload.get('navigation_count')}",
        "",
        "## Navigation cible",
        "",
    ]
    for item in payload.get("navigation", []):
        lines.append(f"- `{item['route']}` — {item['label']} — {item['purpose']}")
    lines.extend(["", "## Next", "", "P219D: patch selected source NiceGUI shell/menu."])
    return "\n".join(lines)


def main() -> None:
    import argparse
    import json

    parser = argparse.ArgumentParser()
    parser.add_argument("--project-root", default=".")
    parser.add_argument("--generated-at", default=None)
    parser.add_argument("--max-files", type=int, default=700)
    args = parser.parse_args()

    payload = build_core_admin_shell_payload(
        args.project_root,
        generated_at=args.generated_at,
        max_files=args.max_files,
    )
    print(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
