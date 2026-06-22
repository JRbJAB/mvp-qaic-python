from __future__ import annotations

import argparse
import hashlib
import json
import os
import sys
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


P136_VERSION = "MVP_QAIC_P136C_NICEGUI_STITCH_OPERATOR_UI_REBUILD_20260622"

DEFAULT_RUN_ID = "P136C-NICEGUI-STITCH-OPERATOR-UI-REBUILD"
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
    "P136C_NICEGUI_STITCH_OPERATOR_UI_REBUILD",
    "STITCH_RENDERED_AS_UI_STEPS",
    "REAL_SAVE_BUTTON",
    "SAVE_RESPONSE_TO_LOCAL_FILE_FROM_UI",
    "JSON_DEBUG_COLLAPSED_BY_DEFAULT",
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


DEFAULT_RESPONSE_TEMPLATE = """# P136C — Réponse GEM à importer

Colle ici la réponse GEM complète depuis le cockpit NiceGUI, puis clique sur le bouton de sauvegarde locale.

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


def _write_text_file(path: Path, text: str, encoding: str = "utf-8") -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding=encoding)


def _open_local_folder(path: Path) -> bool:
    try:
        folder = path if path.is_dir() else path.parent
        if sys.platform.startswith("win"):
            os.startfile(str(folder))  # noqa: S606
            return True
    except OSError:
        return False
    return False


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
                "title": "Prompt",
                "goal": "Préparer le prompt, choisir le GEM actif, copier vers GEM et suivre les garde-fous.",
                "components": [
                    "active_gem_select",
                    "prompt_copy_panel",
                    "gemini_open_button",
                    "safety_guardrails_panel",
                ],
            },
            {
                "screen_id": "response_import",
                "title": "Réponse GEM",
                "goal": "Coller et sauvegarder localement une réponse GEM réelle.",
                "components": [
                    "response_file_status",
                    "response_textarea",
                    "save_response_to_local_file_button",
                    "response_hash_status",
                ],
            },
            {
                "screen_id": "p133_gate",
                "title": "P133 Gate",
                "goal": "Préparer la commande locale de validation P133 sans exécution automatique.",
                "components": [
                    "p133_command_preview",
                    "copy_p133_command_button",
                    "open_export_folder_button",
                    "human_review_warning",
                ],
            },
            {
                "screen_id": "prompt_corrections",
                "title": "Corrections",
                "goal": "Lister les corrections prompts candidates avant application future.",
                "components": [
                    "prompt_corrections_table",
                    "priority_badges",
                    "scope_filter",
                    "next_action_panel",
                ],
            },
            {
                "screen_id": "audit",
                "title": "Audit",
                "goal": "Masquer par défaut les JSON et specs techniques, accessibles uniquement si nécessaire.",
                "components": [
                    "collapsed_json_debug",
                    "stitch_spec_collapsed",
                    "safety_markers_collapsed",
                ],
            },
        ],
        "layout_rules": {
            "density": "operator_dense_but_readable",
            "theme": "dark_professional",
            "primary_layout": "left_workflow_center_tabs_right_decision",
            "no_empty_rows": True,
            "badges_for_safety": True,
            "monospace_for_prompt_and_json": True,
            "json_debug_collapsed_by_default": True,
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
        {
            "correction_id": "P136C_UI_001",
            "priority": "HIGH",
            "status": "DONE",
            "scope": "NICEGUI_OPERATOR_UI",
            "issue": "Le rendu P136-R1 était trop technique et dominé par des JSON dumps.",
            "proposed_fix": "Remplacer la page par un cockpit avec workflow gauche, tabs centraux, décision droite et debug caché.",
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
        "step": "P136C_NICEGUI_STITCH_OPERATOR_UI_REBUILD",
        "version": P136_VERSION,
        "status": "P136C_OPERATOR_UI_REBUILD_READY",
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
        "decision_panel": {
            "image_used_expected": "IMAGE_USED",
            "human_review_required": True,
            "no_order_no_sizing": True,
            "blockers_visible": True,
            "next_action": "SAVE_GEM_RESPONSE_THEN_RUN_P133_GATE",
        },
        "safety_markers": list(SAFETY_MARKERS),
        "features": {
            "real_response_file_import": True,
            "active_gem_selection": True,
            "stitch_ui_logic_integrated": True,
            "stitch_rendered_as_ui_steps": True,
            "operator_ui_rebuild": True,
            "real_save_button": True,
            "save_response_to_local_file_from_ui": True,
            "copy_p133_command": True,
            "open_export_folder": True,
            "json_debug_collapsed_by_default": True,
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
        "# P136C — Prompt Corrections Queue",
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
        "# P136C — Stitch Operator UI Spec",
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
    lines.append("## Layout rules")
    lines.append("")
    for key, value in stitch["layout_rules"].items():
        lines.append(f"- `{key}`: `{value}`")
    lines.append("")
    lines.append("## Forbidden behaviors")
    lines.append("")
    for behavior in stitch["forbidden_behaviors"]:
        lines.append(f"- `{behavior}`")
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def _write_runbook(path: Path, payload: dict[str, Any]) -> None:
    text = f"""# P136C — NiceGUI Stitch Operator UI Rebuild

## Objectif

Remplacer le rendu technique P136-R1 par un cockpit opérateur réellement utilisable.

## GEM sélectionné

- gem_id: `{payload["selected_gem"]["gem_id"]}`
- label: `{payload["selected_gem"]["label"]}`
- prompt_profile: `{payload["selected_gem"]["prompt_profile"]}`

## UI

- workflow gauche
- tabs centrales
- panneau décision à droite
- JSON debug caché par défaut
- bouton sauvegarde réponse GEM locale
- bouton copie commande P133
- bouton ouverture dossier export local

## Fichiers

- Réponse importée: `{payload["response_import"]["imported_response_file"]}`
- Commande P133: `{payload["p133_gate"]["command_file"]}`
- Output P133: `{payload["p133_gate"]["output_dir"]}`
- Stitch spec: `P136_STITCH_UI_LOGIC_SPEC.json`
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


def _priority_class(priority: str) -> str:
    if priority == "HIGH":
        return "qaic-badge qaic-warn"
    if priority == "MEDIUM":
        return "qaic-badge qaic-info"
    return "qaic-badge"


def build_nicegui_app(payload: dict[str, Any]) -> Any:
    try:
        from nicegui import app, ui
        from starlette.responses import Response
    except ImportError as exc:  # pragma: no cover
        raise RuntimeError("NiceGUI is required only for --launch mode.") from exc

    response_file = Path(payload["response_import"]["imported_response_file"])
    output_dir = response_file.parent
    p133_command = payload["p133_gate"]["command_preview"]
    selected_gem_id = payload["selected_gem"]["gem_id"]
    active_options = {
        profile["gem_id"]: f"{profile['gem_id']} — {profile['label']}"
        for profile in payload["active_gem_profiles"]
    }

    @app.get("/favicon.ico")
    async def p136_favicon() -> Response:
        return Response(status_code=204)

    @ui.page("/")
    def p136_home() -> None:
        ui.page_title("MVP QAIC — P136C Operator Cockpit")
        ui.add_head_html(
            """
            <style>
              :root {
                --qaic-bg: #070b14;
                --qaic-panel: rgba(17, 24, 39, .92);
                --qaic-panel-soft: rgba(31, 41, 55, .82);
                --qaic-border: #263249;
                --qaic-text: #e5e7eb;
                --qaic-muted: #9ca3af;
                --qaic-blue: #60a5fa;
                --qaic-green: #34d399;
                --qaic-orange: #f59e0b;
                --qaic-red: #f87171;
              }
              body {
                background:
                  radial-gradient(circle at top left, rgba(96,165,250,.12), transparent 30%),
                  linear-gradient(135deg, #050816 0%, #0b1020 45%, #111827 100%);
                color: var(--qaic-text);
              }
              .q-page { background: transparent; }
              .qaic-shell { width: min(1640px, calc(100vw - 28px)); margin: 0 auto; padding: 14px 0 34px; }
              .qaic-hero, .qaic-card, .qaic-side, .qaic-decision {
                border: 1px solid var(--qaic-border);
                background: var(--qaic-panel);
                border-radius: 18px;
                box-shadow: 0 14px 38px rgba(0,0,0,.26);
              }
              .qaic-hero { padding: 18px; }
              .qaic-card, .qaic-side, .qaic-decision { padding: 14px; }
              .qaic-grid {
                display: grid;
                grid-template-columns: 280px minmax(560px, 1fr) 340px;
                gap: 14px;
                align-items: start;
              }
              @media (max-width: 1250px) { .qaic-grid { grid-template-columns: 1fr; } }
              .qaic-title { font-size: 25px; font-weight: 900; letter-spacing: .2px; }
              .qaic-subtitle { color: var(--qaic-muted); font-size: 13px; }
              .qaic-badge {
                display: inline-flex; align-items: center; gap: 6px;
                border: 1px solid var(--qaic-border); border-radius: 999px;
                background: var(--qaic-panel-soft); padding: 5px 10px; font-size: 12px;
              }
              .qaic-good { color: var(--qaic-green); border-color: rgba(52,211,153,.45); }
              .qaic-warn { color: var(--qaic-orange); border-color: rgba(245,158,11,.48); }
              .qaic-danger { color: var(--qaic-red); border-color: rgba(248,113,113,.48); }
              .qaic-info { color: var(--qaic-blue); border-color: rgba(96,165,250,.45); }
              .qaic-step {
                border: 1px solid var(--qaic-border); border-radius: 14px;
                padding: 10px 12px; background: rgba(15,23,42,.82); margin-bottom: 9px;
              }
              .qaic-step strong { display:block; font-size: 13px; }
              .qaic-step span { display:block; color: var(--qaic-muted); font-size: 12px; margin-top: 3px; }
              .qaic-textarea textarea {
                min-height: 460px; font-family: ui-monospace, SFMono-Regular, Consolas, monospace;
                font-size: 12px; line-height: 1.42; background: #050816 !important; color: #e5e7eb !important;
              }
              .qaic-mini textarea {
                min-height: 240px; font-family: ui-monospace, SFMono-Regular, Consolas, monospace;
                font-size: 12px; background: #050816 !important; color: #e5e7eb !important;
              }
              .qaic-code pre { max-height: 360px; overflow: auto; border-radius: 12px; }
              .qaic-small { color: var(--qaic-muted); font-size: 12px; }
              .qaic-action-row { gap: 8px; flex-wrap: wrap; }
            </style>
            """
        )

        with ui.column().classes("qaic-shell gap-4"):
            with ui.row().classes("qaic-hero w-full items-center justify-between"):
                with ui.column().classes("gap-1"):
                    ui.label("MVP QAIC — Operator Cockpit").classes("qaic-title")
                    ui.label(
                        "P136C : GEM actif → réponse réelle → sauvegarde locale → P133 gate → corrections prompts"
                    ).classes("qaic-subtitle")
                with ui.row().classes("qaic-action-row"):
                    ui.label("LOCAL_PRIVATE_ONLY").classes("qaic-badge qaic-good")
                    ui.label(selected_gem_id).classes("qaic-badge qaic-info")
                    ui.label("NO_ORDER / NO_SIZING").classes("qaic-badge qaic-warn")
                    ui.label("DEBUG_JSON_COLLAPSED").classes("qaic-badge")

            with ui.element("div").classes("qaic-grid"):
                with ui.column().classes("qaic-side"):
                    ui.markdown("### Workflow")
                    steps = [
                        ("1. Prompt", "Choisir le GEM actif et préparer le prompt."),
                        ("2. Réponse GEM", "Coller puis sauvegarder la réponse réelle."),
                        ("3. P133 Gate", "Copier/lancer la commande locale."),
                        ("4. Corrections", "Suivre les corrections prompts candidates."),
                        ("5. Audit", "Voir JSON/Spécifications si nécessaire."),
                    ]
                    for title, subtitle in steps:
                        with ui.element("div").classes("qaic-step"):
                            ui.html(f"<strong>{title}</strong><span>{subtitle}</span>")
                    ui.separator()
                    ui.markdown("### GEM actif")
                    ui.select(
                        options=active_options, value=selected_gem_id, label="Gem actif"
                    ).classes("w-full")
                    ui.markdown(
                        "Le changement visuel ne relance pas automatiquement le module. Pour changer réellement, relancer avec `--gem-id`."
                    ).classes("qaic-small")

                with ui.column().classes("gap-4"):
                    with ui.card().classes("qaic-card w-full"):
                        with ui.tabs().classes("w-full") as tabs:
                            prompt_tab = ui.tab("Prompt")
                            response_tab = ui.tab("Réponse GEM")
                            p133_tab = ui.tab("P133 Gate")
                            corrections_tab = ui.tab("Corrections")
                            audit_tab = ui.tab("Audit")

                        with ui.tab_panels(tabs, value=response_tab).classes("w-full"):
                            with ui.tab_panel(prompt_tab):
                                ui.markdown("### Prompt / GEM actif")
                                ui.markdown(payload["selected_gem"]["description"])
                                ui.code(
                                    json.dumps(
                                        {
                                            "selected_gem": payload["selected_gem"],
                                            "active_gem_ids": payload["active_gem_ids"],
                                        },
                                        ensure_ascii=False,
                                        indent=2,
                                    ),
                                    language="json",
                                ).classes("qaic-code")

                            with ui.tab_panel(response_tab):
                                ui.markdown("### Réponse GEM réelle")
                                ui.markdown(
                                    f"Fichier local cible : `{payload['response_import']['imported_response_file']}`"
                                ).classes("qaic-small")
                                initial_response = ""
                                if response_file.exists():
                                    initial_response = response_file.read_text(
                                        encoding="utf-8", errors="replace"
                                    )
                                response_box = (
                                    ui.textarea(
                                        value=initial_response,
                                        placeholder="Colle ici la réponse GEM complète, puis clique sur Sauvegarder localement.",
                                    )
                                    .props("outlined")
                                    .classes("qaic-textarea w-full")
                                )

                                def save_response() -> None:
                                    text = response_box.value or ""
                                    _write_text_file(response_file, text)
                                    ui.notify(
                                        f"Réponse sauvegardée localement ({len(text)} caractères).",
                                        type="positive",
                                    )

                                with ui.row().classes("qaic-action-row"):
                                    ui.button("Sauvegarder localement", on_click=save_response)
                                    ui.button(
                                        "Ouvrir dossier export",
                                        on_click=lambda: ui.notify(
                                            "Dossier ouvert."
                                            if _open_local_folder(output_dir)
                                            else str(output_dir),
                                            type="positive",
                                        ),
                                    )
                                    ui.button(
                                        "Copier chemin fichier",
                                        on_click=lambda: ui.run_javascript(
                                            "navigator.clipboard.writeText("
                                            + json.dumps(str(response_file), ensure_ascii=False)
                                            + ")"
                                        ),
                                    )

                            with ui.tab_panel(p133_tab):
                                ui.markdown("### Commande P133 locale")
                                ui.markdown(
                                    "Copie cette commande après sauvegarde de la réponse GEM."
                                )
                                ui.code(p133_command, language="powershell").classes("qaic-code")
                                with ui.row().classes("qaic-action-row"):
                                    ui.button(
                                        "Copier commande P133",
                                        on_click=lambda: ui.run_javascript(
                                            "navigator.clipboard.writeText("
                                            + json.dumps(p133_command, ensure_ascii=False)
                                            + ")"
                                        ),
                                    )
                                    ui.button(
                                        "Ouvrir dossier export",
                                        on_click=lambda: ui.notify(
                                            "Dossier ouvert."
                                            if _open_local_folder(output_dir)
                                            else str(output_dir),
                                            type="positive",
                                        ),
                                    )

                            with ui.tab_panel(corrections_tab):
                                ui.markdown("### Corrections prompts")
                                for row in payload["prompt_corrections_queue"]:
                                    with ui.card().classes("w-full"):
                                        with ui.row().classes("items-center gap-2"):
                                            ui.label(row["correction_id"]).classes("qaic-badge")
                                            ui.label(row["priority"]).classes(
                                                _priority_class(row["priority"])
                                            )
                                            ui.label(row["status"]).classes("qaic-badge qaic-info")
                                        ui.markdown(f"**Scope** : `{row['scope']}`")
                                        ui.markdown(row["issue"])
                                        ui.markdown(f"**Correction** : {row['proposed_fix']}")

                            with ui.tab_panel(audit_tab):
                                ui.markdown("### Audit / Debug")
                                with ui.expansion("JSON payload complet", value=False):
                                    ui.code(
                                        json.dumps(payload, ensure_ascii=False, indent=2),
                                        language="json",
                                    ).classes("qaic-code")
                                with ui.expansion("Stitch UI logic spec", value=False):
                                    ui.code(
                                        json.dumps(
                                            payload["stitch_ui_logic"], ensure_ascii=False, indent=2
                                        ),
                                        language="json",
                                    ).classes("qaic-code")
                                with ui.expansion("Safety markers", value=False):
                                    ui.code("\n".join(payload["safety_markers"]), language="text")

                with ui.column().classes("qaic-decision"):
                    ui.markdown("### Décision opérateur")
                    decision = payload["decision_panel"]
                    ui.label("HUMAN_REVIEW_REQUIRED").classes("qaic-badge qaic-warn")
                    ui.label(f"image_used attendu : {decision['image_used_expected']}").classes(
                        "qaic-badge qaic-info"
                    )
                    ui.label("NO_ORDER / NO_SIZING").classes("qaic-badge qaic-danger")
                    ui.separator()
                    ui.markdown("#### Next action")
                    ui.markdown(f"`{decision['next_action']}`")
                    ui.separator()
                    ui.markdown("#### Statut fichiers")
                    ui.markdown(
                        f"""
                        - Réponse source détectée : `{payload["response_import"]["source_response_file_exists"]}`
                        - Caractères réponse : `{payload["response_import"]["response_char_count"]}`
                        - Output P133 : `{payload["p133_gate"]["output_dir"]}`
                        """
                    )
                    ui.separator()
                    ui.markdown("#### Sécurité")
                    ui.markdown(
                        """
                        - Aucun broker
                        - Aucun ordre
                        - Aucun sizing
                        - Aucun auto-apply
                        - Aucun accès Revolut X réel depuis MVP
                        """
                    )

    return ui


def launch_p136(request: P136Request) -> None:
    payload = build_p136_payload(request)
    ui = build_nicegui_app(payload)
    ui.run(host=request.host, port=request.port, reload=False, show=False)


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="P136C NiceGUI Stitch operator UI rebuild")
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
