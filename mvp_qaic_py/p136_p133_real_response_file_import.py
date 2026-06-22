from __future__ import annotations

import argparse
import hashlib
import json
import sys
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


P136_VERSION = "MVP_QAIC_P136_R1_STITCH_UI_LOGIC_FIX_20260622"

DEFAULT_RUN_ID = "P136-R1-P133-REAL-RESPONSE-FILE-IMPORT"
DEFAULT_GEM_ID = "GEM_GENERAL_REVIEW"

ACTIVE_GEM_PROFILES: tuple[dict[str, Any], ...] = (
    {
        "gem_id": "GEM_GENERAL_REVIEW",
        "label": "GEM General Review",
        "status": "ACTIVE",
        "default": True,
        "prompt_profile": "P132_R2_MULTIMODAL_PORTFOLIO_USD",
        "description": "Profil standard pour extraction portefeuille Revolut X / USD avec résumé lisible + JSON pretty.",
    },
    {
        "gem_id": "GEM_PORTFOLIO_REVIEW",
        "label": "GEM Portfolio Review",
        "status": "ACTIVE",
        "default": False,
        "prompt_profile": "P132_R2_MULTIMODAL_PORTFOLIO_USD",
        "description": "Profil centré sur inventaire positions, allocations, PnL et cohérences arithmétiques.",
    },
    {
        "gem_id": "GEM_RISK_GUARD_REVIEW",
        "label": "GEM Risk Guard Review",
        "status": "ACTIVE",
        "default": False,
        "prompt_profile": "P132_R2_RISK_GUARD_REVIEW",
        "description": "Profil centré blockers, incertitudes, human review et garde-fous no order/no sizing.",
    },
)

SAFETY_MARKERS: tuple[str, ...] = (
    "LOCAL_PRIVATE_ONLY",
    "P136_P133_REAL_RESPONSE_FILE_IMPORT",
    "P136_R1_STITCH_UI_LOGIC_INTEGRATED",
    "ACTIVE_GEM_SELECTION_LIST",
    "PROMPT_CORRECTIONS_QUEUE",
    "STITCH_UI_BLUEPRINT_EXPORT",
    "STITCH_HANDOFF_LOCAL_SPEC_ONLY",
    "P133_COMMAND_PREVIEW",
    "NO_PUBLIC_DEPLOY",
    "NO_TUNNEL",
    "NO_REMOTE_ACCESS",
    "NO_BROKER",
    "NO_ORDER",
    "NO_SIZING",
    "NO_AUTO_APPLY_GEM_RESPONSE",
    "NO_REVOLUTX_REAL_ACCESS_FROM_MVP",
    "NO_SHEET_WRITE",
    "NO_BIGQUERY_WRITE",
    "HUMAN_REVIEW_REQUIRED",
)


DEFAULT_RESPONSE_TEMPLATE = """# P136 — Réponse GEM à importer

Colle ici la réponse GEM complète, puis relance P136 avec --response-file ou utilise la commande P133 générée.

Contraintes attendues :
- réponse en français ;
- résumé lisible ;
- bloc JSON fenced `json` pretty-printed ;
- `image_used=IMAGE_USED` si la capture a bien été utilisée ;
- `human_review_required=true` ;
- `no_order_no_sizing=true`.
"""


@dataclass(frozen=True)
class P136Request:
    output_dir: Path = Path("05_EXPORTS/P136_P133_REAL_RESPONSE_FILE_IMPORT")
    exports_dir: Path = Path("05_EXPORTS")
    response_file: Path | None = None
    gem_id: str = DEFAULT_GEM_ID
    run_id: str = DEFAULT_RUN_ID
    generated_at_utc: str | None = None
    host: str = "127.0.0.1"
    port: int = 8088


def _utc_now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def _ensure_dir(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)


def _read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def _sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def _ps_quote(value: str | Path) -> str:
    return "'" + str(value).replace("'", "''") + "'"


def get_active_gem_profiles() -> list[dict[str, Any]]:
    return [dict(profile) for profile in ACTIVE_GEM_PROFILES if profile.get("status") == "ACTIVE"]


def get_active_gem_ids() -> list[str]:
    return [profile["gem_id"] for profile in get_active_gem_profiles()]


def validate_gem_id(gem_id: str) -> dict[str, Any]:
    for profile in get_active_gem_profiles():
        if profile["gem_id"] == gem_id:
            return profile
    allowed = ", ".join(get_active_gem_ids())
    raise ValueError(f"Unknown or inactive gem_id: {gem_id}. Allowed: {allowed}")


def build_p133_capture_command(
    response_file: Path,
    output_dir: Path,
    run_id: str,
    generated_at_utc: str | None = None,
) -> str:
    generated_at = generated_at_utc or _utc_now_iso()
    response_q = _ps_quote(response_file)
    output_q = _ps_quote(output_dir)
    run_id_q = _ps_quote(run_id)
    generated_q = _ps_quote(generated_at)

    return f"""$ErrorActionPreference = "Stop"
chcp 65001 | Out-Null
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
$OutputEncoding = [System.Text.Encoding]::UTF8

$GitExe = (Get-Command git.exe -ErrorAction SilentlyContinue).Source
$RepoRoot = $null

if ($GitExe) {{
  try {{
    $maybeRoot = (& $GitExe rev-parse --show-toplevel 2>$null)
    if ($LASTEXITCODE -eq 0 -and $maybeRoot) {{
      $maybeRoot = $maybeRoot.Trim()
      if ((Split-Path -Leaf $maybeRoot) -eq "MVP_QAIC_PY") {{
        $RepoRoot = $maybeRoot
      }}
    }}
  }} catch {{}}
}}

if (-not $RepoRoot) {{
  $people = [string]::Concat([char]0xD83D, [char]0xDC65)
  $chart  = [string]::Concat([char]0xD83D, [char]0xDCC8)
  $RepoRoot = "G:\\Mon Drive\\$people JULIEN [Perso]\\$chart Trading JRb\\Solutions & Dev (Trading JRb)\\MVP_QAIC_PY"
}}

if (-not (Test-Path -LiteralPath $RepoRoot)) {{
  throw "Repo introuvable: $RepoRoot"
}}

Set-Location -LiteralPath $RepoRoot

$responseText = {response_q}
$outputDir = {output_q}
New-Item -ItemType Directory -Path $outputDir -Force | Out-Null

python -m mvp_qaic_py.gem_multimodal_response_capture_gate `
  --response-text $responseText `
  --output-dir $outputDir `
  --run-id {run_id_q} `
  --generated-at-utc {generated_q}

Write-Host "P133_OUTPUT_DIR=$outputDir"
Write-Host "OPEN_FIRST=$(Join-Path $outputDir 'P133_GEM_RESPONSE_HUMAN_REVIEW.md')"
Write-Host "OPEN_JSON=$(Join-Path $outputDir 'P133_GEM_RESPONSE_PRETTY.json')"
"""


def build_stitch_ui_logic_spec(gem_profile: dict[str, Any]) -> dict[str, Any]:
    return {
        "status": "STITCH_UI_BLUEPRINT_READY",
        "handoff_mode": "LOCAL_SPEC_ONLY",
        "target_runtime": "NiceGUI local private",
        "selected_gem_id": gem_profile["gem_id"],
        "design_intent": "Cockpit opérateur clair pour prompt GEM, réponse GEM réelle, gate P133 et corrections prompts.",
        "screens": [
            {
                "screen_id": "prompt_cockpit",
                "title": "MVP QAIC — GEM Portfolio Prompt Cockpit",
                "goal": "Préparer le prompt, choisir le GEM actif, copier vers GEM et suivre les garde-fous.",
                "components": [
                    "header_status_badges",
                    "active_gem_select",
                    "prompt_copy_panel",
                    "gemini_open_button",
                    "safety_guardrails_panel",
                ],
            },
            {
                "screen_id": "response_import",
                "title": "P136 — Réponse GEM réelle",
                "goal": "Importer une réponse GEM depuis fichier local et préparer le P133 gate.",
                "components": [
                    "response_file_status",
                    "response_text_preview",
                    "p133_command_preview",
                    "human_review_warning",
                ],
            },
            {
                "screen_id": "prompt_corrections",
                "title": "Corrections prompts",
                "goal": "Lister les corrections prompts candidates avant application future.",
                "components": [
                    "prompt_corrections_table",
                    "priority_badges",
                    "scope_filter",
                    "next_action_panel",
                ],
            },
        ],
        "layout_rules": {
            "density": "operator_dense_but_readable",
            "theme": "dark_professional",
            "primary_layout": "two_column_desktop_single_column_mobile",
            "no_empty_rows": True,
            "badges_for_safety": True,
            "monospace_for_prompt_and_json": True,
        },
        "forbidden_behaviors": [
            "no_public_deploy",
            "no_tunnel",
            "no_broker",
            "no_order",
            "no_sizing",
            "no_auto_apply",
            "no_revolutx_real_access_from_mvp",
        ],
    }


def _prompt_corrections_queue(gem_profile: dict[str, Any]) -> list[dict[str, Any]]:
    return [
        {
            "correction_id": "P136_PROMPT_001",
            "priority": "HIGH",
            "status": "TODO",
            "scope": "GEM_SELECTION",
            "issue": "Le cockpit doit permettre le choix contrôlé du Gem actif.",
            "proposed_fix": "Utiliser uniquement gem_id depuis ACTIVE_GEM_PROFILES.",
            "gem_id": gem_profile["gem_id"],
        },
        {
            "correction_id": "P136_PROMPT_002",
            "priority": "HIGH",
            "status": "TODO",
            "scope": "P132_R2_OUTPUT_FORMAT",
            "issue": "Renforcer la sortie résumé lisible + JSON pretty fenced.",
            "proposed_fix": "Ajouter un garde-fou de format dans la prochaine correction de prompt.",
            "gem_id": gem_profile["gem_id"],
        },
        {
            "correction_id": "P136_PROMPT_003",
            "priority": "MEDIUM",
            "status": "TODO",
            "scope": "IMAGE_USAGE_EVIDENCE",
            "issue": "Rendre la preuve d'utilisation image plus visible pour human review.",
            "proposed_fix": "Exiger un court champ/texte d'évidence image_used avant JSON.",
            "gem_id": gem_profile["gem_id"],
        },
        {
            "correction_id": "P136_PROMPT_004",
            "priority": "MEDIUM",
            "status": "TODO",
            "scope": "STITCH_UI_LOGIC",
            "issue": "Aligner les prompts avec la logique UI Stitch/NiceGUI.",
            "proposed_fix": "Synchroniser les écrans prompt, import réponse, P133 gate et corrections dans une spec UI unique.",
            "gem_id": gem_profile["gem_id"],
        },
    ]


def build_p136_payload(request: P136Request) -> dict[str, Any]:
    generated_at = request.generated_at_utc or _utc_now_iso()
    gem_profile = validate_gem_id(request.gem_id)

    imported_response_file = request.output_dir / "P136_IMPORTED_GEM_RESPONSE.md"
    p133_output_dir = request.output_dir / "P133_FROM_P136_REAL_RESPONSE_IMPORT"

    response_source_exists = bool(request.response_file and request.response_file.exists())
    response_text = ""
    if response_source_exists and request.response_file is not None:
        response_text = _read_text(request.response_file)
    elif imported_response_file.exists():
        response_text = _read_text(imported_response_file)

    p133_command = build_p133_capture_command(
        response_file=imported_response_file,
        output_dir=p133_output_dir,
        run_id=f"{request.run_id}-P133-GATE",
        generated_at_utc=generated_at,
    )
    stitch_spec = build_stitch_ui_logic_spec(gem_profile)

    return {
        "step": "P136_P133_REAL_RESPONSE_FILE_IMPORT",
        "version": P136_VERSION,
        "status": "P136_REAL_RESPONSE_IMPORT_READY",
        "generated_at_utc": generated_at,
        "run_id": request.run_id,
        "local_url": f"http://{request.host}:{request.port}",
        "selected_gem": gem_profile,
        "active_gem_ids": get_active_gem_ids(),
        "active_gem_profiles": get_active_gem_profiles(),
        "stitch_ui_logic": stitch_spec,
        "response_import": {
            "source_response_file": str(request.response_file) if request.response_file else None,
            "source_response_file_exists": response_source_exists,
            "imported_response_file": str(imported_response_file),
            "response_char_count": len(response_text),
            "response_line_count": len(response_text.splitlines()),
            "response_sha256": _sha256_text(response_text) if response_text else None,
        },
        "p133_gate": {
            "output_dir": str(p133_output_dir),
            "command_file": str(request.output_dir / "P136_P133_CAPTURE_COMMAND.ps1"),
            "command_preview": p133_command,
            "executes_automatically": False,
            "human_review_required": True,
        },
        "prompt_corrections_queue": _prompt_corrections_queue(gem_profile),
        "safety_markers": list(SAFETY_MARKERS),
        "features": {
            "real_response_file_import": True,
            "active_gem_selection": True,
            "stitch_ui_logic_integrated": True,
            "prompt_corrections_queue": True,
            "p133_command_preview": True,
            "local_private_only": True,
            "no_broker_execution": True,
            "no_order": True,
            "no_sizing": True,
            "no_auto_apply": True,
        },
    }


def _write_prompt_corrections_md(path: Path, payload: dict[str, Any]) -> None:
    rows = payload["prompt_corrections_queue"]
    lines = [
        "# P136 — Prompt Corrections Queue",
        "",
        f"Selected GEM: `{payload['selected_gem']['gem_id']}`",
        "",
        "| correction_id | priority | status | scope | issue | proposed_fix |",
        "|---|---:|---|---|---|---|",
    ]
    for row in rows:
        lines.append(
            "| {correction_id} | {priority} | {status} | {scope} | {issue} | {proposed_fix} |".format(
                **row
            )
        )
    lines.append("")
    lines.append("Safety: local private only, no broker, no order, no sizing, no auto apply.")
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def _write_stitch_spec_md(path: Path, payload: dict[str, Any]) -> None:
    stitch = payload["stitch_ui_logic"]
    lines = [
        "# P136-R1 — Stitch UI Logic Spec",
        "",
        f"Status: `{stitch['status']}`",
        f"Handoff mode: `{stitch['handoff_mode']}`",
        f"Runtime cible: `{stitch['target_runtime']}`",
        f"Selected GEM: `{stitch['selected_gem_id']}`",
        "",
        "## Screens",
        "",
    ]
    for screen in stitch["screens"]:
        lines.append(f"### {screen['screen_id']} — {screen['title']}")
        lines.append("")
        lines.append(screen["goal"])
        lines.append("")
        for component in screen["components"]:
            lines.append(f"- `{component}`")
        lines.append("")
    lines.append("## Forbidden behaviors")
    lines.append("")
    for behavior in stitch["forbidden_behaviors"]:
        lines.append(f"- `{behavior}`")
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def _write_runbook(path: Path, payload: dict[str, Any]) -> None:
    text = f"""# P136-R1 — P133 Real Response File Import + Stitch UI Logic

## Objectif

Importer proprement une réponse GEM réelle depuis fichier local, choisir le GEM actif depuis une liste contrôlée, préparer la commande P133, et exposer une logique UI Stitch/NiceGUI locale.

## GEM sélectionné

- gem_id: `{payload["selected_gem"]["gem_id"]}`
- label: `{payload["selected_gem"]["label"]}`
- prompt_profile: `{payload["selected_gem"]["prompt_profile"]}`

## Stitch UI logic

- status: `{payload["stitch_ui_logic"]["status"]}`
- handoff_mode: `{payload["stitch_ui_logic"]["handoff_mode"]}`
- file: `P136_STITCH_UI_LOGIC_SPEC.json`

## Fichiers

- Réponse importée: `{payload["response_import"]["imported_response_file"]}`
- Commande P133: `{payload["p133_gate"]["command_file"]}`
- Output P133: `{payload["p133_gate"]["output_dir"]}`
- Corrections prompts: `P136_PROMPT_CORRECTIONS_QUEUE.md`

## Commande P133

```powershell
{payload["p133_gate"]["command_preview"]}
```

## Sécurité

- Local privé uniquement.
- Aucun broker, ordre, sizing, auto-apply.
- Human review obligatoire.
"""
    path.write_text(text, encoding="utf-8")


def write_p136_import_pack(request: P136Request) -> dict[str, Any]:
    _ensure_dir(request.output_dir)

    imported_response_file = request.output_dir / "P136_IMPORTED_GEM_RESPONSE.md"
    if request.response_file and request.response_file.exists():
        imported_response_file.write_text(_read_text(request.response_file), encoding="utf-8")
    elif not imported_response_file.exists():
        imported_response_file.write_text(DEFAULT_RESPONSE_TEMPLATE, encoding="utf-8")

    payload = build_p136_payload(request)

    (request.output_dir / "P136_REAL_RESPONSE_FILE_IMPORT_CONTRACT.json").write_text(
        json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=False) + "\n",
        encoding="utf-8",
    )
    (request.output_dir / "P136_ACTIVE_GEM_PROFILES.json").write_text(
        json.dumps(payload["active_gem_profiles"], ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    (request.output_dir / "P136_STITCH_UI_LOGIC_SPEC.json").write_text(
        json.dumps(payload["stitch_ui_logic"], ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    (request.output_dir / "P136_P133_CAPTURE_COMMAND.ps1").write_text(
        payload["p133_gate"]["command_preview"],
        encoding="utf-8-sig",
    )
    _write_prompt_corrections_md(
        request.output_dir / "P136_PROMPT_CORRECTIONS_QUEUE.md",
        payload,
    )
    _write_stitch_spec_md(request.output_dir / "P136_STITCH_UI_LOGIC_SPEC.md", payload)
    _write_runbook(request.output_dir / "P136_RUNBOOK.md", payload)
    return payload


def build_nicegui_app(payload: dict[str, Any]) -> Any:
    try:
        from nicegui import app, ui
        from starlette.responses import Response
    except ImportError as exc:  # pragma: no cover
        raise RuntimeError("NiceGUI is required only for --launch mode.") from exc

    @app.get("/favicon.ico")
    async def p136_favicon() -> Response:
        return Response(status_code=204)

    @ui.page("/")
    def p136_home() -> None:
        ui.page_title("MVP QAIC — P136 GEM Response Import")
        ui.add_head_html(
            """
            <style>
              body { background: #0b1020; color: #e5e7eb; }
              .q-page { background: transparent; }
              .p136-shell { width: min(1450px, calc(100vw - 32px)); margin: 0 auto; padding: 18px 0 40px; }
              .p136-card { border: 1px solid #263249; background: rgba(17,24,39,.92); border-radius: 16px; padding: 16px; }
              .p136-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 16px; }
              @media (max-width: 1050px) { .p136-grid { grid-template-columns: 1fr; } }
              .p136-pill { border: 1px solid #263249; border-radius: 999px; padding: 5px 10px; font-size: 12px; }
              .p136-good { color: #34d399; }
              textarea { font-family: ui-monospace, Consolas, monospace; }
            </style>
            """
        )

        active_options = {
            profile["gem_id"]: f"{profile['gem_id']} — {profile['label']}"
            for profile in payload["active_gem_profiles"]
        }

        with ui.column().classes("p136-shell gap-4"):
            with ui.card().classes("p136-card w-full"):
                ui.markdown("## P136-R1 — GEM Response Import → P133 Gate")
                with ui.row().classes("gap-2"):
                    ui.label("LOCAL_PRIVATE_ONLY").classes("p136-pill p136-good")
                    ui.label("ACTIVE_GEM_SELECTION_LIST").classes("p136-pill")
                    ui.label("STITCH_UI_BLUEPRINT_EXPORT").classes("p136-pill")
                    ui.label("NO_BROKER / NO_ORDER / NO_SIZING").classes("p136-pill")
                ui.markdown(
                    "Choisis le Gem actif, importe/sauvegarde la réponse GEM en fichier local, "
                    "prépare P133, puis garde la logique UI Stitch/NiceGUI alignée."
                )

            with ui.element("div").classes("p136-grid"):
                with ui.card().classes("p136-card w-full"):
                    ui.markdown("### 1) Choix du Gem actif")
                    ui.select(
                        options=active_options,
                        value=payload["selected_gem"]["gem_id"],
                        label="Gem actif",
                    ).classes("w-full")
                    ui.code(
                        json.dumps(payload["active_gem_profiles"], ensure_ascii=False, indent=2),
                        language="json",
                    )

                with ui.card().classes("p136-card w-full"):
                    ui.markdown("### 2) Réponse GEM réelle")
                    ui.markdown(
                        f"Fichier cible local : `{payload['response_import']['imported_response_file']}`"
                    )
                    ui.textarea(
                        value="",
                        placeholder="Coller ici la réponse GEM pour inspection visuelle. La sauvegarde fiable reste le fichier local P136_IMPORTED_GEM_RESPONSE.md.",
                    ).props("rows=20 outlined").classes("w-full")

                with ui.card().classes("p136-card w-full"):
                    ui.markdown("### 3) Commande P133")
                    ui.code(payload["p133_gate"]["command_preview"], language="powershell")

                with ui.card().classes("p136-card w-full"):
                    ui.markdown("### 4) Stitch UI logic")
                    ui.code(
                        json.dumps(payload["stitch_ui_logic"], ensure_ascii=False, indent=2),
                        language="json",
                    )

                with ui.card().classes("p136-card w-full"):
                    ui.markdown("### 5) Corrections prompts")
                    ui.code(
                        json.dumps(
                            payload["prompt_corrections_queue"], ensure_ascii=False, indent=2
                        ),
                        language="json",
                    )

    return ui


def launch_p136(request: P136Request) -> None:
    payload = build_p136_payload(request)
    ui = build_nicegui_app(payload)
    ui.run(host=request.host, port=request.port, reload=False, show=False)


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="P136 P133 real GEM response file import")
    parser.add_argument(
        "--output-dir", type=Path, default=Path("05_EXPORTS/P136_P133_REAL_RESPONSE_FILE_IMPORT")
    )
    parser.add_argument("--exports-dir", type=Path, default=Path("05_EXPORTS"))
    parser.add_argument("--response-file", type=Path, default=None)
    parser.add_argument("--gem-id", choices=get_active_gem_ids(), default=DEFAULT_GEM_ID)
    parser.add_argument("--run-id", default=DEFAULT_RUN_ID)
    parser.add_argument("--generated-at-utc", default=None)
    parser.add_argument("--dry-run-export", action="store_true")
    parser.add_argument("--launch", action="store_true")
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=8088)
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    request = P136Request(
        output_dir=args.output_dir,
        exports_dir=args.exports_dir,
        response_file=args.response_file,
        gem_id=args.gem_id,
        run_id=args.run_id,
        generated_at_utc=args.generated_at_utc,
        host=args.host,
        port=args.port,
    )

    if args.launch:
        launch_p136(request)
        return 0

    payload = write_p136_import_pack(request)
    print(payload["status"])
    print(payload["selected_gem"]["gem_id"])
    print(payload["response_import"]["imported_response_file"])
    print(payload["p133_gate"]["command_file"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
