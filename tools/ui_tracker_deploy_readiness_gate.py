from __future__ import annotations

import argparse
import importlib
import json
import sys
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))


def _deployment_module() -> Any:
    return importlib.import_module("mvp_qaic_reflex_ui.common.tracker_deploy_readiness")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", required=True)
    parser.add_argument("--repo", default=str(REPO_ROOT))
    args = parser.parse_args()

    module = _deployment_module()
    payload = module.deploy_readiness_status(args.repo)
    out_path = Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print(f"UI_TRACKER_DEPLOY_READINESS_JSON={out_path}")
    print(f"READY={payload['ready']}")
    print(f"PRIVATE_REFLEX_ROUTE_DEPLOY_ALLOWED={payload['private_reflex_route_deploy_allowed']}")
    print(f"PUBLIC_REFLEX_DEPLOY_ALLOWED={payload['public_reflex_deploy_allowed']}")
    print(f"PUBLIC_REFLEX_DEPLOY_STATUS={payload['public_reflex_deploy_status']}")
    print(f"STATUS={payload['status']}")
    return 0 if payload["ready"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
