from __future__ import annotations
import json
from nicegui import ui

MODEL = json.loads('{\n  "generated_at_utc": "2026-06-23T00:00:00Z",\n  "issue_type_counts": {\n    "PROMPT_NEXT_TEST": 1,\n    "REVIEW": 1\n  },\n  "items": [\n    {\n      "apply_now": false,\n      "blocked_actions": [\n        "SHEET_WRITE",\n        "AUTO_APPLY",\n        "ORDER",\n        "SIZING"\n      ],\n      "human_review_required": true,\n      "issue_type": "REVIEW",\n      "priority": "P1",\n      "queue_id": "P146-REVIEW-001",\n      "source": "P145_REVIEW_QUEUE",\n      "suggested_action": "Lire la réponse, valider l\'extraction, puis préparer le prochain test réel.",\n      "title": "GEM response accepted for human review"\n    },\n    {\n      "apply_now": false,\n      "blocked_actions": [\n        "SHEET_WRITE",\n        "AUTO_APPLY",\n        "ORDER",\n        "SIZING"\n      ],\n      "human_review_required": true,\n      "issue_type": "PROMPT_NEXT_TEST",\n      "priority": "P2",\n      "queue_id": "P146-PROMPT-002",\n      "source": "P144_WORKFLOW",\n      "suggested_action": "Choisir un prompt validé et consulter son contenu source.",\n      "title": "Next prompt workflow: 📘 PROMPT_LIBRARY"\n    }\n  ],\n  "next": "P147_OPERATOR_POLISH",\n  "priority_counts": {\n    "P1": 1,\n    "P2": 1\n  },\n  "queue_item_count": 2,\n  "run_id": "P146-CORRECTION-QUEUE-UI-20260623",\n  "safety": {\n    "apply_requires_explicit_future_go": true,\n    "apps_script_execution": false,\n    "auto_apply_gem_response": false,\n    "broker": false,\n    "clasp_push": false,\n    "google_sheets_write": false,\n    "human_review_required": true,\n    "live_google_sheets_read": false,\n    "order": false,\n    "public_deploy": false,\n    "sizing": false,\n    "source": "P145_LOCAL_GEM_REVIEW_AND_P144_WORKFLOW"\n  },\n  "source_p144_model_path": "G:\\\\Mon Drive\\\\👥 JULIEN [Perso]\\\\📈 Trading JRb\\\\Solutions & Dev (Trading JRb)\\\\MVP_QAIC_PY\\\\05_EXPORTS\\\\P144_PROMPT_COCKPIT_WORKFLOWS_20260623_124209\\\\P144_PROMPT_WORKFLOW_MODEL.json",\n  "source_p144_status": "P144_PROMPT_COCKPIT_WORKFLOWS_RENDERED_LOCAL_READONLY",\n  "source_p145_payload_path": "G:\\\\Mon Drive\\\\👥 JULIEN [Perso]\\\\📈 Trading JRb\\\\Solutions & Dev (Trading JRb)\\\\MVP_QAIC_PY\\\\05_EXPORTS\\\\P145_GEM_RESPONSE_IMPORT_E2E_20260623_124938\\\\P145_GEM_RESPONSE_IMPORT_PAYLOAD.json",\n  "source_p145_status": "P145_GEM_RESPONSE_IMPORT_E2E_VALIDATED_LOCAL_REVIEW",\n  "status": "P146_CORRECTION_QUEUE_UI_RENDERED_LOCAL_REVIEW_ONLY",\n  "ui_policy": {\n    "apply_button_enabled": false,\n    "auto_apply_enabled": false,\n    "export_changeset_enabled": true,\n    "review_only": true,\n    "sheet_write_enabled": false\n  },\n  "version": "MVP_QAIC_P146_CORRECTION_QUEUE_UI_1.0.0_SAFE"\n}')

@ui.page('/')
def index():
    ui.label('MVP QAIC — Correction Queue').classes('text-h4')
    ui.label('Review only — no Sheet write / no auto apply / no broker').classes('text-caption')
    with ui.row().classes('q-gutter-sm q-mt-md'):
        ui.badge(f"items {MODEL['queue_item_count']}")
        ui.badge('review only')
        ui.badge('apply disabled')
    for item in MODEL['items']:
        with ui.card().classes('q-mt-md'):
            ui.label(item['title']).classes('text-subtitle1')
            ui.label(item['suggested_action']).classes('text-body2')
            with ui.row().classes('q-gutter-xs q-mt-sm'):
                ui.badge(item['priority'])
                ui.badge(item['issue_type'])
                ui.badge(item['source'])
            ui.label('Blocked: ' + ', '.join(item['blocked_actions'])).classes('text-caption q-mt-sm')

if __name__ in {'__main__', '__mp_main__'}:
    ui.run(host='127.0.0.1', port=8088, reload=False, show=True)
