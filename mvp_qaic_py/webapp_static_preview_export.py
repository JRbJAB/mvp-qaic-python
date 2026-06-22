from __future__ import annotations

import html
import json
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from mvp_qaic_py.lexique_method_prompt_context import (
    build_default_demo_lexique,
    build_default_demo_methods,
    build_lexique_method_prompt_context_pack,
)
from mvp_qaic_py.prompt_webapp_benchmark_public import build_mvp_public_prompt_payload
from mvp_qaic_py.webapp_prompt_benchmark_pack import build_webapp_prompt_benchmark_pack


STATIC_PREVIEW_SAFETY: dict[str, bool] = {
    "mvp_public_scope": True,
    "qaic_private_backend_separated": True,
    "no_revolutx_real_access": True,
    "no_broker": True,
    "no_order": True,
    "no_cancel": True,
    "no_replace_order": True,
    "no_auto_sizing": True,
    "no_secret_log": True,
    "no_sheet_write": True,
    "no_apps_script_execution": True,
    "no_clasp": True,
    "no_public_deploy": True,
    "local_static_preview_only": True,
}


def _now_iso(now_utc: str | None = None) -> str:
    if now_utc:
        return now_utc
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def _json(data: Any) -> str:
    return json.dumps(data, ensure_ascii=False, indent=2)


def build_demo_prompt_payload(now_utc: str | None = None) -> dict[str, Any]:
    return build_mvp_public_prompt_payload(
        user_prompt="Analyse BTC et ETH avec une méthode portfolio educational review.",
        portfolio_input="BTC 0.10 60000 6800 800\nETH 1.0 3000 3200 200",
        portfolio_input_type="pasted_text",
        lexique_context={"BTC": "Bitcoin", "ETH": "Ethereum"},
        methods_context={"method": "portfolio educational review"},
        benchmark_context={"profile": "static_preview"},
        now_utc=now_utc,
    )


def build_static_preview_bundle(now_utc: str | None = None) -> dict[str, Any]:
    prompt_payload = build_demo_prompt_payload(now_utc=now_utc)
    lexique_items = build_default_demo_lexique()
    method_items = build_default_demo_methods()

    context_pack = build_lexique_method_prompt_context_pack(
        prompt_payload=prompt_payload,
        lexique_items=lexique_items,
        method_items=method_items,
        now_utc=now_utc,
    )

    webapp_pack = build_webapp_prompt_benchmark_pack(
        lexique_items=lexique_items,
        method_items=method_items,
        now_utc=now_utc,
    )

    return {
        "runtime": "MVP_QAIC_WEBAPP_STATIC_PREVIEW_DATA_EXPORT",
        "version": "P106_WEBAPP_STATIC_PREVIEW_DATA_EXPORT_0_1_0",
        "created_at_utc": _now_iso(now_utc),
        "scope": {
            "mvp": "lexique_webapp_prompts_methods_benchmark_public",
            "qaic_private": "backend_quant_risk_revolutx_execution_locked",
        },
        "safety": dict(STATIC_PREVIEW_SAFETY),
        "routes": webapp_pack["ui_schema"]["routes"],
        "sections": webapp_pack["ui_schema"]["sections"],
        "prompt_payload": prompt_payload,
        "webapp_pack": webapp_pack,
        "context_pack": context_pack,
        "static_files": [
            "index.html",
            "data/webapp_pack.json",
            "data/context_pack.json",
            "data/prompt_payload.json",
            "preview_manifest.json",
            "README_PREVIEW.md",
        ],
    }


def render_index_html(bundle: dict[str, Any]) -> str:
    context_pack = bundle["context_pack"]
    prompt_payload = bundle["prompt_payload"]
    benchmark = prompt_payload["benchmark"]

    routes_html = "\n".join(
        f"<li><code>{html.escape(route['path'])}</code> — {html.escape(route['view'])}</li>"
        for route in bundle["routes"]
    )

    lexique_cards = context_pack["context_cards"]["lexique_cards"]
    method_cards = context_pack["context_cards"]["method_cards"]

    lexique_html = "\n".join(
        f"<article><h3>{html.escape(card['title'])}</h3><p>{html.escape(card['body'])}</p></article>"
        for card in lexique_cards
    )
    method_html = "\n".join(
        f"<article><h3>{html.escape(card['title'])}</h3><p>{html.escape(card['body'])}</p></article>"
        for card in method_cards
    )

    return f"""<!doctype html>
<html lang="fr">
<head>
  <meta charset="utf-8">
  <title>MVP QAIC — Static Preview</title>
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <style>
    body {{ font-family: Arial, sans-serif; margin: 32px; line-height: 1.45; }}
    header, section {{ margin-bottom: 28px; }}
    .grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap: 12px; }}
    .card, article {{ border: 1px solid #ddd; border-radius: 8px; padding: 12px; }}
    code {{ background: #f4f4f4; padding: 2px 4px; }}
    .blocked {{ color: #8a1f11; }}
    .safe {{ color: #126b2d; }}
  </style>
</head>
<body>
  <header>
    <h1>MVP QAIC — WebApp Preview</h1>
    <p><strong>Scope MVP:</strong> lexique + webapp + prompts + méthodes + benchmark public.</p>
    <p><strong>QAIC privé:</strong> backend quant + risque + Revolut X + exécution verrouillée.</p>
    <p class="safe">Safety: no RevolutX réel, no broker, no order, no sizing, no public deploy.</p>
  </header>

  <section>
    <h2>Routes prévues</h2>
    <ul>{routes_html}</ul>
  </section>

  <section>
    <h2>Benchmark prompt</h2>
    <div class="grid">
      <div class="card">Qualité: <strong>{benchmark["quality_score"]}</strong></div>
      <div class="card">Sécurité publique: <strong>{benchmark["public_safety_score"]}</strong></div>
      <div class="card">Complétude données: <strong>{benchmark["data_completeness_score"]}</strong></div>
      <div class="card">Utilité pédagogique: <strong>{benchmark["public_usefulness_score"]}</strong></div>
    </div>
  </section>

  <section>
    <h2>Lexique context</h2>
    <div class="grid">{lexique_html}</div>
  </section>

  <section>
    <h2>Méthodes context</h2>
    <div class="grid">{method_html}</div>
  </section>

  <section>
    <h2>Data files</h2>
    <ul>
      <li><code>data/webapp_pack.json</code></li>
      <li><code>data/context_pack.json</code></li>
      <li><code>data/prompt_payload.json</code></li>
      <li><code>preview_manifest.json</code></li>
    </ul>
  </section>
</body>
</html>
"""


def build_static_preview_files(now_utc: str | None = None) -> dict[str, str]:
    bundle = build_static_preview_bundle(now_utc=now_utc)
    manifest = {
        "runtime": bundle["runtime"],
        "version": bundle["version"],
        "created_at_utc": bundle["created_at_utc"],
        "safety": bundle["safety"],
        "files": bundle["static_files"],
        "route_count": len(bundle["routes"]),
        "section_count": len(bundle["sections"]),
    }

    readme = """# MVP QAIC — Static Preview

Local static preview only.

## Open

Open `index.html` locally.

## Safety

- NO_REVOLUTX_REAL_ACCESS
- NO_BROKER
- NO_ORDER
- NO_CANCEL
- NO_REPLACE_ORDER
- NO_AUTO_SIZING
- NO_SECRET_LOG
- NO_SHEET_WRITE
- NO_APPS_SCRIPT_EXECUTION
- NO_CLASP
- NO_PUBLIC_DEPLOY
"""

    return {
        "index.html": render_index_html(bundle),
        "data/webapp_pack.json": _json(bundle["webapp_pack"]),
        "data/context_pack.json": _json(bundle["context_pack"]),
        "data/prompt_payload.json": _json(bundle["prompt_payload"]),
        "preview_manifest.json": _json(manifest),
        "README_PREVIEW.md": readme,
    }


def write_static_preview_files(
    output_dir: str | Path,
    *,
    now_utc: str | None = None,
) -> list[str]:
    root = Path(output_dir)
    files = build_static_preview_files(now_utc=now_utc)
    written: list[str] = []

    for relative_path, content in files.items():
        path = root / relative_path
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")
        written.append(relative_path)

    return sorted(written)


def summarize_static_preview(output_dir: str | Path, written: list[str]) -> dict[str, Any]:
    return {
        "output_dir": str(output_dir),
        "file_count": len(written),
        "files": sorted(written),
        "has_index": "index.html" in written,
        "has_webapp_pack": "data/webapp_pack.json" in written,
        "has_context_pack": "data/context_pack.json" in written,
        "has_prompt_payload": "data/prompt_payload.json" in written,
        "safety": dict(STATIC_PREVIEW_SAFETY),
    }
