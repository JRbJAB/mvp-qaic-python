# 🛠️ MVP QAIC — Mémo situation Phase 4 → Version finale livrable

**Date :** 2026-06-13  
**Statut :** `PHASE_4_LEXIQUE_EXISTING_CONSOLIDATION_IN_PROGRESS`  
**Priorité projet :** batchs complets, scripts fusionnés, dev utile, zéro empilement inutile.

---

## 1. Cadre projet confirmé

Le projet **MVP QAIC — Crypto Signal OS** est un MVP crypto **Lexique-first**, éducatif, analytique et décisionnel.

Objectif final : transformer le lexique crypto, les méthodes d’analyse et les signaux trading en une base exploitable par :

- une Knowledge Base structurée ;
- des prompts contrôlés ;
- des règles de scoring explicables ;
- des risk guards ;
- des checklists ;
- un journal de décision ;
- une future Web App / interface utilisateur ;
- une transition ultérieure vers QAIC complet.

Règles absolues :

```text
HUMAN_REVIEW_ONLY
NO_AUTO_ORDER
NO_AUTO_SIZING
NO_BROKER_EXECUTION
NO_REAL_ORDER
NO_SECRET_IN_SHEET
NO_SECRET_IN_APPS_SCRIPT
NO_TRADING_BOT
REVOLUT_X_READONLY_ONLY
```

---

## 2. Discipline de développement actée

Décision forte : priorité aux **batchs complets**, pas aux micro-patches.

Règles désormais actives :

- toujours partir de la version source exacte fournie ou confirmée ;
- éviter les scripts doublons ;
- fusionner dans les scripts durables existants quand c’est cohérent ;
- livrer des scripts complets remplaçables ;
- produire ZIP + README + manifest pour chaque batch important ;
- ne pas créer de nouvel onglet sauf nécessité démontrée ;
- ne pas empiler les cockpits/gouvernance ;
- privilégier le dev utile métier ;
- ne pas lancer d’actions destructives ;
- ne pas modifier menu/trigger sauf batch explicitement dédié et validé ;
- pas de test Gem relancé pendant la Phase 4 sauf décision explicite.

---

## 3. Workflow prompt P2 — état stabilisé

La chaîne prompt est considérée suffisante pour l’instant.

Onglets cœur :

```text
📘 PROMPT_LIBRARY
🧪 GPT_RESPONSE_INTAKE
🧾 DECISION_JOURNAL
🧭 PROMPT_IMPROVEMENT_QUEUE
🎛️ PROMPT_VARIANT_CONTROL_CENTER
```

État :

- référence prompt originale verrouillée ;
- variante `prompt_05_full_trading_review__Crypto_Trading_Investing__v20260612211346` prête ;
- tests Gem gelés ;
- cockpit principal stabilisé ;
- mapping boutons réalisé mais non prioritaire ;
- onglets support/dev masqués ou considérés non quotidiens.

Décision : ne plus investir dans la gouvernance P2 tant qu’un bug bloquant n’est pas constaté.

---

## 4. Phase 4 — Lexique / Méthodes / Signaux

Décision utilisateur : passer directement à la Phase 4 et revenir aux tests Gem plus tard.

Erreur corrigée : il ne faut pas créer un nouvel onglet central `LEXIQUE_METHODS_SIGNALS`.

Le système dispose déjà de tables métier existantes riches :

```text
📚 LEXIQUE_MASTER
🔎 SEARCH_COCKPIT
KNOWLEDGE_TERMS
METHOD_LIBRARY
SIGNAL_LIBRARY
SIGNAL_EVALUATION_RULES
QAIC_SIGNAL_MAPPING
QAIC_SIGNAL_MAPPING_COVERAGE
DATA_REQUIREMENTS
RISK_PLAYBOOK
DECISION_MATRIX
TOKEN_TYPE_PROFILES
TRADE_PLAN_METHODS
TP_SL_CALCULATION_RULES
TRAILING_PLAYBOOK
POSITION_FOLLOWUP_RULES
SCORING_MODEL_SPEC
OUTPUT_TEMPLATES
CHECKLISTS
DECISION_TEMPLATES
GLOSSARY_TAGS
```

Décision Phase 4 :

```text
📚 LEXIQUE_MASTER = frontend généré
🔎 SEARCH_COCKPIT = interface de recherche
les tables sources existantes restent les sources de vérité métier
```

---

## 5. Baseline Lexique officielle

Baseline validée et verrouillée :

```text
mvpqaic_31_lexique_master_search_cockpit_core.gs
MVP_QAIC_LEXIQUE_MASTER_SEARCH_COCKPIT_CORE_0.9.0_FINAL_SIMPLE_SAFE
```

Purpose de la baseline :

- arrêter la création de doublons lexique/méthodes/signaux ;
- construire un seul index frontend `📚 LEXIQUE_MASTER` ;
- construire un seul cockpit de recherche `🔎 SEARCH_COCKPIT` ;
- lire seulement les sources existantes ;
- ne pas delete/hide/rename/trigger/network/broker/secret.

Run validé :

```text
MVPQAIC_LexiqueMasterVersion()
version = MVP_QAIC_LEXIQUE_MASTER_SEARCH_COCKPIT_CORE_0.9.0_FINAL_SIMPLE_SAFE
status = OK
source_sheets_count = 19
```

---

## 6. P3-A.1 — Audit Lexique strict baseline 0.9.0

Correction majeure : P3-A a été refusionné proprement depuis la baseline exacte `0.9.0_FINAL_SIMPLE_SAFE`.

Version audit validée :

```text
MVP_QAIC_P3A1_EXISTING_LEXIQUE_GAP_AUDIT_STRICT_0_9_0_BASELINE_FUSION_1.4.1_SAFE
```

Run validé :

```text
status = OK
source_sheets_checked = 21
missing_source_sheets = []
audit_sheet = 🧪 LEXIQUE_GAP_AUDIT
gaps_written = 75
p0_count = 0
p1_count = 0
p2_count = 75
pass_count = 0
missing_source_sheets_count = 0
lexique_master_rows = 478
signal_library_rows = 50
signal_rules_rows = 50
qaic_mapping_rows = 57
policy = AUDIT_EXISTING_TABLES_ONLY_NO_REBUILD_NO_NEW_LEXIQUE_MASTER
```

Lecture :

```text
Aucun blocage runtime.
Aucun gap P0.
Aucun gap P1.
75 gaps P2 = enrichissement qualité, pas urgence.
```

---

## 7. P3-B — Enrichment Queue & Apply-Safe

Batch livré :

```text
MVP_QAIC_P3B_LEXIQUE_ENRICHMENT_QUEUE_APPLY_SAFE_1.4.2_SAFE
```

Objectif :

- utiliser `🧪 LEXIQUE_GAP_AUDIT` existant ;
- créer une queue d’enrichissement révisable ;
- proposer des corrections uniquement si déductibles ;
- ne rien appliquer sans validation humaine ;
- ne pas reconstruire `📚 LEXIQUE_MASTER` ;
- ne pas créer de nouveau lexique central.

Fonctions prévues :

```javascript
MVPQAIC_P3B_LexiqueEnrichmentQueueStatus()
MVPQAIC_P3B_LexiqueEnrichmentQueuePrepare()
MVPQAIC_P3B_LexiqueApplyReviewedSafe()
```

À lancer maintenant :

```javascript
MVPQAIC_P3B_LexiqueEnrichmentQueueStatus()
MVPQAIC_P3B_LexiqueEnrichmentQueuePrepare()
```

À ne pas lancer tant qu’aucune ligne n’est revue :

```javascript
MVPQAIC_P3B_LexiqueApplyReviewedSafe()
```

Condition d’application :

```text
review_decision = APPROVE_APPLY
```

---

## 8. Prochaines étapes jusqu’à version finale

### P3-B — Revue queue enrichissement

Objectif : obtenir une queue claire des 75 gaps P2.

À faire :

```text
1. préparer la queue depuis 🧪 LEXIQUE_GAP_AUDIT
2. inspecter les propositions
3. approuver uniquement les lignes sûres
4. ne rien inventer si information non déductible
```

Sortie attendue :

```text
APPROVED_APPLY
MANUAL_REVIEW
REJECT_NO_ACTION
NEEDS_SOURCE_DECISION
```

---

### P3-C — Apply-safe enrichissement sources

Objectif : appliquer uniquement les enrichissements validés.

Règles :

```text
no overwrite non vide
no blind apply
no source table destructive write
no Lexique Master direct edit
```

Après apply :

```text
relancer MVPQAIC_LexiqueMasterRunAllFast()
relancer MVPQAIC_SearchCockpitRefresh()
relancer P3-A audit pour vérifier baisse des gaps
```

---

### P3-D — Lexique → Prompt Bridge

Objectif : relier le lexique enrichi aux prompts.

À faire :

```text
mapping prompt_id ↔ signal_family
mapping prompt_id ↔ required_data
mapping prompt_id ↔ risk_guard
mapping prompt_id ↔ output_template
```

Livrable attendu :

```text
PROMPT_LEXIQUE_BRIDGE
ou enrichissement contrôlé de 📘 PROMPT_LIBRARY si structure suffisante
```

Attention : ne pas multiplier les onglets. Préférer enrichissement d’existant.

---

### P3-E — Prompt Library Update depuis Lexique

Objectif : que les prompts n’utilisent plus une logique générique.

À faire :

```text
ajouter signal_id obligatoires
ajouter score_id attendus
ajouter required_data par cas
ajouter blockers
ajouter risk guards
ajouter fallback_if_missing
standardiser format réponse
```

---

### P3-F — Reprise test Gem

Objectif : tester les prompts enrichis avec le Gem `Crypto Trading & Investing`.

Ordre :

```text
1. prompt_05_full_trading_review
2. prompt_01_portfolio_analysis
3. prompt_02_market_analysis
4. prompt_03_buy_analysis_multi_horizon
5. prompt_04_volatile_leverage_analysis
```

Règle :

```text
1 prompt
1 variante si besoin
1 test
1 journal
1 décision humaine
```

---

### P4 — Web App / UI MVP

Objectif : transformer le workflow Sheets en expérience utilisateur plus simple.

Socle :

```text
📚 LEXIQUE_MASTER
🔎 SEARCH_COCKPIT
📘 PROMPT_LIBRARY
🧪 GPT_RESPONSE_INTAKE
🧾 DECISION_JOURNAL
🎛️ PROMPT_VARIANT_CONTROL_CENTER
```

Cible :

```text
Web App / AppSheet / Looker Studio / Antigravity / Stitch
```

Pas avant stabilisation P3.

---

### P5 — QAIC Bridge progressif

Objectif : préparer l’intégration future QAIC complet sans importer son runtime lourd.

À faire :

```text
aligner signal_id
aligner score_id
aligner risk_guard
aligner output contracts
préparer bridge read-only
```

---

### Version finale MVP livrable

Version finale attendue :

```text
MVP_QAIC_CRYPTO_SIGNAL_OS_LEXIQUE_FIRST_1.0.0
```

Critères de sortie :

```text
✅ sources lexique consolidées
✅ LEXIQUE_MASTER reconstruit proprement
✅ SEARCH_COCKPIT utilisable quotidiennement
✅ prompts reliés au lexique
✅ risk guards intégrés
✅ journal décisionnel fonctionnel
✅ tests Gem documentés
✅ pas de trading automatique
✅ pas de broker/order/sizing
✅ documentation CDC / planning / instructions à jour
✅ ZIP final Drive-ready
```

---

## 9. Règles de reprise prochaine discussion

À rappeler en ouverture :

```text
On reprend MVP QAIC Phase 4.
Priorité batch complet.
Ne pas créer de nouvel onglet si l’existant suffit.
Ne pas micro-patcher.
Partir de la baseline mvpqaic_31 version 0.9.0 stricte.
P3-A.1 audit validé : 75 gaps P2, aucun P0/P1.
Prochaine action : P3-B queue enrichment status + prepare, pas apply direct.
```

