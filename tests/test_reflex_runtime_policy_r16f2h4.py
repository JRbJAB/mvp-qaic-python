from __future__ import annotations
import importlib.util, json
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
def _guard():
    path = ROOT / "tools" / "reflex_runtime_policy_guard.py"
    spec = importlib.util.spec_from_file_location("guard", path)
    mod = importlib.util.module_from_spec(spec)
    assert spec and spec.loader
    spec.loader.exec_module(mod)
    return mod
def test_policy_locked():
    p = json.loads((ROOT/"config"/"reflex_runtime_policy.json").read_text(encoding="utf-8"))
    assert _guard().validate_policy(p) == []
def test_dev_command_accepted():
    cmd = "python -m reflex run --env dev --backend-host 0.0.0.0 --backend-port 8000 --frontend-port 3000"
    assert _guard().validate_command(cmd) == []
def test_prod_single_port_rejected():
    cmd = "python -m reflex run --env prod --single-port --frontend-port 3055 --backend-port 3055"
    assert _guard().validate_command(cmd)

