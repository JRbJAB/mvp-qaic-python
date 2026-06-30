from __future__ import annotations
import argparse, json
from pathlib import Path

POLICY_ID = "R16F2H4_REFLEX_RUNTIME_POLICY_LOCK"
REQUIRED = ["python","-m","reflex","run","--env","dev","--backend-host","0.0.0.0","--backend-port","8000","--frontend-port","3000"]
FORBIDDEN = ["--env prod","--single-port","reflex export","NiceGUI",".web source patch"]

def load_policy(repo: Path) -> dict:
    path = repo / "config" / "reflex_runtime_policy.json"
    return json.loads(path.read_text(encoding="utf-8"))

def validate_command(command: str) -> list[str]:
    low = command.lower()
    errors = []
    for bad in FORBIDDEN:
        if bad.lower() in low:
            errors.append(f"command contains forbidden primary preview snippet: {bad}")
    for token in REQUIRED:
        if token.lower() not in low:
            errors.append(f"command missing required token: {token}")
    return errors

def validate_policy(policy: dict) -> list[str]:
    errors = []
    if policy.get("policy_id") != POLICY_ID:
        errors.append("policy_id mismatch")
    rt = policy.get("runtime", {})
    if rt.get("mode") != "dev":
        errors.append("runtime.mode must be dev")
    if rt.get("copy_strategy") != "FULL_TRACKED_HEAD_COPY_OUTSIDE_REPO":
        errors.append("copy_strategy must be FULL_TRACKED_HEAD_COPY_OUTSIDE_REPO")
    if rt.get("repo_write_allowed_before_visual_validation") is not False:
        errors.append("repo_write_allowed_before_visual_validation must be false")
    ports = policy.get("ports", {})
    expected = {
        "container_frontend": 3000, "container_backend": 8000,
        "reference_frontend_host": 3035, "reference_backend_host": 8035,
        "preview_frontend_host": 3055, "preview_backend_host": 8055,
    }
    for key, value in expected.items():
        if ports.get(key) != value:
            errors.append(f"{key} must be {value}")
    if ports.get("dynamic_port_fallback_allowed") is not False:
        errors.append("dynamic_port_fallback_allowed must be false")
    cmd = policy.get("commands", {}).get("primary_preview_container_command", "")
    errors.extend(validate_command(cmd))
    gates = set(policy.get("required_gates_before_any_ui_commit", []))
    for gate in ["REFLEX_POLICY_GUARD_OK=True","DOM_CAPTURE_OK=True","PNG_CAPTURE_OK=True","HUMAN_VISUAL_APPROVAL=True"]:
        if gate not in gates:
            errors.append(f"missing required gate: {gate}")
    if policy.get("official_reflex_docs_required") is not True:
        errors.append("official_reflex_docs_required must be true")
    return errors

def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo", default=".")
    ap.add_argument("--command", default="")
    args = ap.parse_args()
    repo = Path(args.repo).resolve()
    try:
        policy = load_policy(repo)
        errors = validate_policy(policy)
        if args.command:
            errors.extend(validate_command(args.command))
    except Exception as exc:
        print("REFLEX_POLICY_GUARD_OK=False")
        print(f"ERROR={type(exc).__name__}:{exc}")
        return 1
    if errors:
        print("REFLEX_POLICY_GUARD_OK=False")
        for e in errors:
            print(f"ERROR={e}")
        return 1
    print("REFLEX_POLICY_GUARD_OK=True")
    print(f"POLICY_ID={POLICY_ID}")
    print("REFLEX_POLICY_GUARD_REQUIRED=True")
    print("PREVIEW_MODE=REFLEX_DEV")
    print("COPY_STRATEGY=FULL_TRACKED_HEAD_COPY_OUTSIDE_REPO")
    print("PRIMARY_PREVIEW_COMMAND=python -m reflex run --env dev --backend-host 0.0.0.0 --backend-port 8000 --frontend-port 3000")
    print("HOST_PREVIEW_PORTS=3055:3000,8055:8000")
    print("FORBID_PROD_SINGLE_PORT_EXPORT_MINIMAL_ALLOWLIST=True")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())

