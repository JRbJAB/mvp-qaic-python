"""R21N local cockpit preview renderer for MVP QAIC.

This module renders a static HTML preview from the R21K/R21L/R21M cockpit queue
model chain. It is stdlib-only and import-safe. File output is restricted to
run-report directories and is not intended for committed HTML artifacts.
"""

from __future__ import annotations

import json
from html import escape
from pathlib import Path
from typing import Any, Final, Mapping

from mvp_qaic_py.cockpit_queue_data_contract_r21k import contract_to_dict
from mvp_qaic_py.cockpit_queue_model_binding_r21l import build_cockpit_queue_model
from mvp_qaic_py.cockpit_queue_visual_planning_r21m import model_to_dict

PREVIEW_ID: Final[str] = "R21N_LOCAL_COCKPIT_PREVIEW_NO_RUNTIME"
REPO_ROOT: Final[Path] = Path(__file__).resolve().parents[1]
DEFAULT_RUN_REPORT_ROOT: Final[Path] = Path(r"C:\JRb_TRADING_OS\_RUN_REPORTS\MVP_QAIC_PY")
PREVIEW_HTML_FILENAME: Final[str] = "r21n_local_cockpit_preview.html"
PREVIEW_MANIFEST_FILENAME: Final[str] = "r21n_local_cockpit_preview_manifest.json"

TRACE_TOKENS: Final[tuple[str, ...]] = (
    "BRAND_CONFIG_TRACE_COCKPIT_READY",
    "UI_TRACKER_TRACE_COCKPIT_READY",
    "TOOL_REGISTRY_CDC_TRACE_COCKPIT_READY",
    "CDC_CONTRACT_TRACE_COCKPIT_READY",
    "QAIC_BRIDGE_TRACE_COCKPIT_READY",
)

BRAND_ASSETS: Final[dict[str, str | bool]] = {
    "QAIT_CHARTE_TEMPLATE": "BOUND",
    "MVP_QAIC_LOGO_VALIDATED": "BOUND",
    "validated_logo": "public/brand/mvp-qaic/logo-mvp-qaic-official-name.png",
    "validated_icon": "public/brand/mvp-qaic/logo-mvp-qaic-icon-only.png",
    "charte_template": "public/brand/mvp-qaic/charte-graphique.png",
    "preserve_q_candlesticks_signal_line": True,
    "no_generated_preview_replaces_validated_logo": True,
}

SAFETY_LOCKS: Final[dict[str, bool]] = {
    "NO_CODEX_RUNTIME": True,
    "NO_RUNTIME": True,
    "NO_DOCKER": True,
    "NO_REFLEX_RUN": True,
    "NO_PROVIDER_CALL": True,
    "NO_BROKER_ORDER_SIZING": True,
    "NO_SHEET_BQ_WRITE": True,
    "NO_05_EXPORTS": True,
    "HUMAN_REVIEW_REQUIRED": True,
}


def build_local_preview_payload() -> dict[str, Any]:
    """Build the local preview payload from R21K, R21L, and R21M sources."""
    r21k_contract = contract_to_dict()
    r21l_model = build_cockpit_queue_model()
    r21m_visual_plan = model_to_dict()

    return {
        "preview_id": PREVIEW_ID,
        "status": "LOCAL_COCKPIT_PREVIEW_READY_NO_RUNTIME",
        "source_bindings": {
            "SOURCE_R21K_CONTRACT_BOUND": r21k_contract["contract_id"]
            == "R21K_COCKPIT_QUEUE_DATA_CONTRACT_NO_RUNTIME",
            "SOURCE_R21L_MODEL_BINDING_BOUND": r21l_model["model_id"]
            == "R21L_COCKPIT_QUEUE_MODEL_BINDING_NO_RUNTIME",
            "SOURCE_R21M_VISUAL_PLANNING_BOUND": r21m_visual_plan["workflow_id"]
            == "R21M_COCKPIT_QUEUE_VISUAL_PLANNING_NO_RUNTIME",
        },
        "trace_tokens": {token: True for token in TRACE_TOKENS},
        "brand_config": dict(BRAND_ASSETS),
        "safety_locks": dict(SAFETY_LOCKS),
        "review_queue_handoff": {
            "section_id": "operator_queue",
            "title": "Review queue / QAIC handoff",
            "mode": "qaic_review_only",
            "qaic_execution_allowed": False,
            "human_review_required": True,
            "source_trace": "QAIC_BRIDGE_TRACE_COCKPIT_READY",
        },
        "r21k_contract": r21k_contract,
        "r21l_model": r21l_model,
        "r21m_visual_plan": r21m_visual_plan,
    }


def _preview_payload(payload: Mapping[str, Any] | None = None) -> Mapping[str, Any]:
    return build_local_preview_payload() if payload is None else payload


def _format_value(value: object) -> str:
    if isinstance(value, bool):
        return "True" if value else "False"
    return str(value)


def _definition_list(items: Mapping[str, object]) -> str:
    rows = []
    for key in sorted(items):
        rows.append(
            "<div class=\"kv-row\">"
            f"<dt>{escape(str(key))}</dt>"
            f"<dd>{escape(_format_value(items[key]))}</dd>"
            "</div>"
        )
    return "<dl class=\"kv-list\">" + "".join(rows) + "</dl>"


def _section_card(title: str, body: str, css_class: str = "panel") -> str:
    return (
        f"<section class=\"{css_class}\">"
        f"<h2>{escape(title)}</h2>"
        f"{body}"
        "</section>"
    )


def _render_lanes(payload: Mapping[str, Any]) -> str:
    visual_plan = payload["r21m_visual_plan"]
    lanes = visual_plan["lanes"]
    lane_html = []
    for lane in lanes:
        cards = "".join(
            "<article class=\"card\">"
            f"<h3>{escape(card['title'])}</h3>"
            f"<p class=\"status\">{escape(card['status'])}</p>"
            f"<p>{escape(card['body'])}</p>"
            f"<code>{escape(card['source_trace'])}</code>"
            "</article>"
            for card in lane["cards"]
        )
        lane_html.append(
            "<div class=\"lane\">"
            f"<h3>{escape(lane['title'])}</h3>"
            f"<p>{escape(lane['source_binding'])}</p>"
            f"<div class=\"cards\">{cards}</div>"
            "</div>"
        )
    return "".join(lane_html)


def _render_queue_rows(payload: Mapping[str, Any]) -> str:
    rows = payload["r21l_model"]["rows"]
    body = []
    for row in rows:
        body.append(
            "<tr>"
            f"<td>{escape(row['row_id'])}</td>"
            f"<td>{escape(row['section_id'])}</td>"
            f"<td>{escape(row['label'])}</td>"
            f"<td>{escape(row['status'])}</td>"
            f"<td><code>{escape(row['source_trace'])}</code></td>"
            "</tr>"
        )
    return (
        "<table><thead><tr><th>Row</th><th>Section</th><th>Label</th>"
        "<th>Status</th><th>Trace</th></tr></thead><tbody>"
        + "".join(body)
        + "</tbody></table>"
    )


def render_local_preview_html(payload: Mapping[str, Any] | None = None) -> str:
    """Render a static local cockpit preview HTML string."""
    preview = _preview_payload(payload)
    source_bindings = preview["source_bindings"]
    trace_tokens = preview["trace_tokens"]
    brand_config = preview["brand_config"]
    safety_locks = preview["safety_locks"]

    html = f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{escape(PREVIEW_ID)}</title>
  <style>
    :root {{ color-scheme: light; --ink:#111827; --muted:#526070; --line:#d8dee8; }}
    body {{ margin:0; font:14px/1.45 Arial, sans-serif; color:var(--ink); background:#f6f8fb; }}
    header {{ padding:28px 32px; background:#ffffff; border-bottom:1px solid var(--line); }}
    main {{ max-width:1180px; margin:0 auto; padding:24px; display:grid; gap:18px; }}
    h1, h2, h3 {{ margin:0 0 10px; letter-spacing:0; }}
    .banner {{ padding:14px 16px; background:#fff4df; border:1px solid #edc778; font-weight:700; }}
    .panel {{ background:#ffffff; border:1px solid var(--line); border-radius:8px; padding:18px; }}
    .grid {{ display:grid; grid-template-columns:repeat(auto-fit,minmax(260px,1fr)); gap:14px; }}
    .kv-list {{ display:grid; gap:8px; margin:0; }}
    .kv-row {{ display:grid; grid-template-columns:minmax(180px, 1fr) 2fr; gap:10px; }}
    dt {{ color:var(--muted); font-weight:700; }}
    dd {{ margin:0; overflow-wrap:anywhere; }}
    .lane {{ border-top:1px solid var(--line); padding-top:14px; margin-top:14px; }}
    .cards {{ display:grid; grid-template-columns:repeat(auto-fit,minmax(220px,1fr)); gap:12px; }}
    .card {{ border:1px solid var(--line); border-radius:8px; padding:14px; background:#fbfcff; }}
    .status {{ margin:0 0 8px; font-weight:700; color:#1f6f54; }}
    code {{ background:#edf2f7; padding:2px 5px; border-radius:4px; overflow-wrap:anywhere; }}
    table {{ width:100%; border-collapse:collapse; }}
    th, td {{ border-bottom:1px solid var(--line); padding:8px; text-align:left; vertical-align:top; }}
  </style>
</head>
<body>
  <header>
    <h1>MVP QAIC local cockpit preview</h1>
    <p>{escape(PREVIEW_ID)} - static preview renderer, no runtime.</p>
  </header>
  <main>
    <div class="banner">NO-RUNTIME SAFETY BANNER: static local preview only.</div>
    <div class="grid">
      {_section_card("Source bindings", _definition_list(source_bindings))}
      {_section_card("Cockpit traces", _definition_list(trace_tokens))}
    </div>
    {_section_card("Brand / config trace", _definition_list(brand_config))}
    {_section_card("Review queue / QAIC handoff", _render_queue_rows(preview))}
    {_section_card("Cockpit visual lanes", _render_lanes(preview))}
    {_section_card("Safety locks", _definition_list(safety_locks))}
  </main>
</body>
</html>
"""
    return html


def render_local_preview_manifest(payload: Mapping[str, Any] | None = None) -> dict[str, Any]:
    """Render the JSON-friendly manifest for local preview output."""
    preview = _preview_payload(payload)
    return {
        "preview_id": PREVIEW_ID,
        "status": preview["status"],
        "html_file": PREVIEW_HTML_FILENAME,
        "source_bindings": dict(preview["source_bindings"]),
        "trace_tokens": dict(preview["trace_tokens"]),
        "brand_config": dict(preview["brand_config"]),
        "safety_locks": dict(preview["safety_locks"]),
        "output_policy": {
            "LOCAL_PREVIEW_RENDERER": True,
            "NO_COMMITTED_HTML_OUTPUT": True,
            "PREVIEW_OUTPUT_RUN_REPORT_ONLY": True,
            "NO_05_EXPORTS": True,
        },
    }


def _is_relative_to(path: Path, base: Path) -> bool:
    try:
        path.relative_to(base)
    except ValueError:
        return False
    return True


def validate_preview_output_path(path: str | Path) -> Path:
    """Validate that preview output targets a run-report directory only."""
    candidate = Path(path).expanduser().resolve()
    parts_lower = {part.lower() for part in candidate.parts}
    forbidden_parts = {"05_exports", "public", "docs"}

    if _is_relative_to(candidate, REPO_ROOT):
        raise ValueError("preview output must not target the repository")
    if forbidden_parts & parts_lower:
        raise ValueError("preview output must not target docs, public, or export directories")
    if "_run_reports" not in parts_lower:
        raise ValueError("preview output must include an _RUN_REPORTS path component")
    if not (
        _is_relative_to(candidate, DEFAULT_RUN_REPORT_ROOT)
        or any(part.lower() == "_run_reports" for part in candidate.parts)
    ):
        raise ValueError("preview output must target a run-report root")

    return candidate


def write_local_preview(out_dir: str | Path) -> dict[str, Any]:
    """Write the local preview HTML and manifest under a validated output path."""
    output_dir = validate_preview_output_path(out_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    payload = build_local_preview_payload()
    html = render_local_preview_html(payload)
    manifest = render_local_preview_manifest(payload)

    html_path = output_dir / PREVIEW_HTML_FILENAME
    manifest_path = output_dir / PREVIEW_MANIFEST_FILENAME
    html_path.write_text(html, encoding="utf-8", newline="\n")
    manifest_path.write_text(
        json.dumps(manifest, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
        newline="\n",
    )

    return {
        "preview_id": PREVIEW_ID,
        "html_path": str(html_path),
        "manifest_path": str(manifest_path),
        "LOCAL_PREVIEW_RENDERER": True,
        "PREVIEW_OUTPUT_RUN_REPORT_ONLY": True,
        "NO_COMMITTED_HTML_OUTPUT": True,
    }
