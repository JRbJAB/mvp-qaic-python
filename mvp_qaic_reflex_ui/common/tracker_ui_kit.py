from __future__ import annotations

from dataclasses import dataclass
from html import escape
from typing import Iterable, Mapping, Sequence


REFERENCE_RENDER_TYPES: dict[str, dict[str, object]] = {
    "migration_tracker_oracle": {
        "title": "Migration Tracker Visual Oracle",
        "purpose": "Reference style for tracker pages.",
        "tokens": [
            "blue progress bars",
            "phase percentages",
            "status badges",
            "operator cards",
            "route and evidence links",
        ],
    },
    "cdc_tracker": {
        "title": "CDC Tracker",
        "purpose": "CDC delivery and route readiness tracking.",
        "tokens": ["CDC", "routes", "source contract", "progress"],
    },
    "dev_tracker": {
        "title": "Dev Tracker",
        "purpose": "Development lifecycle tracking by phase.",
        "tokens": ["phase", "status", "evidence", "progress"],
    },
    "tool_registry_tracker": {
        "title": "Tool Registry Tracker",
        "purpose": "Tool registry CDC and cockpit coverage.",
        "tokens": ["tool registry", "cockpit", "scope", "contract"],
    },
    "benchmark_tracker": {
        "title": "Benchmark Tracker",
        "purpose": "Benchmark cockpit status tracking.",
        "tokens": ["benchmark", "AI trade", "metrics", "status"],
    },
}


COCKPIT_RENDER_BINDINGS: tuple[dict[str, str], ...] = (
    {
        "cockpit": "Migration Tracker",
        "route": "/global-migration",
        "render_type": "migration_tracker_oracle",
        "role": "visual oracle",
    },
    {
        "cockpit": "CDC Delivery Tracker",
        "route": "/cdc-tracker",
        "render_type": "cdc_tracker",
        "role": "CDC source and delivery status",
    },
    {
        "cockpit": "CDC Dev Tracker",
        "route": "/cdc-dev-tracker",
        "render_type": "cdc_tracker",
        "role": "operator CDC tracker page",
    },
    {
        "cockpit": "Dev Tracking",
        "route": "/dev-tracking",
        "render_type": "dev_tracker",
        "role": "development lifecycle cockpit",
    },
    {
        "cockpit": "Tool Registry CDC",
        "route": "/tool-registry-cdc",
        "render_type": "tool_registry_tracker",
        "role": "tool registry contract tracking",
    },
)


STATUS_TO_PERCENT: dict[str, int] = {
    "DONE": 100,
    "ACTIVE": 70,
    "NEXT": 35,
    "BLOCKED": 15,
    "PARKED": 10,
    "FUTURE": 5,
}


@dataclass(frozen=True)
class TrackerItem:
    item_id: str
    title: str
    status: str
    percent: int
    description: str = ""
    route: str = ""
    priority: str = ""


def normalize_percent(value: object, status: str = "") -> int:
    if isinstance(value, bool):
        return 100 if value else 0
    if isinstance(value, (int, float)):
        return max(0, min(100, int(round(value))))
    if isinstance(value, str):
        stripped = value.strip().replace("%", "")
        if stripped.isdigit():
            return max(0, min(100, int(stripped)))
    return STATUS_TO_PERCENT.get(status.upper(), 0)


def make_tracker_item(data: Mapping[str, object], fallback_id: str) -> TrackerItem:
    status = str(data.get("status") or "FUTURE").upper()
    item_id = str(
        data.get("phase_id") or data.get("id") or data.get("key") or data.get("name") or fallback_id
    )
    title = str(data.get("title") or data.get("name") or item_id)
    description = str(
        data.get("notes")
        or data.get("description")
        or data.get("summary")
        or data.get("details")
        or ""
    )
    percent = normalize_percent(
        data.get("percent") or data.get("progress") or data.get("completion") or data.get("pct"),
        status,
    )
    return TrackerItem(
        item_id=item_id,
        title=title,
        status=status,
        percent=percent,
        description=description,
        route=str(data.get("route") or ""),
        priority=str(data.get("priority") or ""),
    )


def tracker_items_from_phase_dicts(phases: Sequence[Mapping[str, object]]) -> list[TrackerItem]:
    return [make_tracker_item(phase, f"phase_{idx}") for idx, phase in enumerate(phases, 1)]


def render_progress(percent: int) -> str:
    safe_percent = max(0, min(100, int(percent)))
    return (
        '<div class="progress-track" data-progress-track="true">'
        f'<div class="progress-bar blue" data-progress="{safe_percent}" '
        f'style="width:{safe_percent}%"></div>'
        "</div>"
        f'<div class="progress-label">{safe_percent}%</div>'
    )


def render_badge(status: str) -> str:
    css = "status-" + escape(status.lower())
    return f'<span class="status-badge {css}">{escape(status)}</span>'


def render_reference_gallery() -> str:
    cards = []
    for ref_id, ref in REFERENCE_RENDER_TYPES.items():
        tokens = ", ".join(str(token) for token in ref["tokens"])
        cards.append(
            '<article class="tracker-card reference-card" '
            f'id="render-type-{escape(ref_id)}" data-render-type="{escape(ref_id)}">'
            f'<div class="card-kicker">{escape(ref_id)}</div>'
            f"<h3>{escape(str(ref['title']))}</h3>"
            f"<p>{escape(str(ref['purpose']))}</p>"
            f'<p class="muted">Tokens: {escape(tokens)}</p>'
            "</article>"
        )
    return (
        '<section class="tracker-panel" data-panel="reference-render-types">'
        "<h2>Reference render types</h2>"
        '<div class="tracker-grid">' + "".join(cards) + "</div></section>"
    )


def render_cockpit_bindings() -> str:
    rows = []
    for binding in COCKPIT_RENDER_BINDINGS:
        render_type = binding["render_type"]
        rows.append(
            "<tr>"
            f"<td>{escape(binding['cockpit'])}</td>"
            f"<td><code>{escape(binding['route'])}</code></td>"
            f'<td><a href="#render-type-{escape(render_type)}">{escape(render_type)}</a></td>'
            f"<td>{escape(binding['role'])}</td>"
            "</tr>"
        )
    return (
        '<section class="tracker-panel" data-panel="cockpit-bindings">'
        "<h2>Cockpit coverage</h2>"
        "<table><thead><tr><th>Cockpit</th><th>Route</th><th>Render type</th>"
        "<th>Role</th></tr></thead><tbody>" + "".join(rows) + "</tbody></table></section>"
    )


def render_tracker_section(
    title: str,
    subtitle: str,
    render_type: str,
    items: Iterable[TrackerItem],
    *,
    route: str = "",
) -> str:
    item_list = list(items)
    rows = []
    cards = []
    for item in item_list:
        rows.append(
            "<tr>"
            f"<td><code>{escape(item.item_id)}</code></td>"
            f"<td>{escape(item.title)}</td>"
            f"<td>{render_badge(item.status)}</td>"
            f"<td>{render_progress(item.percent)}</td>"
            f"<td>{escape(item.priority)}</td>"
            f"<td>{escape(item.description)}</td>"
            "</tr>"
        )
        cards.append(
            '<article class="tracker-card phase-card" '
            f'data-phase-id="{escape(item.item_id)}">'
            f'<div class="card-kicker">{escape(item.item_id)}</div>'
            f"<h3>{escape(item.title)}</h3>"
            f"<div>{render_badge(item.status)}</div>"
            f"{render_progress(item.percent)}"
            f'<p class="muted">{escape(item.description)}</p>'
            "</article>"
        )
    return (
        '<section class="tracker-panel tracker-section" '
        f'data-render-type="{escape(render_type)}" data-route="{escape(route)}">'
        f"<h2>{escape(title)}</h2>"
        f'<p class="section-subtitle">{escape(subtitle)}</p>'
        f'<div class="route-pill">{escape(route)}</div>'
        '<div class="tracker-grid">' + "".join(cards) + "</div>"
        "<table><thead><tr><th>ID</th><th>Title</th><th>Status</th><th>Progress</th>"
        "<th>Priority</th><th>Description</th></tr></thead><tbody>"
        + "".join(rows)
        + "</tbody></table></section>"
    )


def render_preview_page(
    *,
    title: str,
    cdc_items: Sequence[TrackerItem],
    dev_items: Sequence[TrackerItem],
    generated_at: str,
    source_note: str,
) -> str:
    cdc_done = sum(1 for item in cdc_items if item.status == "DONE")
    dev_done = sum(1 for item in dev_items if item.status == "DONE")
    cdc_percent = normalize_percent((cdc_done / max(1, len(cdc_items))) * 100)
    dev_percent = normalize_percent((dev_done / max(1, len(dev_items))) * 100)

    css = """
:root {
  --bg: #f6f8fc;
  --panel: #ffffff;
  --ink: #172033;
  --muted: #64748b;
  --line: #dbe4f0;
  --blue: #2563eb;
  --blue-soft: #dbeafe;
  --green: #16a34a;
  --amber: #d97706;
  --red: #dc2626;
}
body {
  margin: 0;
  font-family: Inter, Segoe UI, Roboto, sans-serif;
  background: var(--bg);
  color: var(--ink);
}
header {
  padding: 28px 36px;
  background: linear-gradient(135deg, #0f2f68, #2563eb);
  color: white;
}
main { padding: 26px 36px; }
h1 { margin: 0 0 8px 0; }
h2 { margin: 0 0 12px 0; }
h3 { margin: 6px 0 10px 0; }
.tracker-panel {
  background: var(--panel);
  border: 1px solid var(--line);
  border-radius: 18px;
  padding: 20px;
  margin: 0 0 18px 0;
  box-shadow: 0 10px 30px rgba(15, 23, 42, 0.06);
}
.tracker-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
  gap: 14px;
}
.tracker-card {
  border: 1px solid var(--line);
  border-radius: 16px;
  padding: 16px;
  background: linear-gradient(180deg, #ffffff, #f8fbff);
}
.card-kicker {
  font-size: 12px;
  font-weight: 800;
  letter-spacing: 0.06em;
  color: var(--blue);
  text-transform: uppercase;
}
.kpi-row {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(210px, 1fr));
  gap: 14px;
  margin: 18px 0;
}
.kpi {
  background: rgba(255,255,255,0.14);
  border: 1px solid rgba(255,255,255,0.24);
  border-radius: 16px;
  padding: 16px;
}
.kpi strong { display: block; font-size: 28px; }
.progress-track {
  height: 11px;
  border-radius: 999px;
  background: var(--blue-soft);
  overflow: hidden;
  margin-top: 12px;
}
.progress-bar.blue {
  height: 100%;
  background: linear-gradient(90deg, #1d4ed8, #60a5fa);
  border-radius: 999px;
}
.progress-label {
  color: var(--blue);
  font-weight: 800;
  font-size: 13px;
  margin-top: 4px;
}
.status-badge {
  display: inline-block;
  padding: 5px 10px;
  border-radius: 999px;
  color: #fff;
  font-size: 12px;
  font-weight: 800;
}
.status-done { background: var(--green); }
.status-active { background: var(--blue); }
.status-next { background: var(--blue); }
.status-blocked { background: var(--red); }
.status-parked { background: var(--amber); }
.status-future { background: #64748b; }
.route-pill {
  display: inline-block;
  margin: 0 0 12px 0;
  padding: 6px 10px;
  border-radius: 999px;
  background: var(--blue-soft);
  color: var(--blue);
  font-weight: 800;
}
.section-subtitle, .muted { color: var(--muted); }
table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 16px;
  font-size: 14px;
}
th, td {
  border-top: 1px solid var(--line);
  padding: 10px;
  vertical-align: top;
  text-align: left;
}
th { color: var(--blue); }
a { color: var(--blue); font-weight: 800; }
"""
    return (
        '<!doctype html><html lang="en"><head><meta charset="utf-8">'
        f"<title>{escape(title)}</title><style>{css}</style></head>"
        '<body data-ui-kit="tracker-common" data-visual-oracle="migration-tracker">'
        "<header>"
        f"<h1>{escape(title)}</h1>"
        "<p>Migration Tracker Visual Oracle alignment preview. "
        "This preview is not a Reflex deployment proof.</p>"
        '<div class="kpi-row">'
        f'<div class="kpi"><span>CDC Tracker progress</span><strong>{cdc_percent}%</strong>'
        f"{render_progress(cdc_percent)}</div>"
        f'<div class="kpi"><span>Dev Tracker progress</span><strong>{dev_percent}%</strong>'
        f"{render_progress(dev_percent)}</div>"
        f'<div class="kpi"><span>Source</span><strong>{escape(source_note)}</strong></div>'
        "</div>"
        "</header><main>"
        + render_reference_gallery()
        + render_cockpit_bindings()
        + render_tracker_section(
            "CDC Tracker",
            "CDC delivery tracker view with route/source readiness steps.",
            "cdc_tracker",
            cdc_items,
            route="/cdc-tracker",
        )
        + render_tracker_section(
            "Dev Tracker",
            "Development lifecycle tracker view with all known phases.",
            "dev_tracker",
            dev_items,
            route="/dev-tracking",
        )
        + '<section class="tracker-panel"><h2>Gate warning</h2>'
        "<p>Visual tests are mandatory before Reflex deployment. "
        "Browser/runtime visual proof is still required before deploy.</p></section>"
        f'<section class="tracker-panel"><h2>Generated</h2><p>{escape(generated_at)}</p></section>'
        "</main></body></html>"
    )
