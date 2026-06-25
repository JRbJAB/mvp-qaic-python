from pathlib import Path

from mvp_qaic_py.p173_nicegui_private_local_runner import (
    build_p173_baseline_frame_audit_plan,
)


def test_p219e1_r3_p173_is_baseline_frame_not_final_ui() -> None:
    payload = build_p173_baseline_frame_audit_plan(".")

    assert payload["STATUS"] == "OK_P219E1_R3_P173_BASELINE_FRAME_AUDIT_PLAN_READY"
    assert payload["baseline_frame"] is True
    assert payload["official_final_ui"] is False
    assert payload["visual_source"] == "mvp_qaic_py/p173_nicegui_private_local_runner.py"
    assert payload["private_admin_app_visual_source"] is False
    assert "/base-python" in payload["quick_access_routes"]
    assert "/google-sheets" in payload["quick_access_routes"]
    assert " --serve-private" in payload["launch_command"]
    assert payload["broker"] is False
    assert payload["order"] is False
    assert payload["sizing"] is False


def test_p219e1_r3_p173_source_contains_audit_marker() -> None:
    source = Path("mvp_qaic_py/p173_nicegui_private_local_runner.py").read_text(encoding="utf-8")

    assert "P219E1_R3_P173_BASELINE_FRAME_ANCHORLESS_MARKER" in source
    assert "P173_BASELINE_FRAME_NOT_FINAL_UI" in source
    assert "build_p173_baseline_frame_audit_plan" in source
