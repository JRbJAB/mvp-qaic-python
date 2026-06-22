# P136 — Prompt Corrections Queue

Selected GEM: `GEM_GENERAL_REVIEW`

| correction_id | priority | status | scope | issue | proposed_fix |
|---|---:|---|---|---|---|
| P136_PROMPT_001 | HIGH | TODO | GEM_SELECTION | Le cockpit doit permettre le choix contrôlé du Gem actif. | Utiliser uniquement gem_id depuis ACTIVE_GEM_PROFILES. |
| P136_PROMPT_002 | HIGH | TODO | P132_R2_OUTPUT_FORMAT | Renforcer la sortie résumé lisible + JSON pretty fenced. | Ajouter un garde-fou de format dans la prochaine correction de prompt. |
| P136_PROMPT_003 | MEDIUM | TODO | IMAGE_USAGE_EVIDENCE | Rendre la preuve d'utilisation image plus visible pour human review. | Exiger un court champ/texte d'évidence image_used avant JSON. |
| P136_PROMPT_004 | MEDIUM | TODO | STITCH_UI_LOGIC | Aligner les prompts avec la logique UI Stitch/NiceGUI. | Synchroniser les écrans prompt, import réponse, P133 gate et corrections dans une spec UI unique. |

Safety: local private only, no broker, no order, no sizing, no auto apply.
