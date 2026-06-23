from __future__ import annotations
import json
from nicegui import ui

PAYLOAD = json.loads('{\n  "fixture_used": true,\n  "gem_response_source_path": "BUILTIN_P145_FIXTURE",\n  "generated_at_utc": "2026-06-23T00:00:00Z",\n  "next": "P146_CORRECTION_QUEUE_UI",\n  "raw_text_length": 718,\n  "response_payload": {\n    "assets": [\n      {\n        "allocation_pct": 63.59,\n        "pnl": -117.69,\n        "symbol": "BTC",\n        "value": 416.92\n      },\n      {\n        "allocation_pct": 30.31,\n        "pnl": 0.06,\n        "symbol": "USDC",\n        "value": 198.75\n      },\n      {\n        "allocation_pct": 6.1,\n        "pnl": 0.0,\n        "symbol": "CASH",\n        "value": 39.99\n      }\n    ],\n    "blockers": [\n      "HUMAN_REVIEW_REQUIRED",\n      "NO_AUTO_APPLY"\n    ],\n    "human_review_required": true,\n    "image_used": true,\n    "no_order_no_sizing": true,\n    "notes_fr": "Fixture locale P145 pour valider le chemin import GEM sans ordre ni sizing.",\n    "portfolio_total_value": 655.66,\n    "reference_currency": "USD",\n    "source_type": "fixture",\n    "status": "REVIEW_REQUIRED"\n  },\n  "review_queue_item": {\n    "allowed_actions": [\n      "HUMAN_REVIEW",\n      "PROMPT_CORRECTION",\n      "SAVE_LOCAL_REPORT"\n    ],\n    "blocked_actions": [\n      "ORDER",\n      "SIZING",\n      "AUTO_APPLY",\n      "SHEET_WRITE"\n    ],\n    "decision_required": "ACCEPT_FOR_ANALYSIS_OR_REJECT_AND_CORRECT_PROMPT",\n    "review_id": "P145-GEM-RESPONSE-REVIEW-001",\n    "status": "REVIEW_REQUIRED"\n  },\n  "run_id": "P145-GEM-RESPONSE-IMPORT-E2E-20260623",\n  "safety": {\n    "apps_script_execution": false,\n    "auto_apply_gem_response": false,\n    "broker": false,\n    "clasp_push": false,\n    "google_sheets_write": false,\n    "human_review_required": true,\n    "live_google_sheets_read": false,\n    "order": false,\n    "public_deploy": false,\n    "sizing": false,\n    "source": "LOCAL_GEM_RESPONSE_FILE_OR_FIXTURE"\n  },\n  "source_p144_model_path": "G:\\\\Mon Drive\\\\👥 JULIEN [Perso]\\\\📈 Trading JRb\\\\Solutions & Dev (Trading JRb)\\\\MVP_QAIC_PY\\\\05_EXPORTS\\\\P144_PROMPT_COCKPIT_WORKFLOWS_20260623_124209\\\\P144_PROMPT_WORKFLOW_MODEL.json",\n  "source_p144_status": "P144_PROMPT_COCKPIT_WORKFLOWS_RENDERED_LOCAL_READONLY",\n  "status": "P145_GEM_RESPONSE_IMPORT_E2E_VALIDATED_LOCAL_REVIEW",\n  "validation": {\n    "blockers": [],\n    "human_review_required": true,\n    "no_auto_apply": true,\n    "no_order_no_sizing": true,\n    "status": "VALIDATED_FOR_HUMAN_REVIEW",\n    "warnings": []\n  },\n  "version": "MVP_QAIC_P145_GEM_RESPONSE_IMPORT_E2E_1.0.0_SAFE",\n  "workflow_step_count": 11\n}')

@ui.page('/')
def index():
    ui.label('MVP QAIC — GEM Response Review').classes('text-h4')
    ui.label('Human review only — no order / no sizing / no auto apply').classes('text-caption')
    with ui.row().classes('q-gutter-sm q-mt-md'):
        ui.badge(PAYLOAD['status'])
        ui.badge(PAYLOAD['validation']['status'])
        ui.badge('fixture' if PAYLOAD['fixture_used'] else 'real file')
    ui.separator().classes('q-my-md')
    ui.label('Validation blockers').classes('text-subtitle1')
    for blocker in PAYLOAD['validation'].get('blockers', []):
        ui.label('BLOCKER: ' + blocker).classes('text-negative')
    ui.label('Warnings').classes('text-subtitle1 q-mt-md')
    for warning in PAYLOAD['validation'].get('warnings', []):
        ui.label('WARNING: ' + warning)
    ui.separator().classes('q-my-md')
    ui.json_editor({'content': {'json': PAYLOAD.get('response_payload')}}).classes('w-full')

if __name__ in {'__main__', '__mp_main__'}:
    ui.run(host='127.0.0.1', port=8088, reload=False, show=True)
