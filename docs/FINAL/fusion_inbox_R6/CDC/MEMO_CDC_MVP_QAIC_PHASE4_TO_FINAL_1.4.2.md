# 🛠️ MVP QAIC — Mémo CDC de situation vers version finale livrable

**Version :** `MVP_QAIC_CDC_SITUATION_TO_FINAL_MEMO_1.4.2`  
**Date :** 2026-06-13  
**Statut :** `PHASE_4_LEXIQUE_USEFUL_DEV_RESUMED`  
**Projet :** 🛠️ MVP QAIC — Crypto Signal OS

---

## 1. Situation actuelle validée

Le projet est revenu sur une trajectoire utile : **Lexique / Méthodes / Signaux**.

La base technique validée côté Lexique est maintenant :

- `mvpqaic_31_lexique_master_search_cockpit_core.gs`
- baseline stricte : `MVP_QAIC_LEXIQUE_MASTER_SEARCH_COCKPIT_CORE_0.9.0_FINAL_SIMPLE_SAFE`
- audit ajouté : `MVP_QAIC_P3A1_EXISTING_LEXIQUE_GAP_AUDIT_STRICT_0_9_0_BASELINE_FUSION_1.4.1_SAFE`
- prochain batch : `MVP_QAIC_P3B_LEXIQUE_ENRICHMENT_QUEUE_APPLY_SAFE_1.4.2_SAFE`

État runtime confirmé :

```text
LEXIQUE_MASTER rows = 478
SIGNAL_LIBRARY rows = 50
SIGNAL_EVALUATION_RULES rows = 50
QAIC_SIGNAL_MAPPING rows = 57
P3-A gaps = 75
P0 = 0
P1 = 0
P2 = 75
missing_source_sheets = 0
```

Lecture : aucun blocage runtime. Les 75 gaps sont de l’enrichissement qualité.

---

## 2. Décision de gouvernance immédiate

La règle projet est désormais : **priorité batch complet**.

À ne plus faire :

- micro-patches successifs sauf blocker réel ;
- nouveaux onglets de gouvernance non nécessaires ;
- nouveau lexique central redondant ;
- reconstruction de tables sources sans preuve ;
- application automatique de corrections métier.

À faire :

- travailler sur les tables existantes ;
- garder `📚 LEXIQUE_MASTER` comme frontend généré ;
- garder `🔎 SEARCH_COCKPIT` comme interface de recherche ;
- enrichir les sources uniquement après queue révisable ;
- appliquer seulement les corrections approuvées humainement.

---

## 3. Architecture CDC actuelle

### Sources métier existantes

Les sources métier restent les tables spécialisées :

- `KNOWLEDGE_TERMS`
- `GLOSSARY_TAGS`
- `METHOD_LIBRARY`
- `SIGNAL_LIBRARY`
- `SIGNAL_EVALUATION_RULES`
- `QAIC_SIGNAL_MAPPING`
- `QAIC_SIGNAL_MAPPING_COVERAGE`
- `DATA_REQUIREMENTS`
- `RISK_PLAYBOOK`
- `DECISION_MATRIX`
- `TOKEN_TYPE_PROFILES`
- `TRADE_PLAN_METHODS`
- `TP_SL_CALCULATION_RULES`
- `TRAILING_PLAYBOOK`
- `POSITION_FOLLOWUP_RULES`
- `SCORING_MODEL_SPEC`
- `OUTPUT_TEMPLATES`
- `CHECKLISTS`
- `DECISION_TEMPLATES`

### Frontend généré

- `📚 LEXIQUE_MASTER` : index consolidé généré depuis les sources.
- `🔎 SEARCH_COCKPIT` : recherche quotidienne dans le lexique.

### Workflow prompt déjà stabilisé

- `📘 PROMPT_LIBRARY`
- `🧪 GPT_RESPONSE_INTAKE`
- `🧾 DECISION_JOURNAL`
- `🧭 PROMPT_IMPROVEMENT_QUEUE`
- `🎛️ PROMPT_VARIANT_CONTROL_CENTER`

---

## 4. Phase actuelle : P3-B

### Objectif P3-B

Transformer l’audit P3-A en queue d’enrichissement exploitable :

```text
🧪 LEXIQUE_GAP_AUDIT
→ review_decision
→ proposed_value
→ proposal_confidence
→ apply_mode
→ apply_status
```

P3-B ne doit pas appliquer automatiquement les 75 gaps.

### Règle d’application

Une correction ne peut être appliquée que si :

- `review_decision = APPROVE_APPLY`
- `target_sheet` est une source, pas `📚 LEXIQUE_MASTER`
- `target_column` est unique
- `source_row` est valide
- `proposed_value` est non vide
- la cellule cible est vide

Aucun overwrite n’est autorisé.

---

## 5. Roadmap utile vers version finale livrable

### P3-B — Enrichment Queue & Apply-Safe

Créer la queue, proposer des valeurs déduites des champs existants, appliquer uniquement les lignes approuvées.

### P3-C — Source Enrichment Review Batch

Repasser sur les lignes appliquées / bloquées / à compléter manuellement.

### P3-D — Rebuild frontend contrôlé

Relancer :

```javascript
MVPQAIC_LexiqueMasterRunAllFast()
MVPQAIC_SearchCockpitRefresh()
```

Puis vérifier que les enrichissements sources remontent dans `📚 LEXIQUE_MASTER`.

### P3-E — Lexique → Prompt Bridge

Relier les concepts, signaux, règles, blockers et risk guards aux prompts :

- `prompt_01_portfolio_analysis`
- `prompt_02_market_analysis`
- `prompt_03_buy_analysis_multi_horizon`
- `prompt_04_volatile_leverage_analysis`
- `prompt_05_full_trading_review`

### P3-F — Prompt useful tests

Reprendre les tests Gem uniquement après enrichissement Lexique suffisant.

### P4 — Web App MVP

Préparer l’interface Web App / Antigravity / Stitch autour du lexique, recherche, prompt, journal et cockpit.

### P5 — QAIC Bridge progressif

Relier progressivement le MVP au QAIC final, sans trading automatique.

---

## 6. Livrable final attendu

La version finale MVP livrable doit fournir :

- un référentiel Lexique / Méthodes / Signaux propre ;
- un moteur de recherche quotidien ;
- une Prompt Library gouvernée ;
- une boucle réponse GPT → audit → journal → amélioration ;
- un Risk Playbook exploitable ;
- un Decision Journal auditable ;
- une interface MVP simple ;
- une passerelle future vers QAIC complet.

---

## 7. Garde-fous permanents

```text
HUMAN_REVIEW_ONLY
NO_AUTO_ORDER
NO_AUTO_SIZING
NO_BROKER_EXECUTION
NO_REAL_ORDER
NO_SECRET_IN_SHEET
NO_SECRET_IN_APPS_SCRIPT
NO_TRADING_BOT
NO_EXTERNAL_NETWORK_UNLESS_EXPLICITLY_APPROVED
```

---

## 8. Décision de clôture de situation

La situation actuelle est saine pour continuer :

```text
P2 workflow prompt = stabilisé
P3-A strict baseline = validé
P3-A audit = 75 gaps P2, aucun P0/P1
P3-B = queue d’enrichissement apply-safe
Priorité = batch complet utile
```

Prochaine étape après P3-B : enrichissement contrôlé, puis rebuild frontend, puis bridge Lexique → Prompt.
