# ruff: noqa: E402
from __future__ import annotations

import argparse
import json
from datetime import datetime
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from mvp_qaic_reflex_ui.common.tracker_ui_kit import (
    TrackerItem,
    render_preview_page,
    tracker_items_from_phase_dicts,
)


def _load_phases() -> list[dict[str, object]]:
    tracker_path = ROOT / "docs" / "dev_tracking" / "DEV_LIFECYCLE_TRACKER.json"
    data = json.loads(tracker_path.read_text(encoding="utf-8"))
    phases = data.get("phases", [])
    if isinstance(phases, dict):
        phases = list(phases.values())
    return [p for p in phases if isinstance(p, dict)]


def _cdc_items() -> list[TrackerItem]:
    return [
        TrackerItem(
            item_id="cdc_route_dev_tracking",
            title="/dev-tracking route",
            status="DONE",
            percent=100,
            description="Dev tracking route registered for operator cockpit.",
            route="/dev-tracking",
            priority="P0",
        ),
        TrackerItem(
            item_id="cdc_route_cdc_dev_tracker",
            title="/cdc-dev-tracker route",
            status="DONE",
            percent=100,
            description="CDC Dev Tracker route registered.",
            route="/cdc-dev-tracker",
            priority="P0",
        ),
        TrackerItem(
            item_id="cdc_route_cdc_tracker",
            title="/cdc-tracker route",
            status="DONE",
            percent=100,
            description="CDC Tracker route registered.",
            route="/cdc-tracker",
            priority="P0",
        ),
        TrackerItem(
            item_id="cdc_source_v25_delivery_tracker",
            title="V25_CDC_DELIVERY_TRACKER source contract",
            status="DONE",
            percent=100,
            description="CDC source data contract is referenced by architecture docs.",
            priority="P0",
        ),
        TrackerItem(
            item_id="cdc_visual_oracle",
            title="Migration Tracker visual oracle",
            status="ACTIVE",
            percent=70,
            description="Preview must match Migration Tracker visual semantics.",
            priority="P0",
        ),
        TrackerItem(
            item_id="cdc_browser_runtime_gate",
            title="Browser/runtime visual proof",
            status="BLOCKED",
            percent=15,
            description="Blocked until Reflex frontend runtime is proven.",
            priority="P0",
        ),
    ]


def render_preview(out_dir: Path) -> Path:
    out_dir.mkdir(parents=True, exist_ok=True)
    phases = _load_phases()
    dev_items = tracker_items_from_phase_dicts(phases)
    cdc_items = _cdc_items()
    html = render_preview_page(
        title="MVP QAIC CDC Dev Tracker - UI Common Tracker Kit Preview",
        cdc_items=cdc_items,
        dev_items=dev_items,
        generated_at=datetime.now().isoformat(timespec="seconds"),
        source_note="DEV_LIFECYCLE_TRACKER.json",
    )
    out_file = out_dir / "tracker_ui_common_preview.html"
    out_file.write_text(html, encoding="utf-8")
    audit = {
        "preview_file": str(out_file),
        "phase_count": len(dev_items),
        "cdc_step_count": len(cdc_items),
        "visual_oracle": "migration_tracker",
        "render_types": [
            "migration_tracker_reference",
            "migration_tracker_oracle",
            "runtime_browser_visual_smoke_future",
            "cdc_dev_tracker",
            "cdc_tracker",
            "dev_tracker",
            "tool_registry_cdc",
            "tool_registry_tracker",
        ],
        "requires_browser_runtime_before_deploy": True,
    }
    (out_dir / "tracker_ui_common_preview_audit.json").write_text(
        json.dumps(audit, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )
    return out_file


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", required=True)
    args = parser.parse_args()
    out_file = render_preview(Path(args.out))
    print("PREVIEW_FILE=" + str(out_file))
    print("STATUS=MVP_TRACKER_UI_COMMON_PREVIEW_READY")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
