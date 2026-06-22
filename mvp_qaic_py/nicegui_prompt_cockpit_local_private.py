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


def build_nicegui_app(payload: dict[str, Any]) -> Any:
    try:
        from nicegui import ui
    except ImportError as exc:  # pragma: no cover
        raise RuntimeError(
            "NiceGUI is not installed. Install it outside this script if you want launch mode. "
            "Dry-run export remains available and does not require NiceGUI."
        ) from exc

    prompt_text = payload.get("prompt_preview", "")
    sources = payload.get("sources", {})

    ui.page_title("P134 MVP QAIC Prompt Cockpit")

    with ui.header().classes("items-center justify-between"):
        ui.label("P134 — NiceGUI Prompt Cockpit Local Private")
        ui.label("LOCAL_PRIVATE_ONLY · NO_PUBLIC_DEPLOY · NO_BROKER")

    with ui.column().classes("w-full gap-4"):
        ui.markdown(
            "## Cockpit local privé\n"
            f"- URL: `{payload['local_url']}`\n"
            "- Host autorisé: `127.0.0.1` / `localhost`\n"
            "- Sécurité: human review, no order, no sizing, no auto apply"
        )

        ui.markdown("## Sources")
        ui.code(json.dumps(sources, ensure_ascii=False, indent=2), language="json")

        ui.markdown("## Prompt P132-R2 à copier dans GEM")
        prompt_area = ui.textarea(value=prompt_text).props("readonly").classes("w-full")
        prompt_area.props("rows=24")

        ui.markdown(
            "## Réponse GEM\n"
            "Colle ici la réponse GEM puis sauvegarde-la via ton workflow local/P133. "
            "Le cockpit ne fait aucun appel provider et n’applique rien automatiquement."
        )
        ui.textarea(placeholder="Coller ici la réponse GEM...").classes("w-full").props("rows=18")

        ui.markdown("## Sécurité")
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

    payload = write_prompt_cockpit_pack(request)
    print(payload["status"])
    print(payload["local_url"])
    print(payload["sources"]["prompt_exists"])
    print(payload["features"]["no_public_deploy"])
    print(payload["features"]["no_broker_execution"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
