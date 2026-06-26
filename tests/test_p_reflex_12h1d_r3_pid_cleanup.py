from __future__ import annotations

from pathlib import Path


def test_p12h1d_r3_stop_start_do_not_use_reserved_pid_variable() -> None:
    for rel in [
        "scripts/STOP_REFLEX_LOCAL_SAFE.ps1",
        "scripts/START_REFLEX_LOCAL_SAFE.ps1",
    ]:
        text = Path(rel).read_text(encoding="utf-8")
        assert "foreach ($pid in $pids)" not in text
        assert "foreach ($listenerPid in $pids)" in text
        assert "Get-Process -Id $listenerPid" in text
        assert "Stop-Process -Id $listenerPid" in text


def test_p12h1d_r3_start_still_syncs_repo_source_to_runtime() -> None:
    text = Path("scripts/START_REFLEX_LOCAL_SAFE.ps1").read_text(encoding="utf-8")
    assert "SYNC REPO SOURCE TO RUNTIME" in text
    assert '$syncDirs = @("mvp_qaic_reflex_ui", "docs")' in text
    assert "SYNCED_DIR=$dir" in text
