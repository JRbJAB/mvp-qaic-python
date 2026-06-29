from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

STATUS_READY = "MVP_R1M_UI_TRACKER_OPERATOR_LAUNCHER_READY"
STATUS_BLOCKED = "MVP_R1M_UI_TRACKER_OPERATOR_LAUNCHER_BLOCKED"
REFLEX_PUBLIC_DEPLOY_STATUS = "BLOCKED_UNTIL_REAL_REFLEX_BROWSER_RUNTIME_VISUAL_MATCH"


def _load_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def _fallback_manifest() -> dict[str, Any]:
    return {
        "tool_id": "ui_common_tracker_kit",
        "tool_name": "UI Common Tracker Kit",
        "status": "internal_tool_deployed",
        "routes": ["/dev-tracking", "/cdc-dev-tracker", "/cdc-tracker"],
        "approved_visual_oracle": "docs/dev_tracking/visual_oracle/APPROVED_TRACKER_PREVIEW.html",
        "public_reflex_deploy_allowed": False,
        "public_reflex_deploy_status": REFLEX_PUBLIC_DEPLOY_STATUS,
    }


def _load_manifest(repo: Path) -> dict[str, Any]:
    manifest_path = repo / "docs" / "dev_tracking" / "ui_tracker_tool_manifest.json"
    manifest = _load_json(manifest_path)
    if not manifest:
        manifest = _fallback_manifest()
    manifest.setdefault("tool_id", "ui_common_tracker_kit")
    manifest.setdefault("tool_name", "UI Common Tracker Kit")
    manifest.setdefault("routes", ["/dev-tracking", "/cdc-dev-tracker", "/cdc-tracker"])
    manifest.setdefault(
        "approved_visual_oracle", "docs/dev_tracking/visual_oracle/APPROVED_TRACKER_PREVIEW.html"
    )
    manifest.setdefault("public_reflex_deploy_allowed", False)
    manifest.setdefault("public_reflex_deploy_status", REFLEX_PUBLIC_DEPLOY_STATUS)
    return manifest


def build_payload(repo: Path) -> dict[str, Any]:
    repo = repo.resolve()
    manifest = _load_manifest(repo)
    approved_oracle = (
        repo / "docs" / "dev_tracking" / "visual_oracle" / "APPROVED_TRACKER_PREVIEW.html"
    )
    approved_oracle_exists = approved_oracle.exists()
    manifest_ok = manifest.get("tool_id") == "ui_common_tracker_kit"
    ready = bool(approved_oracle_exists and manifest_ok)
    status = STATUS_READY if ready else STATUS_BLOCKED

    deployment_gate = {
        "ready": ready,
        "tool_id": "ui_common_tracker_kit",
        "approved_oracle": str(approved_oracle),
        "approved_oracle_exists": approved_oracle_exists,
        "reflex_public_deploy_allowed": False,
        "reflex_public_deploy_status": REFLEX_PUBLIC_DEPLOY_STATUS,
        "real_reflex_browser_runtime_visual_match_required": True,
        "static_preview_proof_allowed": True,
        "public_deploy_requires_browser_match": True,
    }

    return {
        "ready": ready,
        "status": status,
        "manifest": manifest,
        "deployment_gate": deployment_gate,
        "operator_launcher": {
            "tool_id": "ui_common_tracker_kit",
            "entrypoint": "tools/ui_tracker_operator_launcher.py",
            "gate_cli": "tools/ui_tracker_deploy_gate.py",
            "approved_oracle": str(approved_oracle),
            "commands": [
                "python tools/ui_tracker_operator_launcher.py --out <report_json>",
                "python tools/ui_tracker_deploy_gate.py --out <gate_json>",
            ],
        },
        "approved_oracle": str(approved_oracle),
        "approved_oracle_exists": approved_oracle_exists,
        "reflex_public_deploy_allowed": False,
        "reflex_public_deploy_status": REFLEX_PUBLIC_DEPLOY_STATUS,
    }


def write_payload(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description="UI Tracker operator launcher registry gate.")
    parser.add_argument("--out", required=True, help="Output JSON report path")
    parser.add_argument("--repo", default=str(REPO_ROOT), help="Repository root")
    args = parser.parse_args()

    repo = Path(args.repo).resolve()
    out = Path(args.out)
    payload = build_payload(repo)
    write_payload(out, payload)

    print(f"UI_TRACKER_OPERATOR_LAUNCHER_JSON={out}")
    print(f"APPROVED_ORACLE={payload['approved_oracle']}")
    print(f"APPROVED_ORACLE_EXISTS={payload['approved_oracle_exists']}")
    print(f"REFLEX_PUBLIC_DEPLOY_ALLOWED={payload['reflex_public_deploy_allowed']}")
    print(f"REFLEX_PUBLIC_DEPLOY_STATUS={payload['reflex_public_deploy_status']}")
    print(f"READY={payload['ready']}")
    print(f"STATUS={payload['status']}")
    return 0 if payload["ready"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
