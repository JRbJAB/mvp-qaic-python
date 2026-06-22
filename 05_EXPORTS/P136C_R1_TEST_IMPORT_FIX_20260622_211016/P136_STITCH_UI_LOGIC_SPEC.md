# P136C — Stitch Operator UI Spec

Status: `STITCH_UI_BLUEPRINT_READY`
Handoff mode: `LOCAL_SPEC_ONLY`
Runtime cible: `NiceGUI local private`
Selected GEM: `GEM_GENERAL_REVIEW`

## Screens

### prompt_cockpit — Prompt

Préparer le prompt, choisir le GEM actif, copier vers GEM et suivre les garde-fous.

- `active_gem_select`
- `prompt_copy_panel`
- `gemini_open_button`
- `safety_guardrails_panel`

### response_import — Réponse GEM

Coller et sauvegarder localement une réponse GEM réelle.

- `response_file_status`
- `response_textarea`
- `save_response_to_local_file_button`
- `response_hash_status`

### p133_gate — P133 Gate

Préparer la commande locale de validation P133 sans exécution automatique.

- `p133_command_preview`
- `copy_p133_command_button`
- `open_export_folder_button`
- `human_review_warning`

### prompt_corrections — Corrections

Lister les corrections prompts candidates avant application future.

- `prompt_corrections_table`
- `priority_badges`
- `scope_filter`
- `next_action_panel`

### audit — Audit

Masquer par défaut les JSON et specs techniques, accessibles uniquement si nécessaire.

- `collapsed_json_debug`
- `stitch_spec_collapsed`
- `safety_markers_collapsed`

## Layout rules

- `density`: `operator_dense_but_readable`
- `theme`: `dark_professional`
- `primary_layout`: `left_workflow_center_tabs_right_decision`
- `no_empty_rows`: `True`
- `badges_for_safety`: `True`
- `monospace_for_prompt_and_json`: `True`
- `json_debug_collapsed_by_default`: `True`

## Forbidden behaviors

- `no_public_deploy`
- `no_tunnel`
- `no_broker`
- `no_order`
- `no_sizing`
- `no_auto_apply`
- `no_revolutx_real_access_from_mvp`
