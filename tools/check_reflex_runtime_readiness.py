from __future__ import annotations

import argparse
import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOC_DIR = ROOT / "docs" / "dev_tracking"


def _read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return path.read_text(encoding="utf-8-sig")


def _backend_evidence() -> dict[str, object]:
    docs = sorted(
        path
        for path in DOC_DIR.glob("*.md")
        if "BACKEND" in path.name.upper() or "RUNTIME" in path.name.upper()
    )
    matched_docs: list[str] = []
    ok_tokens = (
        "BACKEND_OK=True",
        "BACKEND_PORT_OPEN=True",
        "Backend-only diagnostic passed",
        "backend runtime is proven",
        "backend OK",
    )
    for path in docs:
        text = _read_text(path)
        if any(token.lower() in text.lower() for token in ok_tokens):
            matched_docs.append(str(path.relative_to(ROOT)))
    return {
        "docs_present": [str(path.relative_to(ROOT)) for path in docs],
        "mentions_backend_ok": bool(matched_docs),
        "matched_docs": matched_docs,
    }


def build_readiness_report(root: Path = ROOT) -> dict[str, object]:
    web_dir = root / ".web"
    package_json = web_dir / "package.json"
    node_modules = web_dir / "node_modules"
    react_router = node_modules / ".bin" / "react-router"
    react_router_cmd = node_modules / ".bin" / "react-router.cmd"

    checks = {
        "web_package_json_exists": package_json.exists(),
        "web_node_modules_exists": node_modules.exists(),
        "react_router_bin_exists": react_router.exists() or react_router_cmd.exists(),
    }
    backend = _backend_evidence()
    blockers: list[str] = []

    if not checks["web_package_json_exists"]:
        blockers.append("frontend .web/package.json is missing")
    if not checks["web_node_modules_exists"]:
        blockers.append("frontend .web/node_modules is missing")
    if not checks["react_router_bin_exists"]:
        blockers.append("frontend react-router bin is absent")
    if backend["docs_present"] and not backend["mentions_backend_ok"]:
        blockers.append("backend evidence docs are present but do not mention backend OK")

    runtime_ready = not blockers
    status = "RUNTIME_READY_LOCAL_PREREQS_OK" if runtime_ready else "RUNTIME_BLOCKED_LOCAL_PREREQS"
    return {
        "runtime_ready": runtime_ready,
        "status": status,
        "checked_at": datetime.now().isoformat(timespec="seconds"),
        "checks": checks,
        "backend_evidence": backend,
        "blockers": blockers,
        "policy": {
            "process_free": True,
            "no_bun": True,
            "no_npm": True,
            "no_reflex": True,
            "no_browser": True,
            "no_deploy": True,
            "no_http": True,
            "no_provider_broker_sheet_bq": True,
        },
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", required=True)
    args = parser.parse_args()

    report = build_readiness_report()
    out_path = Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")

    print(f"RUNTIME_READY={str(report['runtime_ready']).lower()}")
    print(f"STATUS={report['status']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
