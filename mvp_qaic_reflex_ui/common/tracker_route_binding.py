from __future__ import annotations

from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

ROUTE_BINDING_STATUS_READY = "MVP_R1P_REFLEX_ROUTE_BINDING_READY"
ROUTE_BINDING_STATUS_BLOCKED = "MVP_R1P_REFLEX_ROUTE_BINDING_BLOCKED"

APPROVED_ORACLE_RELATIVE_PATH = Path(
    "docs/dev_tracking/visual_oracle/APPROVED_TRACKER_PREVIEW.html"
)

REQUIRED_REPO_FILES = (
    Path("mvp_qaic_reflex_ui/common/tracker_ui_kit.py"),
    Path("mvp_qaic_reflex_ui/common/tracker_ui_tool_deployment.py"),
    Path("mvp_qaic_reflex_ui/common/tracker_ui_tool_manifest.py"),
    Path("tools/ui_tracker_deploy_gate.py"),
    Path("tools/ui_tracker_operator_launcher.py"),
    Path("docs/dev_tracking/ui_tracker_tool_manifest.json"),
)

ROUTE_SOURCE_GLOBS = (
    "mvp_qaic_reflex_ui/**/*.py",
    "tools/*.py",
    "docs/dev_tracking/*.md",
    "docs/dev_tracking/*.json",
)


@dataclass(frozen=True)
class TrackerRouteBinding:
    route: str
    route_id: str
    surface: str
    render_contract: str
    oracle_required: bool = True
    public_deploy_allowed: bool = False


def route_bindings() -> tuple[TrackerRouteBinding, ...]:
    """Return the approved Reflex route binding contract for the UI Tracker tool."""
    return (
        TrackerRouteBinding(
            route="/dev-tracking",
            route_id="dev_tracking",
            surface="Dev Tracker",
            render_contract="APPROVED_TRACKER_PREVIEW",
        ),
        TrackerRouteBinding(
            route="/cdc-dev-tracker",
            route_id="cdc_dev_tracker",
            surface="CDC Dev Tracker",
            render_contract="APPROVED_TRACKER_PREVIEW",
        ),
        TrackerRouteBinding(
            route="/cdc-tracker",
            route_id="cdc_tracker",
            surface="CDC Tracker",
            render_contract="APPROVED_TRACKER_PREVIEW",
        ),
    )


def _repo_root(repo_root: str | Path | None = None) -> Path:
    if repo_root is not None:
        return Path(repo_root).resolve()

    return Path(__file__).resolve().parents[2]


def _safe_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8", errors="ignore")
    except OSError:
        return ""


def _source_files(root: Path) -> list[Path]:
    files: list[Path] = []
    for pattern in ROUTE_SOURCE_GLOBS:
        files.extend(root.glob(pattern))

    return sorted({path for path in files if path.is_file()})


def _route_hits(root: Path) -> dict[str, list[str]]:
    hits: dict[str, list[str]] = {binding.route: [] for binding in route_bindings()}
    for path in _source_files(root):
        text = _safe_text(path)
        if not text:
            continue
        for route in hits:
            if route in text:
                hits[route].append(str(path.relative_to(root)).replace("\\", "/"))

    return hits


def route_binding_status(repo_root: str | Path | None = None) -> dict[str, Any]:
    """Return the operator-readable R1P route binding deploy-gate payload."""
    root = _repo_root(repo_root)
    oracle_path = root / APPROVED_ORACLE_RELATIVE_PATH
    required_files = {
        str(path).replace("\\", "/"): (root / path).is_file() for path in REQUIRED_REPO_FILES
    }
    route_hits = _route_hits(root)
    route_bindings_payload = [asdict(binding) for binding in route_bindings()]
    routes_bound = all(bool(files) for files in route_hits.values())
    required_files_ok = all(required_files.values())
    oracle_exists = oracle_path.is_file()

    ready = bool(oracle_exists and required_files_ok and routes_bound)
    status = ROUTE_BINDING_STATUS_READY if ready else ROUTE_BINDING_STATUS_BLOCKED

    return {
        "ready": ready,
        "status": status,
        "route_binding_version": "R1P",
        "approved_oracle": str(oracle_path),
        "approved_oracle_exists": oracle_exists,
        "reflex_public_deploy_allowed": False,
        "reflex_public_deploy_status": ("BLOCKED_UNTIL_REAL_REFLEX_BROWSER_RUNTIME_VISUAL_MATCH"),
        "routes": route_bindings_payload,
        "route_hits": route_hits,
        "routes_bound": routes_bound,
        "required_files": required_files,
        "required_files_ok": required_files_ok,
        "next_gate": "R1Q_DEPLOY_READINESS_FINAL",
    }
