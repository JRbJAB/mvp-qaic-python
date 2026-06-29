"""Operator CLI for the UI Common Tracker Tool deploy gate."""

from __future__ import annotations

import argparse
import importlib
import inspect
import json
import sys
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))


def _load_deployment_status() -> Any:
    module = importlib.import_module("mvp_qaic_reflex_ui.common.tracker_ui_tool_deployment")
    return module.deployment_status


def _default_oracle_path() -> Path:
    return REPO_ROOT / "docs" / "dev_tracking" / "visual_oracle" / "APPROVED_TRACKER_PREVIEW.html"


def _call_deployment_status(approved_oracle: Path) -> Any:
    deployment_status = _load_deployment_status()
    attempts = [
        lambda: deployment_status(),
        lambda: deployment_status(approved_oracle=approved_oracle),
        lambda: deployment_status(approved_oracle_path=approved_oracle),
        lambda: deployment_status(oracle_path=approved_oracle),
        lambda: deployment_status(str(approved_oracle)),
    ]
    errors: list[str] = []
    for attempt in attempts:
        try:
            return attempt()
        except TypeError as exc:
            errors.append(str(exc))
    signature = inspect.signature(deployment_status)
    raise TypeError(
        "Unable to call deployment_status with supported signatures. "
        f"signature={signature}; errors={errors}"
    )


def _to_jsonable(value: Any) -> Any:
    if isinstance(value, Path):
        return str(value)
    if isinstance(value, dict):
        return {str(key): _to_jsonable(item) for key, item in value.items()}
    if isinstance(value, (list, tuple, set)):
        return [_to_jsonable(item) for item in value]
    if hasattr(value, "model_dump"):
        return _to_jsonable(value.model_dump())
    if hasattr(value, "__dict__"):
        return _to_jsonable(vars(value))
    return value


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", required=True, help="Output JSON path")
    parser.add_argument(
        "--approved-oracle",
        default=str(_default_oracle_path()),
        help="Approved tracker visual oracle path",
    )
    args = parser.parse_args()

    out_path = Path(args.out)
    approved_oracle = Path(args.approved_oracle)
    out_path.parent.mkdir(parents=True, exist_ok=True)

    raw_status = _call_deployment_status(approved_oracle)
    payload = _to_jsonable(raw_status)
    if not isinstance(payload, dict):
        payload = {"deployment_status": payload}

    payload.setdefault("approved_oracle", str(approved_oracle))
    payload.setdefault("approved_oracle_exists", approved_oracle.exists())
    payload.setdefault("reflex_public_deploy_allowed", False)
    payload.setdefault(
        "reflex_public_deploy_status",
        "BLOCKED_UNTIL_REAL_REFLEX_BROWSER_RUNTIME_VISUAL_MATCH",
    )
    payload.setdefault("ui_tracker_tool_deploy_gate", "READY_INTERNAL_DEPLOY_GATE")

    out_path.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")

    print(f"UI_TRACKER_TOOL_DEPLOY_GATE_JSON={out_path}")
    print(f"APPROVED_ORACLE={approved_oracle}")
    print(f"APPROVED_ORACLE_EXISTS={approved_oracle.exists()}")
    print(f"REFLEX_PUBLIC_DEPLOY_ALLOWED={payload.get('reflex_public_deploy_allowed')}")
    print(f"REFLEX_PUBLIC_DEPLOY_STATUS={payload.get('reflex_public_deploy_status')}")
    print("STATUS=MVP_R1K_R1L_UI_TRACKER_TOOL_DEPLOY_GATE_READY")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
