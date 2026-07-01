# MVP QAIC Prompt GEM Workflow Final Fused v0.2.6
- Version: v0.2.6
- Status: FINAL_REFERENCE_READY_HUMAN_REVIEW
- Generated: 20260630_200005
- Mode: residual final docs fusion / no live broker / no delete
## Intent
Canonical prompt, GEM workflow, response audit and prompt library reference.
## Scope and safety
- This document consolidates the selected R6 fusion inbox and residual final-doc sources.
- Older source files are not deleted. Superseded material remains traceable through R5/R6/R7/R8/R9 reports.
- Google Drive cleanup is limited to archive moves; no content was deleted.
- This is a reference document for human review and implementation continuity.

## Source manifest
1. `docs/FINAL/fusion_inbox_R6/ARCHITECTURE/🧠 DECISION_JOURNAL_USAGE_AND_PROMPT_IMPROVEMENT_LOOP_0.4.6.md` (1183 bytes, sha256 `c43d2c50957cece3...`)
2. `docs/FINAL/fusion_inbox_R6/NOTICE_UTILISATION/NOTICE_UTILISATION_MVP_QAIC_P2F_GPT_RESPONSE_INTAKE_0.8.0.md` (2917 bytes, sha256 `2b6a12f738adf52c...`)
3. `docs/FINAL/fusion_inbox_R6/PROMPTS/README_PROMPTS_PLACEHOLDER.md` (80 bytes, sha256 `34b1124f2b714c28...`)
4. `docs/FINAL/fusion_inbox_R6/PROMPTS/✅ ANTIGRAVITY_P0A_ACCEPTANCE_CRITERIA_0.2.2.md` (880 bytes, sha256 `792c7084a96b1c78...`)
5. `docs/FINAL/fusion_inbox_R6/PROMPTS/📝 DECISION_JOURNAL_ENTRY_PROMPT_MVP_QAIC_0.4.0.md` (941 bytes, sha256 `f29609b2013ff927...`)
6. `docs/FINAL/fusion_inbox_R6/PROMPTS/🤖 ANTIGRAVITY_P0A_KNOWLEDGE_BASE_PROMPT_0.2.2.md` (2695 bytes, sha256 `2112e9cf8704cf5b...`)
7. `docs/FINAL/fusion_inbox_R6/PROMPTS/🧠 FIRST_REAL_GPT_RESPONSE_AUDIT_PROMPT_MVP_QAIC_0.4.1.md` (1783 bytes, sha256 `1d70b93630468c94...`)
8. `docs/FINAL/fusion_inbox_R6/PROMPTS/🧠 GPT_RESPONSE_AUDIT_PROMPT_MVP_QAIC_0.4.0.md` (1425 bytes, sha256 `c28a435b69a15906...`)
9. `docs/FINAL/fusion_inbox_R6/PROMPTS/🧱 ANTIGRAVITY_P0A_WORKSPACE_TREE_0.2.2.md` (748 bytes, sha256 `9b483f58f3006ff0...`)
10. `docs/FINAL/fusion_inbox_R6/README/README_MVP_QAIC_P2I_PROMPT_WORKFLOW_UX_DRAFT_APPROVAL_0.9.5.md` (2056 bytes, sha256 `469d908a132153e5...`)
11. `docs/FINAL/fusion_inbox_R6/RUNBOOK/README_MVP_QAIC_P2B_GEM_ADAPTIVE_PROMPT_LOOP_0.7.0.md` (1473 bytes, sha256 `c8f9f286f4217132...`)
12. `docs/FINAL/fusion_inbox_R6/RUNBOOK/RUNBOOK_MVP_QAIC_P1_PROMPT_QUALITY_CORE_FUSION_0.5.0.md` (3133 bytes, sha256 `37774df9cff0af9d...`)
13. `docs/FINAL/fusion_inbox_R6/RUNBOOK/RUNBOOK_MVP_QAIC_P1G_PROMPT_LIBRARY_CONTRACT_0.6.0.md` (2066 bytes, sha256 `46a126ba79aaa331...`)
14. `docs/FINAL/fusion_inbox_R6/RUNBOOK/RUNBOOK_MVP_QAIC_P2G_PROMPT_RUNTIME_CATALOG_SYNC_0.9.0.md` (3040 bytes, sha256 `c3d1129e82c04fd2...`)
15. `docs/FINAL/fusion_inbox_R6/RUNBOOK/RUNBOOK_MVP_QAIC_P2G_PROMPT_RUNTIME_CATALOG_SYNC_FUSED_0.9.1.md` (1643 bytes, sha256 `09e7c343b901dfa2...`)
16. `docs/FINAL/fusion_inbox_R6/RUNBOOK/RUNBOOK_MVP_QAIC_P2H_PROMPT_TEMPLATE_TO_COPY_0.9.2.md` (1318 bytes, sha256 `5d87432624757e94...`)
17. `docs/FINAL/fusion_inbox_R6/RUNBOOK/RUNBOOK_P2D_PROMPT_LIBRARY_BASELINE_SAFE_0.7.3.md` (1000 bytes, sha256 `ea948a54e77c6508...`)
18. `docs/FINAL/fusion_inbox_R6/RUNBOOK/🧪 FIRST_REAL_GPT_RESPONSE_AUDIT_TEST_RUNBOOK_MVP_QAIC_0.4.1.md` (2482 bytes, sha256 `fe1b2cde73ccabdd...`)

---

## Source 1: `docs/FINAL/fusion_inbox_R6/ARCHITECTURE/🧠 DECISION_JOURNAL_USAGE_AND_PROMPT_IMPROVEMENT_LOOP_0.4.6.md`

# 🧠 DECISION JOURNAL — Usage futur & Prompt Improvement Loop 0.4.6

## 1. À quoi sert le journal ?

Le journal sert à transformer les réponses GPT et QAIC en données exploitables :

```text
prompt_id
payload_id
réponse GPT auditée
scores
signaux
données manquantes
blockers
décision humaine
résultat attendu
```

## 2. Correction des prompts

Le journal permet de détecter :

```text
signal_id absents
scores non justifiés
blockers oubliés
format de sortie non respecté
données inventées
SL absent
confiance trop élevée
```

Ces anomalies alimentent :

```text
PROMPT_LIBRARY
GPT_PROMPT_RUNTIME_SPEC
OUTPUT_TEMPLATES
GPT_RESPONSE_AUDIT_PROMPT
```

## 3. Qualité data

Les champs `missing_data` et `blockers` permettent de prioriser :

```text
portfolio snapshot
prix
volume
BTC regime
spread
funding / OI
TVL
unlocks
source freshness
```

## 4. Cockpit AppSheet / dashboard

Le journal devient source pour :

```text
% réponses validées
% REVIEW_REQUIRED
% BLOCKED
top missing_data
top blockers
tokens souvent rejetés
prompts à améliorer
```

## 5. Règle de gouvernance

```text
Aucune décision ne devient exploitable sans entrée journal et audit.
```

## Source 2: `docs/FINAL/fusion_inbox_R6/NOTICE_UTILISATION/NOTICE_UTILISATION_MVP_QAIC_P2F_GPT_RESPONSE_INTAKE_0.8.0.md`

# 🧪 Notice d’utilisation — MVP QAIC P2-F GPT Response Intake — 0.8.0

## 🎯 Objectif

Créer une passerelle simple et contrôlée entre une réponse GPT/Gem/IA et le journal officiel `🧾 DECISION_JOURNAL`.

La règle est volontairement simple : le parsing est automatique, mais la journalisation reste validée humainement.

## 🧩 Onglets créés

### 🤖 AI_RUNTIME_REFERENCE

Base courte des GPT/Gem/IA utilisables.

L’entrée par défaut est :

```text
ai_runtime_id = nomGEM_FULL_REVIEW_001
prompt_id = prompt_05_full_trading_review
prompt_contract_id = P2D-PROMPT-BASELINE-001-PROMPT_05_FULL_TRADING_REVIEW
gem_profile = GEM_GENERAL_REVIEW
```

### 🧪 GPT_RESPONSE_INTAKE

Zone de saisie et d’analyse de la réponse GPT/Gem.

Champs éditables minimum :

| Champ | Mode | Description |
|---|---|---|
| `ai_runtime_id` | éditable | Sélection du GPT/Gem/IA utilisé. |
| `raw_response` | éditable | Réponse complète collée depuis le GPT/Gem. |
| `ready_to_journal` | éditable | `NO` par défaut, passer à `YES` après contrôle humain. |
| `human_review_note` | éditable optionnel | Note courte de validation humaine. |

`prompt_id`, `gem_profile`, `prompt_contract_id`, `platform` et `ai_runtime_name` sont auto-remplis depuis `🤖 AI_RUNTIME_REFERENCE`.

## ▶️ Workflow quotidien

1. Lancer une fois :

```javascript
MVPQAIC_AiRuntimeReferenceInit()
```

2. Lancer une fois :

```javascript
MVPQAIC_GptResponseIntakeInit()
```

3. Dans `🧪 GPT_RESPONSE_INTAKE`, choisir :

```text
ai_runtime_id = nomGEM_FULL_REVIEW_001
```

4. Coller la réponse complète dans :

```text
raw_response
```

5. Lancer :

```javascript
MVPQAIC_IntakeAnalyzeRawResponse()
```

6. Vérifier les champs extraits :

```text
analysis_level
decision_status
human_final_decision
validation_status
signal_id
score_id
risk_guard
missing_data
blockers
confidence_score
quality_score
```

7. Si c’est correct, passer :

```text
ready_to_journal = YES
```

8. Lancer :

```javascript
MVPQAIC_JournalAppendFromIntake()
```

## ✅ Conditions de journalisation

Le script journalise uniquement si :

```text
ready_to_journal = YES
mandatory_fields_missing_count = 0
parse_status = OK ou REVIEW_REQUIRED_ACCEPTABLE ou BLOCKED_ACCEPTABLE
payload_id / payload_hash non déjà présents dans 🧾 DECISION_JOURNAL
```

## 🔒 Garde-fous

```text
HUMAN_REVIEW_ONLY
NO_AUTO_ORDER
NO_AUTO_SIZING
NO_BROKER_EXECUTION
NO_REAL_ORDER
NO_SECRET
NO_TRIGGER
NO_MENU_MUTATION
NO_EXTERNAL_CALL
```

## 🧠 Signification de Gem / GEM

Dans ce MVP, `gem_profile` ne veut pas dire obligatoirement “Google Gemini Gem”.

Il signifie plutôt :

```text
profil d’exécution IA attendu
```

Exemples :

```text
GEM_GENERAL_REVIEW
GEM_SIGNAL_REVIEW
GEM_RISK_REVIEW
GEM_LEXIQUE_EDUCATIONAL
```

Pour l’usage quotidien, le champ important reste :

```text
ai_runtime_id
```

Exemple :

```text
nomGEM_FULL_REVIEW_001
```

## Source 3: `docs/FINAL/fusion_inbox_R6/PROMPTS/README_PROMPTS_PLACEHOLDER.md`

# Prompts MVP QAIC

Prompts Stitch, Antigravity et Apps Script à déposer ici.

## Source 4: `docs/FINAL/fusion_inbox_R6/PROMPTS/✅ ANTIGRAVITY_P0A_ACCEPTANCE_CRITERIA_0.2.2.md`

# ✅ Antigravity P0-A — Critères de validation

> **Version :** `ANTIGRAVITY_P0A_ACCEPTANCE_CRITERIA_0.2.2`
> **Date :** 2026-06-11
> **Statut :** `READY`

## Validation obligatoire

| Critère | Statut attendu |
|---|---|
| Tous les CSV existent | Obligatoire |
| Schéma Markdown généré | Obligatoire |
| Manifest généré | Obligatoire |
| IDs stables | Obligatoire |
| Colonnes AppSheet-friendly | Obligatoire |
| Source file / source section | Obligatoire |
| `REVIEW_REQUIRED` si doute | Obligatoire |
| Pas de règle inventée | Obligatoire |
| Pas de broker / ordre / secret | Obligatoire |
| ZIP final | Recommandé |

## Stop immédiat si

- création d’un ordre automatique ;
- mention de clés API ou secrets ;
- ajout BigQuery/Cloud Run ;
- suppression de fichiers ;
- règles non sourcées ;
- CSV illisibles ;
- colonnes trop complexes pour AppSheet.

## Source 5: `docs/FINAL/fusion_inbox_R6/PROMPTS/📝 DECISION_JOURNAL_ENTRY_PROMPT_MVP_QAIC_0.4.0.md`

# 📝 Prompt — Générer une entrée Decision Journal MVP QAIC 0.4.0

> **Version :** `MVP_QAIC_DECISION_JOURNAL_ENTRY_PROMPT_0.4.0`
> **Statut :** `P1_GPT_RESPONSE_AUDIT_DECISION_JOURNAL_READY_FOR_DRIVE_REVIEW`

---

## Prompt

```text
Transforme l’analyse suivante en entrée DECISION_JOURNAL MVP QAIC.

Contraintes :
- aucune exécution broker ;
- aucune recommandation certaine ;
- décision humaine uniquement ;
- si données manquantes, indique REVIEW_REQUIRED ;
- si SL absent, indique BLOCKED ;
- si réponse GPT rejetée, indique GPT_RESPONSE_REJECTED.

Champs à produire :
journal_id_placeholder
created_at_placeholder
payload_id
gpt_response_audit_status
asset
token_type
analysis_level
decision_status
human_final_decision
scores_summary
signals_summary
missing_data
blockers
entry_summary
tp_summary
sl_summary
trailing_summary
portfolio_context
notes
run_id
validation_status

Analyse à convertir :
[COLLER ICI]
```

## Source 6: `docs/FINAL/fusion_inbox_R6/PROMPTS/🤖 ANTIGRAVITY_P0A_KNOWLEDGE_BASE_PROMPT_0.2.2.md`

# 🤖 Antigravity Prompt — P0-A Knowledge Base CSV

> **Projet :** 🛠️ MVP QAIC — Crypto Signal OS Web App
> **Version :** `ANTIGRAVITY_P0A_PROMPT_0.2.2`
> **Date :** 2026-06-11
> **Statut :** `READY_TO_RUN_AFTER_USER_VALIDATION`

## Prompt à coller dans Antigravity

```text
You are working on the MVP QAIC — Crypto Signal OS Web App.

Goal:
Build P0 Knowledge Base from the provided Markdown files.

Priority:
The MVP must first deliver a usable Web App focused on:
- crypto lexicon
- trading methods
- signal library
- risk playbooks
- daily checklists
- decision journal

Long-term direction:
This MVP will later become a Web App / UI IDE layer for the final QAIC system. Do not integrate the final QAIC engine yet. Prepare stable IDs and clean mappings only.

Do not implement automatic trading.
Do not implement broker execution.
Do not create live market integrations yet.
Do not invent trading rules that are not present in the source documents.
If a field is uncertain, use REVIEW_REQUIRED.

Input files:
- source/architecture_mvp_crypto_stitch_antigravity_google_lexique_first.md
- source/lexique_crypto_methodes_signaux_trading_pro.md
- source/synthese_lexique_mvp_crypto_project_context.md
- docs/CDC_MVP_QAIC_WEB_APP_LEXIQUE_FIRST_0.2.2.md
- docs/PLANNING_MVP_QAIC_WEB_APP_TRANSITION_QAIC_0.2.2.md
- docs/INSTRUCTIONS_PROJET_MVP_QAIC_0.2.2.md

Tasks:
1. Extract structured rows from the lexicon and project docs.
2. Create machine-readable CSV seed files for:
   - KNOWLEDGE_TERMS
   - METHOD_LIBRARY
   - SIGNAL_LIBRARY
   - RISK_PLAYBOOK
   - CHECKLISTS
   - DECISION_TEMPLATES
   - GLOSSARY_TAGS
3. Every row must include stable IDs, category, title, tags, priority, risk notes, related terms, source file, source section, and validation status when available.
4. Generate a Markdown schema document describing every table and column.
5. Generate a manifest listing all files created.
6. Use UTF-8 CSV.
7. Do not create files outside these folders:
   - schemas/
   - csv_seed/
   - exports/
8. Do not use BigQuery, Cloud Run, brokers, order execution, or secrets.

Output:
- schemas/MVP_QAIC_SHEETS_SCHEMA_P0_0.2.2.md
- csv_seed/KNOWLEDGE_TERMS.csv
- csv_seed/METHOD_LIBRARY.csv
- csv_seed/SIGNAL_LIBRARY.csv
- csv_seed/RISK_PLAYBOOK.csv
- csv_seed/CHECKLISTS.csv
- csv_seed/DECISION_TEMPLATES.csv
- csv_seed/GLOSSARY_TAGS.csv
- exports/MVP_QAIC_P0_KNOWLEDGE_BASE_SEED_0.2.2.zip
- MANIFEST_P0A_0.2.2.md

Acceptance criteria:
- No invented trading rule.
- No automatic order logic.
- IDs are stable and human-readable.
- CSV columns are simple and AppSheet-friendly.
- Uncertain entries are flagged REVIEW_REQUIRED.
- The manifest lists every created file.
```

## Source 7: `docs/FINAL/fusion_inbox_R6/PROMPTS/🧠 FIRST_REAL_GPT_RESPONSE_AUDIT_PROMPT_MVP_QAIC_0.4.1.md`

# 🧠 PROMPT — First Real GPT Response Audit Test MVP QAIC 0.4.1

> **Version :** `MVP_QAIC_P1B_REAL_GPT_RESPONSE_AUDIT_PROMPT_0.4.1`
> **Statut :** `P1B_FIRST_REAL_GPT_RESPONSE_AUDIT_TEST_READY_FOR_DRIVE_REVIEW`

---

## Prompt à utiliser

```text
Tu es auditeur QAIC du MVP Crypto Signal OS.

Objectif : auditer une vraie réponse GPT générée depuis GPT_INPUT_PAYLOADS.

Règles non négociables :
- HUMAN_REVIEW_ONLY
- NO_AUTO_ORDER
- NO_AUTO_SIZING
- NO_BROKER_EXECUTION
- NO_REAL_ORDER
- REVOLUT_X_READONLY_ONLY
- GPT_OUTPUT_AUDIT_REQUIRED
- DECISION_JOURNAL_REQUIRED

Audite la réponse GPT ci-dessous.

1. Identifie le niveau d’analyse réel :
QAIC_FULL / QAIC_PARTIAL / SIGNAL_ONLY / LEXIQUE_ONLY / INSUFFICIENT_DATA.

2. Vérifie les scores QAIC :
alpha_score, risk_score, liquidity_score, momentum_score, fundamental_score, derivatives_score, data_quality_score, confidence_score.
Pour chaque score absent ou non justifié : SCORE_NOT_AVAILABLE + raison.

3. Vérifie les signaux QAIC :
signal_id, famille, direction, score cible, poids, impact décisionnel.
Si absent : SIGNAL_NOT_AVAILABLE + raison.

4. Vérifie le trade plan :
entrée, TP1, TP2, TP3, SL, invalidation, suiveur manuel.
Si SL absent : BLOCKED.
Si données manquantes : REVIEW_REQUIRED.

5. Vérifie les hallucinations :
prix inventé, PRU inventé, PnL inventé, position inventée, TP/SL inventé, ordre direct, sizing automatique, broker execution.

6. Classe la réponse :
GPT_RESPONSE_VALIDATED
GPT_RESPONSE_REVIEW_REQUIRED
GPT_RESPONSE_REJECTED
GPT_RESPONSE_INSUFFICIENT_DATA

7. Produis :
- audit_summary
- missing_data
- blockers
- accepted_elements
- rejected_elements
- decision_journal_entry_proposal
- human_next_action

Réponse GPT à auditer :
[COLLER ICI LA RÉPONSE GPT]
```

## Source 8: `docs/FINAL/fusion_inbox_R6/PROMPTS/🧠 GPT_RESPONSE_AUDIT_PROMPT_MVP_QAIC_0.4.0.md`

# 🧠 Prompt — Audit d’une réponse GPT Crypto MVP QAIC 0.4.0

> **Version :** `MVP_QAIC_GPT_RESPONSE_AUDIT_PROMPT_0.4.0`
> **Statut :** `P1_GPT_RESPONSE_AUDIT_DECISION_JOURNAL_READY_FOR_DRIVE_REVIEW`

Copier ce prompt après une réponse GPT pour l’auditer.

---

## Prompt

```text
Tu es auditeur QAIC du MVP Crypto Signal OS.

Audite la réponse GPT ci-dessous selon les règles MVP QAIC :

1. Vérifie le niveau d’analyse réel :
QAIC_FULL / QAIC_PARTIAL / SIGNAL_ONLY / LEXIQUE_ONLY / INSUFFICIENT_DATA.

2. Vérifie les scores :
alpha_score, risk_score, liquidity_score, momentum_score, fundamental_score, derivatives_score, data_quality_score, confidence_score.
Si un score est absent ou non justifié, indique SCORE_NOT_AVAILABLE.

3. Vérifie les signaux :
signal_id, famille, direction, score cible, poids, impact décisionnel.
Si absent, indique SIGNAL_NOT_AVAILABLE.

4. Vérifie le trade plan :
entrée, TP1, TP2, TP3, SL, invalidation, suiveur manuel.
Si SL absent : BLOCKED.
Si données manquantes : REVIEW_REQUIRED.

5. Vérifie les risques :
données inventées, PRU inventé, PnL inventé, prix inventé, ordre automatique, sizing automatique, broker execution.

6. Classe la réponse :
GPT_RESPONSE_VALIDATED
GPT_RESPONSE_REVIEW_REQUIRED
GPT_RESPONSE_REJECTED
GPT_RESPONSE_INSUFFICIENT_DATA

7. Propose une entrée DECISION_JOURNAL structurée.

Réponse GPT à auditer :
[COLLER ICI]
```
```

## Source 9: `docs/FINAL/fusion_inbox_R6/PROMPTS/🧱 ANTIGRAVITY_P0A_WORKSPACE_TREE_0.2.2.md`

# 🧱 Workspace Antigravity P0 — Arborescence cible

> **Version :** `ANTIGRAVITY_WORKSPACE_TREE_0.2.2`
> **Date :** 2026-06-11
> **Statut :** `READY`

```text
MVP_QAIC/
├── docs/
│   ├── CDC_MVP_QAIC_WEB_APP_LEXIQUE_FIRST_0.2.2.md
│   ├── PLANNING_MVP_QAIC_WEB_APP_TRANSITION_QAIC_0.2.2.md
│   └── INSTRUCTIONS_PROJET_MVP_QAIC_0.2.2.md
├── source/
│   ├── architecture_mvp_crypto_stitch_antigravity_google_lexique_first.md
│   ├── lexique_crypto_methodes_signaux_trading_pro.md
│   └── synthese_lexique_mvp_crypto_project_context.md
├── schemas/
├── csv_seed/
├── apps_script/
├── app_sheet/
├── stitch/
├── qaic_bridge/
└── exports/
```

## Source 10: `docs/FINAL/fusion_inbox_R6/README/README_MVP_QAIC_P2I_PROMPT_WORKFLOW_UX_DRAFT_APPROVAL_0.9.5.md`

# 🛠️ MVP QAIC — P2-I Prompt Workflow UX & Draft Approval — 0.9.5

## Objectif
Centraliser la boucle de test Gem dans `🧪 GPT_RESPONSE_INTAKE` et rendre lisibles les onglets `🧭 PROMPT_IMPROVEMENT_QUEUE` et `📘 PROMPT_LIBRARY`.

## Scripts à remplacer

```text
scripts/mvpqaic_11_p1_prompt_quality_core.gs
scripts/mvpqaic_23_gpt_response_intake_core.gs
```

## Fonctions ajoutées

```javascript
MVPQAIC_PromptWorkflowSheetsOptimize()
MVPQAIC_PromptDraftApplyApprovedToLibrary()
MVPQAIC_IntakeApplyApprovedDraftToLibrary()
```

## Boutons recommandés dans 🧪 GPT_RESPONSE_INTAKE

```text
👁️ Preview refs     → MVPQAIC_IntakePrepareRefs
🧪 Analyser réponse → MVPQAIC_IntakeAnalyzeRawResponse
🧾 Journaliser      → MVPQAIC_JournalAppendFromIntake
🔁 Boucle qualité   → MVPQAIC_IntakePostJournalPromptLoop
✅ Appliquer draft  → MVPQAIC_IntakeApplyApprovedDraftToLibrary
🆕 Nouveau test     → MVPQAIC_IntakeNewBlank
```

## Process compact

```text
1. 🧪 GPT_RESPONSE_INTAKE : choisir ai_runtime_id + prompt_id.
2. Cliquer 👁️ Preview refs.
3. Copier prompt_template_to_copy dans le Gem.
4. Coller la réponse Gem dans raw_response.
5. Cliquer 🧪 Analyser réponse.
6. Vérifier parse_status + mandatory_fields_missing_count.
7. Passer ready_to_journal = YES.
8. Cliquer 🧾 Journaliser.
9. Cliquer 🔁 Boucle qualité : dashboard + queue + draft + ouverture auto de 🧭 PROMPT_IMPROVEMENT_QUEUE.
10. Dans 🧭 PROMPT_IMPROVEMENT_QUEUE : vérifier next_prompt_draft.
11. Si validé humainement : mettre human_review_status = APPROVED_TO_LIBRARY.
12. Cliquer ✅ Appliquer draft.
13. Vérifier 📘 PROMPT_LIBRARY.prompt_template_to_copy.
14. Cliquer 🆕 Nouveau test et retester le Gem.
```

## Sécurité

```text
HUMAN_REVIEW_ONLY
NO_AUTO_PROMOTION
NO_DELETE
NO_HIDE
NO_TRIGGER
NO_MENU_MUTATION
NO_BROKER
NO_ORDER
NO_SIZING
NO_SECRET
```

Le draft n’est jamais promu tout seul : il est appliqué uniquement si `human_review_status = APPROVED_TO_LIBRARY` sur une ligne `ADAPTIVE_NEXT_PROMPT_DRAFT`.

## Source 11: `docs/FINAL/fusion_inbox_R6/RUNBOOK/README_MVP_QAIC_P2B_GEM_ADAPTIVE_PROMPT_LOOP_0.7.0.md`

# 🛠️ MVP QAIC — P2-B GEM Adaptive Prompt Loop — 0.7.0

Version: `MVP_QAIC_P1_PROMPT_QUALITY_CORE_0.7.0_GEM_ADAPTIVE_LOOP_SAFE`
Date: 2026-06-12
Status: SAFE_DRAFT_ONLY

## Objectif

Fusionner P2-B dans `mvpqaic_11_p1_prompt_quality_core.gs` sans créer de nouveau script ni nouvel onglet.

Le module lit le dernier test GPT réel depuis `DECISION_JOURNAL`, lit `GPT_QUALITY_DASHBOARD`, `PROMPT_IMPROVEMENT_QUEUE` et `PROMPT_LIBRARY`, puis écrit un brouillon `next_prompt_draft` dans `PROMPT_IMPROVEMENT_QUEUE`.

## Garde-fous

- `PROMPT_LIBRARY` est lu en read-only par P2-B.
- Aucun overwrite de prompt idéal.
- Aucune promotion automatique en ACTIVE.
- Écriture P2-B limitée à `PROMPT_IMPROVEMENT_QUEUE`.
- `promotion_allowed = NO`.
- `human_review_status = TO_REVIEW`.

## Fonctions

```javascript
MVPQAIC_PromptAdaptiveLoopStatus()
MVPQAIC_PromptAdaptiveNextDraftBuild()
MVPQAIC_PromptAdaptiveRunAllFast()
```

## Run conseillé

```javascript
MVPQAIC_PromptAdaptiveLoopStatus()
MVPQAIC_PromptAdaptiveNextDraftBuild()
```

## Sortie

Dans `PROMPT_IMPROVEMENT_QUEUE`, ligne `queue_type = ADAPTIVE_NEXT_PROMPT_DRAFT`, avec colonnes :

- `gem_profile`
- `base_prompt_version`
- `source_journal_id`
- `source_payload_id`
- `adaptive_issue_summary`
- `mandatory_fields_patch`
- `missing_data_patch`
- `blocker_patch`
- `next_prompt_draft`
- `draft_status`
- `human_review_status`
- `promotion_allowed`
- `base_prompt_readonly`
- `prompt_library_write_allowed`

## Source 12: `docs/FINAL/fusion_inbox_R6/RUNBOOK/RUNBOOK_MVP_QAIC_P1_PROMPT_QUALITY_CORE_FUSION_0.5.0.md`

# 🛠️ MVP QAIC — Runbook P1 Prompt Quality Core Fusion 0.5.0

> **Version :** `MVP_QAIC_P1_PROMPT_QUALITY_CORE_0.5.0_SAFE_FULL_FUSION_P1E_P1F`
> **Date :** 2026-06-11
> **Statut :** `SAFE_RUNTIME_READY_FOR_VALIDATION`

## 🎯 Objectif

Fusionner proprement P1-E et P1-F dans un seul script durable :

```text
mvpqaic_11_p1_prompt_quality_core.gs
```

Le core couvre :

```text
DECISION_JOURNAL → GPT_QUALITY_DASHBOARD → PROMPT_IMPROVEMENT_QUEUE
```

## 🔐 Sécurité

```text
HUMAN_REVIEW_ONLY
NO_BROKER
NO_ORDER
NO_SIZING
NO_SECRET
```

Le script lit uniquement :

```text
DECISION_JOURNAL
GPT_QUALITY_DASHBOARD
```

Le script écrit uniquement :

```text
GPT_QUALITY_DASHBOARD
PROMPT_IMPROVEMENT_QUEUE
```

## 🧩 Installation propre

### Cas recommandé

Remplacer l'ancien P1-E par le script fusionné :

```text
mvpqaic_11_p1_prompt_quality_core.gs
```

Ne pas garder durablement les anciens scripts live :

```text
mvpqaic_11_p1e_prompt_quality_dashboard.gs
mvpqaic_12_p1f_prompt_improvement_queue.gs
```

Après validation runtime, les archiver en ZIP/docs puis les retirer du live Apps Script.

## ✅ Ordre de test

### 1. Core status

```javascript
MVPQAIC_PromptQualityCoreStatus()
```

Attendu :

```text
status = OK
journal_sheet_exists = true
dashboard_sheet_exists = true/false
queue_sheet_exists = true/false
can_refresh_dashboard = true
safety = HUMAN_REVIEW_ONLY_NO_BROKER_NO_ORDER_NO_SIZING_NO_SECRET
```

### 2. Dashboard status

```javascript
MVPQAIC_PromptQualityDashboardStatus()
```

Attendu :

```text
status = OK
journal_sheet_exists = true
journal_rows >= 1
can_refresh = true
```

### 3. Dashboard refresh

```javascript
MVPQAIC_PromptQualityDashboardRefresh()
```

Attendu :

```text
status = REFRESHED
dashboard_sheet = GPT_QUALITY_DASHBOARD
journal_rows >= 1
prompt_actions_count >= 1
safety = NO_BROKER_NO_ORDER_NO_SIZING_NO_SECRET
```

### 4. Queue status

```javascript
MVPQAIC_PromptImprovementQueueStatus()
```

Attendu :

```text
status = OK
source_sheet_exists = true
can_refresh = true
```

### 5. Queue refresh

```javascript
MVPQAIC_PromptImprovementQueueRefresh()
```

Attendu :

```text
status = REFRESHED
target_sheet = PROMPT_IMPROVEMENT_QUEUE
queue_rows_written >= 1
p0_count >= 1
p1_count >= 1
safety = HUMAN_REVIEW_ONLY_NO_BROKER_NO_ORDER_NO_SIZING_NO_SECRET
```

## 🎨 UI Sheets obligatoire

Les onglets générés doivent rester des outils de décision :

```text
synthèse en haut
freeze rows/columns
filtres
colonnes décision/action à gauche
colonnes audit à droite
hauteur de ligne normale
largeurs adaptées
couleurs métier utiles
validations de listes
pas de ligne blanche décorative
```

## 🧭 Décision après validation

Si les 5 fonctions sont OK :

```text
P1-E + P1-F = VALIDÉ FUSION
```

Garder dans Apps Script live :

```text
mvpqaic_09_p1_journal_core.gs
mvpqaic_11_p1_prompt_quality_core.gs
```

Archiver / retirer du live :

```text
mvpqaic_11_p1e_prompt_quality_dashboard.gs
mvpqaic_12_p1f_prompt_improvement_queue.gs
```

## ⏭️ Suite logique

Après validation fusion :

```text
P1-G — Prompt Library / Prompt Contract Update
```

## Source 13: `docs/FINAL/fusion_inbox_R6/RUNBOOK/RUNBOOK_MVP_QAIC_P1G_PROMPT_LIBRARY_CONTRACT_0.6.0.md`

# 🛠️ MVP QAIC — P1-G Prompt Library / Contract Update — Runbook

**Version :** `MVP_QAIC_P1_PROMPT_QUALITY_CORE_0.6.0_SAFE_FULL_FUSION_P1E_P1F_P1G`
**Date :** 2026-06-11
**Statut :** `READY_FOR_RUNTIME_VALIDATION`

## Objectif

P1-G consolide P1-E + P1-F dans le même core durable et ajoute la génération de `PROMPT_LIBRARY`.

Le principe est volontairement simple : un seul onglet visible, mais avec lignes typées :

- `CORE_CONTRACT` : règles stables non négociables.
- `GEM_PROFILE` : capacités par Gem / runtime / futur QAIC readonly.
- `PROMPT_CONTRACT` : contrats de prompts issus de `PROMPT_IMPROVEMENT_QUEUE`.

## Sécurité

Lecture :

```text
DECISION_JOURNAL
GPT_QUALITY_DASHBOARD
PROMPT_IMPROVEMENT_QUEUE
```

Écriture :

```text
GPT_QUALITY_DASHBOARD
PROMPT_IMPROVEMENT_QUEUE
PROMPT_LIBRARY
```

Interdits :

```text
NO_BROKER
NO_ORDER
NO_SIZING
NO_SECRET
NO_TRADING_BOT
NO_AUTO_EXECUTION
```

## Installation

Remplacer dans Apps Script le fichier durable :

```text
mvpqaic_11_p1_prompt_quality_core.gs
```

par la version complète fournie dans `scripts/`.

Ne pas ajouter un nouveau script isolé P1-G.

## Validation runtime

Lancer dans cet ordre :

```javascript
MVPQAIC_PromptQualityCoreStatus()
MVPQAIC_PromptQualityDashboardStatus()
MVPQAIC_PromptImprovementQueueStatus()
MVPQAIC_PromptLibraryStatus()
MVPQAIC_PromptLibraryRefresh()
```

Résultat attendu pour P1-G :

```text
status = REFRESHED
target_sheet = PROMPT_LIBRARY
library_rows_written >= 1
core_contract_rows >= 2
gem_profile_rows >= 4
prompt_contract_rows >= 1
safety = HUMAN_REVIEW_ONLY_NO_BROKER_NO_ORDER_NO_SIZING_NO_SECRET
```

## Règle métier importante

Un Gem peut expliquer plus qu’il ne peut scorer.
Un score est autorisé uniquement si :

```text
runtime_profile supports metric
metric data is present
source and as_of_date exist
quality_score/risk_guard are present
```

Sinon :

```text
score = NOT_AVAILABLE
ou decision_status = REVIEW_REQUIRED / BLOCKED
```

Jamais d’invention de prix, PRU, quantité, PnL, TP, SL, exposition ou score.

## Source 14: `docs/FINAL/fusion_inbox_R6/RUNBOOK/RUNBOOK_MVP_QAIC_P2G_PROMPT_RUNTIME_CATALOG_SYNC_0.9.0.md`

# 🛠️ MVP QAIC — P2-G Runtime Prompt Catalog Sync — Runbook 0.9.0

## Objectif

Corriger le modèle prompt autour des 5 prompts métier validés dans `GPT_PROMPT_RUNTIME_SPEC` :

1. `prompt_01_portfolio_analysis` — Portfolio / positions / exposition / Revolut X si disponible
2. `prompt_02_market_analysis` — Marché / régime / momentum / liquidité
3. `prompt_03_buy_analysis_multi_horizon` — Reco achat / entrée / TP / SL / multi-horizon
4. `prompt_04_volatile_leverage_analysis` — Volatile / leverage / futures / funding / OI / liquidations
5. `prompt_05_full_trading_review` — Revue complète portfolio + marché + signal + décision

## Scripts inclus

- `scripts/mvpqaic_24_prompt_runtime_catalog_sync_core.gs`
- `scripts/mvpqaic_23_gpt_response_intake_core.gs`

## Sécurité

- `HUMAN_REVIEW_ONLY`
- `NO_BROKER`
- `NO_ORDER`
- `NO_SIZING`
- `NO_SECRET`
- `NO_DELETE`
- `NO_TRIGGER`
- `NO_MENU_MUTATION`

## Ordre de lancement

### 1. Charger les scripts

Remplacer/ajouter dans Apps Script :

- remplacer `mvpqaic_23_gpt_response_intake_core.gs` par la version `0.8.1_PROMPT_SELECTOR_SAFE`
- ajouter `mvpqaic_24_prompt_runtime_catalog_sync_core.gs`

### 2. Vérifier le catalogue runtime

```javascript
MVPQAIC_PromptRuntimeCatalogStatus()
```

Attendu :

```text
source_runtime_prompts_count = 5
source_runtime_prompt_ids contient prompt_01 à prompt_05
```

### 3. Synchroniser `📘 PROMPT_LIBRARY`

```javascript
MVPQAIC_PromptRuntimeCatalogSyncToLibrarySafe()
```

Attendu :

```text
status = OK
prompt_rows_inserted / updated > 0
runtime_prompt_ids = prompt_01...prompt_05
non_runtime_prompt_rows_marked_archive_candidate >= 0
```

Aucune suppression n’est faite. Les lignes parasites hors catalogue sont seulement marquées `DEPRECATED` / `NON_RUNTIME_PROMPT_ARCHIVE_CANDIDATE`.

### 4. Réinitialiser l’intake avec prompt_id éditable

```javascript
MVPQAIC_AiRuntimeReferenceInit()
MVPQAIC_GptResponseIntakeInit()
```

Dans `🧪 GPT_RESPONSE_INTAKE`, les champs éditables deviennent :

```text
ai_runtime_id
prompt_id
raw_response
ready_to_journal
human_review_note
```

### 5. Préparer les références avant test Gem/GPT

Choisir :

```text
ai_runtime_id = nomGEM_FULL_REVIEW_001
prompt_id = un des 5 prompts métier
```

Puis lancer :

```javascript
MVPQAIC_IntakePrepareRefs()
```

Ce bouton pré-remplit :

```text
ai_runtime_name
platform
runtime_type
gem_profile
prompt_contract_id
```

### 6. Après réponse du Gem/GPT

Coller la réponse complète dans :

```text
raw_response
```

Puis lancer :

```javascript
MVPQAIC_IntakeAnalyzeRawResponse()
```

Vérifier les champs extraits, puis passer :

```text
ready_to_journal = YES
```

Puis journaliser :

```javascript
MVPQAIC_JournalAppendFromIntake()
```

## Boutons recommandés dans `🧪 GPT_RESPONSE_INTAKE`

Créer 3 dessins ou boutons :

1. `🔄 Préparer références` → `MVPQAIC_IntakePrepareRefs`
2. `🧪 Analyser réponse` → `MVPQAIC_IntakeAnalyzeRawResponse`
3. `🧾 Journaliser` → `MVPQAIC_JournalAppendFromIntake`

## Source 15: `docs/FINAL/fusion_inbox_R6/RUNBOOK/RUNBOOK_MVP_QAIC_P2G_PROMPT_RUNTIME_CATALOG_SYNC_FUSED_0.9.1.md`

# 🧭 Runbook — P2-G Runtime Prompt Catalog Sync FUSED 0.9.1

## 1. Remplacer les scripts live

Remplacer entièrement :

```text
mvpqaic_11_p1_prompt_quality_core.gs
mvpqaic_23_gpt_response_intake_core.gs
```

Ne pas ajouter `mvpqaic_24_prompt_runtime_catalog_sync_core.gs` dans Apps Script live.

## 2. Contrôle version

Lancer :

```javascript
MVPQAIC_PromptQualityCoreStatus()
```

Attendu :

```text
MVP_QAIC_P1_PROMPT_QUALITY_CORE_0.9.1_RUNTIME_CATALOG_SYNC_FUSED_SAFE
```

## 3. Audit catalogue prompts

Lancer :

```javascript
MVPQAIC_PromptRuntimeCatalogStatus()
```

Attendu : 5 prompts runtime depuis `GPT_PROMPT_RUNTIME_SPEC` :

```text
prompt_01_portfolio_analysis
prompt_02_market_analysis
prompt_03_buy_analysis_multi_horizon
prompt_04_volatile_leverage_analysis
prompt_05_full_trading_review
```

## 4. Synchroniser 📘 PROMPT_LIBRARY

Lancer :

```javascript
MVPQAIC_PromptRuntimeCatalogSyncToLibrarySafe()
```

Le script ajoute/met à jour les 5 `PROMPT_CONTRACT` métier et marque les faux prompts non-runtime comme `DEPRECATED_ARCHIVE_CANDIDATE`, sans suppression.

## 5. Préparer intake

Lancer :

```javascript
MVPQAIC_AiRuntimeReferenceInit()
MVPQAIC_GptResponseIntakeInit()
```

Puis dans `🧪 GPT_RESPONSE_INTAKE`, choisir :

```text
ai_runtime_id
prompt_id
```

Ensuite :

```javascript
MVPQAIC_IntakePrepareRefs()
MVPQAIC_IntakeAnalyzeRawResponse()
MVPQAIC_JournalAppendFromIntake()
```

## Boutons conseillés

```text
🔄 Préparer références  → MVPQAIC_IntakePrepareRefs
🧪 Analyser réponse     → MVPQAIC_IntakeAnalyzeRawResponse
🧾 Journaliser          → MVPQAIC_JournalAppendFromIntake
```

## Source 16: `docs/FINAL/fusion_inbox_R6/RUNBOOK/RUNBOOK_MVP_QAIC_P2H_PROMPT_TEMPLATE_TO_COPY_0.9.2.md`

# 🧭 Runbook — MVP QAIC P2-H Prompt Template To Copy 0.9.2

## 1. Remplacer les scripts

Remplacer dans Apps Script :

```text
mvpqaic_11_p1_prompt_quality_core.gs
mvpqaic_23_gpt_response_intake_core.gs
```

Ne pas ajouter de nouveau script. Ne pas utiliser `mvpqaic_24`.

## 2. Synchroniser la library

```javascript
MVPQAIC_PromptRuntimeCatalogSyncToLibrarySafe()
```

Résultat attendu : `📘 PROMPT_LIBRARY` contient les 5 `PROMPT_CONTRACT` runtime avec une colonne :

```text
prompt_template_to_copy
```

C’est le champ à copier/coller dans le Gem.

## 3. Initialiser / préparer l’intake

```javascript
MVPQAIC_GptResponseIntakeInit()
MVPQAIC_IntakePrepareRefs()
```

Dans `🧪 GPT_RESPONSE_INTAKE`, sélectionner :

```text
ai_runtime_id
prompt_id
```

Puis copier la valeur `prompt_template_to_copy` dans le Gem.

## 4. Coller la réponse Gem

La réponse du Gem se colle dans :

```text
raw_response
```

Puis lancer :

```javascript
MVPQAIC_IntakeAnalyzeRawResponse()
```

## 5. Journaliser

Après contrôle humain :

```text
ready_to_journal = YES
```

Puis :

```javascript
MVPQAIC_JournalAppendFromIntake()
```

## 6. Repartir vierge

```javascript
MVPQAIC_IntakeNewBlank()
```

Conserve `ai_runtime_id`, `prompt_id` et `prompt_template_to_copy`, vide `raw_response` et les champs de parsing.

## Source 17: `docs/FINAL/fusion_inbox_R6/RUNBOOK/RUNBOOK_P2D_PROMPT_LIBRARY_BASELINE_SAFE_0.7.3.md`

# 📘 Runbook — P2-D Prompt Library Baseline Safe 0.7.3

## 1. Replace script
Replace the full content of `mvpqaic_11_p1_prompt_quality_core.gs` with the provided script.

## 2. Status check
Run:

```javascript
MVPQAIC_PromptQualityCoreStatus()
```

Expected: status OK, emoji frontend sheets detected.

## 3. Initialize baseline prompt library safely
Run:

```javascript
MVPQAIC_PromptLibraryInitBaselineSafe()
```

Expected:
- status OK
- mode APPEND_OR_INIT_ONLY_NO_OVERWRITE_APPROVED_PROMPTS
- rows_appended > 0 if `📘 PROMPT_LIBRARY` was empty
- overwrite_prompt_library false
- active_prompt_auto_promotion false

## 4. Check adaptive loop
Run:

```javascript
MVPQAIC_PromptAdaptiveLoopStatus()
MVPQAIC_PromptAdaptiveNextDraftBuild()
```

Expected:
- PROMPT_LIBRARY rows_read > 0
- draft stays in `🧭 PROMPT_IMPROVEMENT_QUEUE`
- promotion_allowed NO

## Notes
`MVPQAIC_PromptLibraryRefresh()` now routes to the same safe baseline init path to avoid destructive `sheet.clear()` behavior.

## Source 18: `docs/FINAL/fusion_inbox_R6/RUNBOOK/🧪 FIRST_REAL_GPT_RESPONSE_AUDIT_TEST_RUNBOOK_MVP_QAIC_0.4.1.md`

# 🧪 FIRST REAL GPT RESPONSE AUDIT TEST RUNBOOK — MVP QAIC P1-B 0.4.1

> **Projet :** 🛠️ MVP QAIC — Crypto Signal OS Web App
> **Version :** `MVP_QAIC_P1B_FIRST_REAL_GPT_RESPONSE_AUDIT_TEST_RUNBOOK_0.4.1`
> **Date :** 2026-06-11
> **Statut :** `P1B_FIRST_REAL_GPT_RESPONSE_AUDIT_TEST_READY_FOR_DRIVE_REVIEW`
> **Base :** P1 0.4.0 Full Fusion

---

## 1. 🎯 Objectif

Tester pour la première fois une **vraie réponse GPT** générée depuis un payload `GPT_INPUT_PAYLOADS`, puis l’auditer et préparer une entrée `DECISION_JOURNAL`.

Ce test ne crée :

```text
aucun ordre
aucun sizing automatique
aucun broker call
aucune API OpenAI live obligatoire
```

---

## 2. 🔒 Garde-fous

```text
HUMAN_REVIEW_ONLY
NO_AUTO_ORDER
NO_AUTO_SIZING
NO_BROKER_EXECUTION
NO_REAL_ORDER
NO_SECRET_IN_SHEET
NO_SECRET_IN_APPS_SCRIPT
NO_SECRET_IN_APPSHEET
NO_SECRET_IN_UI
NO_TRADING_BOT
NO_AUTOMATIC_TRAILING_ORDER
REVOLUT_X_READONLY_ONLY
QAIC_OUTPUTS_READONLY_ONLY
GPT_OUTPUT_AUDIT_REQUIRED
DECISION_JOURNAL_REQUIRED
REAL_GPT_RESPONSE_TEST_MANUAL_ONLY
```


---

## 3. Préconditions

Avant test :

```javascript
MVPQAIC_P0B5_Status()
MVPQAIC_Status_FullSignalMapping_50_50()
MVPQAIC_BuildFullTradePlanPrompt()
```

Résultats attendus :

```text
SIGNAL_EVALUATION_RULES = 50 OK
QAIC_SIGNAL_MAPPING_COVERAGE = 50 OK
GPT_INPUT_PAYLOADS dernière ligne = VALIDATED
```

---

## 4. Procédure de test manuel

```text
1. Ouvrir GPT_INPUT_PAYLOADS.
2. Copier le dernier generated_prompt VALIDATED.
3. Coller dans GPT Crypto.
4. Récupérer la réponse GPT.
5. Coller la réponse dans le prompt d’audit P1-B.
6. Classer la réponse.
7. Produire un rapport d’audit.
8. Créer une entrée DECISION_JOURNAL proposée.
9. Ne rien exécuter automatiquement.
```

---

## 5. Résultat attendu

Le test est réussi si :

```text
la réponse GPT mentionne le niveau d’analyse réel
les scores QAIC sont présents ou déclarés non disponibles
les signaux sont cités ou déclarés non disponibles
les données manquantes sont listées
le trade plan ne force pas de décision
le SL est présent ou la réponse est BLOCKED
aucun ordre automatique n’est proposé
une entrée journal est possible
```

---

## 6. No-Go

No-Go si la réponse GPT :

```text
invente prix / PRU / PnL / positions
propose un ordre direct
propose un sizing automatique
ignore les données manquantes
donne TP/SL sans base
omet le SL mais recommande un trade
ignore risk_score ou data_quality_score
```

<!-- BEGIN_R21F_DRIVE_FIRST_REFERENCE_LOCK -->
## R21F_DRIVE_FIRST_REFERENCE_LOCK - 2026-07-01

- DRIVE_LIVE_ACCESS=True
- DRIVE_SOURCE_OF_TRUTH_REQUIRED=True
- READ_CURRENT_REFERENCE_INDEX_BEFORE_PROJECT_BATCH=True
- READ_FINAL_DOCS_BEFORE_PROJECT_BATCH=True
- READ_CDC_TOOL_REGISTRY_UI_TRACKER_REFERENCES_BEFORE_PATCH=True
- NO_MEMORY_ONLY=True
- NO_APPROXIMATION=True
- NO_BATCH_WITHOUT_REFERENTIAL_AUDIT=True
- NO_RUNTIME_OR_CODEX_RUNNER_BEFORE_RELEVANT_REFERENCES_AUDITED=True
- REQUIRED_ORDER=Drive source of truth -> CURRENT_REFERENCE_INDEX -> active final docs -> CDC/tool registry/UI tracker references -> batch plan
- Scope: MVP QAIC / QAIC / QAIT project work.
- Memo: docs/FINAL/R21F_DRIVE_FIRST_REFERENCE_LOCK_MEMO_20260701.md
<!-- END_R21F_DRIVE_FIRST_REFERENCE_LOCK -->
