from __future__ import annotations

from pathlib import Path
from typing import Any

REQUIRED_ORACLE_TOKENS = (
    "CDC Tracker",
    "Dev Tracker",
    "/dev-tracking",
    "/cdc-dev-tracker",
    "/cdc-tracker",
    "%",
)

REQUIRED_FILES = (
    "docs/dev_tracking/visual_oracle/APPROVED_TRACKER_PREVIEW.html",
    "docs/dev_tracking/ui_tracker_tool_manifest.json",
    "mvp_qaic_reflex_ui/common/tracker_ui_tool_deployment.py",
    "mvp_qaic_reflex_ui/common/tracker_ui_tool_manifest.py",
    "mvp_qaic_reflex_ui/common/tracker_route_binding.py",
    "tools/ui_tracker_operator_launcher.py",
    "tools/ui_tracker_deploy_gate.py",
    "tools/ui_tracker_route_binding_gate.py",
)


def _repo_root(repo: str | Path | None = None) -> Path:
    if repo is not None:
        return Path(repo).resolve()
    return Path(__file__).resolve().parents[2]


def _oracle_status(repo_root: Path) -> dict[str, Any]:
    oracle = repo_root / "docs/dev_tracking/visual_oracle/APPROVED_TRACKER_PREVIEW.html"
    exists = oracle.is_file()
    text = oracle.read_text(encoding="utf-8") if exists else ""
    missing = [token for token in REQUIRED_ORACLE_TOKENS if token not in text]
    blue_ok = any(token in text for token in ("#2563eb", "#1d4ed8", "#3b82f6", "blue", "progress"))
    return {
        "path": str(oracle),
        "exists": exists,
        "missing_tokens": missing,
        "blue_ok": blue_ok,
        "ok": exists and not missing and blue_ok,
    }


def deploy_readiness_status(repo: str | Path | None = None) -> dict[str, Any]:
    repo_root = _repo_root(repo)
    required = {rel: (repo_root / rel).is_file() for rel in REQUIRED_FILES}
    oracle = _oracle_status(repo_root)
    required_files_ok = all(required.values())
    route_binding_ready = required["mvp_qaic_reflex_ui/common/tracker_route_binding.py"]
    tool_registry_ready = required["docs/dev_tracking/ui_tracker_tool_manifest.json"]
    internal_tool_ready = required_files_ok and oracle["ok"] and route_binding_ready
    private_reflex_route_deploy_allowed = internal_tool_ready
    public_reflex_deploy_allowed = False
    status = (
        "MVP_R1Q_UI_TRACKER_DEPLOY_READINESS_FINAL_READY"
        if internal_tool_ready
        else "MVP_R1Q_UI_TRACKER_DEPLOY_READINESS_FINAL_BLOCKED"
    )
    return {
        "ready": internal_tool_ready,
        "status": status,
        "repo": str(repo_root),
        "approved_oracle": oracle,
        "required_files": required,
        "required_files_ok": required_files_ok,
        "tool_registry_ready": tool_registry_ready,
        "route_binding_ready": route_binding_ready,
        "operator_launcher_ready": required["tools/ui_tracker_operator_launcher.py"],
        "deploy_gate_ready": required["tools/ui_tracker_deploy_gate.py"],
        "private_reflex_route_deploy_allowed": private_reflex_route_deploy_allowed,
        "public_reflex_deploy_allowed": public_reflex_deploy_allowed,
        "public_reflex_deploy_status": "BLOCKED_UNTIL_REAL_REFLEX_BROWSER_RUNTIME_VISUAL_MATCH",
        "next_steps": [
            "R1R operator decision for private/public deploy mode",
            "R1S final handoff and resume memo",
        ],
    }
