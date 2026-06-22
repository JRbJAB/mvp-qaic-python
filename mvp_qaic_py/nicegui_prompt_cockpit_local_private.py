from __future__ import annotations

import argparse
import json
from dataclasses import asdict, dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

VERSION = "MVP_QAIC_P134_NICEGUI_PROMPT_COCKPIT_LOCAL_PRIVATE_0_1_0_SAFE"

DEFAULT_HOST = "127.0.0.1"
DEFAULT_PORT = 8088

SAFETY_MARKERS = (
    "LOCAL_PRIVATE_ONLY",
    "HOST_127_0_0_1_ONLY",
    "NO_PUBLIC_DEPLOY",
    "NO_TUNNEL",
    "NO_REMOTE_ACCESS",
    "NO_SHEET_WRITE",
    "NO_GOOGLE_API_CALL",
    "NO_CLASP",
    "NO_APPS_SCRIPT_EXECUTION",
    "NO_BIGQUERY_WRITE",
    "NO_BROKER",
    "NO_ORDER",
    "NO_CANCEL",
    "NO_REPLACE_ORDER",
    "NO_SIZING",
    "NO_AUTO_SIZING",
    "NO_AUTO_APPLY_GEM_RESPONSE",
    "NO_REVOLUTX_REAL_ACCESS_FROM_MVP",
    "HUMAN_REVIEW_REQUIRED",
    "P132_R2_PROMPT_SOURCE",
    "P133_RESPONSE_CAPTURE_GATE_COMPATIBLE",
    "EXPLICIT_NICEGUI_ROOT_PAGE",
    "FAVICON_204_ROUTE",
    "NO_BROWSER_CLIPBOARD_REQUIRED",
    "P135_R2_P134_COMPAT_EXPORTS",
    "P133_COMMAND_PREVIEW",
    "GEM_RESPONSE_LOCAL_SAVE",
    "PROMPT_COPY_BUTTON",
    "P135_OPERATOR_POLISH",
)


@dataclass(frozen=True)
class PromptCockpitRequest:
    output_dir: Path
    exports_dir: Path = Path("05_EXPORTS")
    host: str = DEFAULT_HOST
    port: int = DEFAULT_PORT
    run_id: str = "P134-NICEGUI-PROMPT-COCKPIT-LOCAL-PRIVATE"
    generated_at_utc: str | None = None
    latest_prompt_path: Path | None = None
    latest_p133_gate_path: Path | None = None


def _utc_now_iso() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def _ensure_dir(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)


def _safe_text(path: Path | None, fallback: str = "") -> str:
    if not path or not path.exists():
        return fallback
    return path.read_text(encoding="utf-8")


def _find_latest_file(exports_dir: Path, pattern: str) -> Path | None:
    if not exports_dir.exists():
        return None
    candidates = [p for p in exports_dir.rglob(pattern) if p.is_file()]
    if not candidates:
        return None
    return max(candidates, key=lambda p: p.stat().st_mtime)


def _validate_local_private_host(host: str) -> None:
    allowed = {"127.0.0.1", "localhost"}
    if host not in allowed:
        raise ValueError(
            "P134 NiceGUI cockpit is local-private only. "
            "Allowed host values: 127.0.0.1 or localhost."
        )


def _validate_port(port: int) -> None:
    if port < 1024 or port > 65535:
        raise ValueError("P134 port must be in [1024, 65535].")


def discover_prompt_cockpit_sources(request: PromptCockpitRequest) -> dict[str, Any]:
    prompt_path = request.latest_prompt_path or _find_latest_file(
        request.exports_dir, "P132_GEM_MULTIMODAL_PORTFOLIO_PROMPT.md"
    )
    p133_gate_path = request.latest_p133_gate_path or _find_latest_file(
        request.exports_dir, "P133_GEM_RESPONSE_CAPTURE_GATE.json"
    )
    p133_human_review_path = _find_latest_file(
        request.exports_dir, "P133_GEM_RESPONSE_HUMAN_REVIEW.md"
    )
    p133_pretty_json_path = _find_latest_file(request.exports_dir, "P133_GEM_RESPONSE_PRETTY.json")

    return {
        "latest_prompt_path": str(prompt_path) if prompt_path else None,
        "latest_p133_gate_path": str(p133_gate_path) if p133_gate_path else None,
        "latest_p133_human_review_path": str(p133_human_review_path)
        if p133_human_review_path
        else None,
        "latest_p133_pretty_json_path": str(p133_pretty_json_path)
        if p133_pretty_json_path
        else None,
        "prompt_exists": bool(prompt_path and prompt_path.exists()),
        "p133_gate_exists": bool(p133_gate_path and p133_gate_path.exists()),
    }


def build_prompt_cockpit_payload(request: PromptCockpitRequest) -> dict[str, Any]:
    _validate_local_private_host(request.host)
    _validate_port(request.port)

    generated_at = request.generated_at_utc or _utc_now_iso()
    sources = discover_prompt_cockpit_sources(request)

    prompt_path = Path(sources["latest_prompt_path"]) if sources["latest_prompt_path"] else None
    prompt_text = _safe_text(prompt_path, fallback="# P132-R2 prompt not found yet\n")

    payload = {
        "status": "NICEGUI_PROMPT_COCKPIT_LOCAL_PRIVATE_READY",
        "version": VERSION,
        "run_id": request.run_id,
        "generated_at_utc": generated_at,
        "host": request.host,
        "port": request.port,
        "local_url": f"http://{request.host}:{request.port}",
        "safety_markers": list(SAFETY_MARKERS),
        "request": {
            **asdict(request),
            "output_dir": str(request.output_dir),
            "exports_dir": str(request.exports_dir),
            "latest_prompt_path": str(request.latest_prompt_path)
            if request.latest_prompt_path
            else None,
            "latest_p133_gate_path": str(request.latest_p133_gate_path)
            if request.latest_p133_gate_path
            else None,
        },
        "sources": sources,
        "prompt_preview": prompt_text[:5000],
        "features": {
            "display_latest_p132_r2_prompt": True,
            "copy_prompt_to_clipboard_from_browser": True,
            "paste_gem_response_to_local_textarea": True,
            "save_gem_response_to_local_file": True,
            "run_p133_gate_instruction": True,
            "no_live_provider_call": True,
            "no_public_deploy": True,
            "no_sheet_write": True,
            "no_broker_execution": True,
        },
        "operator_workflow": [
            "Open cockpit locally on 127.0.0.1.",
            "Copy latest P132-R2 prompt from cockpit.",
            "Attach Revolut X screenshot manually in GEM.",
            "Paste GEM response back into local cockpit or save it as a local file.",
            "Run P133 response capture gate locally.",
            "Open P133 human review markdown and pretty JSON.",
        ],
    }
    return payload


def _markdown_runbook(payload: dict[str, Any]) -> str:
    sources = payload["sources"]
    lines = [
        "# P134 — NiceGUI Prompt Cockpit Local Private",
        "",
        "## Statut",
        "",
        f"- Status : `{payload['status']}`",
        f"- Version : `{payload['version']}`",
        f"- URL locale : `{payload['local_url']}`",
        f"- Host : `{payload['host']}`",
        f"- Port : `{payload['port']}`",
        "",
        "## Sources détectées",
        "",
        f"- Prompt P132-R2 : `{sources.get('latest_prompt_path')}`",
        f"- Gate P133 : `{sources.get('latest_p133_gate_path')}`",
        f"- Rapport P133 : `{sources.get('latest_p133_human_review_path')}`",
        f"- Pretty JSON P133 : `{sources.get('latest_p133_pretty_json_path')}`",
        "",
        "## Workflow opérateur",
        "",
    ]
    lines.extend(f"{idx}. {step}" for idx, step in enumerate(payload["operator_workflow"], 1))
    lines.extend(
        [
            "",
            "## Sécurité",
            "",
            "- Local privé uniquement : `127.0.0.1` ou `localhost`.",
            "- Aucun public deploy.",
            "- Aucun tunnel.",
            "- Aucun broker, ordre, sizing, auto-apply.",
            "- Aucun write Sheets/BigQuery/Apps Script.",
            "",
            "## Commande de lancement cockpit",
            "",
            "```powershell",
            "python -m mvp_qaic_py.nicegui_prompt_cockpit_local_private --launch --exports-dir 05_EXPORTS",
            "```",
            "",
            "Si NiceGUI n’est pas installé, le module reste utilisable en mode export/runbook :",
            "",
            "```powershell",
            "python -m mvp_qaic_py.nicegui_prompt_cockpit_local_private --output-dir 05_EXPORTS\\P134_TEST --dry-run-export",
            "```",
        ]
    )
    return "\n".join(lines) + "\n"


def _html_static_preview(payload: dict[str, Any]) -> str:
    prompt = (
        payload.get("prompt_preview", "")
        .replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
    )
    return f"""<!doctype html>
<html lang="fr">
<head>
  <meta charset="utf-8">
  <title>P134 NiceGUI Prompt Cockpit Local Private</title>
</head>
<body>
  <h1>P134 — NiceGUI Prompt Cockpit Local Private</h1>
  <p><strong>Status:</strong> {payload["status"]}</p>
  <p><strong>Local URL:</strong> {payload["local_url"]}</p>
  <p><strong>Safety:</strong> LOCAL_PRIVATE_ONLY / NO_PUBLIC_DEPLOY / NO_BROKER / NO_ORDER / NO_SIZING</p>
  <h2>Prompt preview</h2>
  <pre>{prompt}</pre>
</body>
</html>
"""


def write_prompt_cockpit_pack(request: PromptCockpitRequest) -> dict[str, Any]:
    payload = build_prompt_cockpit_payload(request)
    _ensure_dir(request.output_dir)

    (request.output_dir / "P134_NICEGUI_PROMPT_COCKPIT_CONTRACT.json").write_text(
        json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=False) + "\n",
        encoding="utf-8",
    )
    (request.output_dir / "P134_NICEGUI_PROMPT_COCKPIT_RUNBOOK.md").write_text(
        _markdown_runbook(payload), encoding="utf-8"
    )
    (request.output_dir / "P134_NICEGUI_PROMPT_COCKPIT_STATIC_PREVIEW.html").write_text(
        _html_static_preview(payload), encoding="utf-8"
    )
    (request.output_dir / "P134_LATEST_P132_PROMPT_COPY.md").write_text(
        payload.get("prompt_preview", ""), encoding="utf-8"
    )

    return payload


def build_p133_capture_command(
    response_file: Path,
    output_dir: Path,
    run_id: str,
    generated_at_utc: str | None = None,
) -> str:
    """Return a copy-paste PowerShell command for the local P133 gate."""

    generated_at = generated_at_utc or _utc_now_iso()
    response_file_str = str(response_file)
    output_dir_str = str(output_dir)
    return (
        '$ErrorActionPreference = "Stop"\n'
        "chcp 65001 | Out-Null\n"
        "[Console]::OutputEncoding = [System.Text.Encoding]::UTF8\n"
        "$OutputEncoding = [System.Text.Encoding]::UTF8\n\n"
        f'$responseText = "{response_file_str}"\n'
        f'$outputDir = "{output_dir_str}"\n'
        "New-Item -ItemType Directory -Path $outputDir -Force | Out-Null\n\n"
        "python -m mvp_qaic_py.gem_multimodal_response_capture_gate `\n"
        "  --response-text $responseText `\n"
        "  --output-dir $outputDir `\n"
        f'  --run-id "{run_id}" `\n'
        f'  --generated-at-utc "{generated_at}"\n\n'
        'Write-Host "P133_OUTPUT_DIR=$outputDir"\n'
        "Write-Host \"OPEN_FIRST=$(Join-Path $outputDir 'P133_GEM_RESPONSE_HUMAN_REVIEW.md')\"\n"
        "Write-Host \"OPEN_JSON=$(Join-Path $outputDir 'P133_GEM_RESPONSE_PRETTY.json')\"\n"
    )


def build_operator_polish_payload(request: PromptCockpitRequest) -> dict[str, Any]:
    payload = build_prompt_cockpit_payload(request)
    response_file = request.output_dir / "P135_GEM_RESPONSE_INPUT.md"
    p133_output_dir = request.output_dir / "P133_FROM_P135_OPERATOR_POLISH"
    p133_run_id = f"{request.run_id}-P133-GATE"
    payload["p135_operator_polish"] = {
        "status": "OPERATOR_POLISH_READY",
        "response_file": str(response_file),
        "p133_output_dir": str(p133_output_dir),
        "p133_run_id": p133_run_id,
        "p133_command_preview": build_p133_capture_command(
            response_file=response_file,
            output_dir=p133_output_dir,
            run_id=p133_run_id,
            generated_at_utc=request.generated_at_utc,
        ),
        "ux_features": {
            "prompt_copy_button": True,
            "gem_response_textarea": True,
            "save_response_local_file": True,
            "p133_command_preview": True,
            "no_clipboard_roundtrip_required": True,
            "manual_human_review_flow": True,
        },
    }
    return payload


def write_operator_polish_pack(request: PromptCockpitRequest) -> dict[str, Any]:
    """Write P134-compatible files and P135 operator polish files together.

    P135-R2 fix: P135 is additive. The historical P134 dry-run contract files
    remain part of the CLI output so P134 tests and operator habits keep working.
    """

    write_prompt_cockpit_pack(request)
    payload = build_operator_polish_payload(request)
    _ensure_dir(request.output_dir)

    (request.output_dir / "P135_OPERATOR_POLISH_CONTRACT.json").write_text(
        json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=False) + "\n",
        encoding="utf-8",
    )
    (request.output_dir / "P135_P133_CAPTURE_COMMAND.ps1").write_text(
        payload["p135_operator_polish"]["p133_command_preview"],
        encoding="utf-8-sig",
    )
    (request.output_dir / "P135_GEM_RESPONSE_INPUT.md").write_text(
        "# Colle ici la réponse GEM complète puis sauvegarde ce fichier.\n",
        encoding="utf-8",
    )
    (request.output_dir / "P135_OPERATOR_POLISH_RUNBOOK.md").write_text(
        _operator_polish_runbook(payload),
        encoding="utf-8",
    )
    return payload


def _operator_polish_runbook(payload: dict[str, Any]) -> str:
    p135 = payload["p135_operator_polish"]
    return (
        "# P135 — NiceGUI Prompt Cockpit Operator Polish\n\n"
        "## Objectif\n\n"
        "Rendre le cockpit utilisable sans jongler avec le presse-papier : prompt copiable, "
        "réponse GEM sauvegardable localement, commande P133 prête.\n\n"
        "## Fichiers\n\n"
        f"- Réponse GEM locale : `{p135['response_file']}`\n"
        f"- Output P133 : `{p135['p133_output_dir']}`\n"
        "- Commande P133 : `P135_P133_CAPTURE_COMMAND.ps1`\n\n"
        "## Sécurité\n\n"
        "- Local privé uniquement.\n"
        "- Aucun ordre, sizing, broker, auto-apply.\n"
        "- Aucun write Sheet/BigQuery/Apps Script.\n\n"
        "## Commande P133\n\n"
        "```powershell\n"
        f"{p135['p133_command_preview']}"
        "```\n"
    )


def build_nicegui_app(payload: dict[str, Any]) -> Any:
    """Build NiceGUI app lazily with P135 operator polish."""

    try:
        from nicegui import app, ui
        from starlette.responses import Response
    except ImportError as exc:  # pragma: no cover
        raise RuntimeError(
            "NiceGUI is not installed. Install it outside this script if you want launch mode. "
            "Dry-run export remains available and does not require NiceGUI."
        ) from exc

    prompt_text = payload.get("prompt_preview", "")
    sources = payload.get("sources", {})

    @app.get("/favicon.ico")
    async def p134_favicon() -> Response:
        return Response(status_code=204)

    @ui.page("/")
    def p134_home() -> None:
        ui.page_title("P134/P135 MVP QAIC Prompt Cockpit")

        with ui.header().classes("items-center justify-between"):
            ui.label("P135 — MVP QAIC Prompt Cockpit")
            ui.label("LOCAL_PRIVATE_ONLY · NO_PUBLIC_DEPLOY · NO_BROKER")

        with ui.column().classes("w-full gap-4"):
            ui.markdown(
                "## Cockpit opérateur local privé\n"
                f"- URL: `{payload['local_url']}`\n"
                "- Flux: P132-R2 prompt → GEM avec image → P133 gate local\n"
                "- Sécurité: human review, no order, no sizing, no auto apply"
            )

            with ui.card().classes("w-full"):
                ui.markdown("### 1) Sources détectées")
                ui.code(json.dumps(sources, ensure_ascii=False, indent=2), language="json")

            with ui.card().classes("w-full"):
                ui.markdown("### 2) Prompt P132-R2")
                prompt_area = ui.textarea(value=prompt_text).props("readonly").classes("w-full")
                prompt_area.props("rows=24")
                ui.button(
                    "Copier le prompt",
                    on_click=lambda: ui.run_javascript(
                        "navigator.clipboard.writeText("
                        + json.dumps(prompt_text, ensure_ascii=False)
                        + ")"
                    ),
                )

            with ui.card().classes("w-full"):
                ui.markdown("### 3) Réponse GEM")
                ui.markdown(
                    "Colle ici la réponse GEM. Pour P135, la sauvegarde fiable reste locale fichier/runbook ; "
                    "le cockpit évite les appels externes et n’applique rien automatiquement."
                )
                ui.textarea(placeholder="Coller ici la réponse GEM...").classes("w-full").props(
                    "rows=18"
                )

            with ui.card().classes("w-full"):
                ui.markdown("### 4) Commande P133 locale")
                p135 = payload.get("p135_operator_polish", {})
                command = p135.get(
                    "p133_command_preview",
                    "Génère le pack P135 dry-run pour obtenir la commande P133.",
                )
                ui.code(command, language="powershell")

            with ui.card().classes("w-full"):
                ui.markdown("### Sécurité")
                ui.code("\n".join(SAFETY_MARKERS))

    return ui


def launch_cockpit(request: PromptCockpitRequest) -> None:  # pragma: no cover
    payload = build_prompt_cockpit_payload(request)
    ui = build_nicegui_app(payload)
    ui.run(host=request.host, port=request.port, reload=False, show=False)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="P134 NiceGUI Prompt Cockpit Local Private")
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("05_EXPORTS/P134_NICEGUI_PROMPT_COCKPIT_LOCAL_PRIVATE"),
    )
    parser.add_argument("--exports-dir", type=Path, default=Path("05_EXPORTS"))
    parser.add_argument("--host", default=DEFAULT_HOST)
    parser.add_argument("--port", type=int, default=DEFAULT_PORT)
    parser.add_argument("--run-id", default="P134-NICEGUI-PROMPT-COCKPIT-LOCAL-PRIVATE")
    parser.add_argument("--generated-at-utc")
    parser.add_argument("--dry-run-export", action="store_true")
    parser.add_argument("--launch", action="store_true")
    args = parser.parse_args(argv)

    request = PromptCockpitRequest(
        output_dir=args.output_dir,
        exports_dir=args.exports_dir,
        host=args.host,
        port=args.port,
        run_id=args.run_id,
        generated_at_utc=args.generated_at_utc,
    )

    if args.launch:
        launch_cockpit(request)
        return 0

    payload = write_operator_polish_pack(request)
    print(payload["status"])
    print(payload["local_url"])
    print(payload["sources"]["prompt_exists"])
    print(payload["features"]["no_public_deploy"])
    print(payload["features"]["no_broker_execution"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
