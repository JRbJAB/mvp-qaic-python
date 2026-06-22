from __future__ import annotations

import html
import json
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from mvp_qaic_py.webapp_static_preview_export import build_static_preview_bundle


BINDING_ADMIN_SAFETY: dict[str, bool] = {
    "mvp_public_scope": True,
    "qaic_private_backend_separated": True,
    "canonical_webapp_index_do_not_overwrite": True,
    "admin_html_allowed": True,
    "no_index_html_generation": True,
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
    "local_admin_monitor_only": True,
}


def _now_iso(now_utc: str | None = None) -> str:
    if now_utc:
        return now_utc
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def _json(data: Any) -> str:
    return json.dumps(data, ensure_ascii=False, indent=2)


def build_canonical_binding_contract(now_utc: str | None = None) -> dict[str, Any]:
    bundle = build_static_preview_bundle(now_utc=now_utc)

    return {
        "runtime": "MVP_QAIC_CANONICAL_WEBAPP_BINDING_ADMIN",
        "version": "P107_R1_CANONICAL_WEBAPP_BINDING_ADMIN_0_1_0",
        "created_at_utc": _now_iso(now_utc),
        "status": "CANONICAL_BINDING_READY",
        "scope": {
            "mvp": "lexique_webapp_prompts_methods_benchmark_public",
            "qaic_private": "backend_quant_risk_revolutx_execution_locked",
        },
        "canonical_ui": {
            "role": "validated_webapp_shell",
            "file_name": "Index.html",
            "policy": "DO_NOT_OVERWRITE_FROM_PYTHON",
            "python_role": "generate_data_contracts_context_packs_and_admin_monitor_only",
            "requires_human_review_before_ui_change": True,
        },
        "allowed_generated_files": [
            "data/webapp_pack.json",
            "data/context_pack.json",
            "data/prompt_payload.json",
            "data/binding_contract.json",
            "data/admin_status.json",
            "WEBAPP_BINDING_CONTRACT.md",
            "admin/ADMIN_MONITOR.html",
            "admin/README_ADMIN_MONITOR.md",
        ],
        "forbidden_generated_files": [
            "index.html",
            "Index.html",
            "MVPQAIC_Index.html",
            "Code.gs",
            "appsscript.json",
        ],
        "data_sources": {
            "routes_count": len(bundle["routes"]),
            "sections_count": len(bundle["sections"]),
            "benchmark_available": True,
            "lexique_context_available": True,
            "method_context_available": True,
            "portfolio_prompt_input_modes": ["none", "pasted_text", "structured", "image_capture"],
        },
        "safety": dict(BINDING_ADMIN_SAFETY),
        "next": "P108_UI_POLISH_USING_CANONICAL_INDEX_OR_PUBLIC_DEPLOY_DECISION_GATE",
    }


def build_admin_status(now_utc: str | None = None) -> dict[str, Any]:
    contract = build_canonical_binding_contract(now_utc=now_utc)
    bundle = build_static_preview_bundle(now_utc=now_utc)
    prompt_payload = bundle["prompt_payload"]

    gates = [
        {
            "gate_id": "canonical_index_not_generated",
            "status": "PASS",
            "evidence": "No index.html is part of the generated binding pack.",
        },
        {
            "gate_id": "admin_monitor_generated",
            "status": "PASS",
            "evidence": "admin/ADMIN_MONITOR.html",
        },
        {
            "gate_id": "mvp_qaic_scope_separated",
            "status": "PASS",
            "evidence": contract["scope"],
        },
        {
            "gate_id": "no_public_deploy",
            "status": "PASS",
            "evidence": contract["safety"]["no_public_deploy"],
        },
        {
            "gate_id": "no_trading_execution",
            "status": "PASS",
            "evidence": {
                "no_broker": True,
                "no_order": True,
                "no_auto_sizing": True,
                "no_revolutx_real_access": True,
            },
        },
    ]

    return {
        "runtime": "MVP_QAIC_ADMIN_MONITOR_STATUS",
        "version": "P107_R1_ADMIN_MONITOR_STATUS_0_1_0",
        "created_at_utc": _now_iso(now_utc),
        "status": "ADMIN_MONITOR_READY",
        "decision_status": prompt_payload["decision_status"],
        "benchmark": prompt_payload["benchmark"],
        "routes_count": len(bundle["routes"]),
        "sections_count": len(bundle["sections"]),
        "gates": gates,
        "safety": dict(BINDING_ADMIN_SAFETY),
    }


def render_webapp_binding_contract_md(contract: dict[str, Any]) -> str:
    allowed = "\n".join(f"- `{item}`" for item in contract["allowed_generated_files"])
    forbidden = "\n".join(f"- `{item}`" for item in contract["forbidden_generated_files"])

    return f"""# MVP QAIC — Canonical WebApp Binding Contract

## Status

`{contract["status"]}`

## Canonical UI

- Canonical file: `{contract["canonical_ui"]["file_name"]}`
- Policy: `{contract["canonical_ui"]["policy"]}`
- Python role: `{contract["canonical_ui"]["python_role"]}`
- Human review before UI change: `{contract["canonical_ui"]["requires_human_review_before_ui_change"]}`

## Allowed generated files

{allowed}

## Forbidden generated files

{forbidden}

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

## Next

`{contract["next"]}`
"""


def render_admin_monitor_html(status: dict[str, Any]) -> str:
    gates = "\n".join(
        f"<li><strong>{html.escape(gate['gate_id'])}</strong>: "
        f"<code>{html.escape(gate['status'])}</code></li>"
        for gate in status["gates"]
    )
    benchmark = status["benchmark"]

    return f"""<!doctype html>
<html lang="fr">
<head>
  <meta charset="utf-8">
  <title>MVP QAIC — Admin Monitor</title>
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <style>
    body {{ font-family: Arial, sans-serif; margin: 32px; line-height: 1.45; }}
    .grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap: 12px; }}
    .card {{ border: 1px solid #ddd; border-radius: 8px; padding: 12px; }}
    code {{ background: #f4f4f4; padding: 2px 4px; }}
    .safe {{ color: #126b2d; }}
  </style>
</head>
<body>
  <header>
    <h1>MVP QAIC — Admin Monitor</h1>
    <p>Console locale d'administration et suivi. Ce fichier ne remplace pas l'Index.html WebApp validé.</p>
    <p class="safe">Canonical UI policy: DO_NOT_OVERWRITE_FROM_PYTHON.</p>
  </header>

  <section>
    <h2>Gates</h2>
    <ul>{gates}</ul>
  </section>

  <section>
    <h2>Benchmark</h2>
    <div class="grid">
      <div class="card">Qualité: <strong>{benchmark["quality_score"]}</strong></div>
      <div class="card">Sécurité publique: <strong>{benchmark["public_safety_score"]}</strong></div>
      <div class="card">Complétude données: <strong>{benchmark["data_completeness_score"]}</strong></div>
      <div class="card">Utilité pédagogique: <strong>{benchmark["public_usefulness_score"]}</strong></div>
    </div>
  </section>

  <section>
    <h2>Safety</h2>
    <p>NO_REVOLUTX_REAL_ACCESS | NO_BROKER | NO_ORDER | NO_AUTO_SIZING | NO_PUBLIC_DEPLOY</p>
  </section>
</body>
</html>
"""


def build_binding_admin_files(now_utc: str | None = None) -> dict[str, str]:
    contract = build_canonical_binding_contract(now_utc=now_utc)
    status = build_admin_status(now_utc=now_utc)
    bundle = build_static_preview_bundle(now_utc=now_utc)

    return {
        "data/webapp_pack.json": _json(bundle["webapp_pack"]),
        "data/context_pack.json": _json(bundle["context_pack"]),
        "data/prompt_payload.json": _json(bundle["prompt_payload"]),
        "data/binding_contract.json": _json(contract),
        "data/admin_status.json": _json(status),
        "WEBAPP_BINDING_CONTRACT.md": render_webapp_binding_contract_md(contract),
        "admin/ADMIN_MONITOR.html": render_admin_monitor_html(status),
        "admin/README_ADMIN_MONITOR.md": (
            "# Admin Monitor\n\n"
            "Local admin/suivi HTML only. It does not replace the validated WebApp Index.html.\n"
        ),
    }


def validate_no_canonical_index_generated(files: dict[str, str]) -> dict[str, Any]:
    forbidden = {"index.html", "Index.html", "MVPQAIC_Index.html"}
    generated = set(files)
    forbidden_hits = sorted(generated.intersection(forbidden))

    return {
        "status": "PASS" if not forbidden_hits else "BLOCKED",
        "forbidden_hits": forbidden_hits,
        "generated_file_count": len(generated),
    }


def write_binding_admin_files(
    output_dir: str | Path,
    *,
    now_utc: str | None = None,
) -> list[str]:
    root = Path(output_dir)
    files = build_binding_admin_files(now_utc=now_utc)
    validation = validate_no_canonical_index_generated(files)
    if validation["status"] != "PASS":
        raise RuntimeError(f"Forbidden canonical index generation: {validation}")

    written: list[str] = []
    for relative_path, content in files.items():
        path = root / relative_path
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")
        written.append(relative_path)

    return sorted(written)


def summarize_binding_admin(output_dir: str | Path, written: list[str]) -> dict[str, Any]:
    return {
        "output_dir": str(output_dir),
        "file_count": len(written),
        "files": sorted(written),
        "has_admin_monitor": "admin/ADMIN_MONITOR.html" in written,
        "has_binding_contract": "WEBAPP_BINDING_CONTRACT.md" in written,
        "has_webapp_pack": "data/webapp_pack.json" in written,
        "has_no_index_html": "index.html" not in written and "Index.html" not in written,
        "safety": dict(BINDING_ADMIN_SAFETY),
    }
