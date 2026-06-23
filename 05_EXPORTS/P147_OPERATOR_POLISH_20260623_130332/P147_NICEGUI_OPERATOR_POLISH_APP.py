from __future__ import annotations
import json
from nicegui import ui

MODEL = json.loads('{\n  "generated_at_utc": "2026-06-23T00:00:00Z",\n  "launch": {\n    "command": "python P147_NICEGUI_OPERATOR_POLISH_APP.py",\n    "host": "127.0.0.1",\n    "port": 8088,\n    "public_deploy": false\n  },\n  "navigation": [\n    {\n      "icon": "dashboard",\n      "label": "Dashboard",\n      "priority": "P0",\n      "route": "/"\n    },\n    {\n      "icon": "route",\n      "label": "Prompt Workflow",\n      "priority": "P0",\n      "route": "/workflow"\n    },\n    {\n      "icon": "rule",\n      "label": "Correction Queue",\n      "priority": "P0",\n      "route": "/queue"\n    },\n    {\n      "icon": "psychology",\n      "label": "GEM Review",\n      "priority": "P1",\n      "route": "/gem-review"\n    },\n    {\n      "icon": "lock",\n      "label": "Safety",\n      "priority": "P0",\n      "route": "/safety"\n    },\n    {\n      "icon": "article",\n      "label": "Prompt Library",\n      "priority": "P1",\n      "route": "/workflow/prompt-library"\n    },\n    {\n      "icon": "article",\n      "label": "Variant Control",\n      "priority": "P1",\n      "route": "/workflow/variant-control"\n    },\n    {\n      "icon": "article",\n      "label": "Context Pack",\n      "priority": "P1",\n      "route": "/workflow/context-pack"\n    },\n    {\n      "icon": "article",\n      "label": "Lexique Bridge",\n      "priority": "P1",\n      "route": "/workflow/lexique-bridge"\n    },\n    {\n      "icon": "article",\n      "label": "Ready To Copy",\n      "priority": "P1",\n      "route": "/workflow/ready-to-copy"\n    },\n    {\n      "icon": "article",\n      "label": "Run Queue",\n      "priority": "P1",\n      "route": "/workflow/run-queue"\n    },\n    {\n      "icon": "checklist",\n      "label": "Review Items",\n      "priority": "P0",\n      "route": "/queue/items"\n    }\n  ],\n  "next": "P148_SYNC_STRATEGY_READONLY",\n  "operator_cards": [\n    {\n      "card_id": "workflow_status",\n      "severity": "info",\n      "subtitle": "étapes opérateur",\n      "title": "Workflow prompt",\n      "value": "11"\n    },\n    {\n      "card_id": "queue_status",\n      "severity": "review",\n      "subtitle": "items review-only",\n      "title": "Correction queue",\n      "value": "2"\n    },\n    {\n      "card_id": "safety_status",\n      "severity": "safe",\n      "subtitle": "no write / no broker / no auto apply",\n      "title": "Safety",\n      "value": "LOCKED"\n    }\n  ],\n  "operator_shell": {\n    "default_route": "/",\n    "density": "compact",\n    "layout": "left_nav_top_status_main_cards",\n    "mode": "local_private_review_only",\n    "theme": "clean_light",\n    "title": "MVP QAIC — Prompt Operator Cockpit"\n  },\n  "queue_item_count": 2,\n  "review_policy": {\n    "apply_to_sheet_enabled": false,\n    "auto_apply_gem_response_enabled": false,\n    "broker_actions_enabled": false,\n    "copy_prompt_enabled": true,\n    "export_changeset_enabled": true,\n    "order_actions_enabled": false,\n    "save_local_review_enabled": true,\n    "sizing_enabled": false\n  },\n  "run_id": "P147-OPERATOR-POLISH-20260623",\n  "safety": {\n    "apps_script_execution": false,\n    "auto_apply_gem_response": false,\n    "broker": false,\n    "clasp_push": false,\n    "google_sheets_write": false,\n    "human_review_required": true,\n    "live_google_sheets_read": false,\n    "local_private_only": true,\n    "order": false,\n    "public_deploy": false,\n    "sizing": false,\n    "source": "P146_CORRECTION_QUEUE_AND_P144_WORKFLOW"\n  },\n  "shortcuts": [\n    {\n      "action": "open_dashboard",\n      "description": "Retour dashboard",\n      "keys": "Ctrl+1"\n    },\n    {\n      "action": "open_prompt_workflow",\n      "description": "Ouvrir workflow prompt",\n      "keys": "Ctrl+2"\n    },\n    {\n      "action": "open_correction_queue",\n      "description": "Ouvrir correction queue",\n      "keys": "Ctrl+3"\n    },\n    {\n      "action": "copy_selected_prompt",\n      "description": "Copie manuelle uniquement",\n      "keys": "Ctrl+C"\n    },\n    {\n      "action": "save_local_review",\n      "description": "Sauvegarde locale review-only",\n      "keys": "Ctrl+S"\n    },\n    {\n      "action": "clear_selection",\n      "description": "Annuler sélection",\n      "keys": "Esc"\n    }\n  ],\n  "source_p144_model_path": "G:\\\\Mon Drive\\\\👥 JULIEN [Perso]\\\\📈 Trading JRb\\\\Solutions & Dev (Trading JRb)\\\\MVP_QAIC_PY\\\\05_EXPORTS\\\\P144_PROMPT_COCKPIT_WORKFLOWS_20260623_124209\\\\P144_PROMPT_WORKFLOW_MODEL.json",\n  "source_p144_status": "P144_PROMPT_COCKPIT_WORKFLOWS_RENDERED_LOCAL_READONLY",\n  "source_p146_queue_path": "G:\\\\Mon Drive\\\\👥 JULIEN [Perso]\\\\📈 Trading JRb\\\\Solutions & Dev (Trading JRb)\\\\MVP_QAIC_PY\\\\05_EXPORTS\\\\P146_CORRECTION_QUEUE_UI_20260623_125709\\\\P146_CORRECTION_QUEUE_MODEL.json",\n  "source_p146_status": "P146_CORRECTION_QUEUE_UI_RENDERED_LOCAL_REVIEW_ONLY",\n  "status": "P147_OPERATOR_POLISH_RENDERED_LOCAL_PRIVATE",\n  "version": "MVP_QAIC_P147_OPERATOR_POLISH_1.0.0_SAFE",\n  "workflow_step_count": 11\n}')

def _badge(text: str):
    ui.badge(text).classes('q-mr-xs')

@ui.page('/')
def index():
    ui.label(MODEL['operator_shell']['title']).classes('text-h4')
    ui.label('Local private / review-only / no Sheet write / no broker').classes('text-caption')
    with ui.row().classes('q-gutter-md q-mt-md'):
        for card in MODEL['operator_cards']:
            with ui.card().classes('w-72'):
                ui.label(card['title']).classes('text-subtitle1')
                ui.label(card['value']).classes('text-h5')
                ui.label(card['subtitle']).classes('text-caption')
    ui.separator().classes('q-my-md')
    ui.label('Navigation').classes('text-h6')
    with ui.row().classes('q-gutter-sm'):
        for item in MODEL['navigation']:
            ui.link(item['label'], item['route']).classes('q-pa-sm')
    ui.separator().classes('q-my-md')
    ui.label('Shortcuts').classes('text-h6')
    for shortcut in MODEL['shortcuts']:
        ui.label(shortcut['keys'] + ' — ' + shortcut['description']).classes('text-body2')

@ui.page('/safety')
def safety():
    ui.label('Safety Locks').classes('text-h5')
    for key, value in MODEL['safety'].items():
        ui.label(f'{key}: {value}')

@ui.page('/queue')
def queue():
    ui.label('Correction Queue').classes('text-h5')
    ui.label('Apply disabled. Export/review only.').classes('text-caption')

@ui.page('/workflow')
def workflow():
    ui.label('Prompt Workflow').classes('text-h5')
    ui.label('Prompt workflow shell; data stays local/read-only.').classes('text-caption')

if __name__ in {'__main__', '__mp_main__'}:
    ui.run(host='127.0.0.1', port=8088, reload=False, show=True)
