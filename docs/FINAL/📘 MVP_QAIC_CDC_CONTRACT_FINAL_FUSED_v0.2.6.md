# MVP QAIC CDC Contract Final Fused v0.2.6
- Version: v0.2.6
- Status: FINAL_REFERENCE_READY_HUMAN_REVIEW
- Generated: 20260630_200005
- Mode: residual final docs fusion / no live broker / no delete
## Intent
Canonical CDC and contract reference after R6/R7/R7B residual fusion.
## Scope and safety
- This document consolidates the selected R6 fusion inbox and residual final-doc sources.
- Older source files are not deleted. Superseded material remains traceable through R5/R6/R7/R8/R9 reports.
- Google Drive cleanup is limited to archive moves; no content was deleted.
- This is a reference document for human review and implementation continuity.

## Source manifest
1. `docs/FINAL/fusion_inbox_R6/ARCHITECTURE/🧱 ARCHITECTURE_MVP_QAIC_LEXIQUE_FIRST_0.7.2_REAL_FULL_SOURCE_FUSION.md` (8554 bytes, sha256 `633070d246dbabb9...`)
2. `docs/FINAL/fusion_inbox_R6/ARCHITECTURE/🧱 ARCHITECTURE_MVP_QAIC_LEXIQUE_FIRST_APPSHEET_QAIC_PYTHON_0.6.2.md` (5112 bytes, sha256 `13ccb01776ce5724...`)
3. `docs/FINAL/fusion_inbox_R6/CDC/MEMO_CDC_MVP_QAIC_PHASE4_TO_FINAL_1.4.2.md` (5564 bytes, sha256 `6cc66445834a7116...`)
4. `docs/FINAL/fusion_inbox_R6/CDC/📘 CDC_MVP_QAIC_WEB_APP_LEXIQUE_FIRST_0.6.2_REAL_FUSION_REPAIR.md` (27670 bytes, sha256 `00f3d38c78243036...`)
5. `docs/FINAL/fusion_inbox_R6/CDC/📘 CDC_MVP_QAIC_WEB_APP_LEXIQUE_FIRST_0.7.2_REAL_FULL_SOURCE_FUSION.md` (31100 bytes, sha256 `c5d63c4b023d7671...`)
6. `docs/FINAL/fusion_inbox_R6/FINAL_FUSED/MVP_QAIC_PY/📘 MVP_QAIC_CDC_CONTRACT_FINAL_FUSED_v0.2.2.md` (113936 bytes, sha256 `aaeee5f4bc5685d2...`)
7. `docs/FINAL/fusion_inbox_R6/ARCHITECTURE/🧠 DECISION_JOURNAL_USAGE_AND_PROMPT_IMPROVEMENT_LOOP_0.4.6.md` (1183 bytes, sha256 `c43d2c50957cece3...`)
8. `docs/FINAL/fusion_inbox_R6/CDC/MEMO_MVP_QAIC_PHASE4_TO_FINAL_1.4.2.md` (9525 bytes, sha256 `c0c350b16cdf7904...`)
9. `docs/FINAL/fusion_inbox_R6/MANIFEST/manifest_MVPQAIC_REFERENCE_DOCS_0.6.2_REAL_FUSION_REPAIR.json` (2404 bytes, sha256 `e59413d199de9b63...`)
10. `docs/FINAL/fusion_inbox_R6/PLANNING/🗓️ PLANNING_MVP_QAIC_WEB_APP_TRANSITION_QAIC_0.6.2_REAL_FUSION_REPAIR.md` (26933 bytes, sha256 `6904e0a495e1789f...`)
11. `docs/FINAL/fusion_inbox_R6/PLANNING/🗓️ PLANNING_MVP_QAIC_WEB_APP_TRANSITION_QAIC_0.7.2_REAL_FULL_SOURCE_FUSION.md` (30379 bytes, sha256 `8aae0ef0fba8e5e1...`)
12. `docs/FINAL/fusion_inbox_R6/RUNBOOK/RUNBOOK_MVP_QAIC_P1G_PROMPT_LIBRARY_CONTRACT_0.6.0.md` (2066 bytes, sha256 `46a126ba79aaa331...`)

---

## Source 1: `docs/FINAL/fusion_inbox_R6/ARCHITECTURE/🧱 ARCHITECTURE_MVP_QAIC_LEXIQUE_FIRST_0.7.2_REAL_FULL_SOURCE_FUSION.md`

<!--
REAL FULL SOURCE FUSION 0.7.2
Source original preserved: 🧱 ARCHITECTURE_MVP_QAIC_LEXIQUE_FIRST_APPSHEET_QAIC_PYTHON_0.6.2.md
Source SHA256: 13ccb01776ce5724ee020e4ee3f14d7c1be9c09dc7dddde1d00a319105d49706
Source lines: 138
Fusion rule: original content is kept, then a scope-split correction block is appended.
No Drive overwrite. No Apps Script run. No clasp push.
-->

# 🧱 Architecture — MVP QAIC Lexique-first, AppSheet & Transition QAIC Python — 0.6.2 REAL FUSION REPAIR

> **Projet :** 🛠️ MVP QAIC — Crypto Signal OS Web App
> **Version :** `MVP_QAIC_ARCHITECTURE_0.6.2_REAL_FUSION_REPAIR`
> **Date :** 2026-06-16
> **Statut :** `DRAFT_FOR_HUMAN_VALIDATION`
> **Source :** consolidation réelle CDC 0.3.1 + Planning 0.3.1 + Instructions 0.5.0 + décisions AppSheet/P5 + corrections Portfolio/Broker.

## 1. Architecture cible par couches

| Couche | Outil | Rôle immédiat | Rôle futur |
|---|---|---|---|
| Knowledge | Google Sheets / AppSheet | Lexique, méthodes, signaux, risk playbook | Source consultable et filtrable |
| Prompt OS | Sheets / AppSheet | Prompts 1–5, queue, response intake | Prompt Launcher intelligent |
| Journal | Sheets / AppSheet | Décisions humaines, blockers, missing data | Audit trail QAIC |
| Portfolio | Revolut X read-only / Sheets | Consultation exposition | Risk Gate portfolio |
| Alertes | Sheets / Apps Script / AppSheet | Alertes données/risque | Notifications contrôlées |
| Tickets | Sheets / AppSheet | Manual Trade Tickets | Pré-ordre humain |
| Simulation | QAIC Python | Paper trading | Backtest/dry-run |
| Broker Adapter | QAIC Python / backend sécurisé | Aucun live par défaut | Dry-run puis live gated |


## 📱 État AppSheet MVP validé au 2026-06-16

### Tables MVP injectées

| Table | Rôle | Statut |
|---|---|---|
| `SEARCH_COCKPIT` | Recherche lexique/méthodes/signaux | OK |
| `LEXIQUE_MASTER` | Source lexique principale | OK |
| `PROMPT_LEXIQUE_BRIDGE` | Bridge prompts ↔ lexique | REVIEW clé à améliorer |
| `PROMPT_CONTEXT_PACKS` | Packs contexte prompts | REVIEW clé/colonnes à améliorer |
| `PROMPT_LIBRARY` | Bibliothèque prompts | OK |
| `PROMPT_READY_TO_COPY` | Prompts prêts à copier | REVIEW clé à améliorer |
| `PROMPT_RUN_QUEUE` | Queue de run manuel | OK, `run_queue_id` clé |
| `RESPONSE_INTAKE_QUEUE` | Intake réponse Gem/GPT | OK, `intake_queue_id` clé |
| `JOURNAL_APPEND_QUEUE` | Pré-journalisation | OK, `journal_queue_id` clé |
| `DECISION_JOURNAL` | Journal officiel décisions | OK, `journal_id` clé |

### Vues MVP validées

| Vue | Source | Usage |
|---|---|---|
| `MVP QAIC Home` | `SEARCH_COCKPIT` | Accueil/recherche |
| `Lexique` | `LEXIQUE_MASTER` | Consultation lexique |
| `Prompts Ready` | `PROMPT_READY_TO_COPY` | Prompts prêts à copier |
| `Run Queue` | `PROMPT_RUN_QUEUE` | Flux manuel prompt → réponse |
| `Decision Journal` | `DECISION_JOURNAL` | Audit read-only |

### Règle AppSheet actuelle

```text
App non déployée.
Build manuel.
Pas d’automation AppSheet.
Pas d’action broker.
Pas d’ordre.
Pas de sizing.
Affinage UX après validation structurelle.
```

---



## 💼 Portfolio Revolut X & transition exécution contrôlée

### Priorité produit

Le portefeuille Revolut X n’est **pas reporté hors trajectoire**. Il est intégré comme axe prioritaire après stabilisation du socle Lexique/Prompts/Journal.

| Niveau | Fonction | Autorisation |
|---:|---|---|
| 1 | Consultation portfolio Revolut X | Read-only |
| 2 | Analyse exposition/risque | Read-only + prompts |
| 3 | Alertes portefeuille | Notification / review only |
| 4 | Tickets manuels | Préparation d’action humaine |
| 5 | Paper trading | Simulation contrôlée |
| 6 | Dry-run broker | Test sans ordre réel |
| 7 | Exécution réelle assistée | Uniquement après gates séparés |
| 8 | TP/SL/trailing automatique | Uniquement après architecture QAIC Python sécurisée |

### Ce qui doit être construit progressivement

```text
Portfolio Revolut X read-only
→ Prompt 1 Portfolio Analysis
→ Prompt 5 Full Trading Review
→ Risk Gate
→ Alert Center
→ Manual Trade Ticket
→ Paper Trading
→ Dry-run Broker Adapter
→ QAIC Python Broker Adapter
→ Exécution live seulement après GO explicite, kill switch, logs, secrets sécurisés et validations.
```

### Garde-fous obligatoires

| Domaine | Garde-fou |
|---|---|
| Secrets | Secret Manager / jamais dans Sheets / Apps Script / Drive |
| Exécution | Kill switch visible et testé |
| Données | Vérification freshness, source, prix, PRU, quantité, exposition |
| Risque | Max exposure, concentration, NO_ADD, REDUCE_RISK_REVIEW, BLOCK |
| Logs | Journal immuable / run_id / timestamp / payload_id |
| Validation humaine | Human approval avant tout ordre réel |
| Tests | Paper trading puis dry-run avant live |

---


## 2. Flux d’usage prioritaire

```text
Lexique Master
→ Prompt Launcher 1–5
→ Run Queue
→ Gem / ChatGPT
→ Response Intake
→ Journal Append Queue
→ Decision Journal
→ Portfolio Revolut X read-only
→ Alert Center
→ Manual Trade Ticket
→ Paper Trading / Dry-run QAIC Python
```

## 3. Non-négociables d’architecture

```text
Pas de secret dans Sheets, Apps Script ou Drive.
Pas d’ordre réel depuis AppSheet.
Pas de sizing réel automatique en MVP actuel.
Toute exécution future passe par QAIC Python/backend sécurisé.
Tout signal est croisé avec Data Quality + Portfolio + Risk Guard + Human Review.
```
---

# ✅ FUSION 0.7.2 — Scope Split MVP / QAIC Engine

> **Patch fusionnel ajouté au document original complet**
> **Projet :** 🛠️ MVP QAIC — Crypto Signal OS
> **Version fusionnée :** `0.7.2_REAL_FULL_SOURCE_FUSION_SCOPE_SPLIT`
> **Date :** 2026-06-20
> **Statut :** `READY_FOR_HUMAN_REVIEW_NON_DESTRUCTIVE`
> **Méthode :** contenu original 0.6.2 conservé intégralement, puis correction de doctrine ajoutée sans suppression.

## 0. Décision de programme validée

```text
MVP QAIC = Lexique / méthodes / signaux / Knowledge Base / WebApp pédagogique
QAIC = moteur calcul, trading analytics, portefeuille, risk engine, Revolut API
```

## 1. Correction de doctrine à appliquer à ce document

Toute mention historique du type :

```text
Portfolio Revolut X dans MVP
Revolut API dans MVP
QAIC Python broker adapter dans MVP
paper trading / dry-run / execution contrôlée dans MVP
scoring trading final dans MVP
risk engine portfolio dans MVP
```

doit être lue comme :

```text
Ces éléments relèvent de QAIC Engine.
Le MVP ne conserve que l'explication pédagogique, l'affichage contrôlé, les mappings et les contrats d'import des sorties QAIC.
```

## 2. Frontière officielle

| Domaine | Responsable officiel |
|---|---|
| Lexique crypto | MVP |
| Méthodes / signaux expliqués | MVP |
| WebApp privée / search cockpit | MVP |
| Knowledge Base / source registry | MVP |
| Journal human review pédagogique | MVP |
| Affichage de sorties QAIC | MVP via import contrôlé |
| Calculs trading | QAIC |
| Portefeuille / exposition | QAIC |
| Revolut API | QAIC |
| Risk engine final | QAIC |
| Broker adapter / dry-run / exécution future | QAIC, hors MVP |

## 3. Règles non négociables MVP

```text
NO_REVOLUT_API_IN_MVP = TRUE
NO_TRADING_ENGINE_IN_MVP = TRUE
NO_PORTFOLIO_ENGINE_IN_MVP = TRUE
NO_ORDER_IN_MVP = TRUE
NO_SIZING_IN_MVP = TRUE
NO_BROKER_EXECUTION_IN_MVP = TRUE
NO_SECRET_IN_MVP = TRUE
HUMAN_REVIEW_ONLY = TRUE
```

## 4. Ce qui reste autorisé dans le MVP

```text
- expliquer les concepts trading ;
- documenter Night Watch / trade nocturne comme méthode pédagogique ;
- afficher un output QAIC importé en lecture contrôlée ;
- journaliser la décision humaine ;
- montrer missing_data / blockers / source provenance ;
- relier une fiche lexique à un output QAIC par référence.
```

## 5. Ce qui est transféré à QAIC

```text
- Revolut provider Python ;
- API keys / signatures / secrets ;
- calculs de portefeuille ;
- calculs de signaux ;
- scoring trading officiel ;
- risk engine trading ;
- dry-run / paper trading / broker adapter ;
- toute exécution future, même contrôlée.
```

## 6. Impact spécifique sur `ARCHITECTURE`

Ce document reste source valide pour son contenu historique et structurel, mais ses passages liés à Revolut, portfolio, broker, paper trading, dry-run ou calcul trading sont **superseded** par cette correction 0.7.2.

```text
MVP_SCOPE = LEXIQUE_KB_WEBAPP_ONLY
QAIC_SCOPE = CALC_TRADING_REVOLUT_ENGINE
QAIC_BRIDGE_IN_MVP = OUTPUT_IMPORT_AND_DISPLAY_ONLY
```

## Source 2: `docs/FINAL/fusion_inbox_R6/ARCHITECTURE/🧱 ARCHITECTURE_MVP_QAIC_LEXIQUE_FIRST_APPSHEET_QAIC_PYTHON_0.6.2.md`

# 🧱 Architecture — MVP QAIC Lexique-first, AppSheet & Transition QAIC Python — 0.6.2 REAL FUSION REPAIR

> **Projet :** 🛠️ MVP QAIC — Crypto Signal OS Web App
> **Version :** `MVP_QAIC_ARCHITECTURE_0.6.2_REAL_FUSION_REPAIR`
> **Date :** 2026-06-16
> **Statut :** `DRAFT_FOR_HUMAN_VALIDATION`
> **Source :** consolidation réelle CDC 0.3.1 + Planning 0.3.1 + Instructions 0.5.0 + décisions AppSheet/P5 + corrections Portfolio/Broker.

## 1. Architecture cible par couches

| Couche | Outil | Rôle immédiat | Rôle futur |
|---|---|---|---|
| Knowledge | Google Sheets / AppSheet | Lexique, méthodes, signaux, risk playbook | Source consultable et filtrable |
| Prompt OS | Sheets / AppSheet | Prompts 1–5, queue, response intake | Prompt Launcher intelligent |
| Journal | Sheets / AppSheet | Décisions humaines, blockers, missing data | Audit trail QAIC |
| Portfolio | Revolut X read-only / Sheets | Consultation exposition | Risk Gate portfolio |
| Alertes | Sheets / Apps Script / AppSheet | Alertes données/risque | Notifications contrôlées |
| Tickets | Sheets / AppSheet | Manual Trade Tickets | Pré-ordre humain |
| Simulation | QAIC Python | Paper trading | Backtest/dry-run |
| Broker Adapter | QAIC Python / backend sécurisé | Aucun live par défaut | Dry-run puis live gated |


## 📱 État AppSheet MVP validé au 2026-06-16

### Tables MVP injectées

| Table | Rôle | Statut |
|---|---|---|
| `SEARCH_COCKPIT` | Recherche lexique/méthodes/signaux | OK |
| `LEXIQUE_MASTER` | Source lexique principale | OK |
| `PROMPT_LEXIQUE_BRIDGE` | Bridge prompts ↔ lexique | REVIEW clé à améliorer |
| `PROMPT_CONTEXT_PACKS` | Packs contexte prompts | REVIEW clé/colonnes à améliorer |
| `PROMPT_LIBRARY` | Bibliothèque prompts | OK |
| `PROMPT_READY_TO_COPY` | Prompts prêts à copier | REVIEW clé à améliorer |
| `PROMPT_RUN_QUEUE` | Queue de run manuel | OK, `run_queue_id` clé |
| `RESPONSE_INTAKE_QUEUE` | Intake réponse Gem/GPT | OK, `intake_queue_id` clé |
| `JOURNAL_APPEND_QUEUE` | Pré-journalisation | OK, `journal_queue_id` clé |
| `DECISION_JOURNAL` | Journal officiel décisions | OK, `journal_id` clé |

### Vues MVP validées

| Vue | Source | Usage |
|---|---|---|
| `MVP QAIC Home` | `SEARCH_COCKPIT` | Accueil/recherche |
| `Lexique` | `LEXIQUE_MASTER` | Consultation lexique |
| `Prompts Ready` | `PROMPT_READY_TO_COPY` | Prompts prêts à copier |
| `Run Queue` | `PROMPT_RUN_QUEUE` | Flux manuel prompt → réponse |
| `Decision Journal` | `DECISION_JOURNAL` | Audit read-only |

### Règle AppSheet actuelle

```text
App non déployée.
Build manuel.
Pas d’automation AppSheet.
Pas d’action broker.
Pas d’ordre.
Pas de sizing.
Affinage UX après validation structurelle.
```

---



## 💼 Portfolio Revolut X & transition exécution contrôlée

### Priorité produit

Le portefeuille Revolut X n’est **pas reporté hors trajectoire**. Il est intégré comme axe prioritaire après stabilisation du socle Lexique/Prompts/Journal.

| Niveau | Fonction | Autorisation |
|---:|---|---|
| 1 | Consultation portfolio Revolut X | Read-only |
| 2 | Analyse exposition/risque | Read-only + prompts |
| 3 | Alertes portefeuille | Notification / review only |
| 4 | Tickets manuels | Préparation d’action humaine |
| 5 | Paper trading | Simulation contrôlée |
| 6 | Dry-run broker | Test sans ordre réel |
| 7 | Exécution réelle assistée | Uniquement après gates séparés |
| 8 | TP/SL/trailing automatique | Uniquement après architecture QAIC Python sécurisée |

### Ce qui doit être construit progressivement

```text
Portfolio Revolut X read-only
→ Prompt 1 Portfolio Analysis
→ Prompt 5 Full Trading Review
→ Risk Gate
→ Alert Center
→ Manual Trade Ticket
→ Paper Trading
→ Dry-run Broker Adapter
→ QAIC Python Broker Adapter
→ Exécution live seulement après GO explicite, kill switch, logs, secrets sécurisés et validations.
```

### Garde-fous obligatoires

| Domaine | Garde-fou |
|---|---|
| Secrets | Secret Manager / jamais dans Sheets / Apps Script / Drive |
| Exécution | Kill switch visible et testé |
| Données | Vérification freshness, source, prix, PRU, quantité, exposition |
| Risque | Max exposure, concentration, NO_ADD, REDUCE_RISK_REVIEW, BLOCK |
| Logs | Journal immuable / run_id / timestamp / payload_id |
| Validation humaine | Human approval avant tout ordre réel |
| Tests | Paper trading puis dry-run avant live |

---


## 2. Flux d’usage prioritaire

```text
Lexique Master
→ Prompt Launcher 1–5
→ Run Queue
→ Gem / ChatGPT
→ Response Intake
→ Journal Append Queue
→ Decision Journal
→ Portfolio Revolut X read-only
→ Alert Center
→ Manual Trade Ticket
→ Paper Trading / Dry-run QAIC Python
```

## 3. Non-négociables d’architecture

```text
Pas de secret dans Sheets, Apps Script ou Drive.
Pas d’ordre réel depuis AppSheet.
Pas de sizing réel automatique en MVP actuel.
Toute exécution future passe par QAIC Python/backend sécurisé.
Tout signal est croisé avec Data Quality + Portfolio + Risk Guard + Human Review.
```

## Source 3: `docs/FINAL/fusion_inbox_R6/CDC/MEMO_CDC_MVP_QAIC_PHASE4_TO_FINAL_1.4.2.md`

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

## Source 4: `docs/FINAL/fusion_inbox_R6/CDC/📘 CDC_MVP_QAIC_WEB_APP_LEXIQUE_FIRST_0.6.2_REAL_FUSION_REPAIR.md`

# 📘 CDC — MVP QAIC Web App Lexique-first

> **Projet :** 🛠️ MVP QAIC — Crypto Signal OS Web App
> **Version :** `MVP_QAIC_CDC_0.6.2_REAL_FUSION_REPAIR_APPSHEET_PORTFOLIO_BROKER_TRANSITION`
> **Date :** 2026-06-16
> **Statut :** `DRAFT_FOR_HUMAN_VALIDATION_REAL_FUSION_REPAIR`
> **Format :** Markdown `.md`

---

## 0. 🧾 Historique des changements

| Version | Date | Statut | Changements |
|---|---:|---|---|
| `0.1.0` | 2026-06-11 | Draft | Cadrage initial MVP QAIC Lexique-first |
| `0.2.0` | 2026-06-11 | Drive review ready | Reformulation : Web App rapide Lexique/Méthodes/Signaux d'abord, puis transition progressive vers le QAIC final comme UI / IDE utilisateur |
| `0.2.1` | 2026-06-11 | Drive structure final ready | Confirmation de la structure Drive finale avec ajout de `08_QAIC_BRIDGE/` et `09_WEB_APP_IDE/`, préparation import Drive, bridge QAIC et future UI / IDE QAIC |
| `0.2.2` | 2026-06-11 | Antigravity P0 process ready | Ajout du modus operandi Antigravity : workspace local, lots P0-A à P0-E, garde-fous, critères de validation, livrables attendus avant import Google |
| `0.3.1` | 2026-06-11 | P0-B6 Governance full fusion | Pleine fusion avec les documents 0.2.2 sans suppression ; ajout état P0-A→P0-B5, Full Signal Mapping 50/50, GPT/Revolut X read-only bridge, Runbook, Validation Matrix et prochaine phase P0-C |
| `0.6.2` | 2026-06-16 | Real fusion repair | Réparation après audit : reprise réelle du CDC 0.3.1, intégration AppSheet P5, priorité Lexique/Prompts, correction Portfolio Revolut X non reporté, préparation automation ordres/TP/SL/trailing via QAIC Python sous gates. |

---

## 1. 🎯 Vision produit

Le projet **🛠️ MVP QAIC — Crypto Signal OS Web App** vise à livrer rapidement une **Web App crypto éducative, analytique et décisionnelle**, centrée en priorité sur :

- le **lexique crypto** ;
- les **méthodes d’analyse** ;
- les **signaux trading** ;
- les **playbooks de risque** ;
- les **checklists quotidiennes** ;
- le **scoring explicable** ;
- le **journal de décision**.

Le MVP ne cherche pas à reproduire immédiatement tout le système QAIC complet. Il doit d’abord devenir un outil simple, rapide, lisible et utilisable au quotidien.

La trajectoire validée est double :

```text
Phase 1 — MVP Web App Lexique-first
→ livrer vite une Web App utile autour du lexique, des méthodes et des signaux

Phase 2 — Bridge QAIC
→ préparer les connecteurs et mappings vers l’outil QAIC final en cours de développement

Phase 3 — UI / IDE QAIC
→ transformer progressivement la Web App en interface utilisateur du QAIC complet
```

---

## 2. 🧠 Principe central : Lexique, méthodes et signaux d’abord

Le MVP démarre par la connaissance structurée, pas par un moteur de trading lourd.

```text
Lexique Crypto
↓
Knowledge Base
↓
Method Library
↓
Signal Library
↓
Risk Playbook
↓
Decision Checklist
↓
Scoring explicable
↓
Web App
↓
Journal de décision
```

Le lexique ne doit pas rester un document passif. Il devient :

| Élément du lexique | Transformation MVP |
|---|---|
| Terme crypto/trading | Fiche consultable et filtrable |
| Méthode | Procédure opérationnelle |
| Signal | Règle d’analyse et score partiel |
| Risque | Règle TP / SL / sizing / invalidation |
| Checklist | Routine d’usage quotidien |
| Template | Journal ou plan d’analyse |
| Indicateur | Champ manuel puis calculé plus tard |

---

## 3. 🧭 Positionnement fonctionnel

Le MVP est un **support à la décision**, pas un robot de trading.

Il sert à :

- comprendre les notions crypto/trading ;
- rechercher rapidement une méthode ou un signal ;
- structurer une analyse ;
- réduire les décisions impulsives ;
- standardiser les plans TP / SL ;
- expliquer les scores ;
- journaliser les décisions ;
- préparer l’intégration future du QAIC complet.

Il ne sert pas à :

- passer des ordres ;
- exécuter automatiquement des achats/ventes ;
- gérer un broker ;
- remplacer la revue humaine ;
- promettre une performance ;
- produire du conseil financier personnalisé.

---

## 4. 🧱 Périmètre MVP

### 4.1 Périmètre inclus P0

| Module | Priorité | Description |
|---|---:|---|
| 📚 Knowledge Base | P0 | Lexique structuré et consultable |
| 🔍 Search Engine | P0 | Recherche de termes, méthodes, signaux |
| 🧠 Method Library | P0 | Méthodes d’analyse structurées |
| ⚡ Signal Library | P0 | Signaux positifs, neutres, danger |
| 🛡️ Risk Playbook | P0 | TP1 / TP2 / TP3 / SL / sizing / invalidation |
| ✅ Daily Checklists | P0 | Routine matin / avant analyse / avant décision |
| 🧾 Decision Templates | P0 | Acheter, attendre, éviter, bloquer, revoir |
| 📝 Decision Journal | P0/P1 | Historique des décisions et justifications |

### 4.2 Périmètre P1

| Module | Priorité | Description |
|---|---:|---|
| 🧮 Scoring MVP | P1 | Score manuel ou semi-auto sur 100 |
| 📊 Dashboard simple | P1 | Vue synthétique des signaux et risques |
| 🧭 Daily Plan | P1 | Plan quotidien basé sur checklist + signaux |
| 🧩 AppSheet / Web App | P1 | Interface web/mobile rapide |
| 📈 Looker Studio | P1 | Dashboard visuel de suivi |

### 4.3 Périmètre P2 / transition QAIC

| Module | Priorité | Description |
|---|---:|---|
| 🔌 QAIC Outputs Import | P2 | Import progressif des outputs QAIC |
| 🗺️ QAIC Score Mapping | P2 | Mapping alpha/risk/confidence vers UI MVP |
| 🧪 Backtest Mapping | P2 | Restitution des validations backtest QAIC |
| 🧠 Advanced Decision UI | P2 | UI / IDE pour décision humaine assistée |
| 🗂️ BigQuery Bridge | P2/P3 | Uniquement quand les volumes ou historiques l’exigent |

---

## 5. ☁️ Écosystème Google retenu

### 5.1 Stack initiale

| Couche | Outil | Rôle |
|---|---|---|
| Dossier projet | Google Drive | Docs, exports, backups, ZIP |
| Base MVP | Google Sheets | Tables Knowledge, règles, journal, scoring |
| Automatisation | Apps Script | Setup, formatage, recherche, règles, scoring léger |
| Web App rapide | AppSheet | Interface mobile/web no-code rapide |
| Dashboard | Looker Studio | Synthèse visuelle |
| UI design | Google Stitch | Maquettes et design system |
| Développement agentique | Google Antigravity | Structuration, génération code, tests bornés |

### 5.2 Stack future possible

| Couche | Outil | Usage futur |
|---|---|---|
| Historique scalable | BigQuery | Historique, backtests, logs lourds |
| Backend avancé | Cloud Run | APIs, moteurs plus robustes |
| Auth / temps réel | Firebase | Version web avancée |
| Dev Factory | Python / local / Codex | QAIC avancé, tests, pipelines |

### 5.3 Règle d’or

BigQuery, Cloud Run et Python avancé ne doivent pas précéder le MVP Lexique-first. Ils ne sont activés que si :

- la Web App est utile ;
- les schémas sont stables ;
- les besoins d’historique ou d’intégration QAIC sont confirmés ;
- les coûts et la gouvernance sont maîtrisés.

---

## 6. 📁 Structure Drive cible

```text
🛠️ MVP QAIC — Crypto Signal OS/
│
├── 00_ADMIN/
│   ├── README_PROJECT.md
│   ├── CHANGELOG.md
│   └── DECISIONS_LOG.md
│
├── 01_DOCS/
│   ├── CDC/
│   ├── PLANNING/
│   ├── INSTRUCTIONS/
│   ├── RUNBOOK/
│   └── PROMPTS/
│
├── 02_SHEETS/
│   ├── DEV/
│   ├── EXPORTS_CSV/
│   └── BACKUPS/
│
├── 03_APPS_SCRIPT/
│   ├── SOURCE/
│   ├── BACKUPS/
│   └── ZIP/
│
├── 04_APPSHEET/
│   ├── SPEC/
│   └── SCREENSHOTS/
│
├── 05_LOOKER/
│   ├── DASHBOARD_SPEC/
│   └── EXPORTS/
│
├── 06_STITCH/
│   ├── PROMPTS/
│   └── UI_EXPORTS/
│
├── 07_ANTIGRAVITY/
│   ├── PROMPTS/
│   ├── TASKS/
│   └── OUTPUTS/
│
├── 08_QAIC_BRIDGE/
│   ├── IMPORT_SPECS/
│   ├── MAPPING/
│   └── OUTPUTS/
│
├── 09_WEB_APP_IDE/
│   ├── UI_SPEC/
│   ├── COMPONENTS/
│   └── USER_FLOWS/
│
└── 99_ARCHIVES/
```

### 6.1 Confirmation structure finale validée

La structure Drive finale est validée avec deux ajouts stratégiques par rapport à la version 0.2.0 :

| Dossier | Rôle | Pourquoi il est nécessaire |
|---|---|---|
| `08_QAIC_BRIDGE/` | Préparer l'import, le mapping et la restitution des outputs QAIC final | Évite de coupler trop tôt le MVP à QAIC tout en préparant la transition |
| `09_WEB_APP_IDE/` | Préparer la future UI / IDE utilisateur au-dessus du QAIC complet | Sépare clairement l'AppSheet/Web App rapide de l'interface avancée future |

Décision confirmée : le MVP reste d'abord une Web App rapide Lexique / Méthodes / Signaux, puis il récupère progressivement les outputs QAIC final via une couche bridge documentée et non bloquante.

---

## 7. 📊 Google Sheets DEV

Nom recommandé :

```text
MVP QAIC — Crypto Signal OS — DEV
```

### 7.1 Onglets P0

| Onglet | Rôle |
|---|---|
| `CONFIG` | Paramètres globaux |
| `KNOWLEDGE_TERMS` | Définitions crypto/trading structurées |
| `METHOD_LIBRARY` | Méthodes d’analyse |
| `SIGNAL_LIBRARY` | Signaux trading |
| `RISK_PLAYBOOK` | TP / SL / sizing / invalidation |
| `MARKET_REGIME_RULES` | Règles BTC risk-on/risk-off |
| `VOLATILITY_RULES` | Règles tokens volatils |
| `CHECKLISTS` | Routines quotidiennes |
| `DECISION_TEMPLATES` | Modèles de décision |
| `GLOSSARY_TAGS` | Tags secteur / usage / risque |

### 7.2 Onglets P1

| Onglet | Rôle |
|---|---|
| `TOKENS` | Watchlist ou tokens analysés |
| `MANUAL_ANALYSIS` | Saisie manuelle des signaux |
| `SCORING_RULES` | Règles de scoring |
| `SCORES` | Scores calculés ou semi-auto |
| `DAILY_PLAN` | Plan quotidien |
| `DECISION_JOURNAL` | Journal de décision |
| `ALERTS` | Alertes futures |

### 7.3 Onglets P2 QAIC bridge

| Onglet | Rôle |
|---|---|
| `QAIC_OUTPUTS_IMPORT` | Import des exports QAIC final |
| `QAIC_SCORE_MAPPING` | Mapping scores QAIC → Web App |
| `QAIC_RISK_MAPPING` | Mapping risques QAIC → UI |
| `QAIC_DECISION_MAPPING` | Mapping décisions QAIC → décisions humaines |
| `QAIC_BACKTEST_MAPPING` | Mapping validations backtest |
| `QAIC_INTEGRATION_LOG` | Journal d’intégration QAIC |

---

## 8. 🧩 Web App MVP

### 8.1 Écrans prioritaires

| Écran | Priorité | Description |
|---|---:|---|
| 🏠 Knowledge Home | P0 | Accueil lexique / méthodes / signaux |
| 🔍 Search Term | P0 | Recherche terme ou signal |
| 📚 Term Detail | P0 | Fiche définition |
| 🧠 Method Detail | P0 | Méthode complète avec conditions |
| ⚡ Signal Library | P0 | Bibliothèque filtrable |
| 🛡️ Risk Playbook | P0 | Génération ou consultation TP/SL |
| ✅ Daily Checklist | P0 | Routine quotidienne |
| 📝 Decision Journal | P1 | Justification et historique |
| 📊 Score Detail | P1 | Score et explication |
| 🔌 QAIC Output Detail | P2 | Vue future des outputs QAIC |

### 8.2 Règles UX

- Décision principale visible en moins de 10 secondes.
- Écrans simples et lisibles.
- Labels de risque explicites.
- Couleurs cohérentes : OK / Watch / Warning / Blocked.
- Aucun bouton ou wording qui donne l’impression d’un ordre automatique.
- Toujours afficher l’explication d’un score ou signal.

---

## 9. 🧮 Décisions et scoring

### 9.1 Décisions MVP autorisées

| Décision | Signification |
|---|---|
| `SETUP_STRONG_REVIEW` | Setup fort, revue humaine obligatoire |
| `BUY_SMALL_REVIEW` | Petite exposition possible après revue humaine |
| `WATCH` | Surveillance uniquement |
| `WEAK` | Setup faible |
| `AVOID` | À éviter |
| `BLOCKED` | Bloqué par règle de risque |

### 9.2 Score MVP indicatif

| Bloc | Points max |
|---|---:|
| BTC / market regime | 20 |
| Momentum | 15 |
| Volume | 15 |
| Tendance EMA | 15 |
| RSI | 10 |
| Volatilité / ATR | 10 |
| Liquidité | 10 |
| Narratif | 10 |
| Pénalité FOMO | -20 |

### 9.3 Règle d’explication obligatoire

Chaque décision doit avoir :

```text
score
status
main_reason
risk_warning
invalidation
recommended_review_action
source_rules
```

---

## 10. 🛡️ Sécurité produit

Règles non négociables :

- aucun ordre automatique ;
- aucune connexion broker active ;
- aucun conseil financier personnalisé présenté comme certitude ;
- aucun bouton “Buy now” ou “Sell now” ;
- aucune promesse de performance ;
- revue humaine obligatoire ;
- journalisation des décisions ;
- distinction claire entre analyse, signal, alerte et exécution réelle.

---

## 11. 🔌 Transition vers QAIC final

Le MVP doit anticiper l’intégration future du QAIC final sans l’imposer trop tôt.

### 11.1 Outputs QAIC à intégrer plus tard

| Output QAIC futur | Usage Web App |
|---|---|
| `market_regime_score` | Bloc régime marché |
| `alpha_score` | Score setup avancé |
| `risk_score` | Niveau de risque |
| `confidence_score` | Confiance du signal |
| `quality_score` | Qualité données / setup |
| `decision_status` | Décision proposée |
| `portfolio_warnings` | Alertes portefeuille |
| `backtest_status` | Validation historique |
| `attribution_summary` | Pourquoi le score bouge |

### 11.2 Principe de bridge

Le MVP ne dépend pas du QAIC final pour fonctionner.

Il doit rester utilisable en mode :

```text
standalone lexique-first
```

Puis évoluer vers :

```text
standalone + QAIC outputs
```

Puis :

```text
Web App / UI IDE du QAIC complet
```

---

## 12. ✅ Definition of Done MVP

Le MVP est validé si :

| Critère | Obligatoire |
|---|---:|
| Lexique consultable | Oui |
| Recherche par terme | Oui |
| Méthodes accessibles | Oui |
| Signaux filtrables | Oui |
| Risk Playbook utilisable | Oui |
| Checklists quotidiennes | Oui |
| Journal de décision | Oui |
| Score explicable | Oui |
| Interface Web App/AppSheet utilisable | Oui |
| Aucune exécution d’ordre | Oui |
| Bridge QAIC préparé | Recommandé P2 |

---

## 13. ⚠️ Risques projet et garde-fous

| Risque | Impact | Garde-fou |
|---|---|---|
| Vouloir intégrer tout QAIC trop tôt | MVP ralenti | Lexique-first strict jusqu’au Go-live |
| Schéma Sheets instable | AppSheet cassé | Freeze colonnes avant UI |
| BigQuery prématuré | Complexité/coût | Reporter à P2/P3 |
| Confusion signal / ordre | Risque produit | Labels REVIEW et aucun broker |
| Trop d’onglets | Maintenance lourde | P0 strict, P1 seulement après validation |
| AppSheet trop tôt | Rework UI | Stabiliser tables avant AppSheet |

---

## 14. 🎯 Conclusion

Le MVP QAIC doit d’abord réussir une chose :

```text
Transformer le lexique, les méthodes et les signaux en Web App utile rapidement.
```

Ensuite seulement, il pourra devenir l’interface utilisateur du QAIC final.

La priorité n’est pas la sophistication. La priorité est :

```text
clarté → usage quotidien → discipline → explicabilité → transition QAIC
```


---

## 17. 🤖 Process Antigravity P0 — validé

### 17.1 Rôle exact d’Antigravity

Antigravity est utilisé comme **atelier de production agentique** pour générer des fichiers, scripts, schémas et specs à partir des documents sources validés.

Il ne doit pas être utilisé comme pilote autonome capable de modifier le Drive, le Google Sheet ou le futur QAIC sans validation.

```text
ChatGPT cadre → Antigravity produit → Julien valide → Google Sheets exécute → AppSheet expose
```

### 17.2 Workspace local cible

```text
MVP_QAIC/
├── docs/
├── source/
├── schemas/
├── csv_seed/
├── apps_script/
├── app_sheet/
├── stitch/
├── qaic_bridge/
└── exports/
```

### 17.3 Lots Antigravity P0

| Lot | Nom | Objectif | Livrables |
|---|---|---|---|
| `P0-A` | Knowledge Base CSV | Parser le lexique et produire les tables P0 | `schemas/*.md`, `csv_seed/*.csv`, ZIP seed |
| `P0-B` | Apps Script Foundation | Créer setup, format, import, recherche | `.gs`, manifest, tests manuels |
| `P0-C` | AppSheet/Web App Spec | Préparer vues, actions, navigation | specs AppSheet `.md` |
| `P0-D` | Stitch UI Prompts | Préparer prompts écrans Knowledge-first | prompts Stitch `.md` |
| `P0-E` | QAIC Bridge Placeholders | Préparer mapping futur vers QAIC final | specs bridge, tables mapping |

### 17.4 Premier batch officiel

Le premier lot à lancer est :

```text
P0-A — Convertir le lexique en Knowledge Base CSV + schéma Sheets
```

Livrables attendus :

```text
schemas/MVP_QAIC_SHEETS_SCHEMA_P0_0.2.2.md
csv_seed/KNOWLEDGE_TERMS.csv
csv_seed/METHOD_LIBRARY.csv
csv_seed/SIGNAL_LIBRARY.csv
csv_seed/RISK_PLAYBOOK.csv
csv_seed/CHECKLISTS.csv
csv_seed/DECISION_TEMPLATES.csv
csv_seed/GLOSSARY_TAGS.csv
exports/MVP_QAIC_P0_KNOWLEDGE_BASE_SEED_0.2.2.zip
```

### 17.5 Garde-fous non négociables

Antigravity ne doit jamais :

- créer d’exécution d’ordre ;
- connecter un broker ;
- écrire dans un système live sans validation ;
- supprimer ou renommer des fichiers Drive ;
- inventer des signaux ou règles non sourcés ;
- lancer BigQuery, Cloud Run ou QAIC final avant P0 stable ;
- transformer `BUY_SMALL_REVIEW` en achat automatique.

### 17.6 Critères de validation P0-A

Le batch P0-A est accepté seulement si :

| Critère | Attendu |
|---|---|
| IDs stables | Chaque ligne possède un ID unique et lisible |
| Source section | Chaque ligne conserve une référence section/source |
| Champs machine-readable | Pas de blocs illisibles dans les colonnes critiques |
| Statuts | `VALIDATED`, `REVIEW_REQUIRED`, `DRAFT` |
| Anti-hallucination | Aucune règle inventée |
| Compatibilité AppSheet | Colonnes simples, types cohérents, valeurs contrôlées |
| Compatibilité QAIC Bridge | IDs réutilisables plus tard |


---

## 18. 🧭 P0-B6 — Documentation Update & Project Governance

> **Version ajoutée :** `0.3.1_FULL_FUSION_DRIVE_ALIGNED`
> **Statut :** `P0B6_GOVERNANCE_READY_FOR_DRIVE_REVIEW`
> **Règle appliquée :** cette section est une **extension** du CDC `0.2.2`, pas une réécriture résumée.

### 18.1 État runtime validé avant P0-B6

| Bloc | Statut | Résultat |
|---|---|---|
| `P0-A` | ✅ VALIDÉ | Knowledge Base CSV initiale importée |
| `P0-B` | ✅ VALIDÉ | Apps Script foundation, setup, import, search |
| `P0-B2` | ✅ VALIDÉ | Expansion KB + prompts + templates + data requirements |
| `P0-B3` | ✅ VALIDÉ | Institutional readiness : decision matrix, scoring spec, GPT bridge placeholders |
| `P0-B4 0.2.8` | ✅ VALIDÉ | GPT + Revolut X read-only bridge + scoring/signaux QAIC guard |
| `P0-B5 0.2.10` | ✅ VALIDÉ | Méthodes de trade plan, Entrée / TP1 / TP2 / TP3 / SL, suiveur manuel |
| `Full Signal Mapping 0.2.11` | ✅ VALIDÉ | `SIGNAL_EVALUATION_RULES = 50`, `QAIC_SIGNAL_MAPPING = 57`, `COVERAGE = 50/50` |
| `P0-B6 0.3.1` | ✅ LIVRÉ | Documentation, gouvernance, runbook, validation matrix |

### 18.2 Tables validées dans Google Sheets DEV

| Famille | Tables / onglets |
|---|---|
| Base | `CONFIG`, `KNOWLEDGE_TERMS`, `METHOD_LIBRARY`, `SIGNAL_LIBRARY`, `RISK_PLAYBOOK`, `CHECKLISTS`, `DECISION_TEMPLATES`, `GLOSSARY_TAGS` |
| Expansion | `PROMPT_LIBRARY`, `OUTPUT_TEMPLATES`, `DATA_REQUIREMENTS`, `SEARCH_DEMO` |
| Gouvernance décision | `DECISION_MATRIX`, `SIGNAL_EVALUATION_RULES`, `SCORING_MODEL_SPEC`, `DECISION_JOURNAL` |
| GPT bridge | `GPT_TOOL_BRIDGE`, `GPT_PROMPT_RUNTIME_SPEC`, `GPT_INPUT_PAYLOADS` |
| QAIC bridge | `PORTFOLIO_INPUT_CONTRACT`, `QAIC_SIGNAL_MAPPING`, `QAIC_OUTPUT_CONTRACT`, `QAIC_SIGNAL_MAPPING_COVERAGE` |
| Revolut X read-only | `REVOLUT_X_READONLY_CONTRACT`, `BROKER_READONLY_ADAPTER_SPEC`, `PORTFOLIO_SNAPSHOT`, `QAIC_RUNTIME_BRIDGE_STATUS`, `REVOLUT_X_QAIC_BRIDGE_MAPPING` |
| Trade plan / suiveur | `TOKEN_TYPE_PROFILES`, `TRADE_PLAN_METHODS`, `TP_SL_CALCULATION_RULES`, `TRAILING_PLAYBOOK`, `POSITION_FOLLOWUP_RULES`, `GPT_TRADE_PLAN_RUNTIME_REQUIREMENTS` |

### 18.3 Scoring et signaux QAIC — état institutionnel

Le mapping signaux n’est plus partiel.

```text
SIGNAL_LIBRARY = 50 signaux
SIGNAL_EVALUATION_RULES = 50 règles
QAIC_SIGNAL_MAPPING = 57 mappings
QAIC_SIGNAL_MAPPING_COVERAGE = 50/50
```

Chaque signal doit être rattaché à :

- une famille de signal ;
- une direction ;
- un score cible ;
- un poids ;
- un impact décisionnel ;
- un fallback ;
- une logique de blocage si pertinente.

### 18.4 Prompt GPT QAIC — exigences obligatoires

Tout payload GPT doit demander explicitement :

```text
alpha_score
risk_score
liquidity_score
momentum_score
fundamental_score
derivatives_score
data_quality_score
confidence_score
```

Si le score n’est pas calculable :

```text
SCORE_NOT_AVAILABLE + raison + données manquantes + niveau réel d’analyse
```

Niveaux autorisés :

```text
QAIC_FULL
QAIC_PARTIAL
SIGNAL_ONLY
LEXIQUE_ONLY
INSUFFICIENT_DATA
```

### 18.5 Trade plan methods & trailing — exigences

Chaque recommandation Entrée / TP1 / TP2 / TP3 / SL doit être justifiée par :

| Élément | Exigence |
|---|---|
| Type token | BTC/ETH, large cap, mid cap, microcap/meme, DeFi, narrative |
| Méthode | Retest, pullback, scaled entry, fast derisk, confluence fondamentale, no-trade |
| Entrée | Zone justifiée, jamais inventée |
| TP1 | Dérisk / 1R / résistance proche |
| TP2 | Résistance suivante / 2R |
| TP3 | Runner / extension / résistance higher timeframe |
| SL | Structure, invalidation, ATR ou thesis invalidation |
| Suiveur | Manuel seulement, jamais automatique |
| Données manquantes | `REVIEW_REQUIRED` |
| SL absent | `BLOCKED` |

### 18.6 Bridge Revolut X / QAIC

Le MVP consomme uniquement des sorties read-only.

```text
QAIC/Revolut X read-only
→ PORTFOLIO_SNAPSHOT
→ GPT_INPUT_PAYLOADS
→ GPT Crypto / OpenAI API later
→ Decision Journal
```

Interdictions permanentes :

```text
NO_AUTO_ORDER
NO_AUTO_SIZING
NO_BROKER_EXECUTION
NO_REAL_ORDER
NO_SECRET_IN_SHEET
NO_SECRET_IN_APPS_SCRIPT
NO_AUTOMATIC_TRAILING_ORDER
REVOLUT_X_READONLY_ONLY
HUMAN_REVIEW_ONLY
```

### 18.7 Prochaine étape officielle

```text
P0-C — AppSheet MVP Readiness
```

Objectif : transformer les tables validées en Web App utilisable, sans exécution broker et avec journalisation.


---

## 🛠️ Addendum de réparation documentaire — 0.6.2 REAL FUSION REPAIR

> **Nature de cette version :** réparation de fusion documentaire réelle.
> Cette version **ne remplace pas par un résumé court** les documents de référence précédents. Elle reprend les documents sources validés, conserve leur structure, puis applique les décisions actées depuis la dernière mise à jour.

### Décisions actées intégrées

| Décision | Statut 0.6.2 | Règle corrigée |
|---|---|---|
| Recherche Lexique Master | Priorité immédiate P0 | Le MVP AppSheet doit d’abord rendre le lexique, les méthodes et les signaux consultables/recherchables. |
| Prompts 1 à 5 | Priorité immédiate P0/P1 | Les prompts deviennent le cœur opérationnel : sélection, copie vers Gem, réponse, intake, journalisation. |
| AppSheet MVP actuel | Validé comme AppShell manuel non déployé | 10 tables injectées, navigation OK, affinage UX ultérieur. |
| Portfolio Revolut X | À faire, non reporté | D’abord read-only, puis transition vers exécution contrôlée testée. |
| Ordres / achat / vente / TP / SL / trailing stop | Non exclus du MVP | Préparation, simulations et tests MVP autorisés ; exécution réelle interdite par défaut sans gates. |
| QAIC Python | Cible de transition | Préparer broker adapter, paper trading, dry-run, validations, logs, kill switch. |
| Sécurité | Permanente | HUMAN_REVIEW_ONLY par défaut, NO_AUTO_ORDER/NO_AUTO_SIZING/NO_BROKER_EXECUTION tant que les gates ne sont pas explicitement ouverts. |

### Correction importante

Les formulations anciennes du type “ne jamais coder d’exécution d’ordre” ou “automation exclue” sont remplacées par une règle plus précise :

```text
Interdit maintenant : exécution réelle non validée, ordre réel automatique, sizing réel automatique, secrets exposés, broker live sans architecture sécurisée.
Autorisé dans la trajectoire MVP : préparation fonctionnelle, maquette, tickets manuels, read-only portfolio, paper trading, dry-run, tests contrôlés, bridge QAIC Python.
```

---

## 📱 État AppSheet MVP validé au 2026-06-16

### Tables MVP injectées

| Table | Rôle | Statut |
|---|---|---|
| `SEARCH_COCKPIT` | Recherche lexique/méthodes/signaux | OK |
| `LEXIQUE_MASTER` | Source lexique principale | OK |
| `PROMPT_LEXIQUE_BRIDGE` | Bridge prompts ↔ lexique | REVIEW clé à améliorer |
| `PROMPT_CONTEXT_PACKS` | Packs contexte prompts | REVIEW clé/colonnes à améliorer |
| `PROMPT_LIBRARY` | Bibliothèque prompts | OK |
| `PROMPT_READY_TO_COPY` | Prompts prêts à copier | REVIEW clé à améliorer |
| `PROMPT_RUN_QUEUE` | Queue de run manuel | OK, `run_queue_id` clé |
| `RESPONSE_INTAKE_QUEUE` | Intake réponse Gem/GPT | OK, `intake_queue_id` clé |
| `JOURNAL_APPEND_QUEUE` | Pré-journalisation | OK, `journal_queue_id` clé |
| `DECISION_JOURNAL` | Journal officiel décisions | OK, `journal_id` clé |

### Vues MVP validées

| Vue | Source | Usage |
|---|---|---|
| `MVP QAIC Home` | `SEARCH_COCKPIT` | Accueil/recherche |
| `Lexique` | `LEXIQUE_MASTER` | Consultation lexique |
| `Prompts Ready` | `PROMPT_READY_TO_COPY` | Prompts prêts à copier |
| `Run Queue` | `PROMPT_RUN_QUEUE` | Flux manuel prompt → réponse |
| `Decision Journal` | `DECISION_JOURNAL` | Audit read-only |

### Règle AppSheet actuelle

```text
App non déployée.
Build manuel.
Pas d’automation AppSheet.
Pas d’action broker.
Pas d’ordre.
Pas de sizing.
Affinage UX après validation structurelle.
```

---

## 💼 Portfolio Revolut X & transition exécution contrôlée

### Priorité produit

Le portefeuille Revolut X n’est **pas reporté hors trajectoire**. Il est intégré comme axe prioritaire après stabilisation du socle Lexique/Prompts/Journal.

| Niveau | Fonction | Autorisation |
|---:|---|---|
| 1 | Consultation portfolio Revolut X | Read-only |
| 2 | Analyse exposition/risque | Read-only + prompts |
| 3 | Alertes portefeuille | Notification / review only |
| 4 | Tickets manuels | Préparation d’action humaine |
| 5 | Paper trading | Simulation contrôlée |
| 6 | Dry-run broker | Test sans ordre réel |
| 7 | Exécution réelle assistée | Uniquement après gates séparés |
| 8 | TP/SL/trailing automatique | Uniquement après architecture QAIC Python sécurisée |

### Ce qui doit être construit progressivement

```text
Portfolio Revolut X read-only
→ Prompt 1 Portfolio Analysis
→ Prompt 5 Full Trading Review
→ Risk Gate
→ Alert Center
→ Manual Trade Ticket
→ Paper Trading
→ Dry-run Broker Adapter
→ QAIC Python Broker Adapter
→ Exécution live seulement après GO explicite, kill switch, logs, secrets sécurisés et validations.
```

### Garde-fous obligatoires

| Domaine | Garde-fou |
|---|---|
| Secrets | Secret Manager / jamais dans Sheets / Apps Script / Drive |
| Exécution | Kill switch visible et testé |
| Données | Vérification freshness, source, prix, PRU, quantité, exposition |
| Risque | Max exposure, concentration, NO_ADD, REDUCE_RISK_REVIEW, BLOCK |
| Logs | Journal immuable / run_id / timestamp / payload_id |
| Validation humaine | Human approval avant tout ordre réel |
| Tests | Paper trading puis dry-run avant live |

---

## 🧾 Note de conformité fusion

Ce CDC conserve le corps source du fichier `📘 CDC_MVP_QAIC_WEB_APP_LEXIQUE_FIRST_0.3.1_FULL_FUSION.md`, puis applique les corrections 0.6.2. Il ne doit plus être traité comme une synthèse courte.

## Source 5: `docs/FINAL/fusion_inbox_R6/CDC/📘 CDC_MVP_QAIC_WEB_APP_LEXIQUE_FIRST_0.7.2_REAL_FULL_SOURCE_FUSION.md`

<!--
REAL FULL SOURCE FUSION 0.7.2
Source original preserved: 📘 CDC_MVP_QAIC_WEB_APP_LEXIQUE_FIRST_0.6.2_REAL_FUSION_REPAIR.md
Source SHA256: 00f3d38c78243036b0c16a2fa37fcc5571cbc389282052ed2a27ffd55db83369
Source lines: 829
Fusion rule: original content is kept, then a scope-split correction block is appended.
No Drive overwrite. No Apps Script run. No clasp push.
-->

# 📘 CDC — MVP QAIC Web App Lexique-first

> **Projet :** 🛠️ MVP QAIC — Crypto Signal OS Web App
> **Version :** `MVP_QAIC_CDC_0.6.2_REAL_FUSION_REPAIR_APPSHEET_PORTFOLIO_BROKER_TRANSITION`
> **Date :** 2026-06-16
> **Statut :** `DRAFT_FOR_HUMAN_VALIDATION_REAL_FUSION_REPAIR`
> **Format :** Markdown `.md`

---

## 0. 🧾 Historique des changements

| Version | Date | Statut | Changements |
|---|---:|---|---|
| `0.1.0` | 2026-06-11 | Draft | Cadrage initial MVP QAIC Lexique-first |
| `0.2.0` | 2026-06-11 | Drive review ready | Reformulation : Web App rapide Lexique/Méthodes/Signaux d'abord, puis transition progressive vers le QAIC final comme UI / IDE utilisateur |
| `0.2.1` | 2026-06-11 | Drive structure final ready | Confirmation de la structure Drive finale avec ajout de `08_QAIC_BRIDGE/` et `09_WEB_APP_IDE/`, préparation import Drive, bridge QAIC et future UI / IDE QAIC |
| `0.2.2` | 2026-06-11 | Antigravity P0 process ready | Ajout du modus operandi Antigravity : workspace local, lots P0-A à P0-E, garde-fous, critères de validation, livrables attendus avant import Google |
| `0.3.1` | 2026-06-11 | P0-B6 Governance full fusion | Pleine fusion avec les documents 0.2.2 sans suppression ; ajout état P0-A→P0-B5, Full Signal Mapping 50/50, GPT/Revolut X read-only bridge, Runbook, Validation Matrix et prochaine phase P0-C |
| `0.6.2` | 2026-06-16 | Real fusion repair | Réparation après audit : reprise réelle du CDC 0.3.1, intégration AppSheet P5, priorité Lexique/Prompts, correction Portfolio Revolut X non reporté, préparation automation ordres/TP/SL/trailing via QAIC Python sous gates. |

---

## 1. 🎯 Vision produit

Le projet **🛠️ MVP QAIC — Crypto Signal OS Web App** vise à livrer rapidement une **Web App crypto éducative, analytique et décisionnelle**, centrée en priorité sur :

- le **lexique crypto** ;
- les **méthodes d’analyse** ;
- les **signaux trading** ;
- les **playbooks de risque** ;
- les **checklists quotidiennes** ;
- le **scoring explicable** ;
- le **journal de décision**.

Le MVP ne cherche pas à reproduire immédiatement tout le système QAIC complet. Il doit d’abord devenir un outil simple, rapide, lisible et utilisable au quotidien.

La trajectoire validée est double :

```text
Phase 1 — MVP Web App Lexique-first
→ livrer vite une Web App utile autour du lexique, des méthodes et des signaux

Phase 2 — Bridge QAIC
→ préparer les connecteurs et mappings vers l’outil QAIC final en cours de développement

Phase 3 — UI / IDE QAIC
→ transformer progressivement la Web App en interface utilisateur du QAIC complet
```

---

## 2. 🧠 Principe central : Lexique, méthodes et signaux d’abord

Le MVP démarre par la connaissance structurée, pas par un moteur de trading lourd.

```text
Lexique Crypto
↓
Knowledge Base
↓
Method Library
↓
Signal Library
↓
Risk Playbook
↓
Decision Checklist
↓
Scoring explicable
↓
Web App
↓
Journal de décision
```

Le lexique ne doit pas rester un document passif. Il devient :

| Élément du lexique | Transformation MVP |
|---|---|
| Terme crypto/trading | Fiche consultable et filtrable |
| Méthode | Procédure opérationnelle |
| Signal | Règle d’analyse et score partiel |
| Risque | Règle TP / SL / sizing / invalidation |
| Checklist | Routine d’usage quotidien |
| Template | Journal ou plan d’analyse |
| Indicateur | Champ manuel puis calculé plus tard |

---

## 3. 🧭 Positionnement fonctionnel

Le MVP est un **support à la décision**, pas un robot de trading.

Il sert à :

- comprendre les notions crypto/trading ;
- rechercher rapidement une méthode ou un signal ;
- structurer une analyse ;
- réduire les décisions impulsives ;
- standardiser les plans TP / SL ;
- expliquer les scores ;
- journaliser les décisions ;
- préparer l’intégration future du QAIC complet.

Il ne sert pas à :

- passer des ordres ;
- exécuter automatiquement des achats/ventes ;
- gérer un broker ;
- remplacer la revue humaine ;
- promettre une performance ;
- produire du conseil financier personnalisé.

---

## 4. 🧱 Périmètre MVP

### 4.1 Périmètre inclus P0

| Module | Priorité | Description |
|---|---:|---|
| 📚 Knowledge Base | P0 | Lexique structuré et consultable |
| 🔍 Search Engine | P0 | Recherche de termes, méthodes, signaux |
| 🧠 Method Library | P0 | Méthodes d’analyse structurées |
| ⚡ Signal Library | P0 | Signaux positifs, neutres, danger |
| 🛡️ Risk Playbook | P0 | TP1 / TP2 / TP3 / SL / sizing / invalidation |
| ✅ Daily Checklists | P0 | Routine matin / avant analyse / avant décision |
| 🧾 Decision Templates | P0 | Acheter, attendre, éviter, bloquer, revoir |
| 📝 Decision Journal | P0/P1 | Historique des décisions et justifications |

### 4.2 Périmètre P1

| Module | Priorité | Description |
|---|---:|---|
| 🧮 Scoring MVP | P1 | Score manuel ou semi-auto sur 100 |
| 📊 Dashboard simple | P1 | Vue synthétique des signaux et risques |
| 🧭 Daily Plan | P1 | Plan quotidien basé sur checklist + signaux |
| 🧩 AppSheet / Web App | P1 | Interface web/mobile rapide |
| 📈 Looker Studio | P1 | Dashboard visuel de suivi |

### 4.3 Périmètre P2 / transition QAIC

| Module | Priorité | Description |
|---|---:|---|
| 🔌 QAIC Outputs Import | P2 | Import progressif des outputs QAIC |
| 🗺️ QAIC Score Mapping | P2 | Mapping alpha/risk/confidence vers UI MVP |
| 🧪 Backtest Mapping | P2 | Restitution des validations backtest QAIC |
| 🧠 Advanced Decision UI | P2 | UI / IDE pour décision humaine assistée |
| 🗂️ BigQuery Bridge | P2/P3 | Uniquement quand les volumes ou historiques l’exigent |

---

## 5. ☁️ Écosystème Google retenu

### 5.1 Stack initiale

| Couche | Outil | Rôle |
|---|---|---|
| Dossier projet | Google Drive | Docs, exports, backups, ZIP |
| Base MVP | Google Sheets | Tables Knowledge, règles, journal, scoring |
| Automatisation | Apps Script | Setup, formatage, recherche, règles, scoring léger |
| Web App rapide | AppSheet | Interface mobile/web no-code rapide |
| Dashboard | Looker Studio | Synthèse visuelle |
| UI design | Google Stitch | Maquettes et design system |
| Développement agentique | Google Antigravity | Structuration, génération code, tests bornés |

### 5.2 Stack future possible

| Couche | Outil | Usage futur |
|---|---|---|
| Historique scalable | BigQuery | Historique, backtests, logs lourds |
| Backend avancé | Cloud Run | APIs, moteurs plus robustes |
| Auth / temps réel | Firebase | Version web avancée |
| Dev Factory | Python / local / Codex | QAIC avancé, tests, pipelines |

### 5.3 Règle d’or

BigQuery, Cloud Run et Python avancé ne doivent pas précéder le MVP Lexique-first. Ils ne sont activés que si :

- la Web App est utile ;
- les schémas sont stables ;
- les besoins d’historique ou d’intégration QAIC sont confirmés ;
- les coûts et la gouvernance sont maîtrisés.

---

## 6. 📁 Structure Drive cible

```text
🛠️ MVP QAIC — Crypto Signal OS/
│
├── 00_ADMIN/
│   ├── README_PROJECT.md
│   ├── CHANGELOG.md
│   └── DECISIONS_LOG.md
│
├── 01_DOCS/
│   ├── CDC/
│   ├── PLANNING/
│   ├── INSTRUCTIONS/
│   ├── RUNBOOK/
│   └── PROMPTS/
│
├── 02_SHEETS/
│   ├── DEV/
│   ├── EXPORTS_CSV/
│   └── BACKUPS/
│
├── 03_APPS_SCRIPT/
│   ├── SOURCE/
│   ├── BACKUPS/
│   └── ZIP/
│
├── 04_APPSHEET/
│   ├── SPEC/
│   └── SCREENSHOTS/
│
├── 05_LOOKER/
│   ├── DASHBOARD_SPEC/
│   └── EXPORTS/
│
├── 06_STITCH/
│   ├── PROMPTS/
│   └── UI_EXPORTS/
│
├── 07_ANTIGRAVITY/
│   ├── PROMPTS/
│   ├── TASKS/
│   └── OUTPUTS/
│
├── 08_QAIC_BRIDGE/
│   ├── IMPORT_SPECS/
│   ├── MAPPING/
│   └── OUTPUTS/
│
├── 09_WEB_APP_IDE/
│   ├── UI_SPEC/
│   ├── COMPONENTS/
│   └── USER_FLOWS/
│
└── 99_ARCHIVES/
```

### 6.1 Confirmation structure finale validée

La structure Drive finale est validée avec deux ajouts stratégiques par rapport à la version 0.2.0 :

| Dossier | Rôle | Pourquoi il est nécessaire |
|---|---|---|
| `08_QAIC_BRIDGE/` | Préparer l'import, le mapping et la restitution des outputs QAIC final | Évite de coupler trop tôt le MVP à QAIC tout en préparant la transition |
| `09_WEB_APP_IDE/` | Préparer la future UI / IDE utilisateur au-dessus du QAIC complet | Sépare clairement l'AppSheet/Web App rapide de l'interface avancée future |

Décision confirmée : le MVP reste d'abord une Web App rapide Lexique / Méthodes / Signaux, puis il récupère progressivement les outputs QAIC final via une couche bridge documentée et non bloquante.

---

## 7. 📊 Google Sheets DEV

Nom recommandé :

```text
MVP QAIC — Crypto Signal OS — DEV
```

### 7.1 Onglets P0

| Onglet | Rôle |
|---|---|
| `CONFIG` | Paramètres globaux |
| `KNOWLEDGE_TERMS` | Définitions crypto/trading structurées |
| `METHOD_LIBRARY` | Méthodes d’analyse |
| `SIGNAL_LIBRARY` | Signaux trading |
| `RISK_PLAYBOOK` | TP / SL / sizing / invalidation |
| `MARKET_REGIME_RULES` | Règles BTC risk-on/risk-off |
| `VOLATILITY_RULES` | Règles tokens volatils |
| `CHECKLISTS` | Routines quotidiennes |
| `DECISION_TEMPLATES` | Modèles de décision |
| `GLOSSARY_TAGS` | Tags secteur / usage / risque |

### 7.2 Onglets P1

| Onglet | Rôle |
|---|---|
| `TOKENS` | Watchlist ou tokens analysés |
| `MANUAL_ANALYSIS` | Saisie manuelle des signaux |
| `SCORING_RULES` | Règles de scoring |
| `SCORES` | Scores calculés ou semi-auto |
| `DAILY_PLAN` | Plan quotidien |
| `DECISION_JOURNAL` | Journal de décision |
| `ALERTS` | Alertes futures |

### 7.3 Onglets P2 QAIC bridge

| Onglet | Rôle |
|---|---|
| `QAIC_OUTPUTS_IMPORT` | Import des exports QAIC final |
| `QAIC_SCORE_MAPPING` | Mapping scores QAIC → Web App |
| `QAIC_RISK_MAPPING` | Mapping risques QAIC → UI |
| `QAIC_DECISION_MAPPING` | Mapping décisions QAIC → décisions humaines |
| `QAIC_BACKTEST_MAPPING` | Mapping validations backtest |
| `QAIC_INTEGRATION_LOG` | Journal d’intégration QAIC |

---

## 8. 🧩 Web App MVP

### 8.1 Écrans prioritaires

| Écran | Priorité | Description |
|---|---:|---|
| 🏠 Knowledge Home | P0 | Accueil lexique / méthodes / signaux |
| 🔍 Search Term | P0 | Recherche terme ou signal |
| 📚 Term Detail | P0 | Fiche définition |
| 🧠 Method Detail | P0 | Méthode complète avec conditions |
| ⚡ Signal Library | P0 | Bibliothèque filtrable |
| 🛡️ Risk Playbook | P0 | Génération ou consultation TP/SL |
| ✅ Daily Checklist | P0 | Routine quotidienne |
| 📝 Decision Journal | P1 | Justification et historique |
| 📊 Score Detail | P1 | Score et explication |
| 🔌 QAIC Output Detail | P2 | Vue future des outputs QAIC |

### 8.2 Règles UX

- Décision principale visible en moins de 10 secondes.
- Écrans simples et lisibles.
- Labels de risque explicites.
- Couleurs cohérentes : OK / Watch / Warning / Blocked.
- Aucun bouton ou wording qui donne l’impression d’un ordre automatique.
- Toujours afficher l’explication d’un score ou signal.

---

## 9. 🧮 Décisions et scoring

### 9.1 Décisions MVP autorisées

| Décision | Signification |
|---|---|
| `SETUP_STRONG_REVIEW` | Setup fort, revue humaine obligatoire |
| `BUY_SMALL_REVIEW` | Petite exposition possible après revue humaine |
| `WATCH` | Surveillance uniquement |
| `WEAK` | Setup faible |
| `AVOID` | À éviter |
| `BLOCKED` | Bloqué par règle de risque |

### 9.2 Score MVP indicatif

| Bloc | Points max |
|---|---:|
| BTC / market regime | 20 |
| Momentum | 15 |
| Volume | 15 |
| Tendance EMA | 15 |
| RSI | 10 |
| Volatilité / ATR | 10 |
| Liquidité | 10 |
| Narratif | 10 |
| Pénalité FOMO | -20 |

### 9.3 Règle d’explication obligatoire

Chaque décision doit avoir :

```text
score
status
main_reason
risk_warning
invalidation
recommended_review_action
source_rules
```

---

## 10. 🛡️ Sécurité produit

Règles non négociables :

- aucun ordre automatique ;
- aucune connexion broker active ;
- aucun conseil financier personnalisé présenté comme certitude ;
- aucun bouton “Buy now” ou “Sell now” ;
- aucune promesse de performance ;
- revue humaine obligatoire ;
- journalisation des décisions ;
- distinction claire entre analyse, signal, alerte et exécution réelle.

---

## 11. 🔌 Transition vers QAIC final

Le MVP doit anticiper l’intégration future du QAIC final sans l’imposer trop tôt.

### 11.1 Outputs QAIC à intégrer plus tard

| Output QAIC futur | Usage Web App |
|---|---|
| `market_regime_score` | Bloc régime marché |
| `alpha_score` | Score setup avancé |
| `risk_score` | Niveau de risque |
| `confidence_score` | Confiance du signal |
| `quality_score` | Qualité données / setup |
| `decision_status` | Décision proposée |
| `portfolio_warnings` | Alertes portefeuille |
| `backtest_status` | Validation historique |
| `attribution_summary` | Pourquoi le score bouge |

### 11.2 Principe de bridge

Le MVP ne dépend pas du QAIC final pour fonctionner.

Il doit rester utilisable en mode :

```text
standalone lexique-first
```

Puis évoluer vers :

```text
standalone + QAIC outputs
```

Puis :

```text
Web App / UI IDE du QAIC complet
```

---

## 12. ✅ Definition of Done MVP

Le MVP est validé si :

| Critère | Obligatoire |
|---|---:|
| Lexique consultable | Oui |
| Recherche par terme | Oui |
| Méthodes accessibles | Oui |
| Signaux filtrables | Oui |
| Risk Playbook utilisable | Oui |
| Checklists quotidiennes | Oui |
| Journal de décision | Oui |
| Score explicable | Oui |
| Interface Web App/AppSheet utilisable | Oui |
| Aucune exécution d’ordre | Oui |
| Bridge QAIC préparé | Recommandé P2 |

---

## 13. ⚠️ Risques projet et garde-fous

| Risque | Impact | Garde-fou |
|---|---|---|
| Vouloir intégrer tout QAIC trop tôt | MVP ralenti | Lexique-first strict jusqu’au Go-live |
| Schéma Sheets instable | AppSheet cassé | Freeze colonnes avant UI |
| BigQuery prématuré | Complexité/coût | Reporter à P2/P3 |
| Confusion signal / ordre | Risque produit | Labels REVIEW et aucun broker |
| Trop d’onglets | Maintenance lourde | P0 strict, P1 seulement après validation |
| AppSheet trop tôt | Rework UI | Stabiliser tables avant AppSheet |

---

## 14. 🎯 Conclusion

Le MVP QAIC doit d’abord réussir une chose :

```text
Transformer le lexique, les méthodes et les signaux en Web App utile rapidement.
```

Ensuite seulement, il pourra devenir l’interface utilisateur du QAIC final.

La priorité n’est pas la sophistication. La priorité est :

```text
clarté → usage quotidien → discipline → explicabilité → transition QAIC
```


---

## 17. 🤖 Process Antigravity P0 — validé

### 17.1 Rôle exact d’Antigravity

Antigravity est utilisé comme **atelier de production agentique** pour générer des fichiers, scripts, schémas et specs à partir des documents sources validés.

Il ne doit pas être utilisé comme pilote autonome capable de modifier le Drive, le Google Sheet ou le futur QAIC sans validation.

```text
ChatGPT cadre → Antigravity produit → Julien valide → Google Sheets exécute → AppSheet expose
```

### 17.2 Workspace local cible

```text
MVP_QAIC/
├── docs/
├── source/
├── schemas/
├── csv_seed/
├── apps_script/
├── app_sheet/
├── stitch/
├── qaic_bridge/
└── exports/
```

### 17.3 Lots Antigravity P0

| Lot | Nom | Objectif | Livrables |
|---|---|---|---|
| `P0-A` | Knowledge Base CSV | Parser le lexique et produire les tables P0 | `schemas/*.md`, `csv_seed/*.csv`, ZIP seed |
| `P0-B` | Apps Script Foundation | Créer setup, format, import, recherche | `.gs`, manifest, tests manuels |
| `P0-C` | AppSheet/Web App Spec | Préparer vues, actions, navigation | specs AppSheet `.md` |
| `P0-D` | Stitch UI Prompts | Préparer prompts écrans Knowledge-first | prompts Stitch `.md` |
| `P0-E` | QAIC Bridge Placeholders | Préparer mapping futur vers QAIC final | specs bridge, tables mapping |

### 17.4 Premier batch officiel

Le premier lot à lancer est :

```text
P0-A — Convertir le lexique en Knowledge Base CSV + schéma Sheets
```

Livrables attendus :

```text
schemas/MVP_QAIC_SHEETS_SCHEMA_P0_0.2.2.md
csv_seed/KNOWLEDGE_TERMS.csv
csv_seed/METHOD_LIBRARY.csv
csv_seed/SIGNAL_LIBRARY.csv
csv_seed/RISK_PLAYBOOK.csv
csv_seed/CHECKLISTS.csv
csv_seed/DECISION_TEMPLATES.csv
csv_seed/GLOSSARY_TAGS.csv
exports/MVP_QAIC_P0_KNOWLEDGE_BASE_SEED_0.2.2.zip
```

### 17.5 Garde-fous non négociables

Antigravity ne doit jamais :

- créer d’exécution d’ordre ;
- connecter un broker ;
- écrire dans un système live sans validation ;
- supprimer ou renommer des fichiers Drive ;
- inventer des signaux ou règles non sourcés ;
- lancer BigQuery, Cloud Run ou QAIC final avant P0 stable ;
- transformer `BUY_SMALL_REVIEW` en achat automatique.

### 17.6 Critères de validation P0-A

Le batch P0-A est accepté seulement si :

| Critère | Attendu |
|---|---|
| IDs stables | Chaque ligne possède un ID unique et lisible |
| Source section | Chaque ligne conserve une référence section/source |
| Champs machine-readable | Pas de blocs illisibles dans les colonnes critiques |
| Statuts | `VALIDATED`, `REVIEW_REQUIRED`, `DRAFT` |
| Anti-hallucination | Aucune règle inventée |
| Compatibilité AppSheet | Colonnes simples, types cohérents, valeurs contrôlées |
| Compatibilité QAIC Bridge | IDs réutilisables plus tard |


---

## 18. 🧭 P0-B6 — Documentation Update & Project Governance

> **Version ajoutée :** `0.3.1_FULL_FUSION_DRIVE_ALIGNED`
> **Statut :** `P0B6_GOVERNANCE_READY_FOR_DRIVE_REVIEW`
> **Règle appliquée :** cette section est une **extension** du CDC `0.2.2`, pas une réécriture résumée.

### 18.1 État runtime validé avant P0-B6

| Bloc | Statut | Résultat |
|---|---|---|
| `P0-A` | ✅ VALIDÉ | Knowledge Base CSV initiale importée |
| `P0-B` | ✅ VALIDÉ | Apps Script foundation, setup, import, search |
| `P0-B2` | ✅ VALIDÉ | Expansion KB + prompts + templates + data requirements |
| `P0-B3` | ✅ VALIDÉ | Institutional readiness : decision matrix, scoring spec, GPT bridge placeholders |
| `P0-B4 0.2.8` | ✅ VALIDÉ | GPT + Revolut X read-only bridge + scoring/signaux QAIC guard |
| `P0-B5 0.2.10` | ✅ VALIDÉ | Méthodes de trade plan, Entrée / TP1 / TP2 / TP3 / SL, suiveur manuel |
| `Full Signal Mapping 0.2.11` | ✅ VALIDÉ | `SIGNAL_EVALUATION_RULES = 50`, `QAIC_SIGNAL_MAPPING = 57`, `COVERAGE = 50/50` |
| `P0-B6 0.3.1` | ✅ LIVRÉ | Documentation, gouvernance, runbook, validation matrix |

### 18.2 Tables validées dans Google Sheets DEV

| Famille | Tables / onglets |
|---|---|
| Base | `CONFIG`, `KNOWLEDGE_TERMS`, `METHOD_LIBRARY`, `SIGNAL_LIBRARY`, `RISK_PLAYBOOK`, `CHECKLISTS`, `DECISION_TEMPLATES`, `GLOSSARY_TAGS` |
| Expansion | `PROMPT_LIBRARY`, `OUTPUT_TEMPLATES`, `DATA_REQUIREMENTS`, `SEARCH_DEMO` |
| Gouvernance décision | `DECISION_MATRIX`, `SIGNAL_EVALUATION_RULES`, `SCORING_MODEL_SPEC`, `DECISION_JOURNAL` |
| GPT bridge | `GPT_TOOL_BRIDGE`, `GPT_PROMPT_RUNTIME_SPEC`, `GPT_INPUT_PAYLOADS` |
| QAIC bridge | `PORTFOLIO_INPUT_CONTRACT`, `QAIC_SIGNAL_MAPPING`, `QAIC_OUTPUT_CONTRACT`, `QAIC_SIGNAL_MAPPING_COVERAGE` |
| Revolut X read-only | `REVOLUT_X_READONLY_CONTRACT`, `BROKER_READONLY_ADAPTER_SPEC`, `PORTFOLIO_SNAPSHOT`, `QAIC_RUNTIME_BRIDGE_STATUS`, `REVOLUT_X_QAIC_BRIDGE_MAPPING` |
| Trade plan / suiveur | `TOKEN_TYPE_PROFILES`, `TRADE_PLAN_METHODS`, `TP_SL_CALCULATION_RULES`, `TRAILING_PLAYBOOK`, `POSITION_FOLLOWUP_RULES`, `GPT_TRADE_PLAN_RUNTIME_REQUIREMENTS` |

### 18.3 Scoring et signaux QAIC — état institutionnel

Le mapping signaux n’est plus partiel.

```text
SIGNAL_LIBRARY = 50 signaux
SIGNAL_EVALUATION_RULES = 50 règles
QAIC_SIGNAL_MAPPING = 57 mappings
QAIC_SIGNAL_MAPPING_COVERAGE = 50/50
```

Chaque signal doit être rattaché à :

- une famille de signal ;
- une direction ;
- un score cible ;
- un poids ;
- un impact décisionnel ;
- un fallback ;
- une logique de blocage si pertinente.

### 18.4 Prompt GPT QAIC — exigences obligatoires

Tout payload GPT doit demander explicitement :

```text
alpha_score
risk_score
liquidity_score
momentum_score
fundamental_score
derivatives_score
data_quality_score
confidence_score
```

Si le score n’est pas calculable :

```text
SCORE_NOT_AVAILABLE + raison + données manquantes + niveau réel d’analyse
```

Niveaux autorisés :

```text
QAIC_FULL
QAIC_PARTIAL
SIGNAL_ONLY
LEXIQUE_ONLY
INSUFFICIENT_DATA
```

### 18.5 Trade plan methods & trailing — exigences

Chaque recommandation Entrée / TP1 / TP2 / TP3 / SL doit être justifiée par :

| Élément | Exigence |
|---|---|
| Type token | BTC/ETH, large cap, mid cap, microcap/meme, DeFi, narrative |
| Méthode | Retest, pullback, scaled entry, fast derisk, confluence fondamentale, no-trade |
| Entrée | Zone justifiée, jamais inventée |
| TP1 | Dérisk / 1R / résistance proche |
| TP2 | Résistance suivante / 2R |
| TP3 | Runner / extension / résistance higher timeframe |
| SL | Structure, invalidation, ATR ou thesis invalidation |
| Suiveur | Manuel seulement, jamais automatique |
| Données manquantes | `REVIEW_REQUIRED` |
| SL absent | `BLOCKED` |

### 18.6 Bridge Revolut X / QAIC

Le MVP consomme uniquement des sorties read-only.

```text
QAIC/Revolut X read-only
→ PORTFOLIO_SNAPSHOT
→ GPT_INPUT_PAYLOADS
→ GPT Crypto / OpenAI API later
→ Decision Journal
```

Interdictions permanentes :

```text
NO_AUTO_ORDER
NO_AUTO_SIZING
NO_BROKER_EXECUTION
NO_REAL_ORDER
NO_SECRET_IN_SHEET
NO_SECRET_IN_APPS_SCRIPT
NO_AUTOMATIC_TRAILING_ORDER
REVOLUT_X_READONLY_ONLY
HUMAN_REVIEW_ONLY
```

### 18.7 Prochaine étape officielle

```text
P0-C — AppSheet MVP Readiness
```

Objectif : transformer les tables validées en Web App utilisable, sans exécution broker et avec journalisation.


---

## 🛠️ Addendum de réparation documentaire — 0.6.2 REAL FUSION REPAIR

> **Nature de cette version :** réparation de fusion documentaire réelle.
> Cette version **ne remplace pas par un résumé court** les documents de référence précédents. Elle reprend les documents sources validés, conserve leur structure, puis applique les décisions actées depuis la dernière mise à jour.

### Décisions actées intégrées

| Décision | Statut 0.6.2 | Règle corrigée |
|---|---|---|
| Recherche Lexique Master | Priorité immédiate P0 | Le MVP AppSheet doit d’abord rendre le lexique, les méthodes et les signaux consultables/recherchables. |
| Prompts 1 à 5 | Priorité immédiate P0/P1 | Les prompts deviennent le cœur opérationnel : sélection, copie vers Gem, réponse, intake, journalisation. |
| AppSheet MVP actuel | Validé comme AppShell manuel non déployé | 10 tables injectées, navigation OK, affinage UX ultérieur. |
| Portfolio Revolut X | À faire, non reporté | D’abord read-only, puis transition vers exécution contrôlée testée. |
| Ordres / achat / vente / TP / SL / trailing stop | Non exclus du MVP | Préparation, simulations et tests MVP autorisés ; exécution réelle interdite par défaut sans gates. |
| QAIC Python | Cible de transition | Préparer broker adapter, paper trading, dry-run, validations, logs, kill switch. |
| Sécurité | Permanente | HUMAN_REVIEW_ONLY par défaut, NO_AUTO_ORDER/NO_AUTO_SIZING/NO_BROKER_EXECUTION tant que les gates ne sont pas explicitement ouverts. |

### Correction importante

Les formulations anciennes du type “ne jamais coder d’exécution d’ordre” ou “automation exclue” sont remplacées par une règle plus précise :

```text
Interdit maintenant : exécution réelle non validée, ordre réel automatique, sizing réel automatique, secrets exposés, broker live sans architecture sécurisée.
Autorisé dans la trajectoire MVP : préparation fonctionnelle, maquette, tickets manuels, read-only portfolio, paper trading, dry-run, tests contrôlés, bridge QAIC Python.
```

---

## 📱 État AppSheet MVP validé au 2026-06-16

### Tables MVP injectées

| Table | Rôle | Statut |
|---|---|---|
| `SEARCH_COCKPIT` | Recherche lexique/méthodes/signaux | OK |
| `LEXIQUE_MASTER` | Source lexique principale | OK |
| `PROMPT_LEXIQUE_BRIDGE` | Bridge prompts ↔ lexique | REVIEW clé à améliorer |
| `PROMPT_CONTEXT_PACKS` | Packs contexte prompts | REVIEW clé/colonnes à améliorer |
| `PROMPT_LIBRARY` | Bibliothèque prompts | OK |
| `PROMPT_READY_TO_COPY` | Prompts prêts à copier | REVIEW clé à améliorer |
| `PROMPT_RUN_QUEUE` | Queue de run manuel | OK, `run_queue_id` clé |
| `RESPONSE_INTAKE_QUEUE` | Intake réponse Gem/GPT | OK, `intake_queue_id` clé |
| `JOURNAL_APPEND_QUEUE` | Pré-journalisation | OK, `journal_queue_id` clé |
| `DECISION_JOURNAL` | Journal officiel décisions | OK, `journal_id` clé |

### Vues MVP validées

| Vue | Source | Usage |
|---|---|---|
| `MVP QAIC Home` | `SEARCH_COCKPIT` | Accueil/recherche |
| `Lexique` | `LEXIQUE_MASTER` | Consultation lexique |
| `Prompts Ready` | `PROMPT_READY_TO_COPY` | Prompts prêts à copier |
| `Run Queue` | `PROMPT_RUN_QUEUE` | Flux manuel prompt → réponse |
| `Decision Journal` | `DECISION_JOURNAL` | Audit read-only |

### Règle AppSheet actuelle

```text
App non déployée.
Build manuel.
Pas d’automation AppSheet.
Pas d’action broker.
Pas d’ordre.
Pas de sizing.
Affinage UX après validation structurelle.
```

---

## 💼 Portfolio Revolut X & transition exécution contrôlée

### Priorité produit

Le portefeuille Revolut X n’est **pas reporté hors trajectoire**. Il est intégré comme axe prioritaire après stabilisation du socle Lexique/Prompts/Journal.

| Niveau | Fonction | Autorisation |
|---:|---|---|
| 1 | Consultation portfolio Revolut X | Read-only |
| 2 | Analyse exposition/risque | Read-only + prompts |
| 3 | Alertes portefeuille | Notification / review only |
| 4 | Tickets manuels | Préparation d’action humaine |
| 5 | Paper trading | Simulation contrôlée |
| 6 | Dry-run broker | Test sans ordre réel |
| 7 | Exécution réelle assistée | Uniquement après gates séparés |
| 8 | TP/SL/trailing automatique | Uniquement après architecture QAIC Python sécurisée |

### Ce qui doit être construit progressivement

```text
Portfolio Revolut X read-only
→ Prompt 1 Portfolio Analysis
→ Prompt 5 Full Trading Review
→ Risk Gate
→ Alert Center
→ Manual Trade Ticket
→ Paper Trading
→ Dry-run Broker Adapter
→ QAIC Python Broker Adapter
→ Exécution live seulement après GO explicite, kill switch, logs, secrets sécurisés et validations.
```

### Garde-fous obligatoires

| Domaine | Garde-fou |
|---|---|
| Secrets | Secret Manager / jamais dans Sheets / Apps Script / Drive |
| Exécution | Kill switch visible et testé |
| Données | Vérification freshness, source, prix, PRU, quantité, exposition |
| Risque | Max exposure, concentration, NO_ADD, REDUCE_RISK_REVIEW, BLOCK |
| Logs | Journal immuable / run_id / timestamp / payload_id |
| Validation humaine | Human approval avant tout ordre réel |
| Tests | Paper trading puis dry-run avant live |

---

## 🧾 Note de conformité fusion

Ce CDC conserve le corps source du fichier `📘 CDC_MVP_QAIC_WEB_APP_LEXIQUE_FIRST_0.3.1_FULL_FUSION.md`, puis applique les corrections 0.6.2. Il ne doit plus être traité comme une synthèse courte.
---

# ✅ FUSION 0.7.2 — Scope Split MVP / QAIC Engine

> **Patch fusionnel ajouté au document original complet**
> **Projet :** 🛠️ MVP QAIC — Crypto Signal OS
> **Version fusionnée :** `0.7.2_REAL_FULL_SOURCE_FUSION_SCOPE_SPLIT`
> **Date :** 2026-06-20
> **Statut :** `READY_FOR_HUMAN_REVIEW_NON_DESTRUCTIVE`
> **Méthode :** contenu original 0.6.2 conservé intégralement, puis correction de doctrine ajoutée sans suppression.

## 0. Décision de programme validée

```text
MVP QAIC = Lexique / méthodes / signaux / Knowledge Base / WebApp pédagogique
QAIC = moteur calcul, trading analytics, portefeuille, risk engine, Revolut API
```

## 1. Correction de doctrine à appliquer à ce document

Toute mention historique du type :

```text
Portfolio Revolut X dans MVP
Revolut API dans MVP
QAIC Python broker adapter dans MVP
paper trading / dry-run / execution contrôlée dans MVP
scoring trading final dans MVP
risk engine portfolio dans MVP
```

doit être lue comme :

```text
Ces éléments relèvent de QAIC Engine.
Le MVP ne conserve que l'explication pédagogique, l'affichage contrôlé, les mappings et les contrats d'import des sorties QAIC.
```

## 2. Frontière officielle

| Domaine | Responsable officiel |
|---|---|
| Lexique crypto | MVP |
| Méthodes / signaux expliqués | MVP |
| WebApp privée / search cockpit | MVP |
| Knowledge Base / source registry | MVP |
| Journal human review pédagogique | MVP |
| Affichage de sorties QAIC | MVP via import contrôlé |
| Calculs trading | QAIC |
| Portefeuille / exposition | QAIC |
| Revolut API | QAIC |
| Risk engine final | QAIC |
| Broker adapter / dry-run / exécution future | QAIC, hors MVP |

## 3. Règles non négociables MVP

```text
NO_REVOLUT_API_IN_MVP = TRUE
NO_TRADING_ENGINE_IN_MVP = TRUE
NO_PORTFOLIO_ENGINE_IN_MVP = TRUE
NO_ORDER_IN_MVP = TRUE
NO_SIZING_IN_MVP = TRUE
NO_BROKER_EXECUTION_IN_MVP = TRUE
NO_SECRET_IN_MVP = TRUE
HUMAN_REVIEW_ONLY = TRUE
```

## 4. Ce qui reste autorisé dans le MVP

```text
- expliquer les concepts trading ;
- documenter Night Watch / trade nocturne comme méthode pédagogique ;
- afficher un output QAIC importé en lecture contrôlée ;
- journaliser la décision humaine ;
- montrer missing_data / blockers / source provenance ;
- relier une fiche lexique à un output QAIC par référence.
```

## 5. Ce qui est transféré à QAIC

```text
- Revolut provider Python ;
- API keys / signatures / secrets ;
- calculs de portefeuille ;
- calculs de signaux ;
- scoring trading officiel ;
- risk engine trading ;
- dry-run / paper trading / broker adapter ;
- toute exécution future, même contrôlée.
```

## 6. Impact spécifique sur `CDC`

Ce document reste source valide pour son contenu historique et structurel, mais ses passages liés à Revolut, portfolio, broker, paper trading, dry-run ou calcul trading sont **superseded** par cette correction 0.7.2.

```text
MVP_SCOPE = LEXIQUE_KB_WEBAPP_ONLY
QAIC_SCOPE = CALC_TRADING_REVOLUT_ENGINE
QAIC_BRIDGE_IN_MVP = OUTPUT_IMPORT_AND_DISPLAY_ONLY
```

## Source 6: `docs/FINAL/fusion_inbox_R6/FINAL_FUSED/MVP_QAIC_PY/📘 MVP_QAIC_CDC_CONTRACT_FINAL_FUSED_v0.2.2.md`

# 📘 CDC & Contrats — Version finale fusionnée

**Version :** `0.2.2`
**Statut :** `P203B2_R3_FINAL_FUSION_CONTENT_CANDIDATE`
**Date :** `2026-06-24 17:10:57`
**Theme :** `CDC_CONTRACT`
**Source P203A :** `G:\Mon Drive\👥 JULIEN [Perso]\📈 Trading JRb\Solutions & Dev (Trading JRb)\MVP_QAIC_PY\05_EXPORTS\P203A_R2_EXACT_3_ROOTS_DOCS_AUDIT_20260624_161358`
**Source P203B1 :** `G:\Mon Drive\👥 JULIEN [Perso]\📈 Trading JRb\Solutions & Dev (Trading JRb)\MVP_QAIC_PY\05_EXPORTS\P203B1_R2_DOC_LEGITIMACY_GATE_MD_20260624_163254`

## 1. 🎯 Finalité

Cette version fusionnée regroupe les contenus légitimes, actuels ou historiquement utiles pour la famille `CDC_CONTRACT`.

Elle ne supprime aucun fichier source et n'autorise pas encore l'archivage automatique. L'archivage dépend de la matrice `P203B2_R3_ARCHIVE_GATE_CANDIDATES.csv`.

## 2. 📌 Synthèse de fusion

| Indicateur | Valeur |
|---|---:|
| Candidats rattachés | 804 |
| Sources lisibles intégrées dans cette candidate | 60 |
| ZIP conservés en attente inspection | 19 |
| Sources non lisibles conservées en revue | 0 |
| Archivage exécuté | NON |

## 3. ✅ Sources intégrées dans la candidate

| item_id | statut | fraîcheur | chemin |
|---|---|---|---|
| ITEM-001299 | REVIEW_REQUIRED | CURRENT_OR_RECENT | `00_ADMIN\CHANGELOG_MVP_QAIC_P1G_PROMPT_LIBRARY_CONTRACT_0.6.0.md` |
| ITEM-000003 | REVIEW_REQUIRED | CURRENT_OR_RECENT | `01_DOCS\01_CDC\_CDC_MVP_QAIC_PYTHON_MIGRATION_0.1.0.md` |
| ITEM-000004 | REVIEW_REQUIRED | CURRENT_OR_RECENT | `01_DOCS\01_CDC\📘_CDC_MVP_QAIC_PYTHON_MIGRATION_0.1.0.md` |
| ITEM-000017 | REVIEW_REQUIRED | CURRENT_OR_RECENT | `01_DOCS\CDC\CDC_MVP_QAIC_OPERATIONAL_ROADMAP.md` |
| ITEM-001323 | REVIEW_REQUIRED | CURRENT_OR_RECENT | `01_DOCS\CDC\MEMO_CDC_MVP_QAIC_PHASE4_TO_FINAL_1.4.2.md` |
| ITEM-001324 | REVIEW_REQUIRED | CURRENT_OR_RECENT | `01_DOCS\CDC\MEMO_MVP_QAIC_PHASE4_TO_FINAL_1.4.2.md` |
| ITEM-000018 | REVIEW_REQUIRED | CURRENT_OR_RECENT | `01_DOCS\CDC\📘 CDC_MVP_QAIC_OPERATIONAL_ROADMAP.md` |
| ITEM-001325 | REVIEW_REQUIRED | CURRENT_OR_RECENT | `01_DOCS\CDC\📘 CDC_MVP_QAIC_WEB_APP_LEXIQUE_FIRST_0.6.2_REAL_FUSION_REPAIR.md` |
| ITEM-001326 | REVIEW_REQUIRED | CURRENT_OR_RECENT | `01_DOCS\CDC\📘 CDC_MVP_QAIC_WEB_APP_LEXIQUE_FIRST_0.7.2_REAL_FULL_SOURCE_FUSION.md` |
| ITEM-002458 | REVIEW_REQUIRED | CURRENT_OR_RECENT | `01_DOCS\REFERENCE_DOCS_REAL_FULL_SOURCE_FUSION_0.7.2_20260620\00_ORIGINAL_SOURCES_UNMODIFIED\ORIGINAL__📘 CDC_MVP_QAIC_WEB_APP_LEXIQUE_FIRST_0.6.2_REAL_FUSION_REPAIR.md` |
| ITEM-002464 | REVIEW_REQUIRED | CURRENT_OR_RECENT | `01_DOCS\REFERENCE_DOCS_REAL_FULL_SOURCE_FUSION_0.7.2_20260620\01_FUSED_DOCS_0.7.2\📘 CDC_MVP_QAIC_WEB_APP_LEXIQUE_FIRST_0.7.2_REAL_FULL_SOURCE_FUSION.md` |
| ITEM-001345 | REVIEW_REQUIRED | CURRENT_OR_RECENT | `01_DOCS\RUNBOOK\RUNBOOK_MVP_QAIC_P1G_PROMPT_LIBRARY_CONTRACT_0.6.0.md` |
| ITEM-002015 | REVIEW_REQUIRED | CURRENT_OR_RECENT | `01_DOCS\VALIDATION\P12E_LEXIQUE_20260617-004551\mvpqaic_31_p12e_lexique_contract_status_core.gs` |
| ITEM-002012 | REVIEW_REQUIRED | CURRENT_OR_RECENT | `01_DOCS\VALIDATION\P12E_LEXIQUE_20260617-004551\P12E_LEXIQUE_CONTRACT_20260617-004551.csv` |
| ITEM-002177 | REVIEW_REQUIRED | CURRENT_OR_RECENT | `01_DOCS\VALIDATION\P15A_20260617_122844\P15A_CONSUMER_CONTRACT.md` |
| ITEM-002174 | REVIEW_REQUIRED | CURRENT_OR_RECENT | `01_DOCS\VALIDATION\P15A_20260617_122844\P15A_HEADER_CONTRACT.csv` |
| ITEM-002179 | REVIEW_REQUIRED | CURRENT_OR_RECENT | `01_DOCS\VALIDATION\P15B_20260617_123430\P15B_NAVIGATION_CONTRACT.csv` |
| ITEM-002182 | REVIEW_REQUIRED | CURRENT_OR_RECENT | `01_DOCS\VALIDATION\P15B_20260617_123430\P15B_UI_CONTRACT.md` |
| ITEM-002180 | REVIEW_REQUIRED | CURRENT_OR_RECENT | `01_DOCS\VALIDATION\P15B_20260617_123430\P15B_VIEW_CONTRACT.csv` |
| ITEM-002185 | REVIEW_REQUIRED | CURRENT_OR_RECENT | `01_DOCS\VALIDATION\P15C_20260617_124001\P15C_COMPONENT_SPEC.csv` |
| ITEM-002186 | REVIEW_REQUIRED | CURRENT_OR_RECENT | `01_DOCS\VALIDATION\P15C_20260617_124001\P15C_ROUTE_SPEC.csv` |
| ITEM-002184 | REVIEW_REQUIRED | CURRENT_OR_RECENT | `01_DOCS\VALIDATION\P15C_20260617_124001\P15C_SCREEN_SPEC.csv` |
| ITEM-002188 | REVIEW_REQUIRED | CURRENT_OR_RECENT | `01_DOCS\VALIDATION\P15C_20260617_124001\P15C_WEB_APP_SPEC.md` |
| ITEM-002271 | REVIEW_REQUIRED | CURRENT_OR_RECENT | `01_DOCS\VALIDATION\P21A_20260617_155339\P21A_BUBBLE_CHART_REFERENCE_SPEC.md` |
| ITEM-002414 | REVIEW_REQUIRED | CURRENT_OR_RECENT | `01_DOCS\VALIDATION\P26R_20260618_105204\P26R_TARGET_UX_SPEC.md` |
| ITEM-002424 | REVIEW_REQUIRED | CURRENT_OR_RECENT | `01_DOCS\VALIDATION\P26R2_20260618_105728\P26R2_TARGET_UX_SPEC.md` |
| ITEM-001650 | REVIEW_REQUIRED | CURRENT_OR_RECENT | `01_DOCS\VALIDATION\P7C_APP_SCHEMA_CONTRACT_NO_APPLY_MAXI_20260616-131902\P7C_FIELD_CONTRACT_20260616-131902.csv` |
| ITEM-001654 | REVIEW_REQUIRED | CURRENT_OR_RECENT | `01_DOCS\VALIDATION\P7C_APP_SCHEMA_CONTRACT_NO_APPLY_MAXI_20260616-131902\P7C_MANIFEST_20260616-131902.csv` |
| ITEM-001653 | REVIEW_REQUIRED | CURRENT_OR_RECENT | `01_DOCS\VALIDATION\P7C_APP_SCHEMA_CONTRACT_NO_APPLY_MAXI_20260616-131902\P7C_REPORT_20260616-131902.md` |
| ITEM-001652 | REVIEW_REQUIRED | CURRENT_OR_RECENT | `01_DOCS\VALIDATION\P7C_APP_SCHEMA_CONTRACT_NO_APPLY_MAXI_20260616-131902\P7C_SUMMARY_20260616-131902.csv` |
| ITEM-001649 | REVIEW_REQUIRED | CURRENT_OR_RECENT | `01_DOCS\VALIDATION\P7C_APP_SCHEMA_CONTRACT_NO_APPLY_MAXI_20260616-131902\P7C_TABLE_CONTRACT_20260616-131902.csv` |
| ITEM-001651 | REVIEW_REQUIRED | CURRENT_OR_RECENT | `01_DOCS\VALIDATION\P7C_APP_SCHEMA_CONTRACT_NO_APPLY_MAXI_20260616-131902\P7C_VIEW_CONTRACT_20260616-131902.csv` |
| ITEM-001667 | REVIEW_REQUIRED | CURRENT_OR_RECENT | `01_DOCS\VALIDATION\P8B_REVOLUT_X_QAIC_CONTRACT_PACK_NO_APPLY_20260616-152747\P8A_MVP_QAIC_COMPATIBILITY_MATRIX_20260616-152359.csv` |
| ITEM-001668 | REVIEW_REQUIRED | CURRENT_OR_RECENT | `01_DOCS\VALIDATION\P8B_REVOLUT_X_QAIC_CONTRACT_PACK_NO_APPLY_20260616-152747\P8A_REVOLUT_X_EXECUTION_POLICY_MATRIX_20260616-152359.csv` |
| ITEM-001666 | REVIEW_REQUIRED | CURRENT_OR_RECENT | `01_DOCS\VALIDATION\P8B_REVOLUT_X_QAIC_CONTRACT_PACK_NO_APPLY_20260616-152747\P8A_SUMMARY_20260616-152359.csv` |
| ITEM-001677 | REVIEW_REQUIRED | CURRENT_OR_RECENT | `01_DOCS\VALIDATION\P8B_REVOLUT_X_QAIC_CONTRACT_PACK_NO_APPLY_20260616-152747\P8B_MANIFEST_20260616-152747.csv` |
| ITEM-001670 | REVIEW_REQUIRED | CURRENT_OR_RECENT | `01_DOCS\VALIDATION\P8B_REVOLUT_X_QAIC_CONTRACT_PACK_NO_APPLY_20260616-152747\P8B_MANUAL_EXECUTION_CONTRACT_20260616-152747.csv` |
| ITEM-001673 | REVIEW_REQUIRED | CURRENT_OR_RECENT | `01_DOCS\VALIDATION\P8B_REVOLUT_X_QAIC_CONTRACT_PACK_NO_APPLY_20260616-152747\P8B_MVP_SHEET_PLAN_COMPAT_QAIC_20260616-152747.csv` |
| ITEM-001672 | REVIEW_REQUIRED | CURRENT_OR_RECENT | `01_DOCS\VALIDATION\P8B_REVOLUT_X_QAIC_CONTRACT_PACK_NO_APPLY_20260616-152747\P8B_QAIC_BRIDGE_CONTRACT_20260616-152747.csv` |
| ITEM-001669 | REVIEW_REQUIRED | CURRENT_OR_RECENT | `01_DOCS\VALIDATION\P8B_REVOLUT_X_QAIC_CONTRACT_PACK_NO_APPLY_20260616-152747\P8B_REVOLUT_X_DATA_CONTRACTS_20260616-152747.csv` |
| ITEM-001676 | REVIEW_REQUIRED | CURRENT_OR_RECENT | `01_DOCS\VALIDATION\P8B_REVOLUT_X_QAIC_CONTRACT_PACK_NO_APPLY_20260616-152747\P8B_REVOLUT_X_QAIC_CONTRACT_PACK_REPORT_20260616-152747.md` |
| ITEM-001674 | REVIEW_REQUIRED | CURRENT_OR_RECENT | `01_DOCS\VALIDATION\P8B_REVOLUT_X_QAIC_CONTRACT_PACK_NO_APPLY_20260616-152747\P8B_SCRIPT_CONTRACTS_COMPAT_QAIC_20260616-152747.csv` |
| ITEM-001671 | REVIEW_REQUIRED | CURRENT_OR_RECENT | `01_DOCS\VALIDATION\P8B_REVOLUT_X_QAIC_CONTRACT_PACK_NO_APPLY_20260616-152747\P8B_SECRETS_GOVERNANCE_CONTRACT_20260616-152747.csv` |
| ITEM-001675 | REVIEW_REQUIRED | CURRENT_OR_RECENT | `01_DOCS\VALIDATION\P8B_REVOLUT_X_QAIC_CONTRACT_PACK_NO_APPLY_20260616-152747\P8B_SUMMARY_20260616-152747.csv` |
| ITEM-001680 | REVIEW_REQUIRED | CURRENT_OR_RECENT | `01_DOCS\VALIDATION\P8C_REVOLUT_X_SKELETON_PLAN_NO_APPLY_20260616-153551\P8B_MANUAL_EXECUTION_CONTRACT_20260616-152747.csv` |
| ITEM-001681 | REVIEW_REQUIRED | CURRENT_OR_RECENT | `01_DOCS\VALIDATION\P8C_REVOLUT_X_SKELETON_PLAN_NO_APPLY_20260616-153551\P8B_QAIC_BRIDGE_CONTRACT_20260616-152747.csv` |
| ITEM-001679 | REVIEW_REQUIRED | CURRENT_OR_RECENT | `01_DOCS\VALIDATION\P8C_REVOLUT_X_SKELETON_PLAN_NO_APPLY_20260616-153551\P8B_REVOLUT_X_DATA_CONTRACTS_20260616-152747.csv` |
| ITEM-001732 | REVIEW_REQUIRED | CURRENT_OR_RECENT | `01_DOCS\VALIDATION\P8E_REVOLUT_X_QAIC_DOCS_PACK_NO_APPLY_20260616-160712\MVPQAIC_QAIC_BRIDGE_CONTRACT_20260616-160712.md` |
| ITEM-001730 | REVIEW_REQUIRED | CURRENT_OR_RECENT | `01_DOCS\VALIDATION\P8E_REVOLUT_X_QAIC_DOCS_PACK_NO_APPLY_20260616-160712\MVPQAIC_REVOLUT_X_DATA_CONTRACTS_20260616-160712.md` |
| ITEM-001723 | REVIEW_REQUIRED | CURRENT_OR_RECENT | `01_DOCS\VALIDATION\P8E_REVOLUT_X_QAIC_DOCS_PACK_NO_APPLY_20260616-160712\P8B_MANUAL_EXECUTION_CONTRACT_20260616-152747.csv` |
| ITEM-001725 | REVIEW_REQUIRED | CURRENT_OR_RECENT | `01_DOCS\VALIDATION\P8E_REVOLUT_X_QAIC_DOCS_PACK_NO_APPLY_20260616-160712\P8B_QAIC_BRIDGE_CONTRACT_20260616-152747.csv` |
| ITEM-001722 | REVIEW_REQUIRED | CURRENT_OR_RECENT | `01_DOCS\VALIDATION\P8E_REVOLUT_X_QAIC_DOCS_PACK_NO_APPLY_20260616-160712\P8B_REVOLUT_X_DATA_CONTRACTS_20260616-152747.csv` |
| ITEM-001724 | REVIEW_REQUIRED | CURRENT_OR_RECENT | `01_DOCS\VALIDATION\P8E_REVOLUT_X_QAIC_DOCS_PACK_NO_APPLY_20260616-160712\P8B_SECRETS_GOVERNANCE_CONTRACT_20260616-152747.csv` |
| ITEM-001738 | REVIEW_REQUIRED | CURRENT_OR_RECENT | `01_DOCS\VALIDATION\P9A_COLUMN_REVIEW_PREP_NO_APPLY_20260616-161203\P7C_FIELD_CONTRACT_20260616-131902.csv` |
| ITEM-001737 | REVIEW_REQUIRED | CURRENT_OR_RECENT | `01_DOCS\VALIDATION\P9A_COLUMN_REVIEW_PREP_NO_APPLY_20260616-161203\P7C_TABLE_CONTRACT_20260616-131902.csv` |
| ITEM-001739 | REVIEW_REQUIRED | CURRENT_OR_RECENT | `01_DOCS\VALIDATION\P9A_COLUMN_REVIEW_PREP_NO_APPLY_20260616-161203\P7C_VIEW_CONTRACT_20260616-131902.csv` |
| ITEM-001397 | REVIEW_REQUIRED | CURRENT_OR_RECENT | `01_DOCS\VALIDATION\VALIDATION_MATRIX_MVP_QAIC_P1G_PROMPT_LIBRARY_CONTRACT_0.6.0.md` |
| ITEM-002883 | REVIEW_REQUIRED | CURRENT_OR_RECENT | `02_BUILD\LEXIQUE_READER_MVP\03_BUILD_OUTPUTS\P24D_20260618_000512\P24D_DATA_CONTRACT_FIELDS.csv` |
| ITEM-002884 | REVIEW_REQUIRED | CURRENT_OR_RECENT | `02_BUILD\LEXIQUE_READER_MVP\03_BUILD_OUTPUTS\P24D_20260618_000512\P24D_OUTPUT_CONTRACT.json` |
| ITEM-002885 | REVIEW_REQUIRED | CURRENT_OR_RECENT | `02_BUILD\LEXIQUE_READER_MVP\03_BUILD_OUTPUTS\P24D_20260618_000512\README_P24D_DATA_AND_OUTPUT_CONTRACT.md` |

## 4. 🧩 Contenu fusionné par source

### ITEM-001299 — `00_ADMIN\CHANGELOG_MVP_QAIC_P1G_PROMPT_LIBRARY_CONTRACT_0.6.0.md`

- **Légitimité :** `REVIEW_REQUIRED`
- **Actualité :** `CURRENT_OR_RECENT`
- **Classe :** `DOC_SOURCE_TO_COMPARE`
- **Dernière modification :** `2026-06-11T22:13:30`

```text
# 🧾 Changelog — MVP QAIC P1-G Prompt Library Contract

**Version :** `MVP_QAIC_P1_PROMPT_QUALITY_CORE_0.6.0_SAFE_FULL_FUSION_P1E_P1F_P1G`
**Date :** 2026-06-11

## Ajouts

- Extension du core fusionné P1-E/P1-F vers P1-G.
- Ajout de `PROMPT_LIBRARY`.
- Ajout de fonctions publiques :
  - `MVPQAIC_PromptLibraryStatus()`
  - `MVPQAIC_PromptLibraryRefresh()`
- Modèle de lignes typées :
  - `CORE_CONTRACT`
  - `GEM_PROFILE`
  - `PROMPT_CONTRACT`
- Déclaration des capacités par Gem/runtime : métriques supportées, fiables, partielles, non supportées.
- Règles anti-hallucination scoring : score impossible => `NOT_AVAILABLE`, `REVIEW_REQUIRED` ou `BLOCKED`.

## Gouvernance

- Pas de nouveau script durable isolé.
- Remplacement complet du core `mvpqaic_11_p1_prompt_quality_core.gs`.
- Anciennes versions P1-E/P1-F isolées à archiver/retirer du live après validation.
```

### ITEM-000003 — `01_DOCS\01_CDC\_CDC_MVP_QAIC_PYTHON_MIGRATION_0.1.0.md`

- **Légitimité :** `REVIEW_REQUIRED`
- **Actualité :** `CURRENT_OR_RECENT`
- **Classe :** `DOC_SOURCE_TO_COMPARE`
- **Dernière modification :** `2026-06-20T16:27:59`

```text
# 📋 CDC — Migration MVP QAIC vers Python 0.1.0
## 🎯 Objet et résultat attendu
## ✅ Exigences fonctionnelles
- Conserver le MVP **Lexique / KB / WebApp first**.
- Inventorier en P1 les sources Apps Script, Sheets, WebApp et Lexique/KB sous forme de miroir documentaire.
- Formaliser en P2 les contrats de données, prompts et runtime.
- Préparer en P3 un squelette de package sans logique live.
- Produire en P4 des rapports CLI locaux en lecture seule.
- Couvrir en P5 les validations unitaires, contractuelles et d’intégration hors live.
- Encadrer en P6 l’export/import par contrôles, diff et approbation humaine.
- Garder en P7 le bridge QAIC avancé optionnel, séparé et désactivé par défaut.
## 🧩 Domaines à migrer
1. Lexique KB : entrées, alias, catégories, statut et provenance.
2. Prompt library : identifiants, versions, variables, règles et tests.
3. Decision journal : décisions, contexte, horodatage et traçabilité.
4. GPT response intake : enveloppe, parsing, validation et quarantaine.

--- extrait ---
# 📋 CDC — Migration MVP QAIC vers Python 0.1.0

## 🎯 Objet et résultat attendu

Préparer une architecture Python compatible avec le MVP Google Sheets / Apps Script / WebApp, sans remplacer le MVP ni introduire de moteur de trading. Le lot P0.7.6 livre uniquement la référence, les limites et la procédure de migration.

## ✅ Exigences fonctionnelles

- Conserver le MVP **Lexique / KB / WebApp first**.
- Inventorier en P1 les sources Apps Script, Sheets, WebApp et Lexique/KB sous forme de miroir documentaire.
- Formaliser en P2 les contrats de données, prompts et runtime.
- Préparer en P3 un squelette de package sans logique live.
- Produire en P4 des rapports CLI locaux en lecture seule.
- Couvrir en P5 les validations unitaires, contractuelles et d’intégration hors live.
- Encadrer en P6 l’export/import par contrôles, diff et approbation humaine.
- Garder en P7 le bridge QAIC avancé optionnel, séparé et désactivé par défaut.

## 🧩 Domaines à migrer

1. Lexique KB : entrées, alias, catégories, statut et provenance.
2. Prompt library : identifiants, versions, variables, règles et tests.
3. Decision journal : décisions, contexte, horodatage et traçabilité.
4. GPT response intake : enveloppe, parsing, validation et quarantaine.
5. Quality dashboard : métriques calculées depuis des données validées.
6. WebApp readiness : vues, contrats d’API future et checks de préparation.
7. Bridges AppSheet / Looker / Stitch / Antigravity : adaptateurs futurs, sans couplage au cœur.

## 🛡️ Exigences non fonctionnelles

- Lecture seule par défaut, sorties locales, déterministes et auditables.
- Validation stricte des schémas et rejet explicite des données invalides.
- Aucun secret dans le dépôt ou les exports.
- Journalisation sans données sensibles.
- Compatibilité des formats documentée et versionnée.
- Rollback par abandon des artefacts Python et retour à la source MVP inchangée.

## ⛔ Hors périmètre

Auto-trading, broker, ordres, sizing, API Revolut, moteur QAIC avancé intégré, mutation live, écriture Google Sheets, déploiement Apps Script et gestion de secrets.

## 📏 Critères d’acceptation P0

- Arborescence de référence présente.
- Documents P0.7.6 et manifeste présents.

```

### ITEM-000004 — `01_DOCS\01_CDC\📘_CDC_MVP_QAIC_PYTHON_MIGRATION_0.1.0.md`

- **Légitimité :** `REVIEW_REQUIRED`
- **Actualité :** `CURRENT_OR_RECENT`
- **Classe :** `DOC_SOURCE_TO_COMPARE`
- **Dernière modification :** `2026-06-20T16:27:59`

```text
# 📋 CDC — Migration MVP QAIC vers Python 0.1.0
## 🎯 Objet et résultat attendu
## ✅ Exigences fonctionnelles
- Conserver le MVP **Lexique / KB / WebApp first**.
- Inventorier en P1 les sources Apps Script, Sheets, WebApp et Lexique/KB sous forme de miroir documentaire.
- Formaliser en P2 les contrats de données, prompts et runtime.
- Préparer en P3 un squelette de package sans logique live.
- Produire en P4 des rapports CLI locaux en lecture seule.
- Couvrir en P5 les validations unitaires, contractuelles et d’intégration hors live.
- Encadrer en P6 l’export/import par contrôles, diff et approbation humaine.
- Garder en P7 le bridge QAIC avancé optionnel, séparé et désactivé par défaut.
## 🧩 Domaines à migrer
1. Lexique KB : entrées, alias, catégories, statut et provenance.
2. Prompt library : identifiants, versions, variables, règles et tests.
3. Decision journal : décisions, contexte, horodatage et traçabilité.
4. GPT response intake : enveloppe, parsing, validation et quarantaine.

--- extrait ---
# 📋 CDC — Migration MVP QAIC vers Python 0.1.0

## 🎯 Objet et résultat attendu

Préparer une architecture Python compatible avec le MVP Google Sheets / Apps Script / WebApp, sans remplacer le MVP ni introduire de moteur de trading. Le lot P0.7.6 livre uniquement la référence, les limites et la procédure de migration.

## ✅ Exigences fonctionnelles

- Conserver le MVP **Lexique / KB / WebApp first**.
- Inventorier en P1 les sources Apps Script, Sheets, WebApp et Lexique/KB sous forme de miroir documentaire.
- Formaliser en P2 les contrats de données, prompts et runtime.
- Préparer en P3 un squelette de package sans logique live.
- Produire en P4 des rapports CLI locaux en lecture seule.
- Couvrir en P5 les validations unitaires, contractuelles et d’intégration hors live.
- Encadrer en P6 l’export/import par contrôles, diff et approbation humaine.
- Garder en P7 le bridge QAIC avancé optionnel, séparé et désactivé par défaut.

## 🧩 Domaines à migrer

1. Lexique KB : entrées, alias, catégories, statut et provenance.
2. Prompt library : identifiants, versions, variables, règles et tests.
3. Decision journal : décisions, contexte, horodatage et traçabilité.
4. GPT response intake : enveloppe, parsing, validation et quarantaine.
5. Quality dashboard : métriques calculées depuis des données validées.
6. WebApp readiness : vues, contrats d’API future et checks de préparation.
7. Bridges AppSheet / Looker / Stitch / Antigravity : adaptateurs futurs, sans couplage au cœur.

## 🛡️ Exigences non fonctionnelles

- Lecture seule par défaut, sorties locales, déterministes et auditables.
- Validation stricte des schémas et rejet explicite des données invalides.
- Aucun secret dans le dépôt ou les exports.
- Journalisation sans données sensibles.
- Compatibilité des formats documentée et versionnée.
- Rollback par abandon des artefacts Python et retour à la source MVP inchangée.

## ⛔ Hors périmètre

Auto-trading, broker, ordres, sizing, API Revolut, moteur QAIC avancé intégré, mutation live, écriture Google Sheets, déploiement Apps Script et gestion de secrets.

## 📏 Critères d’acceptation P0

- Arborescence de référence présente.
- Documents P0.7.6 et manifeste présents.

```

### ITEM-000017 — `01_DOCS\CDC\CDC_MVP_QAIC_OPERATIONAL_ROADMAP.md`

- **Légitimité :** `REVIEW_REQUIRED`
- **Actualité :** `CURRENT_OR_RECENT`
- **Classe :** `DOC_SOURCE_TO_COMPARE`
- **Dernière modification :** `2026-06-22T15:21:15`

```text
# CDC — MVP QAIC Operational Roadmap

## Objectif produit

Construire une boucle opérateur exploitable pour revue crypto éducative et support décisionnel :
entrée portfolio/capture, prompt GEM, réponse GEM, review queue, entrée journal locale.

## Hors périmètre

- Trading automatique.
- Ordres broker.
- Sizing automatique.
- Accès Revolut X réel depuis MVP.
- `NO_REVOLUTX_REAL_ACCESS_FROM_MVP`.
- Écriture Google Sheets sans décision explicite séparée.

## Roadmap opérationnelle

| Version | Horizon | Objectif | Critère d'acceptation |
|---|---:|---|---|
| V0.1 | fait | Boucle GEM locale | P118-P122 scellés |
| V0.2 | 1-3 jours | Premier vrai test opérateur | vrai portfolio + vraie réponse GEM + journal local |
| V0.3 | 3-7 jours | Ergonomie locale | helper d'entrée + dossiers run propres |
| V0.4 | 1-2 semaines | Mini cockpit local | interface simple input -> prompt -> capture -> journal |
| V0.5 | 2-4 semaines | Pont MVP vers QAIC privé | export propre sans ordre ni sizing |
| V0.6 | 3-5 semaines | Portfolio review usuel | templates par cas d'usage |
| V0.7 | 4-6 semaines | Historique et qualité | registry runs + métriques erreurs |
| V1.0 | 4-8 semaines | Version opérationnelle contrôlée | usage quotidien stable et auditable |

## Definition of Done V1.0

- Run quotidien en moins de 5 minutes.
- Prompt GEM généré depuis input local.
- Réponse GEM capturée.
- Missing data et blockers visibles.
- Journal local généré.
- Aucune action live implicite.
- Séparation MVP public / QAIC privé respectée.
```

### ITEM-001323 — `01_DOCS\CDC\MEMO_CDC_MVP_QAIC_PHASE4_TO_FINAL_1.4.2.md`

- **Légitimité :** `REVIEW_REQUIRED`
- **Actualité :** `CURRENT_OR_RECENT`
- **Classe :** `DOC_SOURCE_TO_COMPARE`
- **Dernière modification :** `2026-06-13T11:02:54`

```text
# 🛠️ MVP QAIC — Mémo CDC de situation vers version finale livrable
## 1. Situation actuelle validée
- `mvpqaic_31_lexique_master_search_cockpit_core.gs`
- baseline stricte : `MVP_QAIC_LEXIQUE_MASTER_SEARCH_COCKPIT_CORE_0.9.0_FINAL_SIMPLE_SAFE`
- audit ajouté : `MVP_QAIC_P3A1_EXISTING_LEXIQUE_GAP_AUDIT_STRICT_0_9_0_BASELINE_FUSION_1.4.1_SAFE`
- prochain batch : `MVP_QAIC_P3B_LEXIQUE_ENRICHMENT_QUEUE_APPLY_SAFE_1.4.2_SAFE`
## 2. Décision de gouvernance immédiate
- micro-patches successifs sauf blocker réel ;
- nouveaux onglets de gouvernance non nécessaires ;
- nouveau lexique central redondant ;
- reconstruction de tables sources sans preuve ;
- application automatique de corrections métier.
- travailler sur les tables existantes ;
- garder `📚 LEXIQUE_MASTER` comme frontend généré ;
- garder `🔎 SEARCH_COCKPIT` comme interface de recherche ;
- enrichir les sources uniquement après queue révisable ;

--- extrait ---
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
- `OUT
```

### ITEM-001324 — `01_DOCS\CDC\MEMO_MVP_QAIC_PHASE4_TO_FINAL_1.4.2.md`

- **Légitimité :** `REVIEW_REQUIRED`
- **Actualité :** `CURRENT_OR_RECENT`
- **Classe :** `DOC_SOURCE_TO_COMPARE`
- **Dernière modification :** `2026-06-13T13:24:31`

```text
# 🛠️ MVP QAIC — Mémo situation Phase 4 → Version finale livrable
## 1. Cadre projet confirmé
- une Knowledge Base structurée ;
- des prompts contrôlés ;
- des règles de scoring explicables ;
- des risk guards ;
- des checklists ;
- un journal de décision ;
- une future Web App / interface utilisateur ;
- une transition ultérieure vers QAIC complet.
## 2. Discipline de développement actée
- toujours partir de la version source exacte fournie ou confirmée ;
- éviter les scripts doublons ;
- fusionner dans les scripts durables existants quand c’est cohérent ;
- livrer des scripts complets remplaçables ;
- produire ZIP + README + manifest pour chaque batch important ;

--- extrait ---
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
-
```

### ITEM-000018 — `01_DOCS\CDC\📘 CDC_MVP_QAIC_OPERATIONAL_ROADMAP.md`

- **Légitimité :** `REVIEW_REQUIRED`
- **Actualité :** `CURRENT_OR_RECENT`
- **Classe :** `DOC_SOURCE_TO_COMPARE`
- **Dernière modification :** `2026-06-22T15:21:15`

```text
# CDC — MVP QAIC Operational Roadmap

## Objectif produit

Construire une boucle opérateur exploitable pour revue crypto éducative et support décisionnel :
entrée portfolio/capture, prompt GEM, réponse GEM, review queue, entrée journal locale.

## Hors périmètre

- Trading automatique.
- Ordres broker.
- Sizing automatique.
- Accès Revolut X réel depuis MVP.
- `NO_REVOLUTX_REAL_ACCESS_FROM_MVP`.
- Écriture Google Sheets sans décision explicite séparée.

## Roadmap opérationnelle

| Version | Horizon | Objectif | Critère d'acceptation |
|---|---:|---|---|
| V0.1 | fait | Boucle GEM locale | P118-P122 scellés |
| V0.2 | 1-3 jours | Premier vrai test opérateur | vrai portfolio + vraie réponse GEM + journal local |
| V0.3 | 3-7 jours | Ergonomie locale | helper d'entrée + dossiers run propres |
| V0.4 | 1-2 semaines | Mini cockpit local | interface simple input -> prompt -> capture -> journal |
| V0.5 | 2-4 semaines | Pont MVP vers QAIC privé | export propre sans ordre ni sizing |
| V0.6 | 3-5 semaines | Portfolio review usuel | templates par cas d'usage |
| V0.7 | 4-6 semaines | Historique et qualité | registry runs + métriques erreurs |
| V1.0 | 4-8 semaines | Version opérationnelle contrôlée | usage quotidien stable et auditable |

## Definition of Done V1.0

- Run quotidien en moins de 5 minutes.
- Prompt GEM généré depuis input local.
- Réponse GEM capturée.
- Missing data et blockers visibles.
- Journal local généré.
- Aucune action live implicite.
- Séparation MVP public / QAIC privé respectée.
```

### ITEM-001325 — `01_DOCS\CDC\📘 CDC_MVP_QAIC_WEB_APP_LEXIQUE_FIRST_0.6.2_REAL_FUSION_REPAIR.md`

- **Légitimité :** `REVIEW_REQUIRED`
- **Actualité :** `CURRENT_OR_RECENT`
- **Classe :** `DOC_SOURCE_TO_COMPARE`
- **Dernière modification :** `2026-06-16T01:40:04`

```text
# 📘 CDC — MVP QAIC Web App Lexique-first
## 0. 🧾 Historique des changements
## 1. 🎯 Vision produit
- le **lexique crypto** ;
- les **méthodes d’analyse** ;
- les **signaux trading** ;
- les **playbooks de risque** ;
- les **checklists quotidiennes** ;
- le **scoring explicable** ;
- le **journal de décision**.
## 2. 🧠 Principe central : Lexique, méthodes et signaux d’abord
## 3. 🧭 Positionnement fonctionnel
- comprendre les notions crypto/trading ;
- rechercher rapidement une méthode ou un signal ;
- structurer une analyse ;
- réduire les décisions impulsives ;

--- extrait ---
# 📘 CDC — MVP QAIC Web App Lexique-first

> **Projet :** 🛠️ MVP QAIC — Crypto Signal OS Web App
> **Version :** `MVP_QAIC_CDC_0.6.2_REAL_FUSION_REPAIR_APPSHEET_PORTFOLIO_BROKER_TRANSITION`
> **Date :** 2026-06-16
> **Statut :** `DRAFT_FOR_HUMAN_VALIDATION_REAL_FUSION_REPAIR`
> **Format :** Markdown `.md`

---

## 0. 🧾 Historique des changements

| Version | Date | Statut | Changements |
|---|---:|---|---|
| `0.1.0` | 2026-06-11 | Draft | Cadrage initial MVP QAIC Lexique-first |
| `0.2.0` | 2026-06-11 | Drive review ready | Reformulation : Web App rapide Lexique/Méthodes/Signaux d'abord, puis transition progressive vers le QAIC final comme UI / IDE utilisateur |
| `0.2.1` | 2026-06-11 | Drive structure final ready | Confirmation de la structure Drive finale avec ajout de `08_QAIC_BRIDGE/` et `09_WEB_APP_IDE/`, préparation import Drive, bridge QAIC et future UI / IDE QAIC |
| `0.2.2` | 2026-06-11 | Antigravity P0 process ready | Ajout du modus operandi Antigravity : workspace local, lots P0-A à P0-E, garde-fous, critères de validation, livrables attendus avant import Google |
| `0.3.1` | 2026-06-11 | P0-B6 Governance full fusion | Pleine fusion avec les documents 0.2.2 sans suppression ; ajout état P0-A→P0-B5, Full Signal Mapping 50/50, GPT/Revolut X read-only bridge, Runbook, Validation Matrix et prochaine phase P0-C |
| `0.6.2` | 2026-06-16 | Real fusion repair | Réparation après audit : reprise réelle du CDC 0.3.1, intégration AppSheet P5, priorité Lexique/Prompts, correction Portfolio Revolut X non reporté, préparation automation ordres/TP/SL/trailing via QAIC Python sous gates. |

---

## 1. 🎯 Vision produit

Le projet **🛠️ MVP QAIC — Crypto Signal OS Web App** vise à livrer rapidement une **Web App crypto éducative, analytique et décisionnelle**, centrée en priorité sur :

- le **lexique crypto** ;
- les **méthodes d’analyse** ;
- les **signaux trading** ;
- les **playbooks de risque** ;
- les **checklists quotidiennes** ;
- le **scoring explicable** ;
- le **journal de décision**.

Le MVP ne cherche pas à reproduire immédiatement tout le système QAIC complet. Il doit d’abord devenir un outil simple, rapide, lisible et utilisable au quotidien.
```

### ITEM-001326 — `01_DOCS\CDC\📘 CDC_MVP_QAIC_WEB_APP_LEXIQUE_FIRST_0.7.2_REAL_FULL_SOURCE_FUSION.md`

- **Légitimité :** `REVIEW_REQUIRED`
- **Actualité :** `CURRENT_OR_RECENT`
- **Classe :** `DOC_SOURCE_TO_COMPARE`
- **Dernière modification :** `2026-06-20T09:39:50`

```text
# 📘 CDC — MVP QAIC Web App Lexique-first
## 0. 🧾 Historique des changements
## 1. 🎯 Vision produit
- le **lexique crypto** ;
- les **méthodes d’analyse** ;
- les **signaux trading** ;
- les **playbooks de risque** ;
- les **checklists quotidiennes** ;
- le **scoring explicable** ;
- le **journal de décision**.
## 2. 🧠 Principe central : Lexique, méthodes et signaux d’abord
## 3. 🧭 Positionnement fonctionnel
- comprendre les notions crypto/trading ;
- rechercher rapidement une méthode ou un signal ;
- structurer une analyse ;
- réduire les décisions impulsives ;

--- extrait ---
<!--
REAL FULL SOURCE FUSION 0.7.2
Source original preserved: 📘 CDC_MVP_QAIC_WEB_APP_LEXIQUE_FIRST_0.6.2_REAL_FUSION_REPAIR.md
Source SHA256: 00f3d38c78243036b0c16a2fa37fcc5571cbc389282052ed2a27ffd55db83369
Source lines: 829
Fusion rule: original content is kept, then a scope-split correction block is appended.
No Drive overwrite. No Apps Script run. No clasp push.
-->

# 📘 CDC — MVP QAIC Web App Lexique-first

> **Projet :** 🛠️ MVP QAIC — Crypto Signal OS Web App
> **Version :** `MVP_QAIC_CDC_0.6.2_REAL_FUSION_REPAIR_APPSHEET_PORTFOLIO_BROKER_TRANSITION`
> **Date :** 2026-06-16
> **Statut :** `DRAFT_FOR_HUMAN_VALIDATION_REAL_FUSION_REPAIR`
> **Format :** Markdown `.md`

---

## 0. 🧾 Historique des changements

| Version | Date | Statut | Changements |
|---|---:|---|---|
| `0.1.0` | 2026-06-11 | Draft | Cadrage initial MVP QAIC Lexique-first |
| `0.2.0` | 2026-06-11 | Drive review ready | Reformulation : Web App rapide Lexique/Méthodes/Signaux d'abord, puis transition progressive vers le QAIC final comme UI / IDE utilisateur |
| `0.2.1` | 2026-06-11 | Drive structure final ready | Confirmation de la structure Drive finale avec ajout de `08_QAIC_BRIDGE/` et `09_WEB_APP_IDE/`, préparation import Drive, bridge QAIC et future UI / IDE QAIC |
| `0.2.2` | 2026-06-11 | Antigravity P0 process ready | Ajout du modus operandi Antigravity : workspace local, lots P0-A à P0-E, garde-fous, critères de validation, livrables attendus avant import Google |
| `0.3.1` | 2026-06-11 | P0-B6 Governance full fusion | Pleine fusion avec les documents 0.2.2 sans suppression ; ajout état P0-A→P0-B5, Full Signal Mapping 50/50, GPT/Revolut X read-only bridge, Runbook, Validation Matrix et prochaine phase P0-C |
| `0.6.2` | 2026-06-16 | Real fusion repair | Réparation après audit : reprise réelle du CDC 0.3.1, intégration AppSheet P5, priorité Lexique/Prompts, correction Portfolio Revolut X non reporté, préparation automation ordres/TP/SL/trailing via QAIC Python sous gates. |

---

## 1. 🎯 Vision produit

Le projet **🛠️ MVP QAIC — Crypto Signal OS Web App** vise à livrer rapidement une **Web App crypto éducative, analytique et décisionnelle**, centrée en priorité sur :

- l
```

### ITEM-002458 — `01_DOCS\REFERENCE_DOCS_REAL_FULL_SOURCE_FUSION_0.7.2_20260620\00_ORIGINAL_SOURCES_UNMODIFIED\ORIGINAL__📘 CDC_MVP_QAIC_WEB_APP_LEXIQUE_FIRST_0.6.2_REAL_FUSION_REPAIR.md`

- **Légitimité :** `REVIEW_REQUIRED`
- **Actualité :** `CURRENT_OR_RECENT`
- **Classe :** `DOC_SOURCE_TO_COMPARE`
- **Dernière modification :** `2026-06-20T09:48:54`

```text
_Contenu non lisible ou vide._
```

### ITEM-002464 — `01_DOCS\REFERENCE_DOCS_REAL_FULL_SOURCE_FUSION_0.7.2_20260620\01_FUSED_DOCS_0.7.2\📘 CDC_MVP_QAIC_WEB_APP_LEXIQUE_FIRST_0.7.2_REAL_FULL_SOURCE_FUSION.md`

- **Légitimité :** `REVIEW_REQUIRED`
- **Actualité :** `CURRENT_OR_RECENT`
- **Classe :** `DOC_SOURCE_TO_COMPARE`
- **Dernière modification :** `2026-06-20T09:46:17`

```text
_Contenu non lisible ou vide._
```

### ITEM-001345 — `01_DOCS\RUNBOOK\RUNBOOK_MVP_QAIC_P1G_PROMPT_LIBRARY_CONTRACT_0.6.0.md`

- **Légitimité :** `REVIEW_REQUIRED`
- **Actualité :** `CURRENT_OR_RECENT`
- **Classe :** `DOC_SOURCE_TO_COMPARE`
- **Dernière modification :** `2026-06-11T23:49:16`

```text
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
```

### ITEM-002015 — `01_DOCS\VALIDATION\P12E_LEXIQUE_20260617-004551\mvpqaic_31_p12e_lexique_contract_status_core.gs`

- **Légitimité :** `REVIEW_REQUIRED`
- **Actualité :** `CURRENT_OR_RECENT`
- **Classe :** `SCRIPT_OR_UI_SOURCE_TO_CLASSIFY`
- **Dernière modification :** `2026-06-17T00:45:55`

```text
/**
 * MVP QAIC - P12E Lexique Contract Status Core
 * Version: MVP_QAIC_P12E_LEXIQUE_CONTRACT_STATUS_CORE_0_1_0_NO_WRITE_SAFE
 * Status: DEV_LOCAL_ONLY_NO_LIVE_APPLY
 * Safety: HUMAN_REVIEW_ONLY / NO_AUTO_ORDER / NO_AUTO_SIZING / NO_BROKER_EXECUTION / NO_REAL_ORDER
 * Purpose: local-only lexique contract status object. No Spreadsheet service calls. No external calls.
 */
const MVPQAIC_P12E_LEXIQUE_CONTRACT_STATUS_CORE_VERSION =
  'MVP_QAIC_P12E_LEXIQUE_CONTRACT_STATUS_CORE_0_1_0_NO_WRITE_SAFE';

function MVPQAIC_P12E_LexiqueContractStatus() {
  return {
    step: 'MVPQAIC_P12E_LEXIQUE_CONTRACT_STATUS',
    version: MVPQAIC_P12E_LEXIQUE_CONTRACT_STATUS_CORE_VERSION,
    status: 'OK',
    mode: 'HUMAN_REVIEW_ONLY',
    safety: {
      auto_order: false,
      auto_sizing: false,
      broker_execution: false,
      real_order: false,
      sheet_write: false,
      appsheet_api: false,
      external_network_calls: false,
      secret_logging: false
    },
    lexique_contract: {
      domains: ['CRYPTO_TERMS', 'METHODS', 'SIGNALS', 'RISK_RULES', 'PROMPT_OUTPUTS', 'UI_NAVIGATION'],
      required_fields: ['term_id', 'term', 'category', 'definition_short', 'usage_context', 'data_required', 'blocked_if_missing', 'review_status'],
      critical_rule: 'If critical data is missing, return REVIEW_REQUIRED or BLOCKED. Never invent trading values.'
    },
    next_action: 'P12F_LEXIQUE_SCHEMA_LOCAL_SOURCE_NO_LIVE_APPLY'
  };
}

function MVPQAIC_P12E_LexiqueContractStatus_Log() {
  var status = MVPQAIC_P12E_LexiqueContractStatus();
  Logger.log(JSON.stringify(status, null, 2));
  return status;
}
```

### ITEM-002012 — `01_DOCS\VALIDATION\P12E_LEXIQUE_20260617-004551\P12E_LEXIQUE_CONTRACT_20260617-004551.csv`

- **Légitimité :** `REVIEW_REQUIRED`
- **Actualité :** `CURRENT_OR_RECENT`
- **Classe :** `DOC_SOURCE_TO_COMPARE`
- **Dernière modification :** `2026-06-17T00:45:54`

```text
"run_id","field","required","type","rule","apply_now"
"P12E-LEXIQUE-ARCH-20260617-004551","term_id","YES","TEXT","Stable unique identifier","NO"
"P12E-LEXIQUE-ARCH-20260617-004551","term","YES","TEXT","Visible lexique label","NO"
"P12E-LEXIQUE-ARCH-20260617-004551","category","YES","CONTROLLED_LIST","Crypto term, method, signal, risk, prompt output, UI","NO"
"P12E-LEXIQUE-ARCH-20260617-004551","definition_short","YES","TEXT","Decision-grade short definition","NO"
"P12E-LEXIQUE-ARCH-20260617-004551","definition_pro","RECOMMENDED","TEXT","Professional definition","NO"
"P12E-LEXIQUE-ARCH-20260617-004551","usage_context","YES","TEXT","Where and when to use","NO"
"P12E-LEXIQUE-ARCH-20260617-004551","data_required","YES","TEXT","Minimum data before analysis","NO"
"P12E-LEXIQUE-ARCH-20260617-004551","blocked_if_missing","YES","BOOLEAN_OR_LIST","Block if critical data is missing","NO"
"P12E-LEXIQUE-ARCH-20260617-004551","signals_related","RECOMMENDED","TEXT","Related signals or methods","NO"
"P12E-LEXIQUE-ARCH-20260617-004551","review_status","YES","CONTROLLED_LIST","DRAFT, REVIEW_REQUIRED, VALIDATED, DEPRECATED","NO"
```

### ITEM-002177 — `01_DOCS\VALIDATION\P15A_20260617_122844\P15A_CONSUMER_CONTRACT.md`

- **Légitimité :** `REVIEW_REQUIRED`
- **Actualité :** `CURRENT_OR_RECENT`
- **Classe :** `DOC_SOURCE_TO_COMPARE`
- **Dernière modification :** `2026-06-17T12:28:44`

```text
# MVP QAIC P15A - Approved Lexique Consumer Contract

Status: OK
Gate: P15A_APPROVED_LEXIQUE_CONSUMER_CONTRACT_READY_READONLY

## Source
- Approved tab: LEXIQUE_CRYPTO_APPROVED
- Source seal: P14I_20260617_122259

## Shape
- Rows including header: 61
- Data rows: 60
- Columns: 34
- Header status: OK
- Shape status: OK

## Consumer readiness
- Readiness: READY_WITH_REVIEW_FLAGS_FOR_P15B_UI_MAPPING_DESIGN
- Blocker count: 0
- Review flags: DEFINITION_HEADER_NOT_AUTO_DETECTED

## Safety
- Google API call: YES_READ_ONLY
- Sheet write: NO
- Apps Script execution: NO
- AppSheet API: NO
- Broker/order/sizing: NO

Next action: P15B_UI_MAPPING_AND_NAVIGATION_CONTRACT_LOCAL_ONLY
```

### ITEM-002174 — `01_DOCS\VALIDATION\P15A_20260617_122844\P15A_HEADER_CONTRACT.csv`

- **Légitimité :** `REVIEW_REQUIRED`
- **Actualité :** `CURRENT_OR_RECENT`
- **Classe :** `DOC_SOURCE_TO_COMPARE`
- **Dernière modification :** `2026-06-17T12:28:44`

```text
"Index","Header","LowerHeader","ConsumerRoleGuess","RequiredForUI","Notes"
"1","run_id","run_id","DETAIL","NO",""
"2","review_queue_id","review_queue_id","DETAIL","NO",""
"3","priority_rank","priority_rank","DETAIL","NO",""
"4","review_priority","review_priority","DETAIL","NO",""
"5","term_id","term_id","DETAIL","NO",""
"6","term","term","TERM","YES",""
"7","category","category","CATEGORY","YES",""
"8","definition_short","definition_short","DETAIL","NO",""
"9","usage_context","usage_context","DETAIL","NO",""
"10","data_required","data_required","DETAIL","NO",""
"11","blocked_if_missing","blocked_if_missing","DETAIL","NO",""
"12","suggested_human_action","suggested_human_action","DETAIL","NO",""
"13","human_decision","human_decision","DECISION","RECOMMENDED",""
"14","allowed_human_decisions","allowed_human_decisions","DETAIL","NO",""
"15","proposed_definition_short","proposed_definition_short","DETAIL","NO",""
"16","proposed_usage_context","proposed_usage_context","DETAIL","NO",""
"17","proposed_data_required","proposed_data_required","DETAIL","NO",""
"18","proposed_blocked_if_missing","proposed_blocked_if_missing","DETAIL","NO",""
"19","reviewer","reviewer","DETAIL","NO",""
"20","reviewer_notes","reviewer_notes","DETAIL","NO",""
"21","validation_status","validation_status","DETAIL","NO",""
"22","apply_now","apply_now","DETAIL","NO",""
"23","live_apply_allowed","live_apply_allowed","DETAIL","NO",""
"24","p13b_review_status","p13b_review_status","DETAIL","NO",""
"25","human_final_decision","human_final_decision","DETAIL","NO",""
"26","human_proposed_label","human_proposed_label","DETAIL","NO",""
"27","human_proposed_definition","human_proposed_definition","DETAIL","NO",""
"28","human_notes","human_notes","NOTES","RECOMMENDED",""
"29","live_apply_authorized","live_apply_authorized","DETAIL","NO",""
"30","review_owner","review_owner","DETAIL","NO",""
"31","reviewed_at","reviewed_at","DETAIL","NO",""
"32","p13b_local_only_guard","p13b_local_only_guard","DETAIL","NO",""
"33","assistant_completion_ready","assistant_completion_ready","DETAIL","NO",""
"34","assistant_completion_source","assistant_completion_source","DETAIL","NO",""
```

### ITEM-002179 — `01_DOCS\VALIDATION\P15B_20260617_123430\P15B_NAVIGATION_CONTRACT.csv`

- **Légitimité :** `REVIEW_REQUIRED`
- **Actualité :** `CURRENT_OR_RECENT`
- **Classe :** `DOC_SOURCE_TO_COMPARE`
- **Dernière modification :** `2026-06-17T12:34:30`

```text
"NavOrder","Category","Rows","RouteKey","VisibleInMvp","DefaultCollapsed","Notes"
"1","CRYPTO_TERMS","12","crypto_terms","YES","NO","Lexique approved category"
"2","METHODS","12","methods","YES","NO","Lexique approved category"
"3","PROMPT_OUTPUTS","8","prompt_outputs","YES","NO","Lexique approved category"
"4","RISK_RULES","8","risk_rules","YES","NO","Lexique approved category"
"5","SIGNALS","12","signals","YES","NO","Lexique approved category"
"6","UI_NAVIGATION","8","ui_navigation","YES","NO","Lexique approved category"
```

### ITEM-002182 — `01_DOCS\VALIDATION\P15B_20260617_123430\P15B_UI_CONTRACT.md`

- **Légitimité :** `REVIEW_REQUIRED`
- **Actualité :** `CURRENT_OR_RECENT`
- **Classe :** `DOC_SOURCE_TO_COMPARE`
- **Dernière modification :** `2026-06-17T12:34:30`

```text
# MVP QAIC P15B - UI Mapping & Navigation Contract

Status: OK
Gate: P15B_UI_MAPPING_AND_NAVIGATION_CONTRACT_READY_LOCAL_ONLY

## Readiness
- UI readiness: READY_WITH_DEFINITION_MAPPING_REVIEW_FOR_P15C
- Blocker count: 0
- Definition mapping status: REVIEW_REQUIRED_NON_BLOCKING

## Source
- Approved tab: LEXIQUE_CRYPTO_APPROVED
- Source P15A: P15A_20260617_122844
- Categories: 6
- Headers: 34

## Safety
- Google API call: NO
- Sheet write: NO
- Apps Script execution: NO
- AppSheet API: NO
- Broker/order/sizing: NO

Next action: P15C_WEB_APP_READ_MODEL_AND_SCREEN_SPEC_LOCAL_ONLY
```

### ITEM-002180 — `01_DOCS\VALIDATION\P15B_20260617_123430\P15B_VIEW_CONTRACT.csv`

- **Légitimité :** `REVIEW_REQUIRED`
- **Actualité :** `CURRENT_OR_RECENT`
- **Classe :** `DOC_SOURCE_TO_COMPARE`
- **Dernière modification :** `2026-06-17T12:34:30`

```text
"ViewId","ViewName","Purpose","SourceTab","PrimaryFilter","SearchField","DetailField","WriteAllowed","Notes"
"lexique_home","Lexique Home","Category overview and quick access","LEXIQUE_CRYPTO_APPROVED","category","term","definition","NO","MVP landing view"
"lexique_search","Lexique Search","Search terms/methods/signals/rules","LEXIQUE_CRYPTO_APPROVED","category","term","definition","NO","No write in MVP reader"
"lexique_detail","Lexique Detail","Open one entry with notes/governance","LEXIQUE_CRYPTO_APPROVED","category","term","definition","NO","Human review only"
"prompt_support","Prompt Support","Use approved lexique as prompt context","LEXIQUE_CRYPTO_APPROVED","category","term","definition","NO","No trading execution"
```

### ITEM-002185 — `01_DOCS\VALIDATION\P15C_20260617_124001\P15C_COMPONENT_SPEC.csv`

- **Légitimité :** `REVIEW_REQUIRED`
- **Actualité :** `CURRENT_OR_RECENT`
- **Classe :** `DOC_SOURCE_TO_COMPARE`
- **Dernière modification :** `2026-06-17T12:40:02`

```text
"ComponentId","ComponentName","InputModel","Output","Required","Notes"
"category_nav","Category Navigation","category_counts","selected_category","YES","6 categories"
"search_box","Search Box","term|category|detail_fallback","filtered_entries","YES","Client-side search acceptable for 60 rows"
"entry_card","Entry Card","entry_id|term|category","entry_preview","YES","No write"
"definition_panel","Definition Panel","definition_or_detail_fallback","readable_detail","YES","DETAIL_FALLBACK_ALL_NON_CORE_FIELDS"
"governance_badge","Governance Badge","decision|source_row","status_badge","RECOMMENDED","Hidden if field unavailable"
"safety_banner","Safety Banner","static_policy","human_review_only_notice","YES","No broker/order/sizing"
```

### ITEM-002186 — `01_DOCS\VALIDATION\P15C_20260617_124001\P15C_ROUTE_SPEC.csv`

- **Légitimité :** `REVIEW_REQUIRED`
- **Actualité :** `CURRENT_OR_RECENT`
- **Classe :** `DOC_SOURCE_TO_COMPARE`
- **Dernière modification :** `2026-06-17T12:40:02`

```text
"Route","ScreenId","DataFilter","RouteStatus","Notes"
"/lexique","home","none","READY","Default landing"
"/lexique/crypto_terms","category","category=CRYPTO_TERMS","READY","Rows=12"
"/lexique/methods","category","category=METHODS","READY","Rows=12"
"/lexique/prompt_outputs","category","category=PROMPT_OUTPUTS","READY","Rows=8"
"/lexique/risk_rules","category","category=RISK_RULES","READY","Rows=8"
"/lexique/signals","category","category=SIGNALS","READY","Rows=12"
"/lexique/ui_navigation","category","category=UI_NAVIGATION","READY","Rows=8"
"/lexique/search","search","query","READY","Client-side query"
"/lexique/entry/:entry_id","detail","entry_id","READY","Generated entry id"
"/prompt-support","prompt_support","selected_terms","READY","No trading execution"
```

### ITEM-002184 — `01_DOCS\VALIDATION\P15C_20260617_124001\P15C_SCREEN_SPEC.csv`

- **Légitimité :** `REVIEW_REQUIRED`
- **Actualité :** `CURRENT_OR_RECENT`
- **Classe :** `DOC_SOURCE_TO_COMPARE`
- **Dernière modification :** `2026-06-17T12:40:02`

```text
"ScreenId","ScreenName","Route","PrimaryPurpose","DataSource","MainComponents","WriteAllowed","SafetyNotes"
"home","Lexique Home","/lexique","Overview of categories and quick search","LEXIQUE_CRYPTO_APPROVED","CategoryNav|SearchBox|FeaturedTerms","NO","Read-only MVP"
"category","Category List","/lexique/:category","Browse entries by category","LEXIQUE_CRYPTO_APPROVED","CategoryHeader|EntryList|Filters","NO","No trading action"
"search","Search Results","/lexique/search","Search terms/methods/signals/rules","LEXIQUE_CRYPTO_APPROVED","SearchBox|ResultList|CategoryChips","NO","Reader only"
"detail","Entry Detail","/lexique/entry/:entry_id","Read one approved concept","LEXIQUE_CRYPTO_APPROVED","EntryTitle|DefinitionPanel|GovernanceBadges|RelatedTerms","NO","Human review only"
"prompt_support","Prompt Support","/prompt-support","Use lexique as context for safe prompts","LEXIQUE_CRYPTO_APPROVED","PromptContextBuilder|SelectedTerms|SafetyBanner","NO","No order/sizing/broker"
```

### ITEM-002188 — `01_DOCS\VALIDATION\P15C_20260617_124001\P15C_WEB_APP_SPEC.md`

- **Légitimité :** `REVIEW_REQUIRED`
- **Actualité :** `CURRENT_OR_RECENT`
- **Classe :** `DOC_SOURCE_TO_COMPARE`
- **Dernière modification :** `2026-06-17T12:40:02`

```text
# MVP QAIC P15C - Web App Read Model & Screen Spec

Status: OK
Gate: P15C_WEB_APP_READ_MODEL_AND_SCREEN_SPEC_READY_LOCAL_ONLY

## Read model
- Source tab: LEXIQUE_CRYPTO_APPROVED
- Category field: category
- Term field: term
- Definition field:
- Definition display mode: DETAIL_FALLBACK_ALL_NON_CORE_FIELDS

## Screens
- Lexique Home
- Category List
- Search Results
- Entry Detail
- Prompt Support

## Safety
- Read-only web app MVP
- No Sheet write
- No Apps Script execution
- No AppSheet API
- No broker/order/sizing

Next action: P15D_ANTIGRAVITY_STITCH_BUILD_PROMPT_PACK_LOCAL_ONLY
```

### ITEM-002271 — `01_DOCS\VALIDATION\P21A_20260617_155339\P21A_BUBBLE_CHART_REFERENCE_SPEC.md`

- **Légitimité :** `REVIEW_REQUIRED`
- **Actualité :** `CURRENT_OR_RECENT`
- **Classe :** `DOC_SOURCE_TO_COMPARE`
- **Dernière modification :** `2026-06-17T15:53:39`

```text
# P21A - Bubble chart reference spec

Centre : Lecture graphique token Revolut X

Bulles principales :
- Tendance : EMA, MA, MACD, SuperTrend, Ichimoku, Directional Movement
- Momentum : RSI, Stochastic, Stochastic RSI, ROC, Momentum, CCI
- Volatilité : Bollinger Bands, Keltner Channels, Standard Deviation, Historical Volatility
- Volume / Flux : Volume, OBV, MFI, Chaikin Money Flow, VWAP, Volume Profile
- Niveaux : Pivot Points, Donchian Channels, Price Channel, Volume Profile, VWAP
- Structure : Zig Zag, Williams Fractal, Choppiness Index

Chaque bulle doit expliquer :
- rôle
- quand l'utiliser
- lecture rapide
- faux signal typique
- priorité affichage
```

### ITEM-002414 — `01_DOCS\VALIDATION\P26R_20260618_105204\P26R_TARGET_UX_SPEC.md`

- **Légitimité :** `REVIEW_REQUIRED`
- **Actualité :** `CURRENT_OR_RECENT`
- **Classe :** `DOC_SOURCE_TO_COMPARE`
- **Dernière modification :** `2026-06-18T10:52:05`

```text
# P26R — Target UX Spec for Clean Rebuild
## Status
## Core principle
## Valid sources
- Code/data baseline: P24D final sealed webapp baseline.
- Visual asset baseline: P26B3 16:9 high-quality assets.
- Rejected: P26C, P26C2, P26C3 and any derivative patch-chain output.
## Final site structure
### 1. Header
- Product name: QAIC Lexique Crypto
- Safety badge: HUMAN_REVIEW_ONLY / READ_ONLY
- Optional compact navigation.
### 2. Lexique first
- search bar;
- category/family filters;
- list of terms;

--- extrait ---
# P26R — Target UX Spec for Clean Rebuild

## Status
P26C patch chain is rejected. This document defines the clean target UX for P27.

## Core principle
The product must be a lexicon-first educational webapp, not a stack of technical product-version blocks.

## Valid sources
- Code/data baseline: P24D final sealed webapp baseline.
- Visual asset baseline: P26B3 16:9 high-quality assets.
- Rejected: P26C, P26C2, P26C3 and any derivative patch-chain output.

## Final site structure

### 1. Header
- Product name: QAIC Lexique Crypto
- Safety badge: HUMAN_REVIEW_ONLY / READ_ONLY
- Optional compact navigation.

### 2. Lexique first
The landing view starts with:
- search bar;
- category/family filters;
- list of terms;
- clear cards;
- detail drawer/page for each term.

### 3. Fiche detail model
Each fiche must have:
- title;
- source family;
- definition;
- usage;
- when to use;
- what to watch;
- associated topic;
- one thumbnail visual;
- one fullscreen visual;
- optional solo indicator visual if precise indicator.

No random visual injection. Use deterministic mapping from dataset.

### 4. Post-lexique thematic submenu
After the lexicon area, show thematic cards:

- 📊 Indicateurs
- 📉 Exemples graphiques
- 🫧 Carte indicateurs
- 🚀 Workflow quotidien
- 🧭 Méthode de lecture
- ✅ Contrat & sécurité

These are not product-version blocks. They are educational navigation topics.

### 5. Visual behavior
- Topic thumbnail: clean, readable, low text.
- Fullscreen image: detailed 16:9 visual.
- Click behavior: open lightbox.
- Zoom: browser-friendly, but minimal.
- Avoid embedding multiple visuals inside each other.
- Avoid duplicated global visual galleries on every fiche.

### 6. Revolut X Indicators
Represent as an indicator-family section:

- 📈 Tendance
- ⚡ Momentum
- 📦 Volume
- 🌊 Volatilité
- 🧱 Support / Résistance
- ✅ Confirmation

Each indicator fiche receives one precise visual when available.

### 7. Carte indicateurs
This is not an empty page.
It is a map of indicator families and how to combine them:
- trend + momentum;
- volume confirmation;
- volatility context;
- support/resistance structure;
- human review before decision.

### 8. Output format
Clean pr
```

### ITEM-002424 — `01_DOCS\VALIDATION\P26R2_20260618_105728\P26R2_TARGET_UX_SPEC.md`

- **Légitimité :** `REVIEW_REQUIRED`
- **Actualité :** `CURRENT_OR_RECENT`
- **Classe :** `DOC_SOURCE_TO_COMPARE`
- **Dernière modification :** `2026-06-18T10:57:28`

```text
# P26R2 — Target UX Spec for P27 Clean Rebuild

## Decision
P26C / P26C2 / P26C3 must not be used as product baseline.

## Valid sources
- P24D final sealed webapp baseline: content/data baseline.
- P26B3 16:9 visual assets: visual source baseline.

## Product principle
The site is lexique-first. It must not be a stack of technical version chapters.

## Final navigation
1. Header
2. Lexique
3. Fiche detail
4. Thématiques after lexique:
   - 📊 Indicateurs
   - 📉 Exemples graphiques
   - 🫧 Carte indicateurs
   - 🚀 Workflow quotidien
   - 🧭 Méthode de lecture
   - ✅ Contrat & sécurité

## Fiche detail
Each fiche has:
- title;
- family/category;
- definition;
- usage;
- warning;
- one relevant thumbnail visual;
- one fullscreen visual;
- related topic link.

## Visual rules
- No global visual gallery injected everywhere.
- No random DOM regex visual injection.
- No nested/stacked visual cards.
- Miniature is a preview only.
- Fullscreen is used for reading detail.
- For detailed infographics: provide a dedicated full view.

## Revolut X Indicators
Group by family:
- 📈 Tendance
- ⚡ Momentum
- 📦 Volume
- 🌊 Volatilité
- 🧱 Support / Résistance
- ✅ Confirmation

## Carte indicateurs
This is a family map page. It explains how indicator families combine.

## Hidden/internal only
Technical labels like P24D/P26/P27, V3/V3+/V3++ must not appear as main user-facing chapters.
```

### ITEM-001650 — `01_DOCS\VALIDATION\P7C_APP_SCHEMA_CONTRACT_NO_APPLY_MAXI_20260616-131902\P7C_FIELD_CONTRACT_20260616-131902.csv`

- **Légitimité :** `REVIEW_REQUIRED`
- **Actualité :** `CURRENT_OR_RECENT`
- **Classe :** `DOC_SOURCE_TO_COMPARE`
- **Dernière modification :** `2026-06-16T13:19:04`

```text
"run_id","table_code","sheet_title","field_name","field_status","editable","apply_allowed"
"P7C-SCHEMA-20260616-131902","SEARCH_COCKPIT","SEARCH_DEMO","record_id","REQUIRED_OR_RECOMMENDED_REVIEW","NO","NO"
"P7C-SCHEMA-20260616-131902","SEARCH_COCKPIT","SEARCH_DEMO","label","REQUIRED_OR_RECOMMENDED_REVIEW","NO","NO"
"P7C-SCHEMA-20260616-131902","SEARCH_COCKPIT","SEARCH_DEMO","status","REQUIRED_OR_RECOMMENDED_REVIEW","NO","NO"
"P7C-SCHEMA-20260616-131902","SEARCH_COCKPIT","SEARCH_DEMO","category","REQUIRED_OR_RECOMMENDED_REVIEW","NO","NO"
"P7C-SCHEMA-20260616-131902","SEARCH_COCKPIT","SEARCH_DEMO","source","REQUIRED_OR_RECOMMENDED_REVIEW","NO","NO"
"P7C-SCHEMA-20260616-131902","SEARCH_COCKPIT","SEARCH_DEMO","last_reviewed_at","REQUIRED_OR_RECOMMENDED_REVIEW","NO","NO"
"P7C-SCHEMA-20260616-131902","LEXIQUE_MASTER","GLOSSARY_TAGS","record_id","REQUIRED_OR_RECOMMENDED_REVIEW","NO","NO"
"P7C-SCHEMA-20260616-131902","LEXIQUE_MASTER","GLOSSARY_TAGS","label","REQUIRED_OR_RECOMMENDED_REVIEW","NO","NO"
"P7C-SCHEMA-20260616-131902","LEXIQUE_MASTER","GLOSSARY_TAGS","status","REQUIRED_OR_RECOMMENDED_REVIEW","NO","NO"
"P7C-SCHEMA-20260616-131902","LEXIQUE_MASTER","GLOSSARY_TAGS","category","REQUIRED_OR_RECOMMENDED_REVIEW","NO","NO"
"P7C-SCHEMA-20260616-131902","LEXIQUE_MASTER","GLOSSARY_TAGS","source","REQUIRED_OR_RECOMMENDED_REVIEW","NO","NO"
"P7C-SCHEMA-20260616-131902","LEXIQUE_MASTER","GLOSSARY_TAGS","last_reviewed_at","REQUIRED_OR_RECOMMENDED_REVIEW","NO","NO"
"P7C-SCHEMA-20260616-131902","PROMPT_CONTEXT_PACKS","🧠 PROMPT_CONTEXT_PACKS","record_id","REQUIRED_OR_RECOMMENDED_REVIEW","NO","NO"
"P7C-SCHEMA-20260616-131902","PROMPT_CONTEXT_PACKS","🧠 PROMPT_CONTEXT_PACKS","label","REQUIRED_OR_RECOMMENDED_REVIEW","NO","NO"
"P7C-SCHEMA-20260616-131902","PROMPT_CONTEXT_PACKS","🧠 PROMPT_CONTEXT_PACKS","status","REQUIRED_OR_RECOMMENDED_REVIEW","NO","NO"
"P7C-SCHEMA-20260616-131902","PROMPT_CONTEXT_PACKS","🧠 PROMPT_CONTEXT_PACKS","category","REQUIRED_OR_RECOMMENDED_REVIEW","NO","NO"
"P7C-SCHEMA-20260616-131902","PROMPT_CONTEXT_PACKS","🧠 PROMPT_CONTEXT_PACKS","source","REQUIRED_OR_RECOMMENDED_REVIEW","NO","NO"
"P7C-SCHEMA-20260616-131902","PROMPT_CONTEXT_PACKS","🧠 PROMPT_CONTEXT_
```

### ITEM-001654 — `01_DOCS\VALIDATION\P7C_APP_SCHEMA_CONTRACT_NO_APPLY_MAXI_20260616-131902\P7C_MANIFEST_20260616-131902.csv`

- **Légitimité :** `REVIEW_REQUIRED`
- **Actualité :** `CURRENT_OR_RECENT`
- **Classe :** `DOC_SOURCE_TO_COMPARE`
- **Dernière modification :** `2026-06-16T13:19:04`

```text
"run_id","file","path","length","status"
"P7C-SCHEMA-20260616-131902","P7C_FIELD_CONTRACT_20260616-131902.csv","G:\Mon Drive\👥 JULIEN [Perso]\📈 Trading JRb\Solutions & Dev (Trading JRb)\📈 QAIC\🛠️ MVP QAIC — Crypto Signal OS\01_DOCS\VALIDATION\P7C_APP_SCHEMA_CONTRACT_NO_APPLY_MAXI_20260616-131902\P7C_FIELD_CONTRACT_20260616-131902.csv","7801","OK"
"P7C-SCHEMA-20260616-131902","P7C_REPORT_20260616-131902.md","G:\Mon Drive\👥 JULIEN [Perso]\📈 Trading JRb\Solutions & Dev (Trading JRb)\📈 QAIC\🛠️ MVP QAIC — Crypto Signal OS\01_DOCS\VALIDATION\P7C_APP_SCHEMA_CONTRACT_NO_APPLY_MAXI_20260616-131902\P7C_REPORT_20260616-131902.md","310","OK"
"P7C-SCHEMA-20260616-131902","P7C_SUMMARY_20260616-131902.csv","G:\Mon Drive\👥 JULIEN [Perso]\📈 Trading JRb\Solutions & Dev (Trading JRb)\📈 QAIC\🛠️ MVP QAIC — Crypto Signal OS\01_DOCS\VALIDATION\P7C_APP_SCHEMA_CONTRACT_NO_APPLY_MAXI_20260616-131902\P7C_SUMMARY_20260616-131902.csv","428","OK"
"P7C-SCHEMA-20260616-131902","P7C_TABLE_CONTRACT_20260616-131902.csv","G:\Mon Drive\👥 JULIEN [Perso]\📈 Trading JRb\Solutions & Dev (Trading JRb)\📈 QAIC\🛠️ MVP QAIC — Crypto Signal OS\01_DOCS\VALIDATION\P7C_APP_SCHEMA_CONTRACT_NO_APPLY_MAXI_20260616-131902\P7C_TABLE_CONTRACT_20260616-131902.csv","2473","OK"
"P7C-SCHEMA-20260616-131902","P7C_VIEW_CONTRACT_20260616-131902.csv","G:\Mon Drive\👥 JULIEN [Perso]\📈 Trading JRb\Solutions & Dev (Trading JRb)\📈 QAIC\🛠️ MVP QAIC — Crypto Signal OS\01_DOCS\VALIDATION\P7C_APP_SCHEMA_CONTRACT_NO_APPLY_MAXI_20260616-131902\P7C_VIEW_CONTRACT_20260616-131902.csv","670","OK"
```

### ITEM-001653 — `01_DOCS\VALIDATION\P7C_APP_SCHEMA_CONTRACT_NO_APPLY_MAXI_20260616-131902\P7C_REPORT_20260616-131902.md`

- **Légitimité :** `REVIEW_REQUIRED`
- **Actualité :** `CURRENT_OR_RECENT`
- **Classe :** `DOC_SOURCE_TO_COMPARE`
- **Dernière modification :** `2026-06-16T13:19:04`

```text
# MVP QAIC - P7C App Schema Contract
Run ID: P7C-SCHEMA-20260616-131902
Gate: P7C_SCHEMA_CONTRACT_READY_FOR_P7D_SYNTHESIS_NO_APPLY
Tables: 10
Fields: 60
Views: 5
Write allowed: 0
Apply-like: 0
Decision: NO APPLY. No Sheet/AppSheet/Apps Script mutation.
Next: P7D_FINAL_SYNTHESIS_AND_STOP_NO_APPLY
```

### ITEM-001652 — `01_DOCS\VALIDATION\P7C_APP_SCHEMA_CONTRACT_NO_APPLY_MAXI_20260616-131902\P7C_SUMMARY_20260616-131902.csv`

- **Légitimité :** `REVIEW_REQUIRED`
- **Actualité :** `CURRENT_OR_RECENT`
- **Classe :** `DOC_SOURCE_TO_COMPARE`
- **Dernière modification :** `2026-06-16T13:19:04`

```text
"run_id","status","p7c_gate","total_rows","resolved_core_targets","missing_core_targets","table_contract_rows","field_contract_rows","view_contract_rows","write_allowed_rows","apply_like_rows","cleanup_authorized","apply_authorized","next_action"
"P7C-SCHEMA-20260616-131902","OK","P7C_SCHEMA_CONTRACT_READY_FOR_P7D_SYNTHESIS_NO_APPLY","128","10","0","10","60","5","0","0","NO","NO","P7D_FINAL_SYNTHESIS_AND_STOP_NO_APPLY"
```

### ITEM-001649 — `01_DOCS\VALIDATION\P7C_APP_SCHEMA_CONTRACT_NO_APPLY_MAXI_20260616-131902\P7C_TABLE_CONTRACT_20260616-131902.csv`

- **Légitimité :** `REVIEW_REQUIRED`
- **Actualité :** `CURRENT_OR_RECENT`
- **Classe :** `DOC_SOURCE_TO_COMPARE`
- **Dernière modification :** `2026-06-16T13:19:04`

```text
"run_id","table_code","sheet_title","sheet_id","app_module","app_role","key_strategy","read_allowed","write_allowed","delete_allowed","apply_allowed","schema_status"
"P7C-SCHEMA-20260616-131902","SEARCH_COCKPIT","SEARCH_DEMO","913965412","M01_SEARCH_COCKPIT","CORE_TABLE","REVIEW_EXISTING_KEY_OR_CREATE_STABLE_ID_LATER","YES_BLUEPRINT_ONLY","NO","NO","NO","DRAFT_CONTRACT_NO_APPLY"
"P7C-SCHEMA-20260616-131902","LEXIQUE_MASTER","GLOSSARY_TAGS","361912386","M02_LEXIQUE_CORE","CORE_TABLE","REVIEW_EXISTING_KEY_OR_CREATE_STABLE_ID_LATER","YES_BLUEPRINT_ONLY","NO","NO","NO","DRAFT_CONTRACT_NO_APPLY"
"P7C-SCHEMA-20260616-131902","PROMPT_CONTEXT_PACKS","🧠 PROMPT_CONTEXT_PACKS","1225030026","M03_PROMPT_FACTORY","CORE_TABLE","REVIEW_EXISTING_KEY_OR_CREATE_STABLE_ID_LATER","YES_BLUEPRINT_ONLY","NO","NO","NO","DRAFT_CONTRACT_NO_APPLY"
"P7C-SCHEMA-20260616-131902","PROMPT_LEXIQUE_BRIDGE","🔗 PROMPT_LEXIQUE_BRIDGE","1177488306","M03_PROMPT_FACTORY","CORE_TABLE","REVIEW_EXISTING_KEY_OR_CREATE_STABLE_ID_LATER","YES_BLUEPRINT_ONLY","NO","NO","NO","DRAFT_CONTRACT_NO_APPLY"
"P7C-SCHEMA-20260616-131902","PROMPT_LIBRARY","METHOD_LIBRARY","2028965973","M03_PROMPT_FACTORY","CORE_TABLE","REVIEW_EXISTING_KEY_OR_CREATE_STABLE_ID_LATER","YES_BLUEPRINT_ONLY","NO","NO","NO","DRAFT_CONTRACT_NO_APPLY"
"P7C-SCHEMA-20260616-131902","PROMPT_READY_TO_COPY","🧩 PROMPT_READY_TO_COPY","1041347966","M03_PROMPT_FACTORY","CORE_TABLE","REVIEW_EXISTING_KEY_OR_CREATE_STABLE_ID_LATER","YES_BLUEPRINT_ONLY","NO","NO","NO","DRAFT_CONTRACT_NO_APPLY"
"P7C-SCHEMA-20260616-131902","PROMPT_RUN_QUEUE","📤 JOURNAL_APPEND_QUEUE","1366021627","M04_RUN_QUEUES","CORE_TABLE","REVIEW_EXISTING_KEY_OR_CREATE_STABLE_ID_LATER","YES_BLUEPRINT_ONLY","NO","NO","NO","DRAFT_CONTRACT_NO_APPLY"
"P7C-SCHEMA-20260616-131902","RESPONSE_INTAKE_QUEUE","📥 RESPONSE_INTAKE_QUEUE","1785131134","M04_RUN_QUEUES","CORE_TABLE","REVIEW_EXISTING_KEY_OR_CREATE_STABLE_ID_LATER","YES_BLUEPRINT_ONLY","NO","NO","NO","DRAFT_CONTRACT_NO_APPLY"
"P7C-SCHEMA-20260616-131902","DECISION_JOURNAL","DECISION_MATRIX","2113266008","M05_DECISION_JOURNAL","CORE_TABLE","REVIEW_EXISTING_KEY_OR_CREATE_STABLE_ID_LATER","YES_BLUEPRINT_ONLY","NO","NO","NO","DRAFT_CONTRACT_
```

### ITEM-001651 — `01_DOCS\VALIDATION\P7C_APP_SCHEMA_CONTRACT_NO_APPLY_MAXI_20260616-131902\P7C_VIEW_CONTRACT_20260616-131902.csv`

- **Légitimité :** `REVIEW_REQUIRED`
- **Actualité :** `CURRENT_OR_RECENT`
- **Classe :** `DOC_SOURCE_TO_COMPARE`
- **Dernière modification :** `2026-06-16T13:19:04`

```text
"run_id","view_id","label","module_id","view_type","write_allowed","apply_allowed"
"P7C-SCHEMA-20260616-131902","HOME_SEARCH","Accueil / Recherche","M01_SEARCH_COCKPIT","READ_ONLY_BLUEPRINT","NO","NO"
"P7C-SCHEMA-20260616-131902","LEXIQUE_DETAIL","Lexique detail","M02_LEXIQUE_CORE","READ_ONLY_BLUEPRINT","NO","NO"
"P7C-SCHEMA-20260616-131902","PROMPT_READY","Prompts prets a copier","M03_PROMPT_FACTORY","READ_ONLY_BLUEPRINT","NO","NO"
"P7C-SCHEMA-20260616-131902","RUN_QUEUE","Run queue","M04_RUN_QUEUES","READ_ONLY_BLUEPRINT","NO","NO"
"P7C-SCHEMA-20260616-131902","DECISION_JOURNAL","Decision journal","M05_DECISION_JOURNAL","READ_ONLY_BLUEPRINT","NO","NO"
```

### ITEM-001667 — `01_DOCS\VALIDATION\P8B_REVOLUT_X_QAIC_CONTRACT_PACK_NO_APPLY_20260616-152747\P8A_MVP_QAIC_COMPATIBILITY_MATRIX_20260616-152359.csv`

- **Légitimité :** `REVIEW_REQUIRED`
- **Actualité :** `CURRENT_OR_RECENT`
- **Classe :** `DOC_SOURCE_TO_COMPARE`
- **Dernière modification :** `2026-06-16T15:24:05`

```text
"run_id","mvp_component","qaic_inspiration","status","mode","execution"
"P8A-QAIC-REVX-AUDIT-20260616-152359","REVOLUT_X_PORTFOLIO_RAW","V25_REVOLUT_X_BALANCES_RAW","COMPATIBLE_SKELETON_LATER","CSV_IMPORT_FIRST","NO"
"P8A-QAIC-REVX-AUDIT-20260616-152359","REVOLUT_X_PORTFOLIO_NORMALIZED","V25_PORTFOLIO_MASTER / V25_PORTFOLIO_EXPOSURE","COMPATIBLE_NORMALIZATION_LATER","READONLY_DATA","NO"
"P8A-QAIC-REVX-AUDIT-20260616-152359","REVOLUT_X_TRANSACTIONS_RAW","V25_REVOLUT_X_TRADES_RAW / V25_REVOLUT_STATEMENT_TX_RAW","COMPATIBLE_SKELETON_LATER","CSV_IMPORT_FIRST","NO"
"P8A-QAIC-REVX-AUDIT-20260616-152359","REVOLUT_X_TRANSACTIONS_NORMALIZED","V25_REVOLUT_FISCAL_LEDGER","COMPATIBLE_NORMALIZATION_LATER","READONLY_DATA","NO"
"P8A-QAIC-REVX-AUDIT-20260616-152359","PORTFOLIO_RISK_CONTEXT","V25_PORTFOLIO_RISK_DECISION / V25_PORTFOLIO_INTELLIGENCE","COMPATIBLE_RISK_CONTEXT","HUMAN_REVIEW_ONLY","NO"
"P8A-QAIC-REVX-AUDIT-20260616-152359","MANUAL_ACTION_TICKETS","V25_MANUAL_ORDER_TICKETS / V25_PORTFOLIO_EXECUTION_QUEUE","COMPATIBLE_MANUAL_TICKET","MANUAL_ONLY","NO"
"P8A-QAIC-REVX-AUDIT-20260616-152359","ORDER_DRAFTS_FUTURE","V25_ORDER_LOG / V25_MANUAL_ORDER_LIFECYCLE","FUTURE_GATED_CAPABILITY","DRAFT_REVIEW_ONLY","NO_UNTIL_API_DOC_AND_GO"
"P8A-QAIC-REVX-AUDIT-20260616-152359","TP_SL_PLAN_FUTURE","V25_PRE_TRADE_GUARD / V25_ORDER_LOG","FUTURE_GATED_CAPABILITY","PLAN_ONLY","NO_UNTIL_API_DOC_AND_GO"
"P8A-QAIC-REVX-AUDIT-20260616-152359","REVOLUT_X_RECONCILIATION","V25_POST_TRADE_RECONCILIATION","COMPATIBLE_RECONCILIATION","OBSERVED_ACTION_RECONCILE","NO"
"P8A-QAIC-REVX-AUDIT-20260616-152359","QAIC_SIGNAL_INBOX","QAIC_PY / V25_ALPHA_DECISION_COCKPIT","FUTURE_BRIDGE_READY","READONLY_IMPORT","NO"
```

### ITEM-001668 — `01_DOCS\VALIDATION\P8B_REVOLUT_X_QAIC_CONTRACT_PACK_NO_APPLY_20260616-152747\P8A_REVOLUT_X_EXECUTION_POLICY_MATRIX_20260616-152359.csv`

- **Légitimité :** `REVIEW_REQUIRED`
- **Actualité :** `CURRENT_OR_RECENT`
- **Classe :** `DOC_SOURCE_TO_COMPARE`
- **Dernière modification :** `2026-06-16T15:24:06`

```text
"run_id","capability","current_status","required_gate","notes"
"P8A-QAIC-REVX-AUDIT-20260616-152359","CSV_IMPORT_PORTFOLIO","ALLOWED","HUMAN_IMPORT","No API, no secret"
"P8A-QAIC-REVX-AUDIT-20260616-152359","CSV_IMPORT_TRANSACTIONS","ALLOWED","HUMAN_IMPORT","No API, no secret"
"P8A-QAIC-REVX-AUDIT-20260616-152359","READONLY_API_BALANCES","FUTURE_REVIEW","OFFICIAL_DOCS_AND_SECRET_GOVERNANCE","Read-only only"
"P8A-QAIC-REVX-AUDIT-20260616-152359","ORDER_DRAFT","ALLOWED_AS_DRAFT","HUMAN_REVIEW","No execution"
"P8A-QAIC-REVX-AUDIT-20260616-152359","TP_SL_PLAN","ALLOWED_AS_PLAN","HUMAN_REVIEW","No broker update"
"P8A-QAIC-REVX-AUDIT-20260616-152359","MODIFY_ORDER_REQUEST","FUTURE_GATED","OFFICIAL_ORDER_API_AND_EXPLICIT_GO","Manual approval mandatory"
"P8A-QAIC-REVX-AUDIT-20260616-152359","CANCEL_ORDER_REQUEST","FUTURE_GATED","OFFICIAL_ORDER_API_AND_EXPLICIT_GO","Manual approval mandatory"
"P8A-QAIC-REVX-AUDIT-20260616-152359","REAL_ORDER_EXECUTION","BLOCKED_NOW","API_DOCS_RIGHTS_SECURITY_DOUBLE_CONFIRMATION","No auto order ever"
"P8A-QAIC-REVX-AUDIT-20260616-152359","AUTO_SIZING","BLOCKED_ALWAYS","NONE","Human sizing only"
"P8A-QAIC-REVX-AUDIT-20260616-152359","SECRET_IN_SHEET_OR_APPS_SCRIPT","BLOCKED_ALWAYS","NONE","Use local secret folder or future Secret Manager"
```

### ITEM-001666 — `01_DOCS\VALIDATION\P8B_REVOLUT_X_QAIC_CONTRACT_PACK_NO_APPLY_20260616-152747\P8A_SUMMARY_20260616-152359.csv`

- **Légitimité :** `REVIEW_REQUIRED`
- **Actualité :** `CURRENT_OR_RECENT`
- **Classe :** `DOC_SOURCE_TO_COMPARE`
- **Dernière modification :** `2026-06-16T15:24:06`

```text
"run_id","status","p8a_gate","missing_input_files","relevant_qaic_sheets","reference_script_entries","compatibility_rows","execution_policy_rows","blocked_execution_capabilities","cleanup_authorized","apply_authorized","broker_execution_authorized","order_execution_authorized","sizing_authorized","next_action"
"P8A-QAIC-REVX-AUDIT-20260616-152359","OK","P8A_READY_FOR_P8B_CONTRACT_PACK_NO_APPLY","0","45","17","10","10","3","NO","NO","NO","NO","NO","P8B_REVOLUT_X_QAIC_CONTRACT_PACK_NO_APPLY"
```

### ITEM-001677 — `01_DOCS\VALIDATION\P8B_REVOLUT_X_QAIC_CONTRACT_PACK_NO_APPLY_20260616-152747\P8B_MANIFEST_20260616-152747.csv`

- **Légitimité :** `REVIEW_REQUIRED`
- **Actualité :** `CURRENT_OR_RECENT`
- **Classe :** `DOC_SOURCE_TO_COMPARE`
- **Dernière modification :** `2026-06-16T15:27:51`

```text
"run_id","file","path","length","status"
"P8B-REVX-QAIC-CONTRACT-20260616-152747","P8A_MVP_QAIC_COMPATIBILITY_MATRIX_20260616-152359.csv","G:\Mon Drive\👥 JULIEN [Perso]\📈 Trading JRb\Solutions & Dev (Trading JRb)\📈 QAIC\🛠️ MVP QAIC — Crypto Signal OS\01_DOCS\VALIDATION\P8B_REVOLUT_X_QAIC_CONTRACT_PACK_NO_APPLY_20260616-152747\P8A_MVP_QAIC_COMPATIBILITY_MATRIX_20260616-152359.csv","1714","OK"
"P8B-REVX-QAIC-CONTRACT-20260616-152747","P8A_REVOLUT_X_EXECUTION_POLICY_MATRIX_20260616-152359.csv","G:\Mon Drive\👥 JULIEN [Perso]\📈 Trading JRb\Solutions & Dev (Trading JRb)\📈 QAIC\🛠️ MVP QAIC — Crypto Signal OS\01_DOCS\VALIDATION\P8B_REVOLUT_X_QAIC_CONTRACT_PACK_NO_APPLY_20260616-152747\P8A_REVOLUT_X_EXECUTION_POLICY_MATRIX_20260616-152359.csv","1296","OK"
"P8B-REVX-QAIC-CONTRACT-20260616-152747","P8A_SUMMARY_20260616-152359.csv","G:\Mon Drive\👥 JULIEN [Perso]\📈 Trading JRb\Solutions & Dev (Trading JRb)\📈 QAIC\🛠️ MVP QAIC — Crypto Signal OS\01_DOCS\VALIDATION\P8B_REVOLUT_X_QAIC_CONTRACT_PACK_NO_APPLY_20260616-152747\P8A_SUMMARY_20260616-152359.csv","500","OK"
"P8B-REVX-QAIC-CONTRACT-20260616-152747","P8B_MANUAL_EXECUTION_CONTRACT_20260616-152747.csv","G:\Mon Drive\👥 JULIEN [Perso]\📈 Trading JRb\Solutions & Dev (Trading JRb)\📈 QAIC\🛠️ MVP QAIC — Crypto Signal OS\01_DOCS\VALIDATION\P8B_REVOLUT_X_QAIC_CONTRACT_PACK_NO_APPLY_20260616-152747\P8B_MANUAL_EXECUTION_CONTRACT_20260616-152747.csv","1022","OK"
"P8B-REVX-QAIC-CONTRACT-20260616-152747","P8B_MVP_SHEET_PLAN_COMPAT_QAIC_20260616-152747.csv","G:\Mon Drive\👥 JULIEN [Perso]\📈 Trading JRb\Solutions & Dev (Trading JRb)\📈 QAIC\🛠️ MVP QAIC — Crypto Signal OS\01_DOCS\VALIDATION\P8B_REVOLUT_X_QAIC_CONTRACT_PACK_NO_APPLY_20260616-152747\P8B_MVP_SHEET_PLAN_COMPAT_QAIC_20260616-152747.csv","1645","OK"
"P8B-REVX-QAIC-CONTRACT-20260616-152747","P8B_QAIC_BRIDGE_CONTRACT_20260616-152747.csv","G:\Mon Drive\👥 JULIEN [Perso]\📈 Trading JRb\Solutions & Dev (Trading JRb)\📈 QAIC\🛠️ MVP QAIC — Crypto Signal OS\01_DOCS\VALIDATION\P8B_REVOLUT_X_QAIC_CONTRACT_PACK_NO_APPLY_20260616-152747\P8B_QAIC_BRIDGE_CONTRACT_20260616-152747.csv","953","OK"
"P8B-REVX-QAIC-CONTRACT-20260616-152747","P8B_REVOLUT_X_DATA_CONTRACTS_20260616-1
```

### ITEM-001670 — `01_DOCS\VALIDATION\P8B_REVOLUT_X_QAIC_CONTRACT_PACK_NO_APPLY_20260616-152747\P8B_MANUAL_EXECUTION_CONTRACT_20260616-152747.csv`

- **Légitimité :** `REVIEW_REQUIRED`
- **Actualité :** `CURRENT_OR_RECENT`
- **Classe :** `DOC_SOURCE_TO_COMPARE`
- **Dernière modification :** `2026-06-16T15:27:50`

```text
"run_id","object","status","execution_allowed","mode","api_call","notes"
"P8B-REVX-QAIC-CONTRACT-20260616-152747","MANUAL_ACTION_TICKETS","ALLOWED_NOW_AS_NON_EXECUTABLE","FALSE","MANUAL_ONLY","NO","Prepare checklist/ticket only"
"P8B-REVX-QAIC-CONTRACT-20260616-152747","ORDER_DRAFTS_FUTURE","FUTURE_GATED","FALSE","DRAFT_ONLY","NO","Can model proposed order but cannot execute"
"P8B-REVX-QAIC-CONTRACT-20260616-152747","TP_SL_PLAN_FUTURE","FUTURE_GATED","FALSE","PLAN_ONLY","NO","TP/SL plan only, no broker modification"
"P8B-REVX-QAIC-CONTRACT-20260616-152747","ORDER_CHANGE_REQUESTS_FUTURE","FUTURE_GATED","FALSE","REQUEST_ONLY","NO","Modify/cancel request only until official API and explicit GO"
"P8B-REVX-QAIC-CONTRACT-20260616-152747","BROKER_AUDIT_LOG","ALLOWED_AS_AUDIT","FALSE","AUDIT_ONLY","NO","Trace human decisions and observed outcomes"
"P8B-REVX-QAIC-CONTRACT-20260616-152747","KILL_SWITCH","REQUIRED_BEFORE_ANY_FUTURE_EXECUTION","FALSE","SAFETY_GATE","NO","Must block execution path by default"
```

### ITEM-001673 — `01_DOCS\VALIDATION\P8B_REVOLUT_X_QAIC_CONTRACT_PACK_NO_APPLY_20260616-152747\P8B_MVP_SHEET_PLAN_COMPAT_QAIC_20260616-152747.csv`

- **Légitimité :** `REVIEW_REQUIRED`
- **Actualité :** `CURRENT_OR_RECENT`
- **Classe :** `DOC_SOURCE_TO_COMPARE`
- **Dernière modification :** `2026-06-16T15:27:50`

```text
"run_id","sheet_name","status","visible","apply","compatible_qaic"
"P8B-REVX-QAIC-CONTRACT-20260616-152747","REVOLUT_X_PORTFOLIO_RAW","CONTRACT_ONLY_NOT_CREATED","REVIEW_LATER","NO","YES"
"P8B-REVX-QAIC-CONTRACT-20260616-152747","REVOLUT_X_PORTFOLIO_NORMALIZED","CONTRACT_ONLY_NOT_CREATED","REVIEW_LATER","NO","YES"
"P8B-REVX-QAIC-CONTRACT-20260616-152747","REVOLUT_X_TRANSACTIONS_RAW","CONTRACT_ONLY_NOT_CREATED","REVIEW_LATER","NO","YES"
"P8B-REVX-QAIC-CONTRACT-20260616-152747","REVOLUT_X_TRANSACTIONS_NORMALIZED","CONTRACT_ONLY_NOT_CREATED","REVIEW_LATER","NO","YES"
"P8B-REVX-QAIC-CONTRACT-20260616-152747","PORTFOLIO_RISK_CONTEXT","CONTRACT_ONLY_NOT_CREATED","REVIEW_LATER","NO","YES"
"P8B-REVX-QAIC-CONTRACT-20260616-152747","REVOLUT_X_RECONCILIATION","CONTRACT_ONLY_NOT_CREATED","REVIEW_LATER","NO","YES"
"P8B-REVX-QAIC-CONTRACT-20260616-152747","MANUAL_ACTION_TICKETS","CONTRACT_ONLY_NOT_CREATED","REVIEW_LATER","NO","YES"
"P8B-REVX-QAIC-CONTRACT-20260616-152747","QAIC_SIGNAL_INBOX","CONTRACT_ONLY_NOT_CREATED","REVIEW_LATER","NO","YES"
"P8B-REVX-QAIC-CONTRACT-20260616-152747","ORDER_DRAFTS_FUTURE","CONTRACT_ONLY_NOT_CREATED","REVIEW_LATER","NO","YES"
"P8B-REVX-QAIC-CONTRACT-20260616-152747","ORDER_CHANGE_REQUESTS_FUTURE","CONTRACT_ONLY_NOT_CREATED","REVIEW_LATER","NO","YES"
"P8B-REVX-QAIC-CONTRACT-20260616-152747","TP_SL_PLAN_FUTURE","CONTRACT_ONLY_NOT_CREATED","REVIEW_LATER","NO","YES"
"P8B-REVX-QAIC-CONTRACT-20260616-152747","BROKER_AUDIT_LOG","CONTRACT_ONLY_NOT_CREATED","REVIEW_LATER","NO","YES"
"P8B-REVX-QAIC-CONTRACT-20260616-152747","KILL_SWITCH","CONTRACT_ONLY_NOT_CREATED","REVIEW_LATER","NO","YES"
```

### ITEM-001672 — `01_DOCS\VALIDATION\P8B_REVOLUT_X_QAIC_CONTRACT_PACK_NO_APPLY_20260616-152747\P8B_QAIC_BRIDGE_CONTRACT_20260616-152747.csv`

- **Légitimité :** `REVIEW_REQUIRED`
- **Actualité :** `CURRENT_OR_RECENT`
- **Classe :** `DOC_SOURCE_TO_COMPARE`
- **Dernière modification :** `2026-06-16T15:27:50`

```text
"run_id","bridge_object","direction","mode","required_fields"
"P8B-REVX-QAIC-CONTRACT-20260616-152747","QAIC_SIGNAL_INBOX","QAIC_PY_TO_MVP","READONLY_IMPORT","qaic_run_id;signal_id;asset_symbol;alpha_score;risk_score;decision_score;confidence_score;decision_candidate;blocked_reason;as_of_date;mvp_review_status;journal_id"
"P8B-REVX-QAIC-CONTRACT-20260616-152747","DECISION_JOURNAL_ENRICHMENT","MVP_INTERNAL","HUMAN_REVIEW_ONLY","journal_id;human_final_decision;portfolio_context_id;revolut_snapshot_id;manual_ticket_id;reconciliation_id"
"P8B-REVX-QAIC-CONTRACT-20260616-152747","POST_DECISION_RECONCILIATION","REVX_TO_MVP","OBSERVED_ONLY","journal_id;observed_transaction_id;observed_action;observed_quantity;observed_price;match_status;mismatch_reason"
"P8B-REVX-QAIC-CONTRACT-20260616-152747","PROMPT_QUALITY_FEEDBACK","MVP_TO_PROMPT_BACKLOG","QUALITY_CONTROL","journal_id;missing_data;blockers;prompt_quality_feedback;risk_context_status"
```

### ITEM-001669 — `01_DOCS\VALIDATION\P8B_REVOLUT_X_QAIC_CONTRACT_PACK_NO_APPLY_20260616-152747\P8B_REVOLUT_X_DATA_CONTRACTS_20260616-152747.csv`

- **Légitimité :** `REVIEW_REQUIRED`
- **Actualité :** `CURRENT_OR_RECENT`
- **Classe :** `DOC_SOURCE_TO_COMPARE`
- **Dernière modification :** `2026-06-16T15:27:50`

```text
"run_id","contract","purpose","mode","write_target","execution","required_fields"
"P8B-REVX-QAIC-CONTRACT-20260616-152747","REVOLUT_X_PORTFOLIO_RAW","Manual CSV raw portfolio import","CSV_IMPORT_FIRST","RAW_ONLY_LATER","NO","run_id;imported_at;source_file;asset_symbol;quantity;market_value;currency;raw_payload;validation_status"
"P8B-REVX-QAIC-CONTRACT-20260616-152747","REVOLUT_X_PORTFOLIO_NORMALIZED","Clean portfolio snapshot","READONLY_DATA","NORMALIZED_LATER","NO","snapshot_id;run_id;as_of_date;asset_symbol;quantity;avg_cost;last_price;market_value_eur;portfolio_weight_pct;quality_score"
"P8B-REVX-QAIC-CONTRACT-20260616-152747","REVOLUT_X_TRANSACTIONS_RAW","Manual CSV raw transaction import","CSV_IMPORT_FIRST","RAW_ONLY_LATER","NO","run_id;imported_at;source_file;raw_transaction_id;timestamp;type;asset_symbol;quantity;price;fee;currency;raw_payload"
"P8B-REVX-QAIC-CONTRACT-20260616-152747","REVOLUT_X_TRANSACTIONS_NORMALIZED","Clean observed transactions","READONLY_DATA","NORMALIZED_LATER","NO","transaction_id;run_id;executed_at;asset_symbol;side;quantity;price;fee_amount;net_amount;currency;quality_score"
"P8B-REVX-QAIC-CONTRACT-20260616-152747","PORTFOLIO_RISK_CONTEXT","Risk context for GPT, journal and cockpit","HUMAN_REVIEW_ONLY","RISK_CONTEXT_LATER","NO","context_id;run_id;as_of_date;asset_symbol;position_value_eur;portfolio_weight_pct;concentration_risk;data_quality_status;human_review_required"
"P8B-REVX-QAIC-CONTRACT-20260616-152747","REVOLUT_X_RECONCILIATION","Observed action vs journal decision","OBSERVED_ACTION_RECONCILE","RECONCILIATION_LATER","NO","reconciliation_id;journal_id;asset_symbol;human_final_decision;observed_transaction_id;observed_action;match_status;review_required"
```

### ITEM-001676 — `01_DOCS\VALIDATION\P8B_REVOLUT_X_QAIC_CONTRACT_PACK_NO_APPLY_20260616-152747\P8B_REVOLUT_X_QAIC_CONTRACT_PACK_REPORT_20260616-152747.md`

- **Légitimité :** `REVIEW_REQUIRED`
- **Actualité :** `CURRENT_OR_RECENT`
- **Classe :** `DOC_SOURCE_TO_COMPARE`
- **Dernière modification :** `2026-06-16T15:27:51`

```text
# MVP QAIC — P8B Revolut X / QAIC Contract Pack

Run ID: P8B-REVX-QAIC-CONTRACT-20260616-152747
Gate: P8B_CONTRACT_PACK_READY_FOR_P8C_SKELETON_PLAN_NO_APPLY

## Contracts
- Data contracts: 6
- Execution/manual contracts: 6
- Secrets governance rows: 6
- QAIC bridge contracts: 4
- Sheet plan rows: 13
- Script contract rows: 6

## Decision
Revolut X is integrated as data/reconciliation/manual-ticket layer.
Real broker execution remains blocked now.
Future order draft / TP-SL / modify / cancel paths are modeled as gated future capabilities only.

## Safety
NO_SHEET_WRITE / NO_APPS_SCRIPT / NO_APPSHEET_API / NO_BROKER / NO_ORDER / NO_SIZING / NO_SECRET_IN_SHEET / NO_SECRET_IN_APPS_SCRIPT.

## Next
P8C_REVOLUT_X_SKELETON_PLAN_NO_APPLY
```

### ITEM-001674 — `01_DOCS\VALIDATION\P8B_REVOLUT_X_QAIC_CONTRACT_PACK_NO_APPLY_20260616-152747\P8B_SCRIPT_CONTRACTS_COMPAT_QAIC_20260616-152747.csv`

- **Légitimité :** `REVIEW_REQUIRED`
- **Actualité :** `CURRENT_OR_RECENT`
- **Classe :** `DOC_SOURCE_TO_COMPARE`
- **Dernière modification :** `2026-06-16T15:27:50`

```text
"run_id","script_name","role","public_functions","status"
"P8B-REVX-QAIC-CONTRACT-20260616-152747","mvpqaic_30_revolutx_import_core.gs","CSV_IMPORT_RAW","REVX_Status;REVX_Import","DESIGN_ONLY"
"P8B-REVX-QAIC-CONTRACT-20260616-152747","mvpqaic_31_revolutx_normalize_core.gs","NORMALIZATION","REVX_Normalize","DESIGN_ONLY"
"P8B-REVX-QAIC-CONTRACT-20260616-152747","mvpqaic_32_portfolio_risk_context_core.gs","RISK_CONTEXT","Portfolio_Context","DESIGN_ONLY"
"P8B-REVX-QAIC-CONTRACT-20260616-152747","mvpqaic_33_revolutx_reconciliation_core.gs","RECONCILIATION","REVX_Reconcile","DESIGN_ONLY"
"P8B-REVX-QAIC-CONTRACT-20260616-152747","mvpqaic_34_manual_action_tickets_core.gs","MANUAL_TICKETS","Manual_Tickets","DESIGN_ONLY"
"P8B-REVX-QAIC-CONTRACT-20260616-152747","mvpqaic_35_qaic_signal_inbox_core.gs","QAIC_BRIDGE_READONLY","QAIC_Inbox_Status;QAIC_Inbox_Import","DESIGN_ONLY"
```

### ITEM-001671 — `01_DOCS\VALIDATION\P8B_REVOLUT_X_QAIC_CONTRACT_PACK_NO_APPLY_20260616-152747\P8B_SECRETS_GOVERNANCE_CONTRACT_20260616-152747.csv`

- **Légitimité :** `REVIEW_REQUIRED`
- **Actualité :** `CURRENT_OR_RECENT`
- **Classe :** `DOC_SOURCE_TO_COMPARE`
- **Dernière modification :** `2026-06-16T15:27:50`

```text
"run_id","secret_area","allowed","storage","notes"
"P8B-REVX-QAIC-CONTRACT-20260616-152747","GOOGLE_SHEETS","NO","FORBIDDEN","No API key/token/secret in Sheets"
"P8B-REVX-QAIC-CONTRACT-20260616-152747","APPS_SCRIPT","NO","FORBIDDEN","No API key/token/secret in Apps Script"
"P8B-REVX-QAIC-CONTRACT-20260616-152747","DRIVE_DOCS","NO","FORBIDDEN","No secret in Drive docs or exports"
"P8B-REVX-QAIC-CONTRACT-20260616-152747","CHATGPT","NO","FORBIDDEN","Never paste secrets into chat"
"P8B-REVX-QAIC-CONTRACT-20260616-152747","LOCAL_SECRET_FOLDER","YES_METADATA_ONLY","C:\Users\Julie\Documents\JRb-Secrets\QAIC\MVP QAIC","Local only, values never copied"
"P8B-REVX-QAIC-CONTRACT-20260616-152747","FUTURE_SECRET_MANAGER","FUTURE_REVIEW","GOOGLE_SECRET_MANAGER_OR_EQUIVALENT","Only if API integration later"
```

### ITEM-001675 — `01_DOCS\VALIDATION\P8B_REVOLUT_X_QAIC_CONTRACT_PACK_NO_APPLY_20260616-152747\P8B_SUMMARY_20260616-152747.csv`

- **Légitimité :** `REVIEW_REQUIRED`
- **Actualité :** `CURRENT_OR_RECENT`
- **Classe :** `DOC_SOURCE_TO_COMPARE`
- **Dernière modification :** `2026-06-16T15:27:51`

```text
"run_id","status","p8b_gate","missing_p8a_outputs","data_contracts","execution_contracts","secrets_contracts","qaic_bridge_contracts","sheet_plan_rows","script_contract_rows","blocked_execution_objects","forbidden_secret_locations","cleanup_authorized","apply_authorized","broker_execution_authorized","order_execution_authorized","sizing_authorized","next_action"
"P8B-REVX-QAIC-CONTRACT-20260616-152747","OK","P8B_CONTRACT_PACK_READY_FOR_P8C_SKELETON_PLAN_NO_APPLY","0","6","6","6","4","13","6","6","4","NO","NO","NO","NO","NO","P8C_REVOLUT_X_SKELETON_PLAN_NO_APPLY"
```

### ITEM-001680 — `01_DOCS\VALIDATION\P8C_REVOLUT_X_SKELETON_PLAN_NO_APPLY_20260616-153551\P8B_MANUAL_EXECUTION_CONTRACT_20260616-152747.csv`

- **Légitimité :** `REVIEW_REQUIRED`
- **Actualité :** `CURRENT_OR_RECENT`
- **Classe :** `DOC_SOURCE_TO_COMPARE`
- **Dernière modification :** `2026-06-16T15:27:50`

```text
"run_id","object","status","execution_allowed","mode","api_call","notes"
"P8B-REVX-QAIC-CONTRACT-20260616-152747","MANUAL_ACTION_TICKETS","ALLOWED_NOW_AS_NON_EXECUTABLE","FALSE","MANUAL_ONLY","NO","Prepare checklist/ticket only"
"P8B-REVX-QAIC-CONTRACT-20260616-152747","ORDER_DRAFTS_FUTURE","FUTURE_GATED","FALSE","DRAFT_ONLY","NO","Can model proposed order but cannot execute"
"P8B-REVX-QAIC-CONTRACT-20260616-152747","TP_SL_PLAN_FUTURE","FUTURE_GATED","FALSE","PLAN_ONLY","NO","TP/SL plan only, no broker modification"
"P8B-REVX-QAIC-CONTRACT-20260616-152747","ORDER_CHANGE_REQUESTS_FUTURE","FUTURE_GATED","FALSE","REQUEST_ONLY","NO","Modify/cancel request only until official API and explicit GO"
"P8B-REVX-QAIC-CONTRACT-20260616-152747","BROKER_AUDIT_LOG","ALLOWED_AS_AUDIT","FALSE","AUDIT_ONLY","NO","Trace human decisions and observed outcomes"
"P8B-REVX-QAIC-CONTRACT-20260616-152747","KILL_SWITCH","REQUIRED_BEFORE_ANY_FUTURE_EXECUTION","FALSE","SAFETY_GATE","NO","Must block execution path by default"
```

### ITEM-001681 — `01_DOCS\VALIDATION\P8C_REVOLUT_X_SKELETON_PLAN_NO_APPLY_20260616-153551\P8B_QAIC_BRIDGE_CONTRACT_20260616-152747.csv`

- **Légitimité :** `REVIEW_REQUIRED`
- **Actualité :** `CURRENT_OR_RECENT`
- **Classe :** `DOC_SOURCE_TO_COMPARE`
- **Dernière modification :** `2026-06-16T15:27:50`

```text
"run_id","bridge_object","direction","mode","required_fields"
"P8B-REVX-QAIC-CONTRACT-20260616-152747","QAIC_SIGNAL_INBOX","QAIC_PY_TO_MVP","READONLY_IMPORT","qaic_run_id;signal_id;asset_symbol;alpha_score;risk_score;decision_score;confidence_score;decision_candidate;blocked_reason;as_of_date;mvp_review_status;journal_id"
"P8B-REVX-QAIC-CONTRACT-20260616-152747","DECISION_JOURNAL_ENRICHMENT","MVP_INTERNAL","HUMAN_REVIEW_ONLY","journal_id;human_final_decision;portfolio_context_id;revolut_snapshot_id;manual_ticket_id;reconciliation_id"
"P8B-REVX-QAIC-CONTRACT-20260616-152747","POST_DECISION_RECONCILIATION","REVX_TO_MVP","OBSERVED_ONLY","journal_id;observed_transaction_id;observed_action;observed_quantity;observed_price;match_status;mismatch_reason"
"P8B-REVX-QAIC-CONTRACT-20260616-152747","PROMPT_QUALITY_FEEDBACK","MVP_TO_PROMPT_BACKLOG","QUALITY_CONTROL","journal_id;missing_data;blockers;prompt_quality_feedback;risk_context_status"
```

### ITEM-001679 — `01_DOCS\VALIDATION\P8C_REVOLUT_X_SKELETON_PLAN_NO_APPLY_20260616-153551\P8B_REVOLUT_X_DATA_CONTRACTS_20260616-152747.csv`

- **Légitimité :** `REVIEW_REQUIRED`
- **Actualité :** `CURRENT_OR_RECENT`
- **Classe :** `DOC_SOURCE_TO_COMPARE`
- **Dernière modification :** `2026-06-16T15:27:50`

```text
"run_id","contract","purpose","mode","write_target","execution","required_fields"
"P8B-REVX-QAIC-CONTRACT-20260616-152747","REVOLUT_X_PORTFOLIO_RAW","Manual CSV raw portfolio import","CSV_IMPORT_FIRST","RAW_ONLY_LATER","NO","run_id;imported_at;source_file;asset_symbol;quantity;market_value;currency;raw_payload;validation_status"
"P8B-REVX-QAIC-CONTRACT-20260616-152747","REVOLUT_X_PORTFOLIO_NORMALIZED","Clean portfolio snapshot","READONLY_DATA","NORMALIZED_LATER","NO","snapshot_id;run_id;as_of_date;asset_symbol;quantity;avg_cost;last_price;market_value_eur;portfolio_weight_pct;quality_score"
"P8B-REVX-QAIC-CONTRACT-20260616-152747","REVOLUT_X_TRANSACTIONS_RAW","Manual CSV raw transaction import","CSV_IMPORT_FIRST","RAW_ONLY_LATER","NO","run_id;imported_at;source_file;raw_transaction_id;timestamp;type;asset_symbol;quantity;price;fee;currency;raw_payload"
"P8B-REVX-QAIC-CONTRACT-20260616-152747","REVOLUT_X_TRANSACTIONS_NORMALIZED","Clean observed transactions","READONLY_DATA","NORMALIZED_LATER","NO","transaction_id;run_id;executed_at;asset_symbol;side;quantity;price;fee_amount;net_amount;currency;quality_score"
"P8B-REVX-QAIC-CONTRACT-20260616-152747","PORTFOLIO_RISK_CONTEXT","Risk context for GPT, journal and cockpit","HUMAN_REVIEW_ONLY","RISK_CONTEXT_LATER","NO","context_id;run_id;as_of_date;asset_symbol;position_value_eur;portfolio_weight_pct;concentration_risk;data_quality_status;human_review_required"
"P8B-REVX-QAIC-CONTRACT-20260616-152747","REVOLUT_X_RECONCILIATION","Observed action vs journal decision","OBSERVED_ACTION_RECONCILE","RECONCILIATION_LATER","NO","reconciliation_id;journal_id;asset_symbol;human_final_decision;observed_transaction_id;observed_action;match_status;review_required"
```

### ITEM-001732 — `01_DOCS\VALIDATION\P8E_REVOLUT_X_QAIC_DOCS_PACK_NO_APPLY_20260616-160712\MVPQAIC_QAIC_BRIDGE_CONTRACT_20260616-160712.md`

- **Légitimité :** `REVIEW_REQUIRED`
- **Actualité :** `CURRENT_OR_RECENT`
- **Classe :** `DOC_SOURCE_TO_COMPARE`
- **Dernière modification :** `2026-06-16T16:07:15`

```text
# MVP QAIC - QAIC Bridge Contract

Run ID: P8E-DOCS-PACK-20260616-160712
QAIC bridge contract rows detected from P8B: 4

## Future bridge
QAIC Python will provide signals, scores, risks and blocked reasons.
MVP QAIC will receive them in QAIC_SIGNAL_INBOX, review them, journal decisions and reconcile observed Revolut X outcomes.

## Core objects
- QAIC_SIGNAL_INBOX
- DECISION_JOURNAL_ENRICHMENT
- POST_DECISION_RECONCILIATION
- PROMPT_QUALITY_FEEDBACK

## Rule
QAIC may propose. MVP QAIC may explain, journal, control and reconcile. Revolut X remains observed/manual unless a future explicit execution gate is validated.
```

### ITEM-001730 — `01_DOCS\VALIDATION\P8E_REVOLUT_X_QAIC_DOCS_PACK_NO_APPLY_20260616-160712\MVPQAIC_REVOLUT_X_DATA_CONTRACTS_20260616-160712.md`

- **Légitimité :** `REVIEW_REQUIRED`
- **Actualité :** `CURRENT_OR_RECENT`
- **Classe :** `DOC_SOURCE_TO_COMPARE`
- **Dernière modification :** `2026-06-16T16:07:15`

```text
# MVP QAIC - Revolut X Data Contracts

Run ID: P8E-DOCS-PACK-20260616-160712
Data contract rows detected from P8B: 6

## Contracts
1. REVOLUT_X_PORTFOLIO_RAW
2. REVOLUT_X_PORTFOLIO_NORMALIZED
3. REVOLUT_X_TRANSACTIONS_RAW
4. REVOLUT_X_TRANSACTIONS_NORMALIZED
5. PORTFOLIO_RISK_CONTEXT
6. REVOLUT_X_RECONCILIATION

## Skeleton summary from P8C
- Sheet skeleton rows: 13
- Header rows: 170
- Private view rows: 5
- Script plan rows: 6

## Rule
Contracts are documentation-ready only. No sheet creation or live write is authorized in P8E.
```

### ITEM-001723 — `01_DOCS\VALIDATION\P8E_REVOLUT_X_QAIC_DOCS_PACK_NO_APPLY_20260616-160712\P8B_MANUAL_EXECUTION_CONTRACT_20260616-152747.csv`

- **Légitimité :** `REVIEW_REQUIRED`
- **Actualité :** `CURRENT_OR_RECENT`
- **Classe :** `DOC_SOURCE_TO_COMPARE`
- **Dernière modification :** `2026-06-16T15:27:50`

```text
"run_id","object","status","execution_allowed","mode","api_call","notes"
"P8B-REVX-QAIC-CONTRACT-20260616-152747","MANUAL_ACTION_TICKETS","ALLOWED_NOW_AS_NON_EXECUTABLE","FALSE","MANUAL_ONLY","NO","Prepare checklist/ticket only"
"P8B-REVX-QAIC-CONTRACT-20260616-152747","ORDER_DRAFTS_FUTURE","FUTURE_GATED","FALSE","DRAFT_ONLY","NO","Can model proposed order but cannot execute"
"P8B-REVX-QAIC-CONTRACT-20260616-152747","TP_SL_PLAN_FUTURE","FUTURE_GATED","FALSE","PLAN_ONLY","NO","TP/SL plan only, no broker modification"
"P8B-REVX-QAIC-CONTRACT-20260616-152747","ORDER_CHANGE_REQUESTS_FUTURE","FUTURE_GATED","FALSE","REQUEST_ONLY","NO","Modify/cancel request only until official API and explicit GO"
"P8B-REVX-QAIC-CONTRACT-20260616-152747","BROKER_AUDIT_LOG","ALLOWED_AS_AUDIT","FALSE","AUDIT_ONLY","NO","Trace human decisions and observed outcomes"
"P8B-REVX-QAIC-CONTRACT-20260616-152747","KILL_SWITCH","REQUIRED_BEFORE_ANY_FUTURE_EXECUTION","FALSE","SAFETY_GATE","NO","Must block execution path by default"
```

### ITEM-001725 — `01_DOCS\VALIDATION\P8E_REVOLUT_X_QAIC_DOCS_PACK_NO_APPLY_20260616-160712\P8B_QAIC_BRIDGE_CONTRACT_20260616-152747.csv`

- **Légitimité :** `REVIEW_REQUIRED`
- **Actualité :** `CURRENT_OR_RECENT`
- **Classe :** `DOC_SOURCE_TO_COMPARE`
- **Dernière modification :** `2026-06-16T15:27:50`

```text
"run_id","bridge_object","direction","mode","required_fields"
"P8B-REVX-QAIC-CONTRACT-20260616-152747","QAIC_SIGNAL_INBOX","QAIC_PY_TO_MVP","READONLY_IMPORT","qaic_run_id;signal_id;asset_symbol;alpha_score;risk_score;decision_score;confidence_score;decision_candidate;blocked_reason;as_of_date;mvp_review_status;journal_id"
"P8B-REVX-QAIC-CONTRACT-20260616-152747","DECISION_JOURNAL_ENRICHMENT","MVP_INTERNAL","HUMAN_REVIEW_ONLY","journal_id;human_final_decision;portfolio_context_id;revolut_snapshot_id;manual_ticket_id;reconciliation_id"
"P8B-REVX-QAIC-CONTRACT-20260616-152747","POST_DECISION_RECONCILIATION","REVX_TO_MVP","OBSERVED_ONLY","journal_id;observed_transaction_id;observed_action;observed_quantity;observed_price;match_status;mismatch_reason"
"P8B-REVX-QAIC-CONTRACT-20260616-152747","PROMPT_QUALITY_FEEDBACK","MVP_TO_PROMPT_BACKLOG","QUALITY_CONTROL","journal_id;missing_data;blockers;prompt_quality_feedback;risk_context_status"
```

### ITEM-001722 — `01_DOCS\VALIDATION\P8E_REVOLUT_X_QAIC_DOCS_PACK_NO_APPLY_20260616-160712\P8B_REVOLUT_X_DATA_CONTRACTS_20260616-152747.csv`

- **Légitimité :** `REVIEW_REQUIRED`
- **Actualité :** `CURRENT_OR_RECENT`
- **Classe :** `DOC_SOURCE_TO_COMPARE`
- **Dernière modification :** `2026-06-16T15:27:50`

```text
"run_id","contract","purpose","mode","write_target","execution","required_fields"
"P8B-REVX-QAIC-CONTRACT-20260616-152747","REVOLUT_X_PORTFOLIO_RAW","Manual CSV raw portfolio import","CSV_IMPORT_FIRST","RAW_ONLY_LATER","NO","run_id;imported_at;source_file;asset_symbol;quantity;market_value;currency;raw_payload;validation_status"
"P8B-REVX-QAIC-CONTRACT-20260616-152747","REVOLUT_X_PORTFOLIO_NORMALIZED","Clean portfolio snapshot","READONLY_DATA","NORMALIZED_LATER","NO","snapshot_id;run_id;as_of_date;asset_symbol;quantity;avg_cost;last_price;market_value_eur;portfolio_weight_pct;quality_score"
"P8B-REVX-QAIC-CONTRACT-20260616-152747","REVOLUT_X_TRANSACTIONS_RAW","Manual CSV raw transaction import","CSV_IMPORT_FIRST","RAW_ONLY_LATER","NO","run_id;imported_at;source_file;raw_transaction_id;timestamp;type;asset_symbol;quantity;price;fee;currency;raw_payload"
"P8B-REVX-QAIC-CONTRACT-20260616-152747","REVOLUT_X_TRANSACTIONS_NORMALIZED","Clean observed transactions","READONLY_DATA","NORMALIZED_LATER","NO","transaction_id;run_id;executed_at;asset_symbol;side;quantity;price;fee_amount;net_amount;currency;quality_score"
"P8B-REVX-QAIC-CONTRACT-20260616-152747","PORTFOLIO_RISK_CONTEXT","Risk context for GPT, journal and cockpit","HUMAN_REVIEW_ONLY","RISK_CONTEXT_LATER","NO","context_id;run_id;as_of_date;asset_symbol;position_value_eur;portfolio_weight_pct;concentration_risk;data_quality_status;human_review_required"
"P8B-REVX-QAIC-CONTRACT-20260616-152747","REVOLUT_X_RECONCILIATION","Observed action vs journal decision","OBSERVED_ACTION_RECONCILE","RECONCILIATION_LATER","NO","reconciliation_id;journal_id;asset_symbol;human_final_decision;observed_transaction_id;observed_action;match_status;review_required"
```

### ITEM-001724 — `01_DOCS\VALIDATION\P8E_REVOLUT_X_QAIC_DOCS_PACK_NO_APPLY_20260616-160712\P8B_SECRETS_GOVERNANCE_CONTRACT_20260616-152747.csv`

- **Légitimité :** `REVIEW_REQUIRED`
- **Actualité :** `CURRENT_OR_RECENT`
- **Classe :** `DOC_SOURCE_TO_COMPARE`
- **Dernière modification :** `2026-06-16T15:27:50`

```text
"run_id","secret_area","allowed","storage","notes"
"P8B-REVX-QAIC-CONTRACT-20260616-152747","GOOGLE_SHEETS","NO","FORBIDDEN","No API key/token/secret in Sheets"
"P8B-REVX-QAIC-CONTRACT-20260616-152747","APPS_SCRIPT","NO","FORBIDDEN","No API key/token/secret in Apps Script"
"P8B-REVX-QAIC-CONTRACT-20260616-152747","DRIVE_DOCS","NO","FORBIDDEN","No secret in Drive docs or exports"
"P8B-REVX-QAIC-CONTRACT-20260616-152747","CHATGPT","NO","FORBIDDEN","Never paste secrets into chat"
"P8B-REVX-QAIC-CONTRACT-20260616-152747","LOCAL_SECRET_FOLDER","YES_METADATA_ONLY","C:\Users\Julie\Documents\JRb-Secrets\QAIC\MVP QAIC","Local only, values never copied"
"P8B-REVX-QAIC-CONTRACT-20260616-152747","FUTURE_SECRET_MANAGER","FUTURE_REVIEW","GOOGLE_SECRET_MANAGER_OR_EQUIVALENT","Only if API integration later"
```

### ITEM-001738 — `01_DOCS\VALIDATION\P9A_COLUMN_REVIEW_PREP_NO_APPLY_20260616-161203\P7C_FIELD_CONTRACT_20260616-131902.csv`

- **Légitimité :** `REVIEW_REQUIRED`
- **Actualité :** `CURRENT_OR_RECENT`
- **Classe :** `DOC_SOURCE_TO_COMPARE`
- **Dernière modification :** `2026-06-16T13:19:04`

```text
"run_id","table_code","sheet_title","field_name","field_status","editable","apply_allowed"
"P7C-SCHEMA-20260616-131902","SEARCH_COCKPIT","SEARCH_DEMO","record_id","REQUIRED_OR_RECOMMENDED_REVIEW","NO","NO"
"P7C-SCHEMA-20260616-131902","SEARCH_COCKPIT","SEARCH_DEMO","label","REQUIRED_OR_RECOMMENDED_REVIEW","NO","NO"
"P7C-SCHEMA-20260616-131902","SEARCH_COCKPIT","SEARCH_DEMO","status","REQUIRED_OR_RECOMMENDED_REVIEW","NO","NO"
"P7C-SCHEMA-20260616-131902","SEARCH_COCKPIT","SEARCH_DEMO","category","REQUIRED_OR_RECOMMENDED_REVIEW","NO","NO"
"P7C-SCHEMA-20260616-131902","SEARCH_COCKPIT","SEARCH_DEMO","source","REQUIRED_OR_RECOMMENDED_REVIEW","NO","NO"
"P7C-SCHEMA-20260616-131902","SEARCH_COCKPIT","SEARCH_DEMO","last_reviewed_at","REQUIRED_OR_RECOMMENDED_REVIEW","NO","NO"
"P7C-SCHEMA-20260616-131902","LEXIQUE_MASTER","GLOSSARY_TAGS","record_id","REQUIRED_OR_RECOMMENDED_REVIEW","NO","NO"
"P7C-SCHEMA-20260616-131902","LEXIQUE_MASTER","GLOSSARY_TAGS","label","REQUIRED_OR_RECOMMENDED_REVIEW","NO","NO"
"P7C-SCHEMA-20260616-131902","LEXIQUE_MASTER","GLOSSARY_TAGS","status","REQUIRED_OR_RECOMMENDED_REVIEW","NO","NO"
"P7C-SCHEMA-20260616-131902","LEXIQUE_MASTER","GLOSSARY_TAGS","category","REQUIRED_OR_RECOMMENDED_REVIEW","NO","NO"
"P7C-SCHEMA-20260616-131902","LEXIQUE_MASTER","GLOSSARY_TAGS","source","REQUIRED_OR_RECOMMENDED_REVIEW","NO","NO"
"P7C-SCHEMA-20260616-131902","LEXIQUE_MASTER","GLOSSARY_TAGS","last_reviewed_at","REQUIRED_OR_RECOMMENDED_REVIEW","NO","NO"
"P7C-SCHEMA-20260616-131902","PROMPT_CONTEXT_PACKS","🧠 PROMPT_CONTEXT_PACKS","record_id","REQUIRED_OR_RECOMMENDED_REVIEW","NO","NO"
"P7C-SCHEMA-20260616-131902","PROMPT_CONTEXT_PACKS","🧠 PROMPT_CONTEXT_PACKS","label","REQUIRED_OR_RECOMMENDED_REVIEW","NO","NO"
"P7C-SCHEMA-20260616-131902","PROMPT_CONTEXT_PACKS","🧠 PROMPT_CONTEXT_PACKS","status","REQUIRED_OR_RECOMMENDED_REVIEW","NO","NO"
"P7C-SCHEMA-20260616-131902","PROMPT_CONTEXT_PACKS","🧠 PROMPT_CONTEXT_PACKS","category","REQUIRED_OR_RECOMMENDED_REVIEW","NO","NO"
"P7C-SCHEMA-20260616-131902","PROMPT_CONTEXT_PACKS","🧠 PROMPT_CONTEXT_PACKS","source","REQUIRED_OR_RECOMMENDED_REVIEW","NO","NO"
"P7C-SCHEMA-20260616-131902","PROMPT_CONTEXT_PACKS","🧠 PROMPT_CONTEXT_
```

### ITEM-001737 — `01_DOCS\VALIDATION\P9A_COLUMN_REVIEW_PREP_NO_APPLY_20260616-161203\P7C_TABLE_CONTRACT_20260616-131902.csv`

- **Légitimité :** `REVIEW_REQUIRED`
- **Actualité :** `CURRENT_OR_RECENT`
- **Classe :** `DOC_SOURCE_TO_COMPARE`
- **Dernière modification :** `2026-06-16T13:19:04`

```text
"run_id","table_code","sheet_title","sheet_id","app_module","app_role","key_strategy","read_allowed","write_allowed","delete_allowed","apply_allowed","schema_status"
"P7C-SCHEMA-20260616-131902","SEARCH_COCKPIT","SEARCH_DEMO","913965412","M01_SEARCH_COCKPIT","CORE_TABLE","REVIEW_EXISTING_KEY_OR_CREATE_STABLE_ID_LATER","YES_BLUEPRINT_ONLY","NO","NO","NO","DRAFT_CONTRACT_NO_APPLY"
"P7C-SCHEMA-20260616-131902","LEXIQUE_MASTER","GLOSSARY_TAGS","361912386","M02_LEXIQUE_CORE","CORE_TABLE","REVIEW_EXISTING_KEY_OR_CREATE_STABLE_ID_LATER","YES_BLUEPRINT_ONLY","NO","NO","NO","DRAFT_CONTRACT_NO_APPLY"
"P7C-SCHEMA-20260616-131902","PROMPT_CONTEXT_PACKS","🧠 PROMPT_CONTEXT_PACKS","1225030026","M03_PROMPT_FACTORY","CORE_TABLE","REVIEW_EXISTING_KEY_OR_CREATE_STABLE_ID_LATER","YES_BLUEPRINT_ONLY","NO","NO","NO","DRAFT_CONTRACT_NO_APPLY"
"P7C-SCHEMA-20260616-131902","PROMPT_LEXIQUE_BRIDGE","🔗 PROMPT_LEXIQUE_BRIDGE","1177488306","M03_PROMPT_FACTORY","CORE_TABLE","REVIEW_EXISTING_KEY_OR_CREATE_STABLE_ID_LATER","YES_BLUEPRINT_ONLY","NO","NO","NO","DRAFT_CONTRACT_NO_APPLY"
"P7C-SCHEMA-20260616-131902","PROMPT_LIBRARY","METHOD_LIBRARY","2028965973","M03_PROMPT_FACTORY","CORE_TABLE","REVIEW_EXISTING_KEY_OR_CREATE_STABLE_ID_LATER","YES_BLUEPRINT_ONLY","NO","NO","NO","DRAFT_CONTRACT_NO_APPLY"
"P7C-SCHEMA-20260616-131902","PROMPT_READY_TO_COPY","🧩 PROMPT_READY_TO_COPY","1041347966","M03_PROMPT_FACTORY","CORE_TABLE","REVIEW_EXISTING_KEY_OR_CREATE_STABLE_ID_LATER","YES_BLUEPRINT_ONLY","NO","NO","NO","DRAFT_CONTRACT_NO_APPLY"
"P7C-SCHEMA-20260616-131902","PROMPT_RUN_QUEUE","📤 JOURNAL_APPEND_QUEUE","1366021627","M04_RUN_QUEUES","CORE_TABLE","REVIEW_EXISTING_KEY_OR_CREATE_STABLE_ID_LATER","YES_BLUEPRINT_ONLY","NO","NO","NO","DRAFT_CONTRACT_NO_APPLY"
"P7C-SCHEMA-20260616-131902","RESPONSE_INTAKE_QUEUE","📥 RESPONSE_INTAKE_QUEUE","1785131134","M04_RUN_QUEUES","CORE_TABLE","REVIEW_EXISTING_KEY_OR_CREATE_STABLE_ID_LATER","YES_BLUEPRINT_ONLY","NO","NO","NO","DRAFT_CONTRACT_NO_APPLY"
"P7C-SCHEMA-20260616-131902","DECISION_JOURNAL","DECISION_MATRIX","2113266008","M05_DECISION_JOURNAL","CORE_TABLE","REVIEW_EXISTING_KEY_OR_CREATE_STABLE_ID_LATER","YES_BLUEPRINT_ONLY","NO","NO","NO","DRAFT_CONTRACT_
```

### ITEM-001739 — `01_DOCS\VALIDATION\P9A_COLUMN_REVIEW_PREP_NO_APPLY_20260616-161203\P7C_VIEW_CONTRACT_20260616-131902.csv`

- **Légitimité :** `REVIEW_REQUIRED`
- **Actualité :** `CURRENT_OR_RECENT`
- **Classe :** `DOC_SOURCE_TO_COMPARE`
- **Dernière modification :** `2026-06-16T13:19:04`

```text
"run_id","view_id","label","module_id","view_type","write_allowed","apply_allowed"
"P7C-SCHEMA-20260616-131902","HOME_SEARCH","Accueil / Recherche","M01_SEARCH_COCKPIT","READ_ONLY_BLUEPRINT","NO","NO"
"P7C-SCHEMA-20260616-131902","LEXIQUE_DETAIL","Lexique detail","M02_LEXIQUE_CORE","READ_ONLY_BLUEPRINT","NO","NO"
"P7C-SCHEMA-20260616-131902","PROMPT_READY","Prompts prets a copier","M03_PROMPT_FACTORY","READ_ONLY_BLUEPRINT","NO","NO"
"P7C-SCHEMA-20260616-131902","RUN_QUEUE","Run queue","M04_RUN_QUEUES","READ_ONLY_BLUEPRINT","NO","NO"
"P7C-SCHEMA-20260616-131902","DECISION_JOURNAL","Decision journal","M05_DECISION_JOURNAL","READ_ONLY_BLUEPRINT","NO","NO"
```

### ITEM-001397 — `01_DOCS\VALIDATION\VALIDATION_MATRIX_MVP_QAIC_P1G_PROMPT_LIBRARY_CONTRACT_0.6.0.md`

- **Légitimité :** `REVIEW_REQUIRED`
- **Actualité :** `CURRENT_OR_RECENT`
- **Classe :** `DOC_SOURCE_TO_COMPARE`
- **Dernière modification :** `2026-06-11T23:49:16`

```text
# ✅ MVP QAIC — P1-G Validation Matrix

**Version :** `MVP_QAIC_P1_PROMPT_QUALITY_CORE_0.6.0_SAFE_FULL_FUSION_P1E_P1F_P1G`

| Test | Fonction | Attendu | Bloquant si échec |
|---|---|---|---|
| Core status | `MVPQAIC_PromptQualityCoreStatus()` | `status=OK` | Oui |
| Queue disponible | `MVPQAIC_PromptLibraryStatus()` | `can_refresh=true` | Oui |
| Library refresh | `MVPQAIC_PromptLibraryRefresh()` | `status=REFRESHED` | Oui |
| Onglet cible | `PROMPT_LIBRARY` | créé/rafraîchi | Oui |
| CORE_CONTRACT | ligne typée | >= 2 lignes | Oui |
| GEM_PROFILE | lignes runtime | >= 4 lignes | Oui |
| PROMPT_CONTRACT | depuis queue | >= 1 ligne | Oui |
| UI | freeze/filtres/couleurs/listes | OK | Non bloquant mais à corriger |
| Sécurité | logs safety | `NO_BROKER_NO_ORDER_NO_SIZING_NO_SECRET` | Oui |

## Critères d’acceptation

- `PROMPT_LIBRARY` contient des profils Gem séparés du contrat cœur.
- Les métriques/scorings possibles sont déclarés par `gem_profile`.
- Les métriques non supportées sont explicitement interdites ou `NOT_AVAILABLE`.
- Les prompts doivent retourner `REVIEW_REQUIRED` ou `BLOCKED` si les données manquent.
- Aucun nouvel onglet redondant.
- Aucun script temporaire durable ajouté.
```

### ITEM-002883 — `02_BUILD\LEXIQUE_READER_MVP\03_BUILD_OUTPUTS\P24D_20260618_000512\P24D_DATA_CONTRACT_FIELDS.csv`

- **Légitimité :** `REVIEW_REQUIRED`
- **Actualité :** `CURRENT_OR_RECENT`
- **Classe :** `DOC_SOURCE_TO_COMPARE`
- **Dernière modification :** `2026-06-18T00:05:19`

```text
"dataset","field_name","field_role","row_count","non_empty_count","missing_count","safety_note"
"P22B_DATASET_MERGED","entry_id","content_or_metadata","156","156","0","Do not infer trading decision from this field alone"
"P22B_DATASET_MERGED","source_type","partition_key","156","156","0","Do not infer trading decision from this field alone"
"P22B_DATASET_MERGED","category","content_or_metadata","156","156","0","Do not infer trading decision from this field alone"
"P22B_DATASET_MERGED","subcategory","content_or_metadata","156","96","60","Do not infer trading decision from this field alone"
"P22B_DATASET_MERGED","term_fr","content_or_metadata","156","156","0","Do not infer trading decision from this field alone"
"P22B_DATASET_MERGED","term_en","content_or_metadata","156","156","0","Do not infer trading decision from this field alone"
"P22B_DATASET_MERGED","definition_fr","required_content","156","156","0","Do not infer trading decision from this field alone"
"P22B_DATASET_MERGED","usage_fr","recommended_content","156","156","0","Do not infer trading decision from this field alone"
"P22B_DATASET_MERGED","lecture_rapide_fr","content_or_metadata","156","156","0","Do not infer trading decision from this field alone"
"P22B_DATASET_MERGED","pieges_faux_signaux_fr","content_or_metadata","156","156","0","Do not infer trading decision from this field alone"
"P22B_DATASET_MERGED","family_fr","content_or_metadata","156","156","0","Do not infer trading decision from this field alone"
"P22B_DATASET_MERGED","display_tier","content_or_metadata","156","156","0","Do not infer trading decision from this field alone"
"P22B_DATASET_MERGED","recommended_timeframes","content_or_metadata","156","156","0","Do not infer trading decision from this field alone"
"P22B_DATASET_MERGED","default_settings_hint","content_or_metadata","156","156","0","Do not infer trading decision from this field alone"
"P22B_DATASET_MERGED","graph_example_type","content_or_metadata","156","156","0","Do not infer trading decision from this field alone"
"P22B_DATASET_MERGED","graph_example_needed","content_or_metadata","156","156","0","Do not infer trading decision from this field alone"
"P22B_DATASET_MERGED","qaic
```

### ITEM-002884 — `02_BUILD\LEXIQUE_READER_MVP\03_BUILD_OUTPUTS\P24D_20260618_000512\P24D_OUTPUT_CONTRACT.json`

- **Légitimité :** `REVIEW_REQUIRED`
- **Actualité :** `CURRENT_OR_RECENT`
- **Classe :** `DOC_SOURCE_TO_COMPARE`
- **Dernière modification :** `2026-06-18T00:05:19`

```text
{
    "schema":  "P24D_OUTPUT_CONTRACT_V1",
    "mode":  "HUMAN_REVIEW_ONLY",
    "allowed_outputs":  [
                            "EDUCATIONAL_REVIEW_ONLY",
                            "REVIEW_REQUIRED",
                            "BLOCKED"
                        ],
    "required_sections":  [
                              "asset_or_term",
                              "context",
                              "definition_or_indicator",
                              "graph_reading",
                              "missing_data",
                              "blockers",
                              "risk_guard",
                              "human_review_decision"
                          ],
    "forbidden_outputs":  [
                              "AUTO_ORDER",
                              "AUTO_SIZING",
                              "BROKER_EXECUTION",
                              "REAL_ORDER",
                              "HALLUCINATED_SCORE"
                          ],
    "safety":  {
                   "no_auto_order":  true,
                   "no_auto_sizing":  true,
                   "no_broker_execution":  true,
                   "no_real_order":  true,
                   "no_google_api_call":  true,
                   "no_sheet_write":  true,
                   "no_apps_script_execution":  true
               },
    "datasets":  [
                     {
                         "name":  "P22B_DATASET_MERGED",
                         "rows":  156,
                         "role":  "canonical_app_dataset"
                     },
                     {
                         "name":  "P24C_REVIEW_ENRICHMENT_DATASET",
                         "rows":  156,
                         "role":  "educational_review_sidecar"
                     }
                 ]
}
```

### ITEM-002885 — `02_BUILD\LEXIQUE_READER_MVP\03_BUILD_OUTPUTS\P24D_20260618_000512\README_P24D_DATA_AND_OUTPUT_CONTRACT.md`

- **Légitimité :** `REVIEW_REQUIRED`
- **Actualité :** `CURRENT_OR_RECENT`
- **Classe :** `DOC_SOURCE_TO_COMPARE`
- **Dernière modification :** `2026-06-18T00:05:19`

```text
# P24D — Data & Output Contract

## Canonical dataset
- File: P22B_DATASET_MERGED.csv
- Rows: 156
- Original lexique: 60
- Revolut X indicators: 96

## Sidecar dataset
- File: P24C_REVIEW_ENRICHMENT_DATASET.csv
- Rows: 156

## Output mode
Only:
- EDUCATIONAL_REVIEW_ONLY
- REVIEW_REQUIRED
- BLOCKED

## Required output sections
- asset_or_term
- context
- definition_or_indicator
- graph_reading
- missing_data
- blockers
- risk_guard
- human_review_decision

## Forbidden
- AUTO_ORDER
- AUTO_SIZING
- BROKER_EXECUTION
- REAL_ORDER
- HALLUCINATED_SCORE
```

## 5. 🧊 Sources conservées hors fusion

### ZIP à inspecter

- `ITEM-000056` — `05_EXPORTS\P59A4_PY_LIVE_SHEETS_API_DECISION_AND_CONTRACT_20260620\P59A4_PY_LIVE_SHEETS_API_DECISION_AND_CONTRACT.zip` — `REVIEW_REQUIRED_ZIP`
- `ITEM-000771` — `06_REPORTS\MVP_QAIC_P078C_P2_DATA_CONTRACTS_ROBUST_REBUILD_READONLY_20260620_190958.zip` — `REVIEW_REQUIRED_ZIP`
- `ITEM-000773` — `06_REPORTS\MVP_QAIC_P079_P2B_CONTRACT_FIELD_SELECTION_REVIEW_20260620_192723.zip` — `REVIEW_REQUIRED_ZIP`
- `ITEM-001486` — `01_DOCS\VALIDATION\P7C_APP_SCHEMA_CONTRACT_NO_APPLY_MAXI_20260616-131902.zip` — `REVIEW_REQUIRED_ZIP`
- `ITEM-001490` — `01_DOCS\VALIDATION\P8B_REVOLUT_X_QAIC_CONTRACT_PACK_NO_APPLY_20260616-152747.zip` — `REVIEW_REQUIRED_ZIP`
- `ITEM-002949` — `02_BUILD\LEXIQUE_READER_MVP\05_RELEASE\P24D_20260618_000512_FINAL_PRODUCT_V3_CONTRACT_BASELINE.zip` — `REVIEW_REQUIRED_ZIP`
- `ITEM-003020` — `02_BUILD\LEXIQUE_READER_MVP\05_RELEASE\P24D_20260618_000512\P24D_20260618_000512_FINAL_PRODUCT_V3_CONTRACT_BASELINE.zip` — `REVIEW_REQUIRED_ZIP`
- `ITEM-003049` — `02_BUILD\LEXIQUE_READER_MVP\08_PUBLICATION\P24D_20260618_000512_FINAL_PRODUCT_V3_CONTRACT_PUBLICATION_PACK_LOCAL_ONLY.zip` — `REVIEW_REQUIRED_ZIP`
- `ITEM-003116` — `02_BUILD\LEXIQUE_READER_MVP\08_PUBLICATION\P24D_20260618_000512\files\P24D_20260618_000512_FINAL_PRODUCT_V3_CONTRACT_BASELINE.zip` — `REVIEW_REQUIRED_ZIP`
- `ITEM-003133` — `02_BUILD\LEXIQUE_READER_MVP\08_PUBLICATION\P25A_20260618_002252\files\P24D_20260618_000512_FINAL_PRODUCT_V3_CONTRACT_BASELINE.zip` — `REVIEW_REQUIRED_ZIP`
- `ITEM-004855` — `03_EXPORTS\P50D_OUTPUT_CONTRACT_20260619_234723\P50D_PROMPT_OUTPUT_CONTRACT_REVIEW_20260619_234723.zip` — `REVIEW_REQUIRED_ZIP`
- `ITEM-004958` — `03_EXPORTS\P50F_HUMAN_REVIEW_PACK_20260619_235854\P50F_HUMAN_REVIEW_PACK_PROMPT_CONTRACTS_20260619_235854.zip` — `REVIEW_REQUIRED_ZIP`
- `ITEM-005185` — `03_EXPORTS\P51A_PROMPT_REVIEW_DECISION_20260620_004239\P51A_PROMPT_CONTRACT_HUMAN_REVIEW_DECISION_PACK_20260620_004239.zip` — `REVIEW_REQUIRED_ZIP`
- `ITEM-005222` — `03_EXPORTS\P51A2_AUTOFILL_DECISIONS_20260620_005747\P51A2_AUTOFILL_PROMPT_CONTRACT_DECISIONS_20260620_005747.zip` — `REVIEW_REQUIRED_ZIP`
- `ITEM-005248` — `03_EXPORTS\P51B_VALIDATE_DECISIONS_20260620_011301\P51B_VALIDATE_FILLED_PROMPT_CONTRACT_DECISIONS_20260620_011301.zip` — `REVIEW_REQUIRED_ZIP`
- `ITEM-005397` — `03_EXPORTS\P51E_SCRIPT_PATCH_SPEC_PACK_20260620_014912\P51E_SCRIPT_PATCH_SPEC_PACK_20260620_014912.zip` — `REVIEW_REQUIRED_ZIP`
- `ITEM-005441` — `03_EXPORTS\P51F_VALIDATE_SCRIPT_PATCH_SPEC_20260620_015531\P51F_VALIDATE_SCRIPT_PATCH_SPEC_PACK_20260620_015531.zip` — `REVIEW_REQUIRED_ZIP`
- `ITEM-005495` — `03_EXPORTS\P51F2_REPAIR_VALIDATE_SPEC_20260620_020405\P51F2_REPAIR_VALIDATE_SCRIPT_PATCH_SPEC_PACK_20260620_020405.zip` — `REVIEW_REQUIRED_ZIP`
- `ITEM-007960` — `P27A2A_UX_LOCK_CONTRACT_20260618\01_ZIP_RELEASE\MVP_QAIC_P27A2A_UX_LOCK_CONTRACT_PACK.zip` — `REVIEW_REQUIRED_ZIP`

### Non lisibles / formats à revoir

- Aucun format non lisible bloquant pour cette famille.

## 6. 🚦 Décision

- `FINAL_CANDIDATE_READY` : oui, pour les sources textuelles lisibles.
- `ARCHIVE_ALLOWED` : non dans P203B2-R3.
- `NEXT` : `P203B3_ARCHIVE_GATE_AND_FINAL_REFERENCE_INDEX`.

## Source 7: `docs/FINAL/fusion_inbox_R6/ARCHITECTURE/🧠 DECISION_JOURNAL_USAGE_AND_PROMPT_IMPROVEMENT_LOOP_0.4.6.md`

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

## Source 8: `docs/FINAL/fusion_inbox_R6/CDC/MEMO_MVP_QAIC_PHASE4_TO_FINAL_1.4.2.md`

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

## Source 9: `docs/FINAL/fusion_inbox_R6/MANIFEST/manifest_MVPQAIC_REFERENCE_DOCS_0.6.2_REAL_FUSION_REPAIR.json`

```json
{
  "project": "🛠️ MVP QAIC — Crypto Signal OS",
  "version": "0.6.2_REAL_FUSION_REPAIR",
  "date": "2026-06-16",
  "status": "DRAFT_FOR_HUMAN_VALIDATION_REAL_FUSION_REPAIR",
  "verdict_previous_pack": "0.6.1_NOT_REAL_FUSION_REJECTED_REWORK_REQUIRED",
  "source_documents": [
    {
      "title": "📘 CDC_MVP_QAIC_WEB_APP_LEXIQUE_FIRST_0.3.1_FULL_FUSION.md",
      "lines": 705,
      "bytes": 21874
    },
    {
      "title": "🗓️ PLANNING_MVP_QAIC_WEB_APP_TRANSITION_QAIC_0.3.1_FULL_FUSION.md",
      "lines": 827,
      "bytes": 19641
    },
    {
      "title": "🚀 INSTRUCTIONS_PROJET_MVP_QAIC_0.5.0_UI_FULL_FUSION_AND_SMART_CONSOLIDATION.md",
      "lines": 1440,
      "bytes": 38071
    }
  ],
  "generated_files": [
    {
      "title": "README_VALIDATION_PACK_MVP_QAIC_0.6.2_REAL_FUSION_REPAIR.md",
      "lines": 33,
      "bytes": 1260
    },
    {
      "title": "📘 CDC_MVP_QAIC_WEB_APP_LEXIQUE_FIRST_0.6.2_REAL_FUSION_REPAIR.md",
      "lines": 828,
      "bytes": 27670
    },
    {
      "title": "🔎 AUDIT_MVPQAIC_REFERENCE_DOCS_0.6.1_TO_0.6.2.md",
      "lines": 52,
      "bytes": 2503
    },
    {
      "title": "🗓️ PLANNING_MVP_QAIC_WEB_APP_TRANSITION_QAIC_0.6.2_REAL_FUSION_REPAIR.md",
      "lines": 1003,
      "bytes": 26933
    },
    {
      "title": "🚀 INSTRUCTIONS_PROJET_MVP_QAIC_0.6.2_REAL_FUSION_REPAIR.md",
      "lines": 1601,
      "bytes": 45827
    },
    {
      "title": "🧠 SYNTHESE_MVP_QAIC_PROJECT_CONTEXT_0.6.2_REAL_FUSION_REPAIR.md",
      "lines": 22,
      "bytes": 1057
    },
    {
      "title": "🧪 PLAN_TRANSITION_PORTFOLIO_BROKER_AUTOMATION_MVP_0.6.2.md",
      "lines": 66,
      "bytes": 2021
    },
    {
      "title": "🧭 RUNBOOK_MVP_QAIC_APPSHEET_MANUAL_BUILD_0.6.2.md",
      "lines": 61,
      "bytes": 2234
    },
    {
      "title": "🧱 ARCHITECTURE_MVP_QAIC_LEXIQUE_FIRST_APPSHEET_QAIC_PYTHON_0.6.2.md",
      "lines": 137,
      "bytes": 5112
    },
    {
      "title": "🧾 CHANGELOG_MVP_QAIC_REFERENCE_DOCS_0.6.2.md",
      "lines": 11,
      "bytes": 793
    }
  ],
  "rules_added": [
    "No FULL_FUSION claim without source audit",
    "Portfolio Revolut X read-only then controlled execution transition",
    "Automation orders/TP/SL/trailing not excluded; prepared and tested via QAIC Python under gates",
    "Live broker execution forbidden by default until explicit gated validation"
  ]
}
```

## Source 10: `docs/FINAL/fusion_inbox_R6/PLANNING/🗓️ PLANNING_MVP_QAIC_WEB_APP_TRANSITION_QAIC_0.6.2_REAL_FUSION_REPAIR.md`

# 🗓️ Planning — MVP QAIC Web App Lexique-first & Transition QAIC

> **Projet :** 🛠️ MVP QAIC — Crypto Signal OS Web App
> **Version :** `MVP_QAIC_PLANNING_0.6.2_REAL_FUSION_REPAIR_APPSHEET_PORTFOLIO_BROKER_TRANSITION`
> **Date :** 2026-06-16
> **Statut :** `DRAFT_FOR_HUMAN_VALIDATION_REAL_FUSION_REPAIR`
> **Format :** Markdown `.md`

---

## 0. 🧾 Historique des changements

| Version | Date | Statut | Changements |
|---|---:|---|---|
| `0.1.0` | 2026-06-11 | Draft | Planning initial Lexique-first |
| `0.2.0` | 2026-06-11 | Drive review ready | Ajout priorité Web App rapide + préparation bridge vers QAIC final |
| `0.2.1` | 2026-06-11 | Drive structure final ready | Confirmation de la structure Drive finale avec ajout de `08_QAIC_BRIDGE/` et `09_WEB_APP_IDE/`, préparation import Drive, bridge QAIC et future UI / IDE QAIC |
| `0.6.2` | 2026-06-16 | Real fusion repair | Réparation de fusion : conservation du planning 0.3.1, ajout des lots AppSheet P5, Lexique/Prompts/Journal, Portfolio Revolut X read-only puis tests d’exécution contrôlée via QAIC Python. |

---

## 1. 🎯 Objectif du planning

Ce planning organise le lancement de **MVP QAIC** en deux trajectoires complémentaires :

1. **Livraison rapide d’une Web App Lexique-first** centrée sur lexique, méthodes, signaux, risk playbook, checklists et journal.
2. **Préparation d’une transition progressive vers le QAIC final**, afin que cette Web App devienne plus tard l’interface utilisateur / UI IDE du moteur QAIC complet.

Le planning évite volontairement de commencer par une architecture lourde. Le projet avance par lots utiles, testables et réversibles.

---

## 2. 🧭 Modus operandi général

Pour chaque lot :

```text
1. Spécifier le livrable
2. Créer / stabiliser les tables Google Sheets
3. Écrire ou générer le script complet
4. Tester dans DEV
5. Corriger affichage, validations, listes, couleurs
6. Exporter backup / ZIP
7. Mettre à jour changelog
8. Passer au lot suivant
```

Règles :

- pas de BigQuery au lancement ;
- pas de Cloud Run prématuré ;
- pas de trading automatique ;
- pas de broker ;
- pas d’AppSheet avant stabilisation des colonnes ;
- pas de Looker Studio avant données lisibles ;
- pas d’intégration QAIC avant création d’une couche bridge propre.

---

## 3. 🧩 Découpage en lots

| Lot | Nom | Objectif | Statut cible |
|---:|---|---|---|
| 0 | Foundation Google | Dossier, docs, Sheet DEV | Prêt à développer |
| 1 | Knowledge Base | Structurer lexique/méthodes/signaux | Utilisable dans Sheets |
| 2 | Knowledge Engine | Recherche + fonctions Apps Script | Base active |
| 3 | Web App MVP | AppSheet / Web App rapide | Première app utilisable |
| 4 | Scoring MVP | Score explicable manuel/semi-auto | Décision guidée |
| 5 | Journal & Dashboard | Usage quotidien | Routine opérationnelle |
| 6 | QAIC Bridge Prep | Préparer mappings QAIC | Transition possible |
| 7 | QAIC Integration | Brancher outputs QAIC progressivement | Web App devient UI QAIC |
| 8 | Hardening | Docs, tests, stabilisation | Version stable |

---

## 4. 🚦 Phase 0 — Foundation Google

### Objectif

Créer l’environnement propre dans Google Drive et Google Sheets.

### Durée indicative

`J0 à J1`

### Actions

| Action | Outil | Résultat |
|---|---|---|
| Créer dossier Drive racine | Google Drive | `🛠️ MVP QAIC — Crypto Signal OS` |
| Créer sous-dossiers projet | Google Drive | Admin, docs, sheets, scripts, AppSheet, Looker, Stitch, Antigravity, QAIC Bridge, Web App IDE |
| Créer Google Sheet DEV | Google Sheets | `MVP QAIC — Crypto Signal OS — DEV` |
| Ajouter docs de référence | Drive / Markdown | CDC, planning, instructions |
| Créer changelog | Markdown | Historique projet |

### Livrables

```text
📘 CDC_MVP_QAIC_WEB_APP_LEXIQUE_FIRST_0.2.1.md
🗓️ PLANNING_MVP_QAIC_WEB_APP_TRANSITION_QAIC_0.2.1.md
🚀 INSTRUCTIONS_PROJET_MVP_QAIC_0.2.1.md
📁 MVP_QAIC_DRIVE_STRUCTURE_0.2.1_READY_FOR_IMPORT.zip
README_PROJECT.md
CHANGELOG.md
```



### Structure Drive finale obligatoire

La Phase 0 doit créer ou importer la structure Drive finale suivante :

```text
🛠️ MVP QAIC — Crypto Signal OS/
│
├── 00_ADMIN/
│   ├── README_PROJECT.md
│   ├── CHANGELOG.md
│   └── DECISIONS_LOG.md
│
├── 01_DOCS/
│   ├── CDC/
│   ├── PLANNING/
│   ├── INSTRUCTIONS/
│   ├── RUNBOOK/
│   └── PROMPTS/
│
├── 02_SHEETS/
│   ├── DEV/
│   ├── EXPORTS_CSV/
│   └── BACKUPS/
│
├── 03_APPS_SCRIPT/
│   ├── SOURCE/
│   ├── BACKUPS/
│   └── ZIP/
│
├── 04_APPSHEET/
│   ├── SPEC/
│   └── SCREENSHOTS/
│
├── 05_LOOKER/
│   ├── DASHBOARD_SPEC/
│   └── EXPORTS/
│
├── 06_STITCH/
│   ├── PROMPTS/
│   └── UI_EXPORTS/
│
├── 07_ANTIGRAVITY/
│   ├── PROMPTS/
│   ├── TASKS/
│   └── OUTPUTS/
│
├── 08_QAIC_BRIDGE/
│   ├── IMPORT_SPECS/
│   ├── MAPPING/
│   └── OUTPUTS/
│
├── 09_WEB_APP_IDE/
│   ├── UI_SPEC/
│   ├── COMPONENTS/
│   └── USER_FLOWS/
│
└── 99_ARCHIVES/
```

Les dossiers `08_QAIC_BRIDGE/` et `09_WEB_APP_IDE/` sont intégrés dès le départ, même si leur usage complet arrive plus tard. Ils servent à éviter une restructuration lourde au moment de connecter le MVP au QAIC final.

### Gate de sortie

```text
✅ Dossier Drive créé avec `08_QAIC_BRIDGE/` et `09_WEB_APP_IDE/`
✅ Sheet DEV créé
✅ Docs de référence déposés
✅ Règles de sécurité produit validées
```

---

## 5. 📚 Phase 1 — Knowledge Base Lexique-first

### Objectif

Transformer le lexique Markdown en tables Google Sheets structurées.

### Durée indicative

`J1 à J3`

### Onglets à créer

| Onglet | Priorité | But |
|---|---:|---|
| `CONFIG` | P0 | Paramètres globaux |
| `KNOWLEDGE_TERMS` | P0 | Définitions consultables |
| `METHOD_LIBRARY` | P0 | Méthodes structurées |
| `SIGNAL_LIBRARY` | P0 | Signaux structurés |
| `RISK_PLAYBOOK` | P0 | TP / SL / sizing |
| `MARKET_REGIME_RULES` | P0 | Règles BTC risk-on/off |
| `VOLATILITY_RULES` | P0 | Règles tokens volatils |
| `CHECKLISTS` | P0 | Routines d’analyse |
| `DECISION_TEMPLATES` | P0 | Modèles de décisions |
| `GLOSSARY_TAGS` | P0 | Tags et catégories |

### Colonnes minimales recommandées

#### `KNOWLEDGE_TERMS`

```text
term_id
category
term
short_definition
full_definition
daily_use
risk_note
related_terms
tags
priority
source_section
status
updated_at
```

#### `METHOD_LIBRARY`

```text
method_id
method_name
market_context
entry_conditions
confirmation_signals
invalidations
tp_logic
sl_logic
best_timeframes
risk_level
tags
status
```

#### `SIGNAL_LIBRARY`

```text
signal_id
signal_type
signal_name
description
required_data
bullish_or_bearish
weight
false_signal_risk
action
related_methods
tags
status
```

#### `RISK_PLAYBOOK`

```text
profile
max_position_rule
sl_method
tp1_percent_sell
tp2_percent_sell
tp3_percent_sell
runner_percent
max_loss_rule
invalidation_rule
risk_warning
```

### Gate de sortie

```text
✅ Onglets P0 créés
✅ Colonnes validées
✅ Données lexique initiales importées ou préparées
✅ Tables lisibles et filtrables
✅ Aucun onglet inutile créé
```

---

## 6. ⚙️ Phase 2 — Apps Script Knowledge Engine

### Objectif

Rendre la Knowledge Base active avec menus, recherche, formatage et fonctions utilitaires.

### Durée indicative

`J3 à J5`

### Fonctions Apps Script à créer

```javascript
MVPQAIC_Setup()
MVPQAIC_Format_All()
MVPQAIC_SearchKnowledge(query)
MVPQAIC_GetTerm(termId)
MVPQAIC_GetMethod(methodId)
MVPQAIC_GetSignalsByProfile(profile)
MVPQAIC_GetRiskPlaybook(profile)
MVPQAIC_GenerateChecklist(session)
MVPQAIC_ExplainDecision(decisionCode)
MVPQAIC_Status()
```

### Règles techniques

- script complet, remplaçable intégralement ;
- batch read/write ;
- pas de scans globaux inutiles ;
- validations de données ;
- filtres ;
- freeze lignes/colonnes ;
- couleurs utiles ;
- logs compacts ;
- pas de trigger automatique au départ.

### Gate de sortie

```text
✅ Menu MVP QAIC disponible
✅ Setup exécutable
✅ Recherche lexique testée
✅ Formatage stable
✅ Aucun ordre automatique / broker / trigger sensible
```

---

## 7. 🌐 Phase 3 — Web App MVP rapide

### Objectif

Livrer rapidement une première Web App utilisable.

### Durée indicative

`J5 à J8`

### Option rapide recommandée

```text
Google Sheets + AppSheet
```

### Option alternative

```text
Apps Script Web App HTMLService
```

### Écrans prioritaires

| Écran | Source Sheet | Fonction |
|---|---|---|
| Knowledge Home | Plusieurs P0 | Accès aux blocs principaux |
| Search Term | `KNOWLEDGE_TERMS` | Recherche de termes |
| Term Detail | `KNOWLEDGE_TERMS` | Fiche détaillée |
| Method Detail | `METHOD_LIBRARY` | Méthode opérationnelle |
| Signal Library | `SIGNAL_LIBRARY` | Signaux filtrés |
| Risk Playbook | `RISK_PLAYBOOK` | Règles TP/SL |
| Daily Checklist | `CHECKLISTS` | Routine quotidienne |
| Decision Journal | `DECISION_JOURNAL` | Journaliser décision |

### Gate de sortie

```text
✅ Web App accessible
✅ Recherche utilisable
✅ Fiches méthodes lisibles
✅ Risk Playbook consultable
✅ Journal possible
✅ UX mobile acceptable
```

---

## 8. 🧮 Phase 4 — Scoring MVP léger

### Objectif

Ajouter un score explicable sans dépendre encore du QAIC final.

### Durée indicative

`J8 à J11`

### Onglets à ajouter

```text
TOKENS
MANUAL_ANALYSIS
SCORING_RULES
SCORES
DAILY_PLAN
```

### Décisions MVP

| Décision | Usage |
|---|---|
| `SETUP_STRONG_REVIEW` | Setup fort, revue humaine requise |
| `BUY_SMALL_REVIEW` | Petite taille possible après revue humaine |
| `WATCH` | Surveillance |
| `WEAK` | Faible qualité |
| `AVOID` | Éviter |
| `BLOCKED` | Bloqué par risque |

### Gate de sortie

```text
✅ Score /100 calculable
✅ Décision générée
✅ Explication générée
✅ Invalidation affichée
✅ Risk warning affiché
```

---

## 9. 📝 Phase 5 — Journal & Dashboard quotidien

### Objectif

Rendre l’outil utilisable dans une routine quotidienne.

### Durée indicative

`J11 à J14`

### Modules

| Module | Description |
|---|---|
| Daily Plan | Plan du jour |
| Decision Journal | Pourquoi analyser / attendre / éviter |
| Risk Warnings | Alertes risque |
| Score Explanation | Explication du score |
| Checklist Status | État de complétion |
| Looker Overview | Vue synthétique |

### Gate de sortie

```text
✅ Routine quotidienne possible
✅ Journal de décision utilisable
✅ Dashboard clair
✅ Aucun signal non expliqué
```

---

## 10. 🔌 Phase 6 — Préparation bridge QAIC final

### Objectif

Préparer les points d’entrée pour récupérer progressivement l’outil QAIC final.

### Durée indicative

`J14 à J18`

### Onglets bridge

```text
QAIC_OUTPUTS_IMPORT
QAIC_SCORE_MAPPING
QAIC_RISK_MAPPING
QAIC_DECISION_MAPPING
QAIC_BACKTEST_MAPPING
QAIC_INTEGRATION_LOG
```

### Outputs futurs à prévoir

```text
market_regime_score
alpha_score
risk_score
confidence_score
quality_score
decision_status
portfolio_warnings
backtest_status
attribution_summary
```

### Gate de sortie

```text
✅ Bridge non bloquant créé
✅ Le MVP fonctionne sans QAIC final
✅ Les mappings sont documentés
✅ Aucun couplage dur prématuré
```

---

## 11. 🧠 Phase 7 — Intégration progressive QAIC final

### Objectif

Brancher progressivement les outputs du QAIC final quand ils sont stables.

### Durée indicative

`Après stabilisation QAIC final`

### Ordre d’intégration recommandé

| Ordre | Output QAIC | Pourquoi |
|---:|---|---|
| 1 | `market_regime_score` | Impact direct sur décisions |
| 2 | `risk_score` | Sécurité et blocages |
| 3 | `alpha_score` | Scoring avancé |
| 4 | `confidence_score` | Qualité du signal |
| 5 | `backtest_status` | Validation historique |
| 6 | `attribution_summary` | Explicabilité avancée |
| 7 | `portfolio_warnings` | À traiter avec prudence, hors exécution |

### Gate de sortie

```text
✅ Un output QAIC intégré à la Web App
✅ Mapping validé
✅ Explication affichée
✅ Pas de trading automatique
✅ Journalisation des imports QAIC
```

---

## 12. 🎨 Stitch — Planning UI

### Objectif

Créer les maquettes de la Web App.

### Quand

À partir de `J5`, en parallèle de la Phase 3.

### Écrans Stitch

```text
Knowledge Home
Search Term
Term Detail
Method Detail
Signal Library
Risk Playbook
Daily Checklist
Decision Journal
Score Detail
QAIC Output Detail futur
```

### Gate de sortie

```text
✅ Design mobile-first
✅ Hiérarchie claire
✅ Risques visibles
✅ Aucun bouton d’exécution réelle
```

---

## 13. 🤖 Antigravity — Planning développement

### Objectif

Utiliser Antigravity uniquement sur des lots bornés.

### Lots possibles

| Lot Antigravity | Entrée | Sortie attendue |
|---|---|---|
| Parser lexique | Markdown lexique | Tables structurées |
| Setup Apps Script | Schéma Sheets | Script complet setup |
| Knowledge Engine | Tables P0 | Fonctions recherche |
| AppSheet spec | Tables stables | Spec écrans |
| QAIC bridge | Mapping défini | Tables + fonctions import |

### Interdiction

Ne pas demander à Antigravity :

```text
Crée toute l’app crypto complète.
```

Toujours donner :

- périmètre ;
- fichiers autorisés ;
- sorties attendues ;
- interdictions ;
- tests ;
- critères de validation.

---

## 14. 📅 Timeline synthétique

| Jour | Objectif | Livrable |
|---:|---|---|
| J0 | Foundation Drive | Dossier + docs |
| J1 | Sheet DEV | Base créée |
| J2 | Onglets P0 | Knowledge schema |
| J3 | Import lexique | Données initiales |
| J4 | Apps Script setup | Menu + format |
| J5 | Recherche | Knowledge Engine |
| J6 | AppSheet skeleton | Web App v0 |
| J7 | Écrans P0 | Recherche + fiches |
| J8 | Risk Playbook | TP/SL consultables |
| J9 | Journal | Décisions historisées |
| J10 | Scoring MVP | Score /100 |
| J11 | Dashboard | Vue quotidienne |
| J12 | Tests usage | Corrections UX |
| J13 | Looker simple | Dashboard visuel |
| J14 | MVP Review | Go/no-go |
| J15+ | QAIC bridge | Préparation transition |

---

## 15. ✅ Go-live MVP

Le MVP peut être considéré comme lancé si :

```text
✅ La Web App est accessible
✅ La recherche lexique fonctionne
✅ Les méthodes sont lisibles
✅ Les signaux sont filtrables
✅ Le Risk Playbook est utilisable
✅ Les checklists sont utilisables
✅ Le journal fonctionne
✅ Les décisions sont explicables
✅ Aucun ordre automatique n’existe
✅ La transition QAIC est prévue mais non bloquante
```

---

## 16. 🔁 Routine projet après lancement

### Hebdomadaire

```text
1. Revue des termes manquants
2. Revue des méthodes à structurer
3. Revue des signaux à transformer en règles
4. Revue UX Web App
5. Revue journal utilisateur
6. Revue éventuelle des outputs QAIC stables à intégrer
```

### Mensuel

```text
1. Export backup Drive
2. Changelog versionné
3. Audit des tables
4. Nettoyage des champs inutiles
5. Préparation éventuelle bridge QAIC suivant
```

---

## 17. 🎯 Conclusion planning

La priorité est nette :

```text
Livrer vite une Web App Lexique/Méthodes/Signaux.
```

Puis :

```text
Préparer calmement la récupération progressive du QAIC final.
```

Le MVP doit rester simple, utile, explicable et compatible avec l’avenir.


---

# 12. 🤖 Planning opérationnel Antigravity P0

## 12.1 Principe

Antigravity intervient **après cadrage documentaire** et **avant import Google**. Il produit des fichiers contrôlés dans un workspace local, puis l’humain valide avant dépôt Drive, import Sheets ou création AppSheet.

```text
Docs source validées
↓
Workspace local Antigravity
↓
Production P0-A / P0-B / P0-C / P0-D / P0-E
↓
Review humaine
↓
Import Drive / Sheets / AppSheet
```

## 12.2 Ordre des lots

| Ordre | Lot | Action | Validation avant suite |
|---:|---|---|---|
| 1 | `P0-A` | Parser le lexique en CSV + schéma | CSV propres, pas d’invention, IDs stables |
| 2 | `P0-B` | Générer Apps Script setup P0 | Script complet, pas destructif, formatage OK |
| 3 | `P0-C` | Générer spec AppSheet | Vues alignées sur tables P0 |
| 4 | `P0-D` | Générer prompts Stitch | Écrans Knowledge-first cohérents |
| 5 | `P0-E` | Générer placeholders QAIC Bridge | Mapping futur sans connexion réelle |

## 12.3 Planning court recommandé

| Jour | Lot | Objectif | Sortie |
|---:|---|---|---|
| J0 | Préparation | Créer workspace local et déposer sources | `MVP_QAIC/` prêt |
| J1 | `P0-A` | Knowledge Base CSV | `csv_seed/*.csv` + schéma |
| J2 | Review P0-A | Contrôle qualité des CSV | corrections / `VALIDATED` |
| J3 | `P0-B` | Apps Script setup | `.gs` complets |
| J4 | Test P0-B | Google Sheet DEV | onglets P0 formatés |
| J5 | `P0-C` | AppSheet spec | vues + actions |
| J6 | `P0-D` | Stitch prompts | écrans UI |
| J7 | `P0-E` | QAIC Bridge placeholders | specs mapping futur |

## 12.4 Stop conditions

Arrêter le batch Antigravity si :

- fichiers inattendus ou hors périmètre ;
- règles de trading inventées ;
- tentative de broker/exécution ;
- schéma trop large ou non AppSheet-friendly ;
- absence de manifest ;
- absence de statut `REVIEW_REQUIRED` sur les champs incertains ;
- proposition de BigQuery/Cloud Run prématurée ;
- suppression/renommage non demandé.

## 12.5 Prochaine action immédiate

Le prochain travail après cette mise à jour documentaire est :

```text
Préparer le pack de lancement Antigravity P0-A
```

Contenu attendu :

```text
ANTIGRAVITY_P0A_KNOWLEDGE_BASE_PROMPT_0.2.2.md
ANTIGRAVITY_P0A_ACCEPTANCE_CRITERIA_0.2.2.md
ANTIGRAVITY_P0A_WORKSPACE_TREE_0.2.2.md
```


---

## 18. 🧭 Planning P0-B6 — Gouvernance documentaire validée

> Cette section complète le planning `0.2.2` sans supprimer les phases initiales.

### 18.1 Jalons réalisés

| Ordre | Phase | Objectif | Statut |
|---:|---|---|---|
| 1 | `P0-A` | Knowledge Base CSV initiale | ✅ Fait |
| 2 | `P0-B` | Apps Script foundation | ✅ Fait |
| 3 | `P0-B2` | Expansion KB + prompts | ✅ Fait |
| 4 | `P0-B3` | Institutional readiness | ✅ Fait |
| 5 | `P0-B4` | GPT/Revolut X read-only bridge | ✅ Fait |
| 6 | `P0-B5` | Trade plan methods & trailing | ✅ Fait |
| 7 | `P0-B5.6` | Full Signal Mapping 50/50 | ✅ Fait |
| 8 | `P0-B6` | Docs / governance / runbook | ✅ Fait |
| 9 | `P0-C` | AppSheet MVP readiness | 🔜 Suivant |
| 10 | `P0-D` | Stitch UI prompts | Après P0-C |
| 11 | `P0-E` | QAIC bridge operational specs | Après premier usage AppSheet |
| 12 | `P1` | Journal + dashboards + QAIC response audit | Après MVP UI |

### 18.2 P0-C — AppSheet MVP Readiness

Livrables attendus :

```text
APPSHEET_SPEC_MVP_QAIC_0.3.2.md
APPSHEET_TABLES_AND_COLUMNS_0.3.2.md
APPSHEET_VIEWS_0.3.2.md
APPSHEET_ACTIONS_0.3.2.md
APPSHEET_SECURITY_AND_GUARDS_0.3.2.md
APPSHEET_TEST_PLAN_0.3.2.md
```

Vues prioritaires :

| Vue | Table principale | Objectif |
|---|---|---|
| 🏠 Home | CONFIG / synthèse | Accès rapide |
| 🔍 Search | KNOWLEDGE_TERMS | Recherche lexique |
| 📚 Term Detail | KNOWLEDGE_TERMS | Compréhension |
| 🧠 Methods | METHOD_LIBRARY | Méthodes |
| ⚡ Signals | SIGNAL_LIBRARY | Signaux |
| 🧮 Scores | SCORING_MODEL_SPEC / SIGNAL_EVALUATION_RULES | Explication |
| 🎯 Trade Plan | TRADE_PLAN_METHODS / TP_SL_CALCULATION_RULES | Plan sans exécution |
| 🛡️ Risk | RISK_PLAYBOOK / DECISION_MATRIX | Garde-fous |
| 🧾 Payloads | GPT_INPUT_PAYLOADS | Copie GPT |
| 📝 Journal | DECISION_JOURNAL | Décision humaine |

### 18.3 Stop conditions P0-C

Arrêter si :

```text
colonnes instables
décision ambiguë type Buy/Sell direct
bouton d’ordre réel
absence de garde-fou HUMAN_REVIEW_ONLY
absence de journal
```

---

## 🛠️ Addendum de réparation documentaire — 0.6.2 REAL FUSION REPAIR

> **Nature de cette version :** réparation de fusion documentaire réelle.
> Cette version **ne remplace pas par un résumé court** les documents de référence précédents. Elle reprend les documents sources validés, conserve leur structure, puis applique les décisions actées depuis la dernière mise à jour.

### Décisions actées intégrées

| Décision | Statut 0.6.2 | Règle corrigée |
|---|---|---|
| Recherche Lexique Master | Priorité immédiate P0 | Le MVP AppSheet doit d’abord rendre le lexique, les méthodes et les signaux consultables/recherchables. |
| Prompts 1 à 5 | Priorité immédiate P0/P1 | Les prompts deviennent le cœur opérationnel : sélection, copie vers Gem, réponse, intake, journalisation. |
| AppSheet MVP actuel | Validé comme AppShell manuel non déployé | 10 tables injectées, navigation OK, affinage UX ultérieur. |
| Portfolio Revolut X | À faire, non reporté | D’abord read-only, puis transition vers exécution contrôlée testée. |
| Ordres / achat / vente / TP / SL / trailing stop | Non exclus du MVP | Préparation, simulations et tests MVP autorisés ; exécution réelle interdite par défaut sans gates. |
| QAIC Python | Cible de transition | Préparer broker adapter, paper trading, dry-run, validations, logs, kill switch. |
| Sécurité | Permanente | HUMAN_REVIEW_ONLY par défaut, NO_AUTO_ORDER/NO_AUTO_SIZING/NO_BROKER_EXECUTION tant que les gates ne sont pas explicitement ouverts. |

### Correction importante

Les formulations anciennes du type “ne jamais coder d’exécution d’ordre” ou “automation exclue” sont remplacées par une règle plus précise :

```text
Interdit maintenant : exécution réelle non validée, ordre réel automatique, sizing réel automatique, secrets exposés, broker live sans architecture sécurisée.
Autorisé dans la trajectoire MVP : préparation fonctionnelle, maquette, tickets manuels, read-only portfolio, paper trading, dry-run, tests contrôlés, bridge QAIC Python.
```

---

## 📱 État AppSheet MVP validé au 2026-06-16

### Tables MVP injectées

| Table | Rôle | Statut |
|---|---|---|
| `SEARCH_COCKPIT` | Recherche lexique/méthodes/signaux | OK |
| `LEXIQUE_MASTER` | Source lexique principale | OK |
| `PROMPT_LEXIQUE_BRIDGE` | Bridge prompts ↔ lexique | REVIEW clé à améliorer |
| `PROMPT_CONTEXT_PACKS` | Packs contexte prompts | REVIEW clé/colonnes à améliorer |
| `PROMPT_LIBRARY` | Bibliothèque prompts | OK |
| `PROMPT_READY_TO_COPY` | Prompts prêts à copier | REVIEW clé à améliorer |
| `PROMPT_RUN_QUEUE` | Queue de run manuel | OK, `run_queue_id` clé |
| `RESPONSE_INTAKE_QUEUE` | Intake réponse Gem/GPT | OK, `intake_queue_id` clé |
| `JOURNAL_APPEND_QUEUE` | Pré-journalisation | OK, `journal_queue_id` clé |
| `DECISION_JOURNAL` | Journal officiel décisions | OK, `journal_id` clé |

### Vues MVP validées

| Vue | Source | Usage |
|---|---|---|
| `MVP QAIC Home` | `SEARCH_COCKPIT` | Accueil/recherche |
| `Lexique` | `LEXIQUE_MASTER` | Consultation lexique |
| `Prompts Ready` | `PROMPT_READY_TO_COPY` | Prompts prêts à copier |
| `Run Queue` | `PROMPT_RUN_QUEUE` | Flux manuel prompt → réponse |
| `Decision Journal` | `DECISION_JOURNAL` | Audit read-only |

### Règle AppSheet actuelle

```text
App non déployée.
Build manuel.
Pas d’automation AppSheet.
Pas d’action broker.
Pas d’ordre.
Pas de sizing.
Affinage UX après validation structurelle.
```

---

## 💼 Portfolio Revolut X & transition exécution contrôlée

### Priorité produit

Le portefeuille Revolut X n’est **pas reporté hors trajectoire**. Il est intégré comme axe prioritaire après stabilisation du socle Lexique/Prompts/Journal.

| Niveau | Fonction | Autorisation |
|---:|---|---|
| 1 | Consultation portfolio Revolut X | Read-only |
| 2 | Analyse exposition/risque | Read-only + prompts |
| 3 | Alertes portefeuille | Notification / review only |
| 4 | Tickets manuels | Préparation d’action humaine |
| 5 | Paper trading | Simulation contrôlée |
| 6 | Dry-run broker | Test sans ordre réel |
| 7 | Exécution réelle assistée | Uniquement après gates séparés |
| 8 | TP/SL/trailing automatique | Uniquement après architecture QAIC Python sécurisée |

### Ce qui doit être construit progressivement

```text
Portfolio Revolut X read-only
→ Prompt 1 Portfolio Analysis
→ Prompt 5 Full Trading Review
→ Risk Gate
→ Alert Center
→ Manual Trade Ticket
→ Paper Trading
→ Dry-run Broker Adapter
→ QAIC Python Broker Adapter
→ Exécution live seulement après GO explicite, kill switch, logs, secrets sécurisés et validations.
```

### Garde-fous obligatoires

| Domaine | Garde-fou |
|---|---|
| Secrets | Secret Manager / jamais dans Sheets / Apps Script / Drive |
| Exécution | Kill switch visible et testé |
| Données | Vérification freshness, source, prix, PRU, quantité, exposition |
| Risque | Max exposure, concentration, NO_ADD, REDUCE_RISK_REVIEW, BLOCK |
| Logs | Journal immuable / run_id / timestamp / payload_id |
| Validation humaine | Human approval avant tout ordre réel |
| Tests | Paper trading puis dry-run avant live |

---


---

## 12. 📱 Phase P5 — AppSheet MVP réel validé manuellement

| Lot | Objectif | Statut |
|---|---|---|
| P5A à P5G | WebApp readiness, schema contract, navigation, blueprint, go/no-go | Réalisé |
| P5H à P5J | Plan réparation schema, dry-run evidence, preflight, apply guarded | Réalisé |
| P5K à P5N | Handoff pack, runbook build manuel | Réalisé |
| P5O/P5P | Post-build validation et evidence closure | En attente résultats humains |

### Tables MVP AppSheet à maintenir

```text
SEARCH_COCKPIT
LEXIQUE_MASTER
PROMPT_LEXIQUE_BRIDGE
PROMPT_CONTEXT_PACKS
PROMPT_LIBRARY
PROMPT_READY_TO_COPY
PROMPT_RUN_QUEUE
RESPONSE_INTAKE_QUEUE
JOURNAL_APPEND_QUEUE
DECISION_JOURNAL
```

### Prochaine priorité opérationnelle

```text
1. Affiner UX Lexique / Prompts / Journal
2. Ajouter Daily Review / Prompt Launcher 1–5
3. Ajouter Portfolio Revolut X read-only
4. Ajouter Alert Center
5. Ajouter Manual Trade Tickets
6. Ajouter Paper Trading
7. Ajouter Dry-run broker adapter QAIC Python
8. Tester transition TP/SL/trailing stop en simulation
```

---

## 13. 💼 Phase Portfolio / Broker Transition — MVP testable, non live par défaut

| Phase | Objectif | Gate |
|---:|---|---|
| B0 | Portfolio Revolut X read-only | Source fiable + aucune écriture broker |
| B1 | Prompt 1 Portfolio Analysis | Données portfolio complètes |
| B2 | Prompt 5 Daily Full Review | Market + portfolio + data quality |
| B3 | Alert Center | Alertes sans exécution |
| B4 | Manual Trade Ticket | Validation humaine |
| B5 | Paper trading | Simulation |
| B6 | Dry-run broker | Zéro ordre réel |
| B7 | Live assisted execution | GO explicite séparé + kill switch + secrets sécurisés |
| B8 | TP/SL/trailing automation | Projet durci QAIC Python / backend |

---

## Source 11: `docs/FINAL/fusion_inbox_R6/PLANNING/🗓️ PLANNING_MVP_QAIC_WEB_APP_TRANSITION_QAIC_0.7.2_REAL_FULL_SOURCE_FUSION.md`

<!--
REAL FULL SOURCE FUSION 0.7.2
Source original preserved: 🗓️ PLANNING_MVP_QAIC_WEB_APP_TRANSITION_QAIC_0.6.2_REAL_FUSION_REPAIR.md
Source SHA256: 6904e0a495e1789faa9d582e726f401eccc3e6cbf630279768e805a92ba94630
Source lines: 1004
Fusion rule: original content is kept, then a scope-split correction block is appended.
No Drive overwrite. No Apps Script run. No clasp push.
-->

# 🗓️ Planning — MVP QAIC Web App Lexique-first & Transition QAIC

> **Projet :** 🛠️ MVP QAIC — Crypto Signal OS Web App
> **Version :** `MVP_QAIC_PLANNING_0.6.2_REAL_FUSION_REPAIR_APPSHEET_PORTFOLIO_BROKER_TRANSITION`
> **Date :** 2026-06-16
> **Statut :** `DRAFT_FOR_HUMAN_VALIDATION_REAL_FUSION_REPAIR`
> **Format :** Markdown `.md`

---

## 0. 🧾 Historique des changements

| Version | Date | Statut | Changements |
|---|---:|---|---|
| `0.1.0` | 2026-06-11 | Draft | Planning initial Lexique-first |
| `0.2.0` | 2026-06-11 | Drive review ready | Ajout priorité Web App rapide + préparation bridge vers QAIC final |
| `0.2.1` | 2026-06-11 | Drive structure final ready | Confirmation de la structure Drive finale avec ajout de `08_QAIC_BRIDGE/` et `09_WEB_APP_IDE/`, préparation import Drive, bridge QAIC et future UI / IDE QAIC |
| `0.6.2` | 2026-06-16 | Real fusion repair | Réparation de fusion : conservation du planning 0.3.1, ajout des lots AppSheet P5, Lexique/Prompts/Journal, Portfolio Revolut X read-only puis tests d’exécution contrôlée via QAIC Python. |

---

## 1. 🎯 Objectif du planning

Ce planning organise le lancement de **MVP QAIC** en deux trajectoires complémentaires :

1. **Livraison rapide d’une Web App Lexique-first** centrée sur lexique, méthodes, signaux, risk playbook, checklists et journal.
2. **Préparation d’une transition progressive vers le QAIC final**, afin que cette Web App devienne plus tard l’interface utilisateur / UI IDE du moteur QAIC complet.

Le planning évite volontairement de commencer par une architecture lourde. Le projet avance par lots utiles, testables et réversibles.

---

## 2. 🧭 Modus operandi général

Pour chaque lot :

```text
1. Spécifier le livrable
2. Créer / stabiliser les tables Google Sheets
3. Écrire ou générer le script complet
4. Tester dans DEV
5. Corriger affichage, validations, listes, couleurs
6. Exporter backup / ZIP
7. Mettre à jour changelog
8. Passer au lot suivant
```

Règles :

- pas de BigQuery au lancement ;
- pas de Cloud Run prématuré ;
- pas de trading automatique ;
- pas de broker ;
- pas d’AppSheet avant stabilisation des colonnes ;
- pas de Looker Studio avant données lisibles ;
- pas d’intégration QAIC avant création d’une couche bridge propre.

---

## 3. 🧩 Découpage en lots

| Lot | Nom | Objectif | Statut cible |
|---:|---|---|---|
| 0 | Foundation Google | Dossier, docs, Sheet DEV | Prêt à développer |
| 1 | Knowledge Base | Structurer lexique/méthodes/signaux | Utilisable dans Sheets |
| 2 | Knowledge Engine | Recherche + fonctions Apps Script | Base active |
| 3 | Web App MVP | AppSheet / Web App rapide | Première app utilisable |
| 4 | Scoring MVP | Score explicable manuel/semi-auto | Décision guidée |
| 5 | Journal & Dashboard | Usage quotidien | Routine opérationnelle |
| 6 | QAIC Bridge Prep | Préparer mappings QAIC | Transition possible |
| 7 | QAIC Integration | Brancher outputs QAIC progressivement | Web App devient UI QAIC |
| 8 | Hardening | Docs, tests, stabilisation | Version stable |

---

## 4. 🚦 Phase 0 — Foundation Google

### Objectif

Créer l’environnement propre dans Google Drive et Google Sheets.

### Durée indicative

`J0 à J1`

### Actions

| Action | Outil | Résultat |
|---|---|---|
| Créer dossier Drive racine | Google Drive | `🛠️ MVP QAIC — Crypto Signal OS` |
| Créer sous-dossiers projet | Google Drive | Admin, docs, sheets, scripts, AppSheet, Looker, Stitch, Antigravity, QAIC Bridge, Web App IDE |
| Créer Google Sheet DEV | Google Sheets | `MVP QAIC — Crypto Signal OS — DEV` |
| Ajouter docs de référence | Drive / Markdown | CDC, planning, instructions |
| Créer changelog | Markdown | Historique projet |

### Livrables

```text
📘 CDC_MVP_QAIC_WEB_APP_LEXIQUE_FIRST_0.2.1.md
🗓️ PLANNING_MVP_QAIC_WEB_APP_TRANSITION_QAIC_0.2.1.md
🚀 INSTRUCTIONS_PROJET_MVP_QAIC_0.2.1.md
📁 MVP_QAIC_DRIVE_STRUCTURE_0.2.1_READY_FOR_IMPORT.zip
README_PROJECT.md
CHANGELOG.md
```



### Structure Drive finale obligatoire

La Phase 0 doit créer ou importer la structure Drive finale suivante :

```text
🛠️ MVP QAIC — Crypto Signal OS/
│
├── 00_ADMIN/
│   ├── README_PROJECT.md
│   ├── CHANGELOG.md
│   └── DECISIONS_LOG.md
│
├── 01_DOCS/
│   ├── CDC/
│   ├── PLANNING/
│   ├── INSTRUCTIONS/
│   ├── RUNBOOK/
│   └── PROMPTS/
│
├── 02_SHEETS/
│   ├── DEV/
│   ├── EXPORTS_CSV/
│   └── BACKUPS/
│
├── 03_APPS_SCRIPT/
│   ├── SOURCE/
│   ├── BACKUPS/
│   └── ZIP/
│
├── 04_APPSHEET/
│   ├── SPEC/
│   └── SCREENSHOTS/
│
├── 05_LOOKER/
│   ├── DASHBOARD_SPEC/
│   └── EXPORTS/
│
├── 06_STITCH/
│   ├── PROMPTS/
│   └── UI_EXPORTS/
│
├── 07_ANTIGRAVITY/
│   ├── PROMPTS/
│   ├── TASKS/
│   └── OUTPUTS/
│
├── 08_QAIC_BRIDGE/
│   ├── IMPORT_SPECS/
│   ├── MAPPING/
│   └── OUTPUTS/
│
├── 09_WEB_APP_IDE/
│   ├── UI_SPEC/
│   ├── COMPONENTS/
│   └── USER_FLOWS/
│
└── 99_ARCHIVES/
```

Les dossiers `08_QAIC_BRIDGE/` et `09_WEB_APP_IDE/` sont intégrés dès le départ, même si leur usage complet arrive plus tard. Ils servent à éviter une restructuration lourde au moment de connecter le MVP au QAIC final.

### Gate de sortie

```text
✅ Dossier Drive créé avec `08_QAIC_BRIDGE/` et `09_WEB_APP_IDE/`
✅ Sheet DEV créé
✅ Docs de référence déposés
✅ Règles de sécurité produit validées
```

---

## 5. 📚 Phase 1 — Knowledge Base Lexique-first

### Objectif

Transformer le lexique Markdown en tables Google Sheets structurées.

### Durée indicative

`J1 à J3`

### Onglets à créer

| Onglet | Priorité | But |
|---|---:|---|
| `CONFIG` | P0 | Paramètres globaux |
| `KNOWLEDGE_TERMS` | P0 | Définitions consultables |
| `METHOD_LIBRARY` | P0 | Méthodes structurées |
| `SIGNAL_LIBRARY` | P0 | Signaux structurés |
| `RISK_PLAYBOOK` | P0 | TP / SL / sizing |
| `MARKET_REGIME_RULES` | P0 | Règles BTC risk-on/off |
| `VOLATILITY_RULES` | P0 | Règles tokens volatils |
| `CHECKLISTS` | P0 | Routines d’analyse |
| `DECISION_TEMPLATES` | P0 | Modèles de décisions |
| `GLOSSARY_TAGS` | P0 | Tags et catégories |

### Colonnes minimales recommandées

#### `KNOWLEDGE_TERMS`

```text
term_id
category
term
short_definition
full_definition
daily_use
risk_note
related_terms
tags
priority
source_section
status
updated_at
```

#### `METHOD_LIBRARY`

```text
method_id
method_name
market_context
entry_conditions
confirmation_signals
invalidations
tp_logic
sl_logic
best_timeframes
risk_level
tags
status
```

#### `SIGNAL_LIBRARY`

```text
signal_id
signal_type
signal_name
description
required_data
bullish_or_bearish
weight
false_signal_risk
action
related_methods
tags
status
```

#### `RISK_PLAYBOOK`

```text
profile
max_position_rule
sl_method
tp1_percent_sell
tp2_percent_sell
tp3_percent_sell
runner_percent
max_loss_rule
invalidation_rule
risk_warning
```

### Gate de sortie

```text
✅ Onglets P0 créés
✅ Colonnes validées
✅ Données lexique initiales importées ou préparées
✅ Tables lisibles et filtrables
✅ Aucun onglet inutile créé
```

---

## 6. ⚙️ Phase 2 — Apps Script Knowledge Engine

### Objectif

Rendre la Knowledge Base active avec menus, recherche, formatage et fonctions utilitaires.

### Durée indicative

`J3 à J5`

### Fonctions Apps Script à créer

```javascript
MVPQAIC_Setup()
MVPQAIC_Format_All()
MVPQAIC_SearchKnowledge(query)
MVPQAIC_GetTerm(termId)
MVPQAIC_GetMethod(methodId)
MVPQAIC_GetSignalsByProfile(profile)
MVPQAIC_GetRiskPlaybook(profile)
MVPQAIC_GenerateChecklist(session)
MVPQAIC_ExplainDecision(decisionCode)
MVPQAIC_Status()
```

### Règles techniques

- script complet, remplaçable intégralement ;
- batch read/write ;
- pas de scans globaux inutiles ;
- validations de données ;
- filtres ;
- freeze lignes/colonnes ;
- couleurs utiles ;
- logs compacts ;
- pas de trigger automatique au départ.

### Gate de sortie

```text
✅ Menu MVP QAIC disponible
✅ Setup exécutable
✅ Recherche lexique testée
✅ Formatage stable
✅ Aucun ordre automatique / broker / trigger sensible
```

---

## 7. 🌐 Phase 3 — Web App MVP rapide

### Objectif

Livrer rapidement une première Web App utilisable.

### Durée indicative

`J5 à J8`

### Option rapide recommandée

```text
Google Sheets + AppSheet
```

### Option alternative

```text
Apps Script Web App HTMLService
```

### Écrans prioritaires

| Écran | Source Sheet | Fonction |
|---|---|---|
| Knowledge Home | Plusieurs P0 | Accès aux blocs principaux |
| Search Term | `KNOWLEDGE_TERMS` | Recherche de termes |
| Term Detail | `KNOWLEDGE_TERMS` | Fiche détaillée |
| Method Detail | `METHOD_LIBRARY` | Méthode opérationnelle |
| Signal Library | `SIGNAL_LIBRARY` | Signaux filtrés |
| Risk Playbook | `RISK_PLAYBOOK` | Règles TP/SL |
| Daily Checklist | `CHECKLISTS` | Routine quotidienne |
| Decision Journal | `DECISION_JOURNAL` | Journaliser décision |

### Gate de sortie

```text
✅ Web App accessible
✅ Recherche utilisable
✅ Fiches méthodes lisibles
✅ Risk Playbook consultable
✅ Journal possible
✅ UX mobile acceptable
```

---

## 8. 🧮 Phase 4 — Scoring MVP léger

### Objectif

Ajouter un score explicable sans dépendre encore du QAIC final.

### Durée indicative

`J8 à J11`

### Onglets à ajouter

```text
TOKENS
MANUAL_ANALYSIS
SCORING_RULES
SCORES
DAILY_PLAN
```

### Décisions MVP

| Décision | Usage |
|---|---|
| `SETUP_STRONG_REVIEW` | Setup fort, revue humaine requise |
| `BUY_SMALL_REVIEW` | Petite taille possible après revue humaine |
| `WATCH` | Surveillance |
| `WEAK` | Faible qualité |
| `AVOID` | Éviter |
| `BLOCKED` | Bloqué par risque |

### Gate de sortie

```text
✅ Score /100 calculable
✅ Décision générée
✅ Explication générée
✅ Invalidation affichée
✅ Risk warning affiché
```

---

## 9. 📝 Phase 5 — Journal & Dashboard quotidien

### Objectif

Rendre l’outil utilisable dans une routine quotidienne.

### Durée indicative

`J11 à J14`

### Modules

| Module | Description |
|---|---|
| Daily Plan | Plan du jour |
| Decision Journal | Pourquoi analyser / attendre / éviter |
| Risk Warnings | Alertes risque |
| Score Explanation | Explication du score |
| Checklist Status | État de complétion |
| Looker Overview | Vue synthétique |

### Gate de sortie

```text
✅ Routine quotidienne possible
✅ Journal de décision utilisable
✅ Dashboard clair
✅ Aucun signal non expliqué
```

---

## 10. 🔌 Phase 6 — Préparation bridge QAIC final

### Objectif

Préparer les points d’entrée pour récupérer progressivement l’outil QAIC final.

### Durée indicative

`J14 à J18`

### Onglets bridge

```text
QAIC_OUTPUTS_IMPORT
QAIC_SCORE_MAPPING
QAIC_RISK_MAPPING
QAIC_DECISION_MAPPING
QAIC_BACKTEST_MAPPING
QAIC_INTEGRATION_LOG
```

### Outputs futurs à prévoir

```text
market_regime_score
alpha_score
risk_score
confidence_score
quality_score
decision_status
portfolio_warnings
backtest_status
attribution_summary
```

### Gate de sortie

```text
✅ Bridge non bloquant créé
✅ Le MVP fonctionne sans QAIC final
✅ Les mappings sont documentés
✅ Aucun couplage dur prématuré
```

---

## 11. 🧠 Phase 7 — Intégration progressive QAIC final

### Objectif

Brancher progressivement les outputs du QAIC final quand ils sont stables.

### Durée indicative

`Après stabilisation QAIC final`

### Ordre d’intégration recommandé

| Ordre | Output QAIC | Pourquoi |
|---:|---|---|
| 1 | `market_regime_score` | Impact direct sur décisions |
| 2 | `risk_score` | Sécurité et blocages |
| 3 | `alpha_score` | Scoring avancé |
| 4 | `confidence_score` | Qualité du signal |
| 5 | `backtest_status` | Validation historique |
| 6 | `attribution_summary` | Explicabilité avancée |
| 7 | `portfolio_warnings` | À traiter avec prudence, hors exécution |

### Gate de sortie

```text
✅ Un output QAIC intégré à la Web App
✅ Mapping validé
✅ Explication affichée
✅ Pas de trading automatique
✅ Journalisation des imports QAIC
```

---

## 12. 🎨 Stitch — Planning UI

### Objectif

Créer les maquettes de la Web App.

### Quand

À partir de `J5`, en parallèle de la Phase 3.

### Écrans Stitch

```text
Knowledge Home
Search Term
Term Detail
Method Detail
Signal Library
Risk Playbook
Daily Checklist
Decision Journal
Score Detail
QAIC Output Detail futur
```

### Gate de sortie

```text
✅ Design mobile-first
✅ Hiérarchie claire
✅ Risques visibles
✅ Aucun bouton d’exécution réelle
```

---

## 13. 🤖 Antigravity — Planning développement

### Objectif

Utiliser Antigravity uniquement sur des lots bornés.

### Lots possibles

| Lot Antigravity | Entrée | Sortie attendue |
|---|---|---|
| Parser lexique | Markdown lexique | Tables structurées |
| Setup Apps Script | Schéma Sheets | Script complet setup |
| Knowledge Engine | Tables P0 | Fonctions recherche |
| AppSheet spec | Tables stables | Spec écrans |
| QAIC bridge | Mapping défini | Tables + fonctions import |

### Interdiction

Ne pas demander à Antigravity :

```text
Crée toute l’app crypto complète.
```

Toujours donner :

- périmètre ;
- fichiers autorisés ;
- sorties attendues ;
- interdictions ;
- tests ;
- critères de validation.

---

## 14. 📅 Timeline synthétique

| Jour | Objectif | Livrable |
|---:|---|---|
| J0 | Foundation Drive | Dossier + docs |
| J1 | Sheet DEV | Base créée |
| J2 | Onglets P0 | Knowledge schema |
| J3 | Import lexique | Données initiales |
| J4 | Apps Script setup | Menu + format |
| J5 | Recherche | Knowledge Engine |
| J6 | AppSheet skeleton | Web App v0 |
| J7 | Écrans P0 | Recherche + fiches |
| J8 | Risk Playbook | TP/SL consultables |
| J9 | Journal | Décisions historisées |
| J10 | Scoring MVP | Score /100 |
| J11 | Dashboard | Vue quotidienne |
| J12 | Tests usage | Corrections UX |
| J13 | Looker simple | Dashboard visuel |
| J14 | MVP Review | Go/no-go |
| J15+ | QAIC bridge | Préparation transition |

---

## 15. ✅ Go-live MVP

Le MVP peut être considéré comme lancé si :

```text
✅ La Web App est accessible
✅ La recherche lexique fonctionne
✅ Les méthodes sont lisibles
✅ Les signaux sont filtrables
✅ Le Risk Playbook est utilisable
✅ Les checklists sont utilisables
✅ Le journal fonctionne
✅ Les décisions sont explicables
✅ Aucun ordre automatique n’existe
✅ La transition QAIC est prévue mais non bloquante
```

---

## 16. 🔁 Routine projet après lancement

### Hebdomadaire

```text
1. Revue des termes manquants
2. Revue des méthodes à structurer
3. Revue des signaux à transformer en règles
4. Revue UX Web App
5. Revue journal utilisateur
6. Revue éventuelle des outputs QAIC stables à intégrer
```

### Mensuel

```text
1. Export backup Drive
2. Changelog versionné
3. Audit des tables
4. Nettoyage des champs inutiles
5. Préparation éventuelle bridge QAIC suivant
```

---

## 17. 🎯 Conclusion planning

La priorité est nette :

```text
Livrer vite une Web App Lexique/Méthodes/Signaux.
```

Puis :

```text
Préparer calmement la récupération progressive du QAIC final.
```

Le MVP doit rester simple, utile, explicable et compatible avec l’avenir.


---

# 12. 🤖 Planning opérationnel Antigravity P0

## 12.1 Principe

Antigravity intervient **après cadrage documentaire** et **avant import Google**. Il produit des fichiers contrôlés dans un workspace local, puis l’humain valide avant dépôt Drive, import Sheets ou création AppSheet.

```text
Docs source validées
↓
Workspace local Antigravity
↓
Production P0-A / P0-B / P0-C / P0-D / P0-E
↓
Review humaine
↓
Import Drive / Sheets / AppSheet
```

## 12.2 Ordre des lots

| Ordre | Lot | Action | Validation avant suite |
|---:|---|---|---|
| 1 | `P0-A` | Parser le lexique en CSV + schéma | CSV propres, pas d’invention, IDs stables |
| 2 | `P0-B` | Générer Apps Script setup P0 | Script complet, pas destructif, formatage OK |
| 3 | `P0-C` | Générer spec AppSheet | Vues alignées sur tables P0 |
| 4 | `P0-D` | Générer prompts Stitch | Écrans Knowledge-first cohérents |
| 5 | `P0-E` | Générer placeholders QAIC Bridge | Mapping futur sans connexion réelle |

## 12.3 Planning court recommandé

| Jour | Lot | Objectif | Sortie |
|---:|---|---|---|
| J0 | Préparation | Créer workspace local et déposer sources | `MVP_QAIC/` prêt |
| J1 | `P0-A` | Knowledge Base CSV | `csv_seed/*.csv` + schéma |
| J2 | Review P0-A | Contrôle qualité des CSV | corrections / `VALIDATED` |
| J3 | `P0-B` | Apps Script setup | `.gs` complets |
| J4 | Test P0-B | Google Sheet DEV | onglets P0 formatés |
| J5 | `P0-C` | AppSheet spec | vues + actions |
| J6 | `P0-D` | Stitch prompts | écrans UI |
| J7 | `P0-E` | QAIC Bridge placeholders | specs mapping futur |

## 12.4 Stop conditions

Arrêter le batch Antigravity si :

- fichiers inattendus ou hors périmètre ;
- règles de trading inventées ;
- tentative de broker/exécution ;
- schéma trop large ou non AppSheet-friendly ;
- absence de manifest ;
- absence de statut `REVIEW_REQUIRED` sur les champs incertains ;
- proposition de BigQuery/Cloud Run prématurée ;
- suppression/renommage non demandé.

## 12.5 Prochaine action immédiate

Le prochain travail après cette mise à jour documentaire est :

```text
Préparer le pack de lancement Antigravity P0-A
```

Contenu attendu :

```text
ANTIGRAVITY_P0A_KNOWLEDGE_BASE_PROMPT_0.2.2.md
ANTIGRAVITY_P0A_ACCEPTANCE_CRITERIA_0.2.2.md
ANTIGRAVITY_P0A_WORKSPACE_TREE_0.2.2.md
```


---

## 18. 🧭 Planning P0-B6 — Gouvernance documentaire validée

> Cette section complète le planning `0.2.2` sans supprimer les phases initiales.

### 18.1 Jalons réalisés

| Ordre | Phase | Objectif | Statut |
|---:|---|---|---|
| 1 | `P0-A` | Knowledge Base CSV initiale | ✅ Fait |
| 2 | `P0-B` | Apps Script foundation | ✅ Fait |
| 3 | `P0-B2` | Expansion KB + prompts | ✅ Fait |
| 4 | `P0-B3` | Institutional readiness | ✅ Fait |
| 5 | `P0-B4` | GPT/Revolut X read-only bridge | ✅ Fait |
| 6 | `P0-B5` | Trade plan methods & trailing | ✅ Fait |
| 7 | `P0-B5.6` | Full Signal Mapping 50/50 | ✅ Fait |
| 8 | `P0-B6` | Docs / governance / runbook | ✅ Fait |
| 9 | `P0-C` | AppSheet MVP readiness | 🔜 Suivant |
| 10 | `P0-D` | Stitch UI prompts | Après P0-C |
| 11 | `P0-E` | QAIC bridge operational specs | Après premier usage AppSheet |
| 12 | `P1` | Journal + dashboards + QAIC response audit | Après MVP UI |

### 18.2 P0-C — AppSheet MVP Readiness

Livrables attendus :

```text
APPSHEET_SPEC_MVP_QAIC_0.3.2.md
APPSHEET_TABLES_AND_COLUMNS_0.3.2.md
APPSHEET_VIEWS_0.3.2.md
APPSHEET_ACTIONS_0.3.2.md
APPSHEET_SECURITY_AND_GUARDS_0.3.2.md
APPSHEET_TEST_PLAN_0.3.2.md
```

Vues prioritaires :

| Vue | Table principale | Objectif |
|---|---|---|
| 🏠 Home | CONFIG / synthèse | Accès rapide |
| 🔍 Search | KNOWLEDGE_TERMS | Recherche lexique |
| 📚 Term Detail | KNOWLEDGE_TERMS | Compréhension |
| 🧠 Methods | METHOD_LIBRARY | Méthodes |
| ⚡ Signals | SIGNAL_LIBRARY | Signaux |
| 🧮 Scores | SCORING_MODEL_SPEC / SIGNAL_EVALUATION_RULES | Explication |
| 🎯 Trade Plan | TRADE_PLAN_METHODS / TP_SL_CALCULATION_RULES | Plan sans exécution |
| 🛡️ Risk | RISK_PLAYBOOK / DECISION_MATRIX | Garde-fous |
| 🧾 Payloads | GPT_INPUT_PAYLOADS | Copie GPT |
| 📝 Journal | DECISION_JOURNAL | Décision humaine |

### 18.3 Stop conditions P0-C

Arrêter si :

```text
colonnes instables
décision ambiguë type Buy/Sell direct
bouton d’ordre réel
absence de garde-fou HUMAN_REVIEW_ONLY
absence de journal
```

---

## 🛠️ Addendum de réparation documentaire — 0.6.2 REAL FUSION REPAIR

> **Nature de cette version :** réparation de fusion documentaire réelle.
> Cette version **ne remplace pas par un résumé court** les documents de référence précédents. Elle reprend les documents sources validés, conserve leur structure, puis applique les décisions actées depuis la dernière mise à jour.

### Décisions actées intégrées

| Décision | Statut 0.6.2 | Règle corrigée |
|---|---|---|
| Recherche Lexique Master | Priorité immédiate P0 | Le MVP AppSheet doit d’abord rendre le lexique, les méthodes et les signaux consultables/recherchables. |
| Prompts 1 à 5 | Priorité immédiate P0/P1 | Les prompts deviennent le cœur opérationnel : sélection, copie vers Gem, réponse, intake, journalisation. |
| AppSheet MVP actuel | Validé comme AppShell manuel non déployé | 10 tables injectées, navigation OK, affinage UX ultérieur. |
| Portfolio Revolut X | À faire, non reporté | D’abord read-only, puis transition vers exécution contrôlée testée. |
| Ordres / achat / vente / TP / SL / trailing stop | Non exclus du MVP | Préparation, simulations et tests MVP autorisés ; exécution réelle interdite par défaut sans gates. |
| QAIC Python | Cible de transition | Préparer broker adapter, paper trading, dry-run, validations, logs, kill switch. |
| Sécurité | Permanente | HUMAN_REVIEW_ONLY par défaut, NO_AUTO_ORDER/NO_AUTO_SIZING/NO_BROKER_EXECUTION tant que les gates ne sont pas explicitement ouverts. |

### Correction importante

Les formulations anciennes du type “ne jamais coder d’exécution d’ordre” ou “automation exclue” sont remplacées par une règle plus précise :

```text
Interdit maintenant : exécution réelle non validée, ordre réel automatique, sizing réel automatique, secrets exposés, broker live sans architecture sécurisée.
Autorisé dans la trajectoire MVP : préparation fonctionnelle, maquette, tickets manuels, read-only portfolio, paper trading, dry-run, tests contrôlés, bridge QAIC Python.
```

---

## 📱 État AppSheet MVP validé au 2026-06-16

### Tables MVP injectées

| Table | Rôle | Statut |
|---|---|---|
| `SEARCH_COCKPIT` | Recherche lexique/méthodes/signaux | OK |
| `LEXIQUE_MASTER` | Source lexique principale | OK |
| `PROMPT_LEXIQUE_BRIDGE` | Bridge prompts ↔ lexique | REVIEW clé à améliorer |
| `PROMPT_CONTEXT_PACKS` | Packs contexte prompts | REVIEW clé/colonnes à améliorer |
| `PROMPT_LIBRARY` | Bibliothèque prompts | OK |
| `PROMPT_READY_TO_COPY` | Prompts prêts à copier | REVIEW clé à améliorer |
| `PROMPT_RUN_QUEUE` | Queue de run manuel | OK, `run_queue_id` clé |
| `RESPONSE_INTAKE_QUEUE` | Intake réponse Gem/GPT | OK, `intake_queue_id` clé |
| `JOURNAL_APPEND_QUEUE` | Pré-journalisation | OK, `journal_queue_id` clé |
| `DECISION_JOURNAL` | Journal officiel décisions | OK, `journal_id` clé |

### Vues MVP validées

| Vue | Source | Usage |
|---|---|---|
| `MVP QAIC Home` | `SEARCH_COCKPIT` | Accueil/recherche |
| `Lexique` | `LEXIQUE_MASTER` | Consultation lexique |
| `Prompts Ready` | `PROMPT_READY_TO_COPY` | Prompts prêts à copier |
| `Run Queue` | `PROMPT_RUN_QUEUE` | Flux manuel prompt → réponse |
| `Decision Journal` | `DECISION_JOURNAL` | Audit read-only |

### Règle AppSheet actuelle

```text
App non déployée.
Build manuel.
Pas d’automation AppSheet.
Pas d’action broker.
Pas d’ordre.
Pas de sizing.
Affinage UX après validation structurelle.
```

---

## 💼 Portfolio Revolut X & transition exécution contrôlée

### Priorité produit

Le portefeuille Revolut X n’est **pas reporté hors trajectoire**. Il est intégré comme axe prioritaire après stabilisation du socle Lexique/Prompts/Journal.

| Niveau | Fonction | Autorisation |
|---:|---|---|
| 1 | Consultation portfolio Revolut X | Read-only |
| 2 | Analyse exposition/risque | Read-only + prompts |
| 3 | Alertes portefeuille | Notification / review only |
| 4 | Tickets manuels | Préparation d’action humaine |
| 5 | Paper trading | Simulation contrôlée |
| 6 | Dry-run broker | Test sans ordre réel |
| 7 | Exécution réelle assistée | Uniquement après gates séparés |
| 8 | TP/SL/trailing automatique | Uniquement après architecture QAIC Python sécurisée |

### Ce qui doit être construit progressivement

```text
Portfolio Revolut X read-only
→ Prompt 1 Portfolio Analysis
→ Prompt 5 Full Trading Review
→ Risk Gate
→ Alert Center
→ Manual Trade Ticket
→ Paper Trading
→ Dry-run Broker Adapter
→ QAIC Python Broker Adapter
→ Exécution live seulement après GO explicite, kill switch, logs, secrets sécurisés et validations.
```

### Garde-fous obligatoires

| Domaine | Garde-fou |
|---|---|
| Secrets | Secret Manager / jamais dans Sheets / Apps Script / Drive |
| Exécution | Kill switch visible et testé |
| Données | Vérification freshness, source, prix, PRU, quantité, exposition |
| Risque | Max exposure, concentration, NO_ADD, REDUCE_RISK_REVIEW, BLOCK |
| Logs | Journal immuable / run_id / timestamp / payload_id |
| Validation humaine | Human approval avant tout ordre réel |
| Tests | Paper trading puis dry-run avant live |

---


---

## 12. 📱 Phase P5 — AppSheet MVP réel validé manuellement

| Lot | Objectif | Statut |
|---|---|---|
| P5A à P5G | WebApp readiness, schema contract, navigation, blueprint, go/no-go | Réalisé |
| P5H à P5J | Plan réparation schema, dry-run evidence, preflight, apply guarded | Réalisé |
| P5K à P5N | Handoff pack, runbook build manuel | Réalisé |
| P5O/P5P | Post-build validation et evidence closure | En attente résultats humains |

### Tables MVP AppSheet à maintenir

```text
SEARCH_COCKPIT
LEXIQUE_MASTER
PROMPT_LEXIQUE_BRIDGE
PROMPT_CONTEXT_PACKS
PROMPT_LIBRARY
PROMPT_READY_TO_COPY
PROMPT_RUN_QUEUE
RESPONSE_INTAKE_QUEUE
JOURNAL_APPEND_QUEUE
DECISION_JOURNAL
```

### Prochaine priorité opérationnelle

```text
1. Affiner UX Lexique / Prompts / Journal
2. Ajouter Daily Review / Prompt Launcher 1–5
3. Ajouter Portfolio Revolut X read-only
4. Ajouter Alert Center
5. Ajouter Manual Trade Tickets
6. Ajouter Paper Trading
7. Ajouter Dry-run broker adapter QAIC Python
8. Tester transition TP/SL/trailing stop en simulation
```

---

## 13. 💼 Phase Portfolio / Broker Transition — MVP testable, non live par défaut

| Phase | Objectif | Gate |
|---:|---|---|
| B0 | Portfolio Revolut X read-only | Source fiable + aucune écriture broker |
| B1 | Prompt 1 Portfolio Analysis | Données portfolio complètes |
| B2 | Prompt 5 Daily Full Review | Market + portfolio + data quality |
| B3 | Alert Center | Alertes sans exécution |
| B4 | Manual Trade Ticket | Validation humaine |
| B5 | Paper trading | Simulation |
| B6 | Dry-run broker | Zéro ordre réel |
| B7 | Live assisted execution | GO explicite séparé + kill switch + secrets sécurisés |
| B8 | TP/SL/trailing automation | Projet durci QAIC Python / backend |

---
---

# ✅ FUSION 0.7.2 — Scope Split MVP / QAIC Engine

> **Patch fusionnel ajouté au document original complet**
> **Projet :** 🛠️ MVP QAIC — Crypto Signal OS
> **Version fusionnée :** `0.7.2_REAL_FULL_SOURCE_FUSION_SCOPE_SPLIT`
> **Date :** 2026-06-20
> **Statut :** `READY_FOR_HUMAN_REVIEW_NON_DESTRUCTIVE`
> **Méthode :** contenu original 0.6.2 conservé intégralement, puis correction de doctrine ajoutée sans suppression.

## 0. Décision de programme validée

```text
MVP QAIC = Lexique / méthodes / signaux / Knowledge Base / WebApp pédagogique
QAIC = moteur calcul, trading analytics, portefeuille, risk engine, Revolut API
```

## 1. Correction de doctrine à appliquer à ce document

Toute mention historique du type :

```text
Portfolio Revolut X dans MVP
Revolut API dans MVP
QAIC Python broker adapter dans MVP
paper trading / dry-run / execution contrôlée dans MVP
scoring trading final dans MVP
risk engine portfolio dans MVP
```

doit être lue comme :

```text
Ces éléments relèvent de QAIC Engine.
Le MVP ne conserve que l'explication pédagogique, l'affichage contrôlé, les mappings et les contrats d'import des sorties QAIC.
```

## 2. Frontière officielle

| Domaine | Responsable officiel |
|---|---|
| Lexique crypto | MVP |
| Méthodes / signaux expliqués | MVP |
| WebApp privée / search cockpit | MVP |
| Knowledge Base / source registry | MVP |
| Journal human review pédagogique | MVP |
| Affichage de sorties QAIC | MVP via import contrôlé |
| Calculs trading | QAIC |
| Portefeuille / exposition | QAIC |
| Revolut API | QAIC |
| Risk engine final | QAIC |
| Broker adapter / dry-run / exécution future | QAIC, hors MVP |

## 3. Règles non négociables MVP

```text
NO_REVOLUT_API_IN_MVP = TRUE
NO_TRADING_ENGINE_IN_MVP = TRUE
NO_PORTFOLIO_ENGINE_IN_MVP = TRUE
NO_ORDER_IN_MVP = TRUE
NO_SIZING_IN_MVP = TRUE
NO_BROKER_EXECUTION_IN_MVP = TRUE
NO_SECRET_IN_MVP = TRUE
HUMAN_REVIEW_ONLY = TRUE
```

## 4. Ce qui reste autorisé dans le MVP

```text
- expliquer les concepts trading ;
- documenter Night Watch / trade nocturne comme méthode pédagogique ;
- afficher un output QAIC importé en lecture contrôlée ;
- journaliser la décision humaine ;
- montrer missing_data / blockers / source provenance ;
- relier une fiche lexique à un output QAIC par référence.
```

## 5. Ce qui est transféré à QAIC

```text
- Revolut provider Python ;
- API keys / signatures / secrets ;
- calculs de portefeuille ;
- calculs de signaux ;
- scoring trading officiel ;
- risk engine trading ;
- dry-run / paper trading / broker adapter ;
- toute exécution future, même contrôlée.
```

## 6. Impact spécifique sur `PLANNING`

Ce document reste source valide pour son contenu historique et structurel, mais ses passages liés à Revolut, portfolio, broker, paper trading, dry-run ou calcul trading sont **superseded** par cette correction 0.7.2.

```text
MVP_SCOPE = LEXIQUE_KB_WEBAPP_ONLY
QAIC_SCOPE = CALC_TRADING_REVOLUT_ENGINE
QAIC_BRIDGE_IN_MVP = OUTPUT_IMPORT_AND_DISPLAY_ONLY
```

## Source 12: `docs/FINAL/fusion_inbox_R6/RUNBOOK/RUNBOOK_MVP_QAIC_P1G_PROMPT_LIBRARY_CONTRACT_0.6.0.md`

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
