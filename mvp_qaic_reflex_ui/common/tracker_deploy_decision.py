from __future__ import annotations

from pathlib import Path
from typing import Any

PRIVATE_DEPLOY_DECISION = "APPROVE_PRIVATE_REFLEX_ROUTE_DEPLOY"
PUBLIC_DEPLOY_DECISION = "BLOCK_PUBLIC_REFLEX_DEPLOY"
STATUS_READY = "MVP_R1R_UI_TRACKER_DEPLOY_DECISION_READY"
PUBLIC_BLOCK_REASON = "BLOCKED_UNTIL_REAL_REFLEX_BROWSER_RUNTIME_VISUAL_MATCH"

REQUIRED_FILES = (
    "docs/dev_tracking/visual_oracle/APPROVED_TRACKER_PREVIEW.html",
    "docs/dev_tracking/UI_TRACKER_DEPLOY_READINESS_FINAL_R1Q_20260629.md",
    "docs/dev_tracking/UI_TRACKER_REFLEX_ROUTE_BINDING_R1P_20260629.md",
    "docs/dev_tracking/ui_tracker_tool_manifest.json",
    "mvp_qaic_reflex_ui/common/tracker_deploy_readiness.py",
    "mvp_qaic_reflex_ui/common/tracker_route_binding.py",
    "mvp_qaic_reflex_ui/common/tracker_ui_tool_manifest.py",
    "tools/ui_tracker_deploy_readiness_gate.py",
    "tools/ui_tracker_route_binding_gate.py",
    "tools/ui_tracker_operator_launcher.py",
)


def _exists(repo: Path, rel_path: str) -> bool:
    return (repo / rel_path).is_file()


def deploy_decision_status(repo: Path | str | None = None) -> dict[str, Any]:
    repo_path = Path(repo) if repo is not None else Path.cwd()
    missing = [rel for rel in REQUIRED_FILES if not _exists(repo_path, rel)]
    private_allowed = not missing
    public_allowed = False
    ready = private_allowed and not public_allowed
    return {
        "ready": ready,
        "status": STATUS_READY if ready else "MVP_R1R_UI_TRACKER_DEPLOY_DECISION_BLOCKED",
        "decision": {
            "private_reflex_route_deploy": PRIVATE_DEPLOY_DECISION
            if private_allowed
            else "BLOCK_PRIVATE_REFLEX_ROUTE_DEPLOY",
            "public_reflex_deploy": PUBLIC_DEPLOY_DECISION,
        },
        "private_reflex_route_deploy_allowed": private_allowed,
        "public_reflex_deploy_allowed": public_allowed,
        "public_reflex_deploy_status": PUBLIC_BLOCK_REASON,
        "required_files_ok": not missing,
        "missing_required_files": missing,
        "approved_oracle": str(
            repo_path / "docs/dev_tracking/visual_oracle/APPROVED_TRACKER_PREVIEW.html"
        ),
        "safety": {
            "no_public_deploy": True,
            "no_bun_loop": True,
            "no_broker_order_sizing": True,
            "human_review_required_for_public_deploy": True,
        },
        "next": "R1S_HANDOFF_FINAL",
    }
