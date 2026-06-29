"""Deployment contract for the UI Common Tracker Tool.

This module is intentionally small and dependency-light: it is used by tests,
operator gates, and release scripts to prevent confusing the approved static
preview with a public Reflex deployment.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

APPROVED_ORACLE_RELATIVE_PATH = Path(
    "docs/dev_tracking/visual_oracle/APPROVED_TRACKER_PREVIEW.html"
)

REQUIRED_ORACLE_TOKENS: tuple[str, ...] = (
    "MVP QAIC CDC Dev Tracker",
    "Migration Tracker Visual Oracle",
    "CDC Tracker",
    "Dev Tracker",
    "/dev-tracking",
    "/cdc-dev-tracker",
    "/cdc-tracker",
    "%",
)

REQUIRED_BLUE_TOKENS: tuple[str, ...] = (
    "#2563eb",
    "#1d4ed8",
    "#3b82f6",
    "progress",
)

TRACKER_TOOL_ROUTES: tuple[str, ...] = (
    "/dev-tracking",
    "/cdc-dev-tracker",
    "/cdc-tracker",
)

TRACKER_RENDER_TYPES: tuple[str, ...] = (
    "migration_tracker_reference",
    "migration_tracker_oracle",
    "cdc_tracker",
    "cdc_dev_tracker",
    "dev_tracker",
    "tool_registry_cdc",
    "tool_registry_tracker",
    "benchmark_tracker",
)

REFLEX_PUBLIC_DEPLOY_STATUS_BLOCKED = "BLOCKED_UNTIL_REAL_REFLEX_BROWSER_RUNTIME_VISUAL_MATCH"


@dataclass(frozen=True)
class UITrackerToolDeploymentStatus:
    """Serializable deployment status for the UI Common Tracker Tool."""

    ui_tracker_tool_deployed: bool
    approved_oracle_exists: bool
    approved_oracle_ok: bool
    missing_oracle_tokens: tuple[str, ...]
    blue_visual_ok: bool
    routes: tuple[str, ...]
    render_types: tuple[str, ...]
    static_preview_supported: bool
    reflex_public_deploy_allowed: bool
    reflex_public_deploy_status: str
    status: str

    def as_dict(self) -> dict[str, Any]:
        return asdict(self)


def repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def approved_oracle_path(root: Path | None = None) -> Path:
    base = root or repo_root()
    return base / APPROVED_ORACLE_RELATIVE_PATH


def validate_approved_oracle(root: Path | None = None) -> tuple[bool, tuple[str, ...], bool]:
    oracle = approved_oracle_path(root)
    if not oracle.exists():
        return False, REQUIRED_ORACLE_TOKENS, False

    html = oracle.read_text(encoding="utf-8", errors="replace")
    missing = tuple(token for token in REQUIRED_ORACLE_TOKENS if token not in html)
    blue_visual_ok = any(token in html for token in REQUIRED_BLUE_TOKENS)
    return len(missing) == 0 and blue_visual_ok, missing, blue_visual_ok


def deployment_status(root: Path | None = None) -> UITrackerToolDeploymentStatus:
    oracle = approved_oracle_path(root)
    oracle_ok, missing, blue_visual_ok = validate_approved_oracle(root)
    ui_tracker_tool_deployed = oracle.exists() and oracle_ok
    status = (
        "UI_TRACKER_TOOL_DEPLOYED_REFLEX_PUBLIC_DEPLOY_BLOCKED"
        if ui_tracker_tool_deployed
        else "UI_TRACKER_TOOL_NOT_DEPLOYABLE_APPROVED_ORACLE_INVALID"
    )

    return UITrackerToolDeploymentStatus(
        ui_tracker_tool_deployed=ui_tracker_tool_deployed,
        approved_oracle_exists=oracle.exists(),
        approved_oracle_ok=oracle_ok,
        missing_oracle_tokens=missing,
        blue_visual_ok=blue_visual_ok,
        routes=TRACKER_TOOL_ROUTES,
        render_types=TRACKER_RENDER_TYPES,
        static_preview_supported=ui_tracker_tool_deployed,
        reflex_public_deploy_allowed=False,
        reflex_public_deploy_status=REFLEX_PUBLIC_DEPLOY_STATUS_BLOCKED,
        status=status,
    )
