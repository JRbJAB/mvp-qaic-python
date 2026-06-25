from __future__ import annotations

from datetime import UTC, datetime
from html import escape
from pathlib import Path
import re
from typing import Any

from mvp_qaic_py.p219b_core_admin_registry import build_core_admin_registry
from mvp_qaic_py.p219c_core_admin_shell_wiring import build_core_admin_shell_payload
from mvp_qaic_py.private_admin_app.navigation import get_admin_navigation, get_navigation_groups

OLD_MENU_SOURCE_REL = "mvp_qaic_py/p173_nicegui_private_local_runner.py"

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


def _now_iso() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def _read_text(path: Path) -> str:
    for encoding in ("utf-8", "utf-8-sig", "cp1252"):
        try:
            return path.read_text(encoding=encoding)
        except Exception:
            continue
    return ""


def inspect_p173_old_menu(project_root: str | Path) -> dict[str, Any]:
    root = Path(project_root)
    source = root / OLD_MENU_SOURCE_REL
    text = _read_text(source) if source.exists() else ""
    low = text.lower()

    routes = re.findall(r"@ui\.page\(['\"]([^'\"]+)['\"]\)", text)
    functions = re.findall(r"^def\s+([a-zA-Z0-9_]+)\(", text, flags=re.MULTILINE)

    evidence = {
        "exists": source.exists(),
        "path": OLD_MENU_SOURCE_REL,
        "size_bytes": source.stat().st_size if source.exists() else 0,
        "has_nicegui": "nicegui" in low or "ui." in low,
        "has_left_drawer": "left_drawer" in low or "drawer" in low,
        "has_tabs": "tabs" in low or "tab_panels" in low,
        "has_links": "ui.link" in low or "href=" in low or "link" in low,
        "has_base_python": "base python" in low or "base_python" in low or "python base" in low,
        "has_sheets": "sheets" in low or "google sheets" in low or "sheet" in low,
        "has_drive": "drive" in low,
        "has_github": "github" in low or "git" in low,
        "routes": routes,
        "functions": functions[:40],
    }

    menu_score = sum(
        1
        for key in (
            "has_nicegui",
            "has_left_drawer",
            "has_tabs",
            "has_links",
            "has_base_python",
            "has_sheets",
            "has_drive",
            "has_github",
        )
        if evidence[key]
    )
    evidence["menu_evidence_score"] = menu_score
    evidence["STATUS"] = (
        "OK_P173_OLD_MENU_SOURCE_CONFIRMED"
        if evidence["exists"] and menu_score >= 3
        else "REVIEW_P173_OLD_MENU_SOURCE_WEAK_EVIDENCE"
    )
    return evidence


def build_private_admin_shell_payload(
    project_root: str | Path,
    *,
    generated_at: str | None = None,
    max_files: int = 700,
) -> dict[str, Any]:
    generated = generated_at or _now_iso()
    old_menu = inspect_p173_old_menu(project_root)
    core_registry = build_core_admin_registry(
        project_root,
        generated_at=generated,
        max_files=max_files,
    )
    shell_registry = build_core_admin_shell_payload(
        project_root,
        generated_at=generated,
        max_files=max_files,
    )
    navigation = get_admin_navigation()
    nav_groups = get_navigation_groups()

    blockers: list[str] = []
    if not old_menu["exists"]:
        blockers.append("P173_OLD_MENU_SOURCE_MISSING")
    if old_menu["STATUS"].startswith("REVIEW_"):
        blockers.append("P173_OLD_MENU_WEAK_EVIDENCE")

    status = (
        "OK_P219D1_PRIVATE_ADMIN_SHELL_PAYLOAD_READY"
        if not blockers
        else "REVIEW_P219D1_PRIVATE_ADMIN_SHELL_NEEDS_HUMAN_CONFIRMATION"
    )

    return {
        "STATUS": status,
        "generated_at": generated,
        "blocker_count": len(blockers),
        "blockers": blockers,
        "old_menu_source": old_menu,
        "durable_shell": {
            "package": "mvp_qaic_py.private_admin_app",
            "navigation": "mvp_qaic_py/private_admin_app/navigation.py",
            "shell": "mvp_qaic_py/private_admin_app/shell.py",
            "source_old_menu": OLD_MENU_SOURCE_REL,
            "mode": "PORT_P173_MENU_TO_DURABLE_SHELL",
        },
        "navigation": navigation,
        "navigation_groups": nav_groups,
        "navigation_count": len(navigation),
        "core_registry_status": core_registry.get("STATUS"),
        "shell_registry_status": shell_registry.get("STATUS"),
        "selected_source_shell": shell_registry.get("shell_strategy", {}).get(
            "selected_shell_path"
        ),
        "selected_shell_is_source": shell_registry.get("shell_strategy", {}).get(
            "selected_shell_is_source"
        ),
        "safety_flags": SAFETY_FLAGS,
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
        "recommended_next": "P219D2_INTEGRATE_REAL_P173_MENU_DETAILS_AND_PAGE_STUBS_VISUAL_GATE",
    }


def build_private_admin_shell_html(payload: dict[str, Any]) -> str:
    nav_rows = "\n".join(
        "<tr>"
        f"<td>{escape(str(item['group']))}</td>"
        f"<td>{escape(str(item['label']))}</td>"
        f"<td><code>{escape(str(item['route']))}</code></td>"
        f"<td>{escape(str(item['purpose']))}</td>"
        "</tr>"
        for item in payload["navigation"]
    )
    safety_rows = "\n".join(
        f"<tr><td>{escape(flag)}</td><td>{escape(str(value))}</td></tr>"
        for flag, value in payload["safety_flags"].items()
    )
    old = payload["old_menu_source"]
    return "\n".join(
        [
            "<section class='private-admin-shell'>",
            "<h1>MVP QAIC — Private Admin Shell</h1>",
            f"<p>Status: <strong>{escape(str(payload['STATUS']))}</strong></p>",
            "<h2>Source historique P173</h2>",
            "<ul>",
            f"<li>Path: <code>{escape(str(old['path']))}</code></li>",
            f"<li>Status: <strong>{escape(str(old['STATUS']))}</strong></li>",
            f"<li>Menu evidence score: {escape(str(old['menu_evidence_score']))}</li>",
            f"<li>Base Python: {escape(str(old['has_base_python']))}</li>",
            f"<li>Sheets: {escape(str(old['has_sheets']))}</li>",
            f"<li>Left drawer: {escape(str(old['has_left_drawer']))}</li>",
            f"<li>Links: {escape(str(old['has_links']))}</li>",
            "</ul>",
            "<h2>Menu latéral officiel durable</h2>",
            "<table><thead><tr><th>Groupe</th><th>Page</th><th>Route</th><th>Objectif</th></tr></thead><tbody>",
            nav_rows,
            "</tbody></table>",
            "<h2>Safety registry</h2>",
            "<table><thead><tr><th>Flag</th><th>Value</th></tr></thead><tbody>",
            safety_rows,
            "</tbody></table>",
            "</section>",
        ]
    )


def build_architecture_blueprint_svg() -> str:
    def box(x: int, y: int, w: int, h: int, title: str, sub: str) -> str:
        return (
            f"<rect x='{x}' y='{y}' width='{w}' height='{h}' rx='16' fill='white' stroke='#d1d5db'/>"
            f"<text x='{x + 16}' y='{y + 28}' font-size='15' font-weight='800' fill='#111827'>{escape(title)}</text>"
            f"<text x='{x + 16}' y='{y + 52}' font-size='12' fill='#4b5563'>{escape(sub)}</text>"
        )

    return "\n".join(
        [
            "<svg xmlns='http://www.w3.org/2000/svg' width='1280' height='680' viewBox='0 0 1280 680'>",
            "<rect width='100%' height='100%' fill='#f6f7fb'/>",
            "<text x='40' y='48' font-size='28' font-weight='900' fill='#111827'>MVP QAIC — Private Admin App</text>",
            "<text x='40' y='78' font-size='13' fill='#4b5563'>P173 old menu → durable NiceGUI shell → core registries → visual gates</text>",
            box(40, 120, 300, 90, "P173 Old Menu", "source historique à reprendre"),
            box(420, 120, 300, 90, "Private Admin Shell", "navigation durable + pages"),
            box(800, 120, 300, 90, "Core Registries", "routes/docs/config/safety/runs"),
            box(40, 300, 300, 90, "Base Python", "modules, repo, noyau"),
            box(420, 300, 300, 90, "Google Sheets", "cockpit/export/read-only"),
            box(800, 300, 300, 90, "Prompt Workflow", "templates/history/responses"),
            box(40, 480, 300, 90, "Documents", "lexique/méthodes/docs"),
            box(420, 480, 300, 90, "Architecture", "SVG/maps/boundaries"),
            box(800, 480, 300, 90, "Audit / Safety", "gates/tests/no broker"),
            "<line x1='340' y1='165' x2='420' y2='165' stroke='#6b7280' stroke-width='2'/>",
            "<line x1='720' y1='165' x2='800' y2='165' stroke='#6b7280' stroke-width='2'/>",
            "<line x1='190' y1='210' x2='190' y2='300' stroke='#6b7280' stroke-width='2'/>",
            "<line x1='570' y1='210' x2='570' y2='300' stroke='#6b7280' stroke-width='2'/>",
            "<line x1='950' y1='210' x2='950' y2='300' stroke='#6b7280' stroke-width='2'/>",
            "<line x1='190' y1='390' x2='190' y2='480' stroke='#6b7280' stroke-width='2'/>",
            "<line x1='570' y1='390' x2='570' y2='480' stroke='#6b7280' stroke-width='2'/>",
            "<line x1='950' y1='390' x2='950' y2='480' stroke='#6b7280' stroke-width='2'/>",
            "</svg>",
        ]
    )


def render_private_admin_shell_nicegui(ui: Any, payload: dict[str, Any]) -> dict[str, Any]:
    html = build_private_admin_shell_html(payload)
    svg = build_architecture_blueprint_svg()
    summary = (
        "## Private Admin Shell\n\n"
        f"- Status: {payload['STATUS']}\n"
        f"- Old menu: {payload['old_menu_source']['path']}\n"
        f"- Navigation count: {payload['navigation_count']}\n"
        f"- Selected source shell: {payload['selected_source_shell']}\n"
        "- Safety: HUMAN_REVIEW_ONLY / NO_AUTO_APPLY / NO_BROKER / NO_ORDER / NO_SIZING\n"
    )
    rendered: list[dict[str, str]] = []
    if hasattr(ui, "html"):
        ui.html(svg)
        rendered.append({"type": "html", "content": "architecture_blueprint_svg"})
        ui.html(html)
        rendered.append({"type": "html", "content": "private_admin_shell_html"})
    if hasattr(ui, "markdown"):
        ui.markdown(summary)
        rendered.append({"type": "markdown", "content": "private_admin_shell_summary"})
    return {
        "STATUS": "OK_P219D1_PRIVATE_ADMIN_SHELL_NICEGUI_RENDERED",
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
    parser.add_argument("--max-files", type=int, default=700)
    args = parser.parse_args()

    payload = build_private_admin_shell_payload(
        args.project_root,
        generated_at=args.generated_at,
        max_files=args.max_files,
    )
    print(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
