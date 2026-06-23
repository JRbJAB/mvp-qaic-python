from __future__ import annotations

import argparse
import csv
import json
import shutil
import sys
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any
from zipfile import ZIP_DEFLATED, ZipFile

VERSION = "MVP_QAIC_P150B_LOCAL_PRIVATE_RELEASE_PACK_1.0.0_SAFE"
STATUS_READY = "P150B_LOCAL_PRIVATE_RELEASE_PACK_READY"

RELEASE_PREFIXES = [
    "P140_NICEGUI_COCKPIT_REPLICA_RENDERER_",
    "P141_NICEGUI_COCKPIT_REPLICA_LOCAL_LAUNCH_",
    "P142_UI_FIDELITY_SHELL_",
    "P143B_DATA_PREVIEW_SOURCE_EXPANSION_",
    "P144_PROMPT_COCKPIT_WORKFLOWS_",
    "P145_GEM_RESPONSE_IMPORT_E2E_",
    "P146_CORRECTION_QUEUE_UI_",
    "P147_OPERATOR_POLISH_",
    "P148_SYNC_STRATEGY_READONLY_",
    "P149_MIGRATION_CLOSE_GATE_",
    "P150_PUBLIC_PREP_SELECTOR_OR_STOP_",
]

IMPORTANT_FILENAMES = {
    "P140_SUMMARY.json",
    "P141_SUMMARY.json",
    "P142_SUMMARY.json",
    "P143B_SUMMARY.json",
    "P144_SUMMARY.json",
    "P145_SUMMARY.json",
    "P146_SUMMARY.json",
    "P147_SUMMARY.json",
    "P148_SUMMARY.json",
    "P149_SUMMARY.json",
    "P150_SUMMARY.json",
    "P149_POST_MIGRATION_RUNBOOK.md",
    "P150_OPERATOR_HANDOFF.md",
    "P150_NEXT_OPTIONS.csv",
    "P148_SOURCE_REGISTRY.csv",
    "P146_CORRECTION_ACTIONS.csv",
    "P144_OPERATOR_ACTIONS.csv",
}

SAFETY_MARKERS = {
    "release_pack_only": True,
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
    "future_sheet_write_requires_explicit_go": True,
    "future_public_deploy_requires_explicit_go": True,
}


@dataclass(frozen=True)
class ReleasePackRequest:
    p150_selector_path: Path
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


def safe_release_name(path: Path) -> str:
    return path.name.replace(" ", "_").replace("/", "_").replace("\\", "_")


def collect_release_evidence(exports_root: Path) -> list[dict[str, Any]]:
    evidence: list[dict[str, Any]] = []
    for prefix in RELEASE_PREFIXES:
        folder = latest_export_for_prefix(exports_root, prefix)
        found = folder is not None
        selected_files: list[str] = []
        selected_paths: list[Path] = []
        if folder:
            for file in sorted(folder.iterdir()):
                if not file.is_file():
                    continue
                if file.name.lower() == "desktop.ini":
                    continue
                if file.name in IMPORTANT_FILENAMES or file.suffix.lower() in {
                    ".md",
                    ".json",
                    ".csv",
                }:
                    selected_files.append(file.name)
                    selected_paths.append(file)
        evidence.append(
            {
                "prefix": prefix,
                "found": found,
                "export_dir": str(folder) if folder else "",
                "selected_file_count": len(selected_files),
                "selected_files": selected_files,
                "selected_paths": [str(path) for path in selected_paths],
                "gate": "OK" if found and selected_files else "MISSING",
            }
        )
    return evidence


def validate_selector(selector: dict[str, Any]) -> list[str]:
    blockers: list[str] = []
    if selector.get("status") != "P150_PUBLIC_PREP_SELECTOR_OR_STOP_READY_READONLY":
        blockers.append("P150_SELECTOR_STATUS_NOT_READY")
    if selector.get("recommended_next") != "P150B_LOCAL_PRIVATE_RELEASE_PACK":
        blockers.append("P150_RECOMMENDED_NEXT_NOT_P150B")
    if selector.get("blocker_count", 0) != 0:
        blockers.append("P150_BLOCKERS_NOT_ZERO")
    if selector.get("safety", {}).get("google_sheets_write") is not False:
        blockers.append("GOOGLE_SHEETS_WRITE_NOT_FALSE")
    if selector.get("safety", {}).get("public_deploy") is not False:
        blockers.append("PUBLIC_DEPLOY_NOT_FALSE")
    return blockers


def build_manifest(selector: dict[str, Any], evidence: list[dict[str, Any]]) -> dict[str, Any]:
    blockers = validate_selector(selector)
    missing = [item["prefix"] for item in evidence if item["gate"] != "OK"]
    if missing:
        blockers.append("MISSING_RELEASE_EVIDENCE:" + ",".join(missing))

    return {
        "status": STATUS_READY if not blockers else "P150B_LOCAL_PRIVATE_RELEASE_PACK_BLOCKED",
        "version": VERSION,
        "source_p150_status": selector.get("status"),
        "source_recommended_next": selector.get("recommended_next"),
        "release_name": "MVP_QAIC_LOCAL_PRIVATE_PROMPT_COCKPIT_RELEASE_P150B",
        "release_scope": "LOCAL_PRIVATE_PROMPT_COCKPIT_ONLY",
        "evidence_count": len(evidence),
        "evidence_ok_count": sum(1 for item in evidence if item["gate"] == "OK"),
        "selected_file_total": sum(int(item["selected_file_count"]) for item in evidence),
        "blocker_count": len(blockers),
        "blockers": blockers,
        "evidence": evidence,
        "release_gates": {
            "migration_closed": True,
            "local_private_ready": True,
            "public_deploy_ready": False,
            "sheet_write_ready": False,
            "requires_human_review_before_public": True,
        },
        "safety": dict(SAFETY_MARKERS),
        "next": "STOP_OR_P150A_REAL_GEM_RESPONSE_IMPORT_OR_P150_PUBLIC_PREP_NO_DEPLOY",
    }


def copy_release_files(manifest: dict[str, Any], output_dir: Path) -> list[dict[str, str]]:
    evidence_dir = output_dir / "release_evidence"
    evidence_dir.mkdir(parents=True, exist_ok=True)
    copied: list[dict[str, str]] = []
    for item in manifest["evidence"]:
        prefix_dir = evidence_dir / item["prefix"].rstrip("_")
        prefix_dir.mkdir(parents=True, exist_ok=True)
        for raw_path in item["selected_paths"]:
            src = Path(raw_path)
            if not src.exists() or not src.is_file():
                continue
            dst = prefix_dir / safe_release_name(src)
            shutil.copy2(src, dst)
            copied.append(
                {
                    "source": str(src),
                    "dest": str(dst),
                    "release_relative_path": dst.relative_to(output_dir).as_posix(),
                }
            )
    return copied


def write_release_zip(output_dir: Path, zip_name: str) -> Path:
    zip_path = output_dir / zip_name
    with ZipFile(zip_path, "w", compression=ZIP_DEFLATED) as archive:
        for file in sorted(output_dir.rglob("*")):
            if not file.is_file():
                continue
            if file == zip_path:
                continue
            if file.name.lower() == "desktop.ini":
                continue
            archive.write(file, arcname=file.relative_to(output_dir).as_posix())
    return zip_path


def write_outputs(manifest: dict[str, Any], output_dir: Path) -> dict[str, str]:
    output_dir.mkdir(parents=True, exist_ok=True)

    copied = copy_release_files(manifest, output_dir)
    manifest["copied_file_count"] = len(copied)
    manifest["copied_files"] = copied

    manifest_path = output_dir / "P150B_RELEASE_MANIFEST.json"
    evidence_csv = output_dir / "P150B_RELEASE_EVIDENCE_INDEX.csv"
    notes_md = output_dir / "P150B_RELEASE_NOTES.md"
    launch_md = output_dir / "P150B_LOCAL_LAUNCH_COMMANDS.md"
    summary_path = output_dir / "P150B_SUMMARY.json"

    manifest_path.write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2, sort_keys=True), encoding="utf-8"
    )

    with evidence_csv.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=["prefix", "found", "gate", "export_dir", "selected_file_count"],
        )
        writer.writeheader()
        for item in manifest["evidence"]:
            writer.writerow({field: item.get(field, "") for field in writer.fieldnames})

    notes_md.write_text(
        "\n".join(
            [
                "# P150B — Local Private Release Pack",
                "",
                f"- Status: `{manifest['status']}`",
                f"- Release: `{manifest['release_name']}`",
                f"- Evidence OK: `{manifest['evidence_ok_count']}/{manifest['evidence_count']}`",
                f"- Copied files: `{manifest['copied_file_count']}`",
                "",
                "## Scope",
                "",
                "- MVP QAIC prompt cockpit local/private",
                "- NiceGUI local only",
                "- Prompt workflow + GEM review + correction queue",
                "",
                "## Safety",
                "",
                "- No Sheet write",
                "- No public deploy",
                "- No Apps Script / CLASP",
                "- No broker/order/sizing",
                "- Future Sheet/public actions require explicit GO",
                "",
            ]
        ),
        encoding="utf-8",
    )

    launch_md.write_text(
        "\n".join(
            [
                "# P150B — Local Launch Commands",
                "",
                "```powershell",
                '$ErrorActionPreference = "Stop"',
                "chcp 65001 | Out-Null",
                "[Console]::OutputEncoding = [System.Text.Encoding]::UTF8",
                "$OutputEncoding = [System.Text.Encoding]::UTF8",
                "",
                "# Depuis le repo MVP_QAIC_PY",
                "python -m mvp_qaic_py.p147_operator_polish --help",
                "# Les Apps NiceGUI exportées restent à lancer manuellement depuis 05_EXPORTS.",
                "```",
                "",
                "Rappel : pas de public deploy, pas de Sheet write, pas de broker/order/sizing.",
                "",
            ]
        ),
        encoding="utf-8",
    )

    summary = {
        "status": manifest["status"],
        "release_name": manifest["release_name"],
        "evidence_ok_count": manifest["evidence_ok_count"],
        "evidence_count": manifest["evidence_count"],
        "selected_file_total": manifest["selected_file_total"],
        "copied_file_count": manifest["copied_file_count"],
        "blocker_count": manifest["blocker_count"],
        "google_sheets_write": False,
        "live_google_sheets_read": False,
        "public_deploy": False,
        "broker": False,
        "order": False,
        "sizing": False,
        "auto_apply_gem_response": False,
        "future_sheet_write_requires_explicit_go": True,
        "future_public_deploy_requires_explicit_go": True,
        "output_dir": str(output_dir),
        "next": manifest["next"],
    }
    summary_path.write_text(
        json.dumps(summary, ensure_ascii=False, indent=2, sort_keys=True), encoding="utf-8"
    )

    release_zip = write_release_zip(output_dir, "P150B_LOCAL_PRIVATE_RELEASE_PACK.zip")

    return {
        "manifest_json": str(manifest_path),
        "evidence_csv": str(evidence_csv),
        "release_notes_md": str(notes_md),
        "launch_commands_md": str(launch_md),
        "summary_json": str(summary_path),
        "release_zip": str(release_zip),
    }


def run_release_pack(request: ReleasePackRequest) -> dict[str, Any]:
    selector = load_json(request.p150_selector_path)
    evidence = collect_release_evidence(request.exports_root)
    manifest = build_manifest(selector, evidence)
    manifest["run_id"] = request.run_id
    manifest["generated_at_utc"] = request.generated_at_utc
    manifest["source_p150_selector_path"] = str(request.p150_selector_path)
    manifest["exports_root"] = str(request.exports_root)
    outputs = write_outputs(manifest, request.output_dir)
    manifest["output_files"] = outputs
    (request.output_dir / "P150B_RELEASE_MANIFEST.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2, sort_keys=True),
        encoding="utf-8",
    )
    return manifest


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="P150B local private release pack.")
    parser.add_argument("--p150-selector", required=True)
    parser.add_argument("--exports-root", required=True)
    parser.add_argument("--output-dir", required=True)
    parser.add_argument("--run-id", default="P150B-LOCAL-PRIVATE-RELEASE-PACK")
    parser.add_argument("--generated-at-utc", default=utc_now_iso())
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    manifest = run_release_pack(
        ReleasePackRequest(
            p150_selector_path=Path(args.p150_selector),
            exports_root=Path(args.exports_root),
            output_dir=Path(args.output_dir),
            run_id=args.run_id,
            generated_at_utc=args.generated_at_utc,
        )
    )
    print(manifest["status"])
    print(f"release_name={manifest['release_name']}")
    print(f"evidence_ok_count={manifest['evidence_ok_count']}")
    print(f"evidence_count={manifest['evidence_count']}")
    print(f"copied_file_count={manifest['copied_file_count']}")
    print(f"blocker_count={manifest['blocker_count']}")
    print("google_sheets_write=false")
    print("public_deploy=false")
    print(f"output_dir={args.output_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
