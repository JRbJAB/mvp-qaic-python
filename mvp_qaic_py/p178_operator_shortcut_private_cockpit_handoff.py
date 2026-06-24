from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from mvp_qaic_py.p177_gem_portfolio_prompt_workflow_usable_smoke import (
    build_gem_portfolio_prompt_smoke,
)


SAFETY_FLAGS: dict[str, bool] = {
    "gem_call_executed": False,
    "google_sheets_write": False,
    "live_google_api_call_from_python": False,
    "apps_script_execution": False,
    "clasp_push": False,
    "public_serve": False,
    "broker": False,
    "order": False,
    "sizing": False,
    "auto_apply_gem_response": False,
    "source_prompt_modified": False,
}


def _utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def build_operator_handoff_payload(
    project_root: str | Path,
    *,
    generated_at: str | None = None,
) -> dict[str, Any]:
    root = Path(project_root)
    p177 = build_gem_portfolio_prompt_smoke(root)
    generated = generated_at or _utc_now()

    blockers: list[str] = list(p177.get("blockers", []))
    if not p177.get("smoke_ready"):
        blockers.append("P177_PROMPT_WORKFLOW_NOT_READY")

    launcher_path = root / "00_OPERATOR_SHORTCUTS" / "P178_RUN_PRIVATE_COCKPIT.ps1"
    handoff_path = root / "00_OPERATOR_SHORTCUTS" / "P178_OPERATOR_HANDOFF.md"

    operator_steps = [
        "Open PowerShell.",
        "Run 00_OPERATOR_SHORTCUTS\\P178_RUN_PRIVATE_COCKPIT.ps1.",
        "Open http://127.0.0.1:8088 if the browser does not open automatically.",
        "Use Prompt GEM tab to copy the prompt.",
        "Paste screenshot/image into GEM manually.",
        "Save GEM response locally for review.",
        "Do not apply decisions automatically.",
    ]

    ready = not blockers and p177.get("smoke_ready") is True

    return {
        "STATUS": "OK_P178_OPERATOR_SHORTCUT_PRIVATE_COCKPIT_HANDOFF_READY"
        if ready
        else "BLOCKED_P178_OPERATOR_SHORTCUT_PRIVATE_COCKPIT_HANDOFF",
        "generated_at": generated,
        "project_root": str(root),
        "source_step": "P177_GEM_PORTFOLIO_PROMPT_WORKFLOW_USABLE_SMOKE",
        "shortcut_dir": str(root / "00_OPERATOR_SHORTCUTS"),
        "launcher_path": str(launcher_path),
        "handoff_path": str(handoff_path),
        "private_url": "http://127.0.0.1:8088",
        "host": "127.0.0.1",
        "port": 8088,
        "operator_step_count": len(operator_steps),
        "operator_steps": operator_steps,
        "handoff_ready": ready,
        "blocker_count": len(blockers),
        "blockers": blockers,
        **SAFETY_FLAGS,
        "recommended_next": "P179_PRIVATE_COCKPIT_OPERATOR_USAGE_SMOKE_OR_CLOSE",
    }


def render_launcher_ps1(project_root: str | Path) -> str:
    root = Path(project_root)
    return "\n".join(
        [
            '$ErrorActionPreference = "Stop"',
            "chcp 65001 | Out-Null",
            "[Console]::OutputEncoding = [System.Text.Encoding]::UTF8",
            "$OutputEncoding = [System.Text.Encoding]::UTF8",
            "",
            'Write-Host "============================================================"',
            'Write-Host "MVP QAIC - PRIVATE LOCAL COCKPIT"',
            'Write-Host "URL: http://127.0.0.1:8088"',
            'Write-Host "PRIVATE ONLY / NO PUBLIC SERVE / NO SHEET WRITE / NO BROKER"',
            'Write-Host "============================================================"',
            "",
            f'Set-Location -LiteralPath "{root}"',
            "",
            "python -m mvp_qaic_py.p173_nicegui_private_local_runner --project-root . --host 127.0.0.1 --port 8088 --serve-private",
            "",
        ]
    )


def render_handoff_md(payload: dict[str, Any]) -> str:
    steps = "\n".join(
        f"{index + 1}. {step}" for index, step in enumerate(payload["operator_steps"])
    )
    return "\n".join(
        [
            "# P178 Operator Handoff — MVP QAIC Private Cockpit",
            "",
            f"- STATUS: {payload['STATUS']}",
            f"- Private URL: {payload['private_url']}",
            f"- Launcher: `{payload['launcher_path']}`",
            "",
            "## Usage opérateur",
            "",
            steps,
            "",
            "## Garde-fous",
            "",
            "- Host local uniquement: 127.0.0.1",
            "- Public serve: False",
            "- Google Sheets write: False",
            "- Live Google API from Python: False",
            "- Apps Script execution: False",
            "- CLASP push: False",
            "- GEM call from Python: False",
            "- Auto apply GEM response: False",
            "- Broker/order/sizing: False",
            "",
            "## Next",
            "",
            payload["recommended_next"],
            "",
        ]
    )


def export_operator_handoff(
    project_root: str | Path,
    *,
    export_dir: str | Path | None = None,
) -> dict[str, Any]:
    root = Path(project_root)
    shortcut_dir = root / "00_OPERATOR_SHORTCUTS"
    shortcut_dir.mkdir(parents=True, exist_ok=True)

    payload = build_operator_handoff_payload(root)

    launcher_path = shortcut_dir / "P178_RUN_PRIVATE_COCKPIT.ps1"
    launcher_path.write_text(render_launcher_ps1(root), encoding="utf-8")

    handoff_path = shortcut_dir / "P178_OPERATOR_HANDOFF.md"
    handoff_path.write_text(render_handoff_md(payload), encoding="utf-8")

    if export_dir is None:
        stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        export_path = (
            root / "05_EXPORTS" / f"P178_OPERATOR_SHORTCUT_PRIVATE_COCKPIT_HANDOFF_{stamp}"
        )
    else:
        export_path = Path(export_dir)

    export_path.mkdir(parents=True, exist_ok=True)
    payload = {
        **payload,
        "export_dir": str(export_path),
        "launcher_created": launcher_path.exists(),
        "handoff_created": handoff_path.exists(),
    }

    (export_path / "P178_SUMMARY.json").write_text(
        json.dumps(payload, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )
    (export_path / "P178_OPERATOR_HANDOFF_COPY.md").write_text(
        render_handoff_md(payload),
        encoding="utf-8",
    )

    report = [
        "# P178 Operator Shortcut And Private Cockpit Handoff",
        "",
        f"- STATUS: {payload['STATUS']}",
        f"- handoff_ready: {payload['handoff_ready']}",
        f"- launcher_created: {payload['launcher_created']}",
        f"- handoff_created: {payload['handoff_created']}",
        f"- private_url: {payload['private_url']}",
        f"- blocker_count: {payload['blocker_count']}",
        "",
        "Safety:",
        "- GEM_CALL_EXECUTED=False",
        "- AUTO_APPLY_GEM_RESPONSE=False",
        "- SOURCE_PROMPT_MODIFIED=False",
        "- GOOGLE_SHEETS_WRITE=False",
        "- LIVE_GOOGLE_API_CALL_FROM_PYTHON=False",
        "- APPS_SCRIPT_EXECUTION=False",
        "- CLASP_PUSH=False",
        "- PUBLIC_SERVE=False",
        "- BROKER=False",
        "- ORDER=False",
        "- SIZING=False",
        "",
        "Next:",
        f"- {payload['recommended_next']}",
    ]
    (export_path / "P178_OPERATOR_SHORTCUT_HANDOFF_REPORT.md").write_text(
        "\n".join(report) + "\n",
        encoding="utf-8",
    )

    return payload


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="P178 operator shortcut and private cockpit handoff."
    )
    parser.add_argument("--project-root", default=".")
    parser.add_argument("--export-dir", default=None)
    parser.add_argument("--write-export", action="store_true")
    parser.add_argument("--json", action="store_true")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = _build_parser().parse_args(argv)
    if args.write_export:
        payload = export_operator_handoff(args.project_root, export_dir=args.export_dir)
    else:
        payload = build_operator_handoff_payload(args.project_root)

    if args.json:
        print(json.dumps(payload, indent=2, ensure_ascii=False))
    else:
        print(payload["STATUS"])
        print(f"HANDOFF_READY={payload['handoff_ready']}")
        print(f"OPERATOR_STEP_COUNT={payload['operator_step_count']}")
        print(f"BLOCKER_COUNT={payload['blocker_count']}")

    return 0 if payload["handoff_ready"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
