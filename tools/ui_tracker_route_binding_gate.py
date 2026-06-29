from __future__ import annotations

import argparse
import json
import sys
from importlib import import_module
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[1]


def _ensure_repo_on_path(repo: Path) -> None:
    repo_text = str(repo.resolve())
    if repo_text not in sys.path:
        sys.path.insert(0, repo_text)


def _route_binding_status(repo: Path) -> dict[str, Any]:
    _ensure_repo_on_path(repo)
    module = import_module("mvp_qaic_reflex_ui.common.tracker_route_binding")
    return module.route_binding_status(repo)


def _write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


def main() -> int:
    parser = argparse.ArgumentParser(description="R1P UI Tracker Reflex route binding deploy gate.")
    parser.add_argument("--out", required=True, help="Output JSON path.")
    parser.add_argument("--repo", default=str(REPO_ROOT), help="Repository root.")
    args = parser.parse_args()

    repo = Path(args.repo).resolve()
    payload = _route_binding_status(repo)
    out = Path(args.out)
    _write_json(out, payload)

    print(f"UI_TRACKER_ROUTE_BINDING_JSON={out}")
    print(f"APPROVED_ORACLE={payload['approved_oracle']}")
    print(f"APPROVED_ORACLE_EXISTS={payload['approved_oracle_exists']}")
    print(f"ROUTES_BOUND={payload['routes_bound']}")
    print(f"REQUIRED_FILES_OK={payload['required_files_ok']}")
    print(f"REFLEX_PUBLIC_DEPLOY_ALLOWED={payload['reflex_public_deploy_allowed']}")
    print(f"REFLEX_PUBLIC_DEPLOY_STATUS={payload['reflex_public_deploy_status']}")
    print(f"STATUS={payload['status']}")

    return 0 if payload["ready"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
