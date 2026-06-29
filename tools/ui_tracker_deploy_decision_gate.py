from __future__ import annotations

import argparse
import importlib
import json
import sys
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[1]


def _load_status(repo: Path) -> dict[str, Any]:
    if str(repo) not in sys.path:
        sys.path.insert(0, str(repo))
    module = importlib.import_module("mvp_qaic_reflex_ui.common.tracker_deploy_decision")
    return module.deploy_decision_status(repo)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", required=True)
    parser.add_argument("--repo", default=str(REPO_ROOT))
    args = parser.parse_args()

    repo = Path(args.repo).resolve()
    payload = _load_status(repo)
    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print(f"UI_TRACKER_DEPLOY_DECISION_JSON={out}")
    print(f"READY={payload['ready']}")
    print(f"PRIVATE_REFLEX_ROUTE_DEPLOY_ALLOWED={payload['private_reflex_route_deploy_allowed']}")
    print(f"PUBLIC_REFLEX_DEPLOY_ALLOWED={payload['public_reflex_deploy_allowed']}")
    print(f"PUBLIC_REFLEX_DEPLOY_STATUS={payload['public_reflex_deploy_status']}")
    print(f"STATUS={payload['status']}")
    return 0 if payload["ready"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
