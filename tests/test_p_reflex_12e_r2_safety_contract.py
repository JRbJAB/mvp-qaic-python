from __future__ import annotations

from pathlib import Path


GENERATED_SOURCE_PATHS = [
    Path("mvp_qaic_reflex_ui") / "tracker_auto_update.py",
    Path("mvp_qaic_reflex_ui") / "svg_schema_viewer.py",
    Path("mvp_qaic_reflex_ui") / "auto_update_trackers_page.py",
    Path("mvp_qaic_reflex_ui") / "mission_control_auto_update_panel.py",
]

# Action markers only. Required negative safety flags such as
# NO_BROKER_ORDER_SIZING must remain allowed and asserted separately.
FORBIDDEN_ACTION_MARKERS = [
    "requests.post(",
    "requests.get(",
    "httpx.",
    "urlopen(",
    "place_order",
    "create_order",
    "broker_order",
    "auto_sizing",
    "clasp push",
    "bq query",
]

ALLOWED_NEGATIVE_SAFETY_TOKENS = [
    "no_broker_order_sizing",
]


def _without_allowed_negative_safety_tokens(text: str) -> str:
    lowered = text.lower()
    for token in ALLOWED_NEGATIVE_SAFETY_TOKENS:
        lowered = lowered.replace(token, "")
    return lowered


def test_p12e_r2_generated_sources_do_not_contain_live_action_markers() -> None:
    repo = Path.cwd()
    for rel_path in GENERATED_SOURCE_PATHS:
        path = repo / rel_path
        assert path.exists(), f"missing generated source: {path}"
        scan_text = _without_allowed_negative_safety_tokens(path.read_text(encoding="utf-8"))
        for marker in FORBIDDEN_ACTION_MARKERS:
            assert marker not in scan_text, f"{marker} found in {path}"


def test_p12e_r2_tracker_keeps_required_negative_safety_flags() -> None:
    tracker = Path("mvp_qaic_reflex_ui/tracker_auto_update.py").read_text(encoding="utf-8")
    required = [
        "NO_PUBLIC_DEPLOY",
        "NO_LIVE_ACTION",
        "NO_BROKER_ORDER_SIZING",
        "NO_SHEET_WRITE",
        "NO_BIGQUERY_WRITE",
        "HUMAN_REVIEW_ONLY",
    ]
    for flag in required:
        assert flag in tracker
