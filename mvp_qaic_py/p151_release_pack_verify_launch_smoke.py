from __future__ import annotations

import argparse
import csv
import json
import sys
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any
from zipfile import ZipFile

VERSION = "MVP_QAIC_P151_RELEASE_PACK_VERIFY_LAUNCH_SMOKE_1.0.0_SAFE"
STATUS_READY = "P151_RELEASE_PACK_VERIFY_LAUNCH_SMOKE_READY"

REQUIRED_ZIP_ENTRIES = [
    "P150B_RELEASE_MANIFEST.json",
    "P150B_SUMMARY.json",
    "P150B_RELEASE_NOTES.md",
    "P150B_LOCAL_LAUNCH_COMMANDS.md",
    "P150B_RELEASE_EVIDENCE_INDEX.csv",
]

REQUIRED_EVIDENCE_PREFIXES = [
    "release_evidence/P140_NICEGUI_COCKPIT_REPLICA_RENDERER/",
    "release_evidence/P141_NICEGUI_COCKPIT_REPLICA_LOCAL_LAUNCH/",
    "release_evidence/P142_UI_FIDELITY_SHELL/",
    "release_evidence/P143B_DATA_PREVIEW_SOURCE_EXPANSION/",
    "release_evidence/P144_PROMPT_COCKPIT_WORKFLOWS/",
    "release_evidence/P145_GEM_RESPONSE_IMPORT_E2E/",
    "release_evidence/P146_CORRECTION_QUEUE_UI/",
    "release_evidence/P147_OPERATOR_POLISH/",
    "release_evidence/P148_SYNC_STRATEGY_READONLY/",
    "release_evidence/P149_MIGRATION_CLOSE_GATE/",
    "release_evidence/P150_PUBLIC_PREP_SELECTOR_OR_STOP/",
]

FORBIDDEN_ZIP_MARKERS = [
    ".git/",
    ".venv/",
    "__pycache__/",
    "desktop.ini",
    ".env",
    "client_secret",
    "credentials.json",
    "token.json",
]

SAFETY_MARKERS = {
    "verify_only": True,
    "local_private_only": True,
    "live_google_sheets_read": False,
    "google_sheets_write": False,
    "apps_script_execution": False,
    "clasp_push": False,
    "broker": False,
    "order": False,
    "sizing": False,
    "auto_apply_gem_response": False,
    "public_deploy": False,
    "server_launch_executed": False,
    "future_public_deploy_requires_explicit_go": True,
    "future_sheet_write_requires_explicit_go": True,
}


@dataclass(frozen=True)
class VerifyRequest:
    p150b_manifest_path: Path
    release_zip_path: Path
    exports_root: Path
    output_dir: Path
    run_id: str
    generated_at_utc: str


def utc_now_iso() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def latest_export_for_prefix(exports_root: Path, prefix: str) -> Path | None:
    matches = [
        item for item in exports_root.iterdir() if item.is_dir() and item.name.startswith(prefix)
    ]
    if not matches:
        return None
    return sorted(matches, key=lambda path: path.stat().st_mtime, reverse=True)[0]


def read_zip_entries(zip_path: Path) -> list[str]:
    if not zip_path.exists():
        raise FileNotFoundError(f"release_zip not found: {zip_path}")
    with ZipFile(zip_path, "r") as archive:
        return sorted(archive.namelist())


def validate_manifest(manifest: dict[str, Any]) -> list[str]:
    blockers: list[str] = []
    if manifest.get("status") != "P150B_LOCAL_PRIVATE_RELEASE_PACK_READY":
        blockers.append("P150B_MANIFEST_STATUS_NOT_READY")
    if int(manifest.get("blocker_count", 0) or 0) != 0:
        blockers.append("P150B_BLOCKERS_NOT_ZERO")
    safety = manifest.get("safety", {})
    if safety.get("google_sheets_write") is not False:
        blockers.append("GOOGLE_SHEETS_WRITE_NOT_FALSE")
    if safety.get("public_deploy") is not False:
        blockers.append("PUBLIC_DEPLOY_NOT_FALSE")
    if safety.get("broker") is not False:
        blockers.append("BROKER_NOT_FALSE")
    return blockers


def validate_zip(entries: list[str]) -> tuple[list[str], list[str]]:
    blockers: list[str] = []
    warnings: list[str] = []
    entry_set = set(entries)

    for required in REQUIRED_ZIP_ENTRIES:
        if required not in entry_set:
            blockers.append(f"ZIP_REQUIRED_ENTRY_MISSING:{required}")

    for prefix in REQUIRED_EVIDENCE_PREFIXES:
        if not any(entry.startswith(prefix) for entry in entries):
            blockers.append(f"ZIP_REQUIRED_EVIDENCE_PREFIX_MISSING:{prefix}")

    lowered = [entry.lower() for entry in entries]
    for marker in FORBIDDEN_ZIP_MARKERS:
        if any(marker in entry for entry in lowered):
            blockers.append(f"ZIP_FORBIDDEN_MARKER:{marker}")

    if len(entries) < 20:
        warnings.append("ZIP_ENTRY_COUNT_LOW_REVIEW")

    return blockers, warnings


def find_launch_candidates(exports_root: Path) -> list[dict[str, str]]:
    candidates: list[dict[str, str]] = []
    mapping = [
        ("P147_OPERATOR_POLISH_", "P147_NICEGUI_OPERATOR_POLISH_APP.py", "operator_polish"),
        ("P146_CORRECTION_QUEUE_UI_", "P146_NICEGUI_CORRECTION_QUEUE_APP.py", "correction_queue"),
        ("P145_GEM_RESPONSE_IMPORT_E2E_", "P145_NICEGUI_GEM_RESPONSE_REVIEW_APP.py", "gem_review"),
        (
            "P144_PROMPT_COCKPIT_WORKFLOWS_",
            "P144_NICEGUI_PROMPT_WORKFLOW_APP.py",
            "prompt_workflow",
        ),
        (
            "P143B_DATA_PREVIEW_SOURCE_EXPANSION_",
            "P143B_NICEGUI_DATA_PREVIEW_APP.py",
            "data_preview",
        ),
    ]
    for prefix, filename, role in mapping:
        folder = latest_export_for_prefix(exports_root, prefix)
        path = folder / filename if folder else None
        candidates.append(
            {
                "role": role,
                "prefix": prefix,
                "found": str(bool(path and path.exists())).lower(),
                "path": str(path) if path and path.exists() else "",
                "launch_command": f"python {path}" if path and path.exists() else "",
            }
        )
    return candidates


def build_launch_script(candidates: list[dict[str, str]]) -> str:
    primary = next(
        (
            item
            for item in candidates
            if item["role"] == "operator_polish" and item["found"] == "true"
        ),
        None,
    )
    primary_path = primary["path"] if primary else ""
    return "\n".join(
        [
            '$ErrorActionPreference = "Stop"',
            "chcp 65001 | Out-Null",
            "[Console]::OutputEncoding = [System.Text.Encoding]::UTF8",
            "$OutputEncoding = [System.Text.Encoding]::UTF8",
            '$env:PYTHONUTF8 = "1"',
            '$env:PYTHONIOENCODING = "utf-8"',
            "",
            "# MVP QAIC P151 — local launch smoke command",
            "# Vérification seulement : aucun Sheet write, aucun public deploy, aucun broker/order/sizing.",
            "",
            f'$app = "{primary_path}"',
            'if (-not (Test-Path -LiteralPath $app)) { throw "App NiceGUI introuvable: $app" }',
            'Write-Host "LOCAL_PRIVATE_APP=$app"',
            'Write-Host "Launch manually with: python `"$app`""',
            "# Décommenter volontairement la ligne suivante seulement pour lancer l'UI locale.",
            '# & python "$app"',
            "",
        ]
    )


def build_report(
    manifest: dict[str, Any], zip_entries: list[str], exports_root: Path, release_zip_path: Path
) -> dict[str, Any]:
    manifest_blockers = validate_manifest(manifest)
    zip_blockers, zip_warnings = validate_zip(zip_entries)
    candidates = find_launch_candidates(exports_root)
    launch_blockers: list[str] = []
    if not any(
        item["role"] == "operator_polish" and item["found"] == "true" for item in candidates
    ):
        launch_blockers.append("OPERATOR_POLISH_APP_NOT_FOUND")

    blockers = manifest_blockers + zip_blockers + launch_blockers
    warnings = zip_warnings

    return {
        "status": STATUS_READY if not blockers else "P151_RELEASE_PACK_VERIFY_LAUNCH_SMOKE_BLOCKED",
        "version": VERSION,
        "release_name": manifest.get("release_name", ""),
        "source_p150b_status": manifest.get("status"),
        "release_zip_path": str(release_zip_path),
        "zip_entry_count": len(zip_entries),
        "required_zip_entry_count": len(REQUIRED_ZIP_ENTRIES),
        "required_evidence_prefix_count": len(REQUIRED_EVIDENCE_PREFIXES),
        "launch_candidate_count": len(candidates),
        "launch_smoke_ready": not launch_blockers,
        "blocker_count": len(blockers),
        "warning_count": len(warnings),
        "blockers": blockers,
        "warnings": warnings,
        "launch_candidates": candidates,
        "zip_entries": zip_entries,
        "safety": dict(SAFETY_MARKERS),
        "next": "P152_REAL_GEM_RESPONSE_IMPORT_OR_STOP",
    }


def write_outputs(report: dict[str, Any], output_dir: Path) -> dict[str, str]:
    output_dir.mkdir(parents=True, exist_ok=True)

    report_path = output_dir / "P151_RELEASE_PACK_VERIFY_REPORT.json"
    zip_index_path = output_dir / "P151_RELEASE_ZIP_INDEX.csv"
    launch_ps1 = output_dir / "P151_LOCAL_LAUNCH_SMOKE.ps1"
    md_path = output_dir / "P151_RELEASE_PACK_VERIFY_LAUNCH_SMOKE.md"
    summary_path = output_dir / "P151_SUMMARY.json"

    report_path.write_text(
        json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True), encoding="utf-8"
    )
    launch_ps1.write_text(build_launch_script(report["launch_candidates"]), encoding="utf-8-sig")

    with zip_index_path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=["entry"])
        writer.writeheader()
        for entry in report["zip_entries"]:
            writer.writerow({"entry": entry})

    md_path.write_text(
        "\n".join(
            [
                "# P151 — Release Pack Verify + Launch Smoke",
                "",
                f"- Status: `{report['status']}`",
                f"- Release: `{report['release_name']}`",
                f"- ZIP entries: `{report['zip_entry_count']}`",
                f"- Launch smoke ready: `{report['launch_smoke_ready']}`",
                f"- Blockers: `{report['blocker_count']}`",
                "",
                "## Safety",
                "",
                "- Verify only",
                "- No server launch executed",
                "- No Sheet write",
                "- No public deploy",
                "- No Apps Script / CLASP",
                "- No broker/order/sizing",
                "",
                f"Next: `{report['next']}`",
                "",
            ]
        ),
        encoding="utf-8",
    )

    summary = {
        "status": report["status"],
        "release_name": report["release_name"],
        "zip_entry_count": report["zip_entry_count"],
        "launch_smoke_ready": report["launch_smoke_ready"],
        "blocker_count": report["blocker_count"],
        "warning_count": report["warning_count"],
        "google_sheets_write": False,
        "live_google_sheets_read": False,
        "public_deploy": False,
        "server_launch_executed": False,
        "broker": False,
        "order": False,
        "sizing": False,
        "auto_apply_gem_response": False,
        "output_dir": str(output_dir),
        "next": report["next"],
    }
    summary_path.write_text(
        json.dumps(summary, ensure_ascii=False, indent=2, sort_keys=True), encoding="utf-8"
    )
    return {
        "verify_report_json": str(report_path),
        "zip_index_csv": str(zip_index_path),
        "local_launch_smoke_ps1": str(launch_ps1),
        "markdown": str(md_path),
        "summary_json": str(summary_path),
    }


def run_verify(request: VerifyRequest) -> dict[str, Any]:
    manifest = load_json(request.p150b_manifest_path)
    entries = read_zip_entries(request.release_zip_path)
    report = build_report(manifest, entries, request.exports_root, request.release_zip_path)
    report["run_id"] = request.run_id
    report["generated_at_utc"] = request.generated_at_utc
    report["source_p150b_manifest_path"] = str(request.p150b_manifest_path)
    report["exports_root"] = str(request.exports_root)
    outputs = write_outputs(report, request.output_dir)
    report["output_files"] = outputs
    (request.output_dir / "P151_RELEASE_PACK_VERIFY_REPORT.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True),
        encoding="utf-8",
    )
    return report


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="P151 release pack verify and launch smoke.")
    parser.add_argument("--p150b-manifest", required=True)
    parser.add_argument("--release-zip", required=True)
    parser.add_argument("--exports-root", required=True)
    parser.add_argument("--output-dir", required=True)
    parser.add_argument("--run-id", default="P151-RELEASE-PACK-VERIFY-LAUNCH-SMOKE")
    parser.add_argument("--generated-at-utc", default=utc_now_iso())
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    report = run_verify(
        VerifyRequest(
            p150b_manifest_path=Path(args.p150b_manifest),
            release_zip_path=Path(args.release_zip),
            exports_root=Path(args.exports_root),
            output_dir=Path(args.output_dir),
            run_id=args.run_id,
            generated_at_utc=args.generated_at_utc,
        )
    )
    print(report["status"])
    print(f"release_name={report['release_name']}")
    print(f"zip_entry_count={report['zip_entry_count']}")
    print(f"launch_smoke_ready={str(report['launch_smoke_ready']).lower()}")
    print(f"blocker_count={report['blocker_count']}")
    print(f"warning_count={report['warning_count']}")
    print("google_sheets_write=false")
    print("public_deploy=false")
    print("server_launch_executed=false")
    print(f"output_dir={args.output_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
