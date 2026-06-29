from __future__ import annotations

from pathlib import Path

FINAL_HANDOFF_STATUS = "MVP_R1S_UI_TRACKER_FINAL_HANDOFF_READY"
PUBLIC_BLOCK_STATUS = "BLOCKED_UNTIL_REAL_REFLEX_BROWSER_RUNTIME_VISUAL_MATCH"

REQUIRED_RELATIVE_FILES = (
    "docs/dev_tracking/visual_oracle/APPROVED_TRACKER_PREVIEW.html",
    "docs/dev_tracking/UI_TRACKER_OPERATOR_LAUNCHER_R1M_20260629.md",
    "docs/dev_tracking/UI_TRACKER_REFLEX_ROUTE_BINDING_R1P_20260629.md",
    "docs/dev_tracking/UI_TRACKER_DEPLOY_READINESS_FINAL_R1Q_20260629.md",
    "docs/dev_tracking/UI_TRACKER_DEPLOY_DECISION_R1R_20260629.md",
    "docs/dev_tracking/ui_tracker_tool_manifest.json",
    "mvp_qaic_reflex_ui/common/tracker_ui_tool_manifest.py",
    "mvp_qaic_reflex_ui/common/tracker_ui_tool_deployment.py",
    "mvp_qaic_reflex_ui/common/tracker_route_binding.py",
    "mvp_qaic_reflex_ui/common/tracker_deploy_readiness.py",
    "mvp_qaic_reflex_ui/common/tracker_deploy_decision.py",
    "tools/ui_tracker_operator_launcher.py",
    "tools/ui_tracker_deploy_gate.py",
    "tools/ui_tracker_route_binding_gate.py",
    "tools/ui_tracker_deploy_readiness_gate.py",
    "tools/ui_tracker_deploy_decision_gate.py",
)

PHASES = (
    ("R1I", "approved_visual_oracle_locked"),
    ("R1J", "reflex_kit_preview_gate"),
    ("R1K", "ui_tracker_tool_deploy_gate"),
    ("R1L", "reflex_preview_deploy_gate"),
    ("R1M", "operator_launcher_registry"),
    ("R1N2", "local_web_cleanup_clean"),
    ("R1O2", "browser_oracle_visual_match_pass"),
    ("R1P", "reflex_routes_bound"),
    ("R1Q", "deploy_readiness_final"),
    ("R1R", "deploy_decision_final"),
    ("R1S", "final_handoff"),
)


def _repo_root(repo_root: str | Path | None = None) -> Path:
    if repo_root is not None:
        return Path(repo_root).resolve()
    return Path(__file__).resolve().parents[2]


def final_handoff_status(repo_root: str | Path | None = None) -> dict[str, object]:
    root = _repo_root(repo_root)
    required = [root / relative for relative in REQUIRED_RELATIVE_FILES]
    missing = [str(path.relative_to(root)) for path in required if not path.exists()]
    ready = not missing

    return {
        "ready": ready,
        "status": FINAL_HANDOFF_STATUS if ready else "MVP_R1S_UI_TRACKER_FINAL_HANDOFF_BLOCKED",
        "repo_root": str(root),
        "missing_files": missing,
        "phases": [
            {"phase": phase, "status": status, "done": phase != "R1S" or ready}
            for phase, status in PHASES
        ],
        "routes": ["/dev-tracking", "/cdc-dev-tracker", "/cdc-tracker"],
        "approved_oracle": str(
            root / "docs/dev_tracking/visual_oracle/APPROVED_TRACKER_PREVIEW.html"
        ),
        "private_reflex_route_deploy_allowed": ready,
        "public_reflex_deploy_allowed": False,
        "public_reflex_deploy_status": PUBLIC_BLOCK_STATUS,
        "operator_next": "Use private Reflex route deploy only; keep public deploy blocked until real Reflex browser runtime visual match.",
    }
