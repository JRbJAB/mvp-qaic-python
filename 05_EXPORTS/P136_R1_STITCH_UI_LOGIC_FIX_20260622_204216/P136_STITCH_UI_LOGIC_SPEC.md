# P136-R1 — Stitch UI Logic Spec

Status: `STITCH_UI_BLUEPRINT_READY`
Handoff mode: `LOCAL_SPEC_ONLY`
Runtime cible: `NiceGUI local private`
Selected GEM: `GEM_GENERAL_REVIEW`

## Screens

### prompt_cockpit — MVP QAIC — GEM Portfolio Prompt Cockpit

Préparer le prompt, choisir le GEM actif, copier vers GEM et suivre les garde-fous.

- `header_status_badges`
- `active_gem_select`
- `prompt_copy_panel`
- `gemini_open_button`
- `safety_guardrails_panel`

### response_import — P136 — Réponse GEM réelle

Importer une réponse GEM depuis fichier local et préparer le P133 gate.

- `response_file_status`
- `response_text_preview`
- `p133_command_preview`
- `human_review_warning`

### prompt_corrections — Corrections prompts

Lister les corrections prompts candidates avant application future.

- `prompt_corrections_table`
- `priority_badges`
- `scope_filter`
- `next_action_panel`

## Forbidden behaviors

- `no_public_deploy`
- `no_tunnel`
- `no_broker`
- `no_order`
- `no_sizing`
- `no_auto_apply`
- `no_revolutx_real_access_from_mvp`
