from __future__ import annotations

import argparse
import csv
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Mapping, Sequence

from mvp_qaic_py.image_manual_transcription_bridge import discover_latest_p128_dir

VERSION = "MVP_QAIC_P131_REAL_IMAGE_TRANSCRIPTION_OPERATOR_TEST_0_1_0_SAFE"

SAFETY_MARKERS = (
    "LOCAL_ONLY",
    "REAL_OPERATOR_TEST_ONLY",
    "HUMAN_REVIEW_ONLY",
    "MANUAL_TRANSCRIPTION_REQUIRED",
    "NO_OCR_CLAIM",
    "NO_AUTOMATED_VISUAL_EXTRACTION",
    "NO_INVENTED_PORTFOLIO_DATA",
    "NO_INDEX_EDIT",
    "NO_CLASP",
    "NO_APPS_SCRIPT_EXECUTION",
    "NO_SHEET_WRITE",
    "NO_PUBLIC_DEPLOY",
    "NO_BROKER",
    "NO_ORDER",
    "NO_CANCEL",
    "NO_REPLACE_ORDER",
    "NO_AUTO_SIZING",
    "NO_AUTO_APPLY_GEM_RESPONSE",
    "NO_REVOLUTX_REAL_ACCESS_FROM_MVP",
)

OUTPUT_FILES = (
    "P131_OPERATOR_TEST_GUIDE.md",
    "P131_REAL_IMAGE_INBOX/README.md",
    "P131_REAL_IMAGE_INBOX/.gitkeep",
    "P131_FILLED_TRANSCRIPTION_OUTBOX/P131_MANUAL_TRANSCRIPTION_REAL_TEST.md",
    "P131_FILLED_TRANSCRIPTION_OUTBOX/P131_SAFE_FAKE_EXAMPLE_NOT_REAL.md",
    "P131_OPERATOR_COMMANDS.md",
    "P131_REAL_TEST_CHECKLIST.csv",
    "P131_REAL_TEST_CONTRACT.json",
    "P131_REAL_TEST_MANIFEST.json",
    "P131_README.md",
)

P130_EXPORT_PATTERN = "P130_OPERATOR_E2E_IMAGE_PROMPT_LOOP_*"


@dataclass(frozen=True)
class RealImageTranscriptionOperatorTestRequest:
    output_dir: str | Path
    exports_dir: str | Path | None = None
    p128_dir: str | Path | None = None
    p130_dir: str | Path | None = None
    run_id: str = "P131-REAL-IMAGE-TRANSCRIPTION-OPERATOR-TEST"
    generated_at_utc: str | None = None
    notes: str | None = None


def _write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text.rstrip() + "\n", encoding="utf-8")


def _write_json(path: Path, payload: Mapping[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )


def discover_p130_dirs(exports_dir: str | Path) -> list[Path]:
    root = Path(exports_dir)
    if not root.exists():
        return []
    candidates = [path for path in root.glob(P130_EXPORT_PATTERN) if path.is_dir()]
    return sorted(
        candidates,
        key=lambda path: (path.stat().st_mtime_ns, str(path)),
        reverse=True,
    )


def discover_latest_p130_dir(exports_dir: str | Path) -> Path | None:
    dirs = discover_p130_dirs(exports_dir)
    return dirs[0] if dirs else None


def _resolve_p128_dir(p128_dir: str | Path | None, exports_dir: Path | None) -> Path | None:
    if p128_dir:
        return Path(p128_dir)
    if exports_dir:
        return discover_latest_p128_dir(exports_dir)
    return None


def _resolve_p130_dir(p130_dir: str | Path | None, exports_dir: Path | None) -> Path | None:
    if p130_dir:
        return Path(p130_dir)
    if exports_dir:
        return discover_latest_p130_dir(exports_dir)
    return None


def _write_checklist(path: Path) -> None:
    rows = [
        (
            "1",
            "Put real screenshot/image in P131_REAL_IMAGE_INBOX",
            "YES",
            "LOCAL_ONLY",
            "OPERATOR_ACTION",
        ),
        (
            "2",
            "Fill P131_MANUAL_TRANSCRIPTION_REAL_TEST.md manually",
            "YES",
            "MANUAL_TRANSCRIPTION_REQUIRED",
            "OPERATOR_ACTION",
        ),
        ("3", "Do not use OCR or automated extraction", "YES", "NO_OCR_CLAIM", "READY"),
        ("4", "Run P130 with --manual-transcription-path", "YES", "HUMAN_REVIEW_ONLY", "READY"),
        (
            "5",
            "Confirm E2E_READY_FOR_GEM_COPY_PASTE before GEM",
            "YES",
            "NO_AUTO_APPLY_GEM_RESPONSE",
            "REQUIRED",
        ),
        (
            "6",
            "Then paste GEM answer manually and run P125/P126",
            "YES",
            "NO_SHEET_WRITE",
            "OPERATOR_ACTION",
        ),
    ]
    fields = ["step", "name", "required", "safety", "status"]
    with path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        for step, name, required, safety, status in rows:
            writer.writerow(
                {
                    "step": step,
                    "name": name,
                    "required": required,
                    "safety": safety,
                    "status": status,
                }
            )


def build_real_test_contract() -> dict[str, Any]:
    return {
        "contract": "P131_REAL_IMAGE_TRANSCRIPTION_OPERATOR_TEST",
        "version": VERSION,
        "status": "REAL_OPERATOR_TEST_CONTRACT_READY",
        "purpose": "Prepare a local real-image operator test workspace that can feed P130 with a human-filled transcription.",
        "allowed": [
            "place real screenshot/image locally",
            "fill manual transcription manually",
            "run P130 with explicit manual transcription path",
            "inspect P130 status before GEM",
            "copy/paste GEM manually",
        ],
        "forbidden": [
            "ocr_claim",
            "automated_visual_extraction",
            "invented_portfolio_data",
            "apps_script_execution",
            "sheet_write",
            "clasp_push",
            "public_deploy",
            "broker_execution",
            "order_execution",
            "auto_sizing",
            "auto_apply_gem_response",
            "revolutx_real_access_from_mvp",
        ],
        "manual_transcription_required": True,
        "no_ocr_claim": True,
        "no_automated_visual_extraction": True,
        "no_invented_portfolio_data": True,
        "safety_markers": list(SAFETY_MARKERS),
        "outputs": list(OUTPUT_FILES),
    }


def _guide(p128_dir: Path | None, p130_dir: Path | None) -> str:
    return f"""
# P131 Real Image Transcription Operator Test

## Goal

Run a real local operator test with a screenshot/image, but keep all interpretation human-reviewed.

## Source context

Latest P128:
`{p128_dir or ""}`

Latest P130:
`{p130_dir or ""}`

## Steps

1. Put the real portfolio screenshot/image in `P131_REAL_IMAGE_INBOX`.
2. Open `P131_FILLED_TRANSCRIPTION_OUTBOX/P131_MANUAL_TRANSCRIPTION_REAL_TEST.md`.
3. Fill symbol, quantity, value_eur, unclear rows, and notes manually.
4. Run the P130 command from `P131_OPERATOR_COMMANDS.md`.
5. Continue only if P130 returns `E2E_READY_FOR_GEM_COPY_PASTE`.

## Hard stop

If P130 remains `E2E_WAITING_FOR_MANUAL_TRANSCRIPTION`, the transcription is still incomplete.
If P130 returns `E2E_BLOCKED_REVIEW_REQUIRED`, resolve blockers before GEM.

## Boundaries

No OCR.
No automated visual extraction.
No invented portfolio data.
No Sheets write.
No broker, no order, no sizing.
"""


def _inbox_readme() -> str:
    return """
# P131 Real Image Inbox

Place the real portfolio screenshot/image here.

Do not commit private screenshots unless intentionally accepted by the operator.
This folder is for local operator testing.
"""


def _manual_transcription_template() -> str:
    return """
# P131 Manual Transcription Real Test

Fill this file manually from the screenshot/image.

source_image_file:
transcribed_by:
transcription_datetime_local:
portfolio_platform_visible:
confidence: REVIEW

## Assets

ASSET_1:
- symbol:
- quantity:
- value_eur:
- source: manual_image_transcription
- confidence: REVIEW
- notes:

ASSET_2:
- symbol:
- quantity:
- value_eur:
- source: manual_image_transcription
- confidence: REVIEW
- notes:

ASSET_3:
- symbol:
- quantity:
- value_eur:
- source: manual_image_transcription
- confidence: REVIEW
- notes:

## Missing / unclear data

- missing_current_prices:
- missing_timestamp:
- unclear_rows:
- unclear_values:
- operator_notes:

## Safety

HUMAN_REVIEW_ONLY
MANUAL_TRANSCRIPTION_REQUIRED
NO_OCR_CLAIM
NO_AUTOMATED_VISUAL_EXTRACTION
NO_INVENTED_PORTFOLIO_DATA
NO_BROKER
NO_ORDER
NO_SIZING
"""


def _safe_fake_example() -> str:
    return """
# P131 Safe Fake Example — Not Real Portfolio Data

Do not use this as your portfolio.
This is only a format example.

ASSET_1:
- symbol: BTC
- quantity: 0.010
- value_eur: 650
- source: manual_image_transcription
- confidence: REVIEW
- notes: FAKE_EXAMPLE_NOT_REAL

ASSET_2:
- symbol: ETH
- quantity: 0.100
- value_eur: 300
- source: manual_image_transcription
- confidence: REVIEW
- notes: FAKE_EXAMPLE_NOT_REAL

Safety:
NO_INVENTED_PORTFOLIO_DATA means do not use these fake values for a real run.
"""


def _operator_commands(
    output_dir: Path, transcription_path: Path, p130_rerun_dir: Path, exports_dir: Path | None
) -> str:
    exports_text = str(exports_dir) if exports_dir else "<MVP_QAIC_PY>\\05_EXPORTS"
    return f"""
# P131 Operator Commands

## 1. Fill manual transcription

Open and fill:

```text
{transcription_path}
```

## 2. Rerun P130 with explicit manual transcription

```powershell
python -m mvp_qaic_py.operator_e2e_image_prompt_loop --output-dir "{p130_rerun_dir}" --exports-dir "{exports_text}" --manual-transcription-path "{transcription_path}" --run-id P131-P130-RERUN
```

## 3. Expected P130 status after valid manual fill

```text
E2E_READY_FOR_GEM_COPY_PASTE
```

## 4. Then follow commands generated inside the P130 rerun folder

Open:

```text
{p130_rerun_dir}
```

## 5. Safety

LOCAL_ONLY / HUMAN_REVIEW_ONLY / NO_OCR_CLAIM / NO_AUTOMATED_VISUAL_EXTRACTION / NO_INVENTED_PORTFOLIO_DATA / NO_SHEET_WRITE / NO_BROKER / NO_ORDER / NO_SIZING / NO_AUTO_APPLY_GEM_RESPONSE.

## Workspace

```text
{output_dir}
```
"""


def _readme() -> str:
    return """
# P131 Real Image Transcription Operator Test

This pack creates a local workspace for a real screenshot/image test.

It does not process the image.
It does not OCR.
It does not extract values automatically.
The operator must manually fill the transcription file.
"""


def write_real_image_transcription_operator_test(
    request: RealImageTranscriptionOperatorTestRequest,
) -> dict[str, Any]:
    out = Path(request.output_dir)
    out.mkdir(parents=True, exist_ok=True)

    exports_dir = Path(request.exports_dir) if request.exports_dir else None
    p128_dir = _resolve_p128_dir(request.p128_dir, exports_dir)
    p130_dir = _resolve_p130_dir(request.p130_dir, exports_dir)

    image_inbox = out / "P131_REAL_IMAGE_INBOX"
    transcription_outbox = out / "P131_FILLED_TRANSCRIPTION_OUTBOX"
    p130_rerun_dir = out / "P131_P130_RERUN_AFTER_REAL_TRANSCRIPTION"
    image_inbox.mkdir(parents=True, exist_ok=True)
    transcription_outbox.mkdir(parents=True, exist_ok=True)
    p130_rerun_dir.mkdir(parents=True, exist_ok=True)

    guide_path = out / "P131_OPERATOR_TEST_GUIDE.md"
    inbox_readme_path = image_inbox / "README.md"
    inbox_gitkeep_path = image_inbox / ".gitkeep"
    transcription_path = transcription_outbox / "P131_MANUAL_TRANSCRIPTION_REAL_TEST.md"
    fake_example_path = transcription_outbox / "P131_SAFE_FAKE_EXAMPLE_NOT_REAL.md"
    commands_path = out / "P131_OPERATOR_COMMANDS.md"
    checklist_path = out / "P131_REAL_TEST_CHECKLIST.csv"
    contract_path = out / "P131_REAL_TEST_CONTRACT.json"
    manifest_path = out / "P131_REAL_TEST_MANIFEST.json"
    readme_path = out / "P131_README.md"

    _write(guide_path, _guide(p128_dir, p130_dir))
    _write(inbox_readme_path, _inbox_readme())
    _write(inbox_gitkeep_path, "")
    _write(transcription_path, _manual_transcription_template())
    _write(fake_example_path, _safe_fake_example())
    _write(commands_path, _operator_commands(out, transcription_path, p130_rerun_dir, exports_dir))
    _write_checklist(checklist_path)
    _write_json(contract_path, build_real_test_contract())
    _write(readme_path, _readme())

    manifest = {
        "status": "REAL_IMAGE_TRANSCRIPTION_OPERATOR_TEST_READY",
        "step": "P131_REAL_IMAGE_TRANSCRIPTION_OPERATOR_TEST",
        "version": VERSION,
        "run_id": request.run_id,
        "generated_at_utc": request.generated_at_utc,
        "output_dir": str(out),
        "exports_dir": str(exports_dir) if exports_dir else None,
        "p128_dir": str(p128_dir) if p128_dir else None,
        "p128_dir_valid": bool(p128_dir and str(p128_dir) != "G" and p128_dir.exists()),
        "p130_dir": str(p130_dir) if p130_dir else None,
        "p130_dir_valid": bool(p130_dir and str(p130_dir) != "G" and p130_dir.exists()),
        "image_inbox": str(image_inbox),
        "manual_transcription_path": str(transcription_path),
        "p130_rerun_dir": str(p130_rerun_dir),
        "expected_after_manual_fill": "E2E_READY_FOR_GEM_COPY_PASTE",
        "ready_for_real_operator_test": True,
        "human_review_only": True,
        "manual_transcription_required": True,
        "no_ocr_claim": True,
        "no_automated_visual_extraction": True,
        "no_invented_portfolio_data": True,
        "no_sheet_write": True,
        "no_auto_apply_gem_response": True,
        "no_order_no_sizing": True,
        "safety_markers": list(SAFETY_MARKERS),
        "files": [
            str(guide_path),
            str(inbox_readme_path),
            str(inbox_gitkeep_path),
            str(transcription_path),
            str(fake_example_path),
            str(commands_path),
            str(checklist_path),
            str(contract_path),
            str(readme_path),
        ],
        "next": "RUN_REAL_OPERATOR_TEST_FILL_TRANSCRIPTION_THEN_P132_REAL_GEM_COPY_PASTE_TEST",
    }
    _write_json(manifest_path, manifest)
    manifest["files"].append(str(manifest_path))
    return manifest


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        prog="python -m mvp_qaic_py.real_image_transcription_operator_test",
        description="Create P131 real image manual transcription operator test workspace.",
    )
    parser.add_argument("--output-dir", required=True)
    parser.add_argument("--exports-dir")
    parser.add_argument("--p128-dir")
    parser.add_argument("--p130-dir")
    parser.add_argument("--run-id", default="P131-REAL-IMAGE-TRANSCRIPTION-OPERATOR-TEST")
    parser.add_argument("--generated-at-utc")
    parser.add_argument("--notes")
    return parser.parse_args(argv)


def main(argv: Sequence[str] | None = None) -> int:
    args = parse_args(argv)
    result = write_real_image_transcription_operator_test(
        RealImageTranscriptionOperatorTestRequest(
            output_dir=args.output_dir,
            exports_dir=args.exports_dir,
            p128_dir=args.p128_dir,
            p130_dir=args.p130_dir,
            run_id=args.run_id,
            generated_at_utc=args.generated_at_utc,
            notes=args.notes,
        )
    )
    print(result["status"])
    print(result["ready_for_real_operator_test"])
    print(result["p128_dir_valid"])
    print(result["p130_dir_valid"])
    print(result["manual_transcription_path"])
    print(result["output_dir"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
