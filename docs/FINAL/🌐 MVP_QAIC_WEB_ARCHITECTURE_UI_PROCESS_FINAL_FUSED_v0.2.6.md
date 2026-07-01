# MVP QAIC Web Architecture UI Process Final Fused v0.2.6
- Version: v0.2.6
- Status: FINAL_REFERENCE_READY_HUMAN_REVIEW
- Generated: 20260630_200005
- Mode: residual final docs fusion / no live broker / no delete
## Intent
Canonical web architecture, UI transition, Reflex/AppSheet and frontend process reference.
## Scope and safety
- This document consolidates the selected R6 fusion inbox and residual final-doc sources.
- Older source files are not deleted. Superseded material remains traceable through R5/R6/R7/R8/R9 reports.
- Google Drive cleanup is limited to archive moves; no content was deleted.
- This is a reference document for human review and implementation continuity.

## Source manifest
1. `docs/FINAL/fusion_inbox_R6/ARCHITECTURE/🧠 DECISION_JOURNAL_USAGE_AND_PROMPT_IMPROVEMENT_LOOP_0.4.6.md` (1183 bytes, sha256 `c43d2c50957cece3...`)
2. `docs/FINAL/fusion_inbox_R6/ARCHITECTURE/🧱 ARCHITECTURE_MVP_QAIC_LEXIQUE_FIRST_0.7.2_REAL_FULL_SOURCE_FUSION.md` (8554 bytes, sha256 `633070d246dbabb9...`)
3. `docs/FINAL/fusion_inbox_R6/ARCHITECTURE/🧱 ARCHITECTURE_MVP_QAIC_LEXIQUE_FIRST_APPSHEET_QAIC_PYTHON_0.6.2.md` (5112 bytes, sha256 `13ccb01776ce5724...`)
4. `docs/FINAL/fusion_inbox_R6/CDC/📘 CDC_MVP_QAIC_WEB_APP_LEXIQUE_FIRST_0.6.2_REAL_FUSION_REPAIR.md` (27670 bytes, sha256 `00f3d38c78243036...`)
5. `docs/FINAL/fusion_inbox_R6/CDC/📘 CDC_MVP_QAIC_WEB_APP_LEXIQUE_FIRST_0.7.2_REAL_FULL_SOURCE_FUSION.md` (31100 bytes, sha256 `c5d63c4b023d7671...`)
6. `docs/FINAL/fusion_inbox_R6/INSTRUCTIONS/INSTRUCTIONS_UI_IMPERATIVE_MVP_QAIC_1.0.2.md` (1733 bytes, sha256 `babd2b74b1c0ab4d...`)
7. `docs/FINAL/fusion_inbox_R6/MANIFEST/MANIFEST_MVP_QAIC_INSTRUCTIONS_0.5.0_UI_FULL_FUSION.md` (1543 bytes, sha256 `b0e8bb665825cf38...`)
8. `docs/FINAL/fusion_inbox_R6/PLANNING/🗓️ PLANNING_MVP_QAIC_WEB_APP_TRANSITION_QAIC_0.6.2_REAL_FUSION_REPAIR.md` (26933 bytes, sha256 `6904e0a495e1789f...`)
9. `docs/FINAL/fusion_inbox_R6/PLANNING/🗓️ PLANNING_MVP_QAIC_WEB_APP_TRANSITION_QAIC_0.7.2_REAL_FULL_SOURCE_FUSION.md` (30379 bytes, sha256 `8aae0ef0fba8e5e1...`)
10. `docs/FINAL/fusion_inbox_R6/README/README_MVP_QAIC_P2C_FRONTEND_RENAME_SAFE_FALLBACKS_0.8.0.md` (1110 bytes, sha256 `5492a5ef5deef576...`)
11. `docs/FINAL/fusion_inbox_R6/README/README_MVP_QAIC_P2L_JOURNAL_UI_AND_INSTRUCTIONS_1.0.2_SAFE.md` (722 bytes, sha256 `8ec63bf3951f3670...`)
12. `docs/FINAL/fusion_inbox_R6/README/README_P2C_FRONTEND_RENAME_CORRECTED.md` (974 bytes, sha256 `9df40fa90f1b900b...`)
13. `docs/FINAL/fusion_inbox_R6/RUNBOOK/RUNBOOK_MVP_QAIC_P2T_FINAL_CLEAN_UI_BEFORE_REPROCESS_1.1.0_SAFE.md` (1513 bytes, sha256 `6f0901dbb5ddb5ee...`)
14. `docs/FINAL/fusion_inbox_R6/RUNBOOK/🧭 RUNBOOK_MVP_QAIC_APPSHEET_MANUAL_BUILD_0.6.2.md` (2234 bytes, sha256 `144c6477df530f5b...`)
15. `docs/FINAL/fusion_inbox_R6/README/README_MVP_QAIC_P3E_RISK_PLAYBOOK_POSITION_ACTION_SIMPLE_APPLY_1.4.5_SAFE.md` (1488 bytes, sha256 `729ec3d08a6faa77...`)

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

## Source 2: `docs/FINAL/fusion_inbox_R6/ARCHITECTURE/🧱 ARCHITECTURE_MVP_QAIC_LEXIQUE_FIRST_0.7.2_REAL_FULL_SOURCE_FUSION.md`

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

## Source 3: `docs/FINAL/fusion_inbox_R6/ARCHITECTURE/🧱 ARCHITECTURE_MVP_QAIC_LEXIQUE_FIRST_APPSHEET_QAIC_PYTHON_0.6.2.md`

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

## Source 6: `docs/FINAL/fusion_inbox_R6/INSTRUCTIONS/INSTRUCTIONS_UI_IMPERATIVE_MVP_QAIC_1.0.2.md`

# 🧭 Instructions impératives UI — MVP QAIC — 1.0.2

## Statut
`MANDATORY_UI_STANDARD_ACTIVE`

## Règle permanente
Chaque onglet visible du MVP QAIC doit être un cockpit opérationnel lisible, pas une table brute.

## Obligatoire pour chaque onglet visible
- Colonnes essentielles à gauche, audit/détails à droite.
- Hauteur de ligne forcée compacte pour les lignes simples : `24 px` par défaut.
- Textes longs en `CLIP`, pas en wrap massif qui gonfle les lignes.
- Largeurs de colonnes maîtrisées par script.
- Freeze utile, limité, sans bloquer la navigation horizontale.
- Filtres activés sur la ligne d’en-tête utile.
- Couleurs métier cohérentes : OK vert, REVIEW orange, BLOCKED/INVALID rouge, informations bleu/gris.
- Zéro ligne blanche décorative.
- Aucun nouvel onglet UI sans nécessité démontrée.
- Toute fonction qui crée, rafraîchit ou modifie un onglet visible doit appeler son formatteur UI en dernier.

## Onglets prioritaires actuels
- `🧪 GPT_RESPONSE_INTAKE` : cockpit de test Gem/GPT.
- `🧾 DECISION_JOURNAL` : journal officiel, ouvert automatiquement après journalisation.
- `🧭 PROMPT_IMPROVEMENT_QUEUE` : lecture prioritaire du `next_prompt_draft`.
- `📘 PROMPT_LIBRARY` : lecture prioritaire de `prompt_template_to_copy`.

## Règle spéciale DECISION_JOURNAL
`MVPQAIC_JournalAppendFromIntake()` doit :
1. bloquer les lignes incomplètes ;
2. ajouter une ligne complète uniquement ;
3. appliquer l’ergonomie ultime ;
4. ouvrir automatiquement `🧾 DECISION_JOURNAL` sur la ligne ajoutée.

## Règle spéciale mémoire projet
Cette règle UI est prioritaire pour tous les futurs scripts MVP QAIC / QAIC / QAIT : pas de livraison “fonctionnelle mais illisible”.

## Source 7: `docs/FINAL/fusion_inbox_R6/MANIFEST/MANIFEST_MVP_QAIC_INSTRUCTIONS_0.5.0_UI_FULL_FUSION.md`

# 📦 MANIFEST — MVP QAIC Instructions 0.5.0 UI Full Fusion

> **Projet :** 🛠️ MVP QAIC — Crypto Signal OS Web App  
> **Version :** `MVP_QAIC_INSTRUCTIONS_0.5.0_UI_FULL_FUSION_AND_SMART_CONSOLIDATION`  
> **Date :** 2026-06-12  
> **Statut :** `READY_FOR_DRIVE_REVIEW`  

## Fichiers finaux

```text
docs/🚀 INSTRUCTIONS_PROJET_MVP_QAIC_0.5.0_UI_FULL_FUSION_AND_SMART_CONSOLIDATION.md
docs/VERSION_COURTE_PROJET_CHATGPT_MVP_QAIC_0.5.0.md
docs/CHANGELOG_MVP_QAIC_INSTRUCTIONS_0.5.0.md
docs/VALIDATION_MVP_QAIC_INSTRUCTIONS_0.5.0.md
docs/README_MVP_QAIC_INSTRUCTIONS_0.5.0.md
```

## Sources fusionnées

```text
source/🚀 INSTRUCTIONS_PROJET_MVP_QAIC_0.4.9_CURATED_BATCH_DEV_GOVERNANCE_FULL_FUSION.md
source/INSTRUCTIONS_UI_IMPERATIVE_MVP_QAIC_1.0.2.md
source/VERSION_COURTE_PROJET_CHATGPT_MVP_QAIC_0.4.9.md
```

## Décision de gouvernance

Cette livraison est une **full fusion** : les règles UI impératives ne restent pas en addendum séparé. Elles sont intégrées dans le master instructions `0.5.0` à la section `21B`.

## Règles ajoutées

```text
fusion intelligente obligatoire avec l’existant
pas d’addendum isolé si full fusion attendue
pas de script doublon si responsabilité déjà couverte
UI cockpit obligatoire pour tout onglet visible
hauteur compacte forcée 24 px
largeurs maîtrisées
WrapStrategy.CLIP pour textes longs
formatteur UI appelé en dernier
DECISION_JOURNAL ouvert après append
PROMPT_IMPROVEMENT_QUEUE ouvert après boucle qualité
PROMPT_LIBRARY ouvert après application draft
```

## Source 8: `docs/FINAL/fusion_inbox_R6/PLANNING/🗓️ PLANNING_MVP_QAIC_WEB_APP_TRANSITION_QAIC_0.6.2_REAL_FUSION_REPAIR.md`

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

## Source 9: `docs/FINAL/fusion_inbox_R6/PLANNING/🗓️ PLANNING_MVP_QAIC_WEB_APP_TRANSITION_QAIC_0.7.2_REAL_FULL_SOURCE_FUSION.md`

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

## Source 10: `docs/FINAL/fusion_inbox_R6/README/README_MVP_QAIC_P2C_FRONTEND_RENAME_SAFE_FALLBACKS_0.8.0.md`

# 🛠️ MVP QAIC — P2-C Frontend Rename Safe Fallbacks — 0.8.0

## Version
`MVP_QAIC_P1_PROMPT_QUALITY_CORE_0.8.0_FRONTEND_RENAME_SAFE_FALLBACKS`

## Objectif
Renommer proprement les onglets frontend prompt avec emoji, sans suppression ni écrasement, et avec compatibilité old/new names dans le core prompt.

## Renommages prévus
- `DECISION_JOURNAL` → `🧾 DECISION_JOURNAL`
- `GPT_QUALITY_DASHBOARD` → `📊 GPT_QUALITY_DASHBOARD`
- `PROMPT_IMPROVEMENT_QUEUE` → `🧭 PROMPT_IMPROVEMENT_QUEUE`
- `PROMPT_LIBRARY` → `📘 PROMPT_LIBRARY`

## Fonctions P2-C
```javascript
MVPQAIC_FrontendRenameStatus()
MVPQAIC_FrontendRenameDryRun()
MVPQAIC_FrontendRenameApplySafe()
```

## Garde-fous
- Dry-run disponible avant apply.
- Apply bloqué si old et new existent en même temps.
- Aucun delete.
- Aucun overwrite.
- Aucun trigger/menu mutation.
- Fallback old/new actif dans le core prompt.

## Ordre conseillé
```javascript
MVPQAIC_FrontendRenameStatus()
MVPQAIC_FrontendRenameDryRun()
MVPQAIC_FrontendRenameApplySafe()
MVPQAIC_PromptQualityCoreStatus()
MVPQAIC_PromptAdaptiveLoopStatus()
```

## Source 11: `docs/FINAL/fusion_inbox_R6/README/README_MVP_QAIC_P2L_JOURNAL_UI_AND_INSTRUCTIONS_1.0.2_SAFE.md`

# MVP QAIC P2-L — Journal UI & Instructions 1.0.2 SAFE

## Fichiers
- `scripts/mvpqaic_23_gpt_response_intake_core.gs`
- `docs/INSTRUCTIONS_UI_IMPERATIVE_MVP_QAIC_1.0.2.md`

## À remplacer
Remplacer uniquement :
`mvpqaic_23_gpt_response_intake_core.gs`

## Fonctions utiles
- `MVPQAIC_JournalAppendFromIntake()` : journalise puis ouvre `🧾 DECISION_JOURNAL`.
- `MVPQAIC_JournalFormatUltimate()` : applique / réapplique l’ergonomie ultime du journal.
- `MVPQAIC_JournalMarkIncompleteAppends()` : marque les lignes incomplètes existantes sans suppression.

## Sécurité
- No delete.
- No hide.
- No trigger.
- No menu mutation.
- No broker/order/sizing/secret.
- Journal append bloqué si champs essentiels vides.

## Source 12: `docs/FINAL/fusion_inbox_R6/README/README_P2C_FRONTEND_RENAME_CORRECTED.md`

# 🛠️ MVP QAIC — P2-C Frontend Rename Corrected Standalone

## Statut
SAFE_CORRECTED — ne pas utiliser le pack précédent `MVP_QAIC_P2C_FRONTEND_RENAME_SAFE_FALLBACKS_0.8.0_SAFE`.

## Correction de responsabilité
- `mvpqaic_11_p1_prompt_quality_core.gs` reste le core prompt.
- Il reçoit seulement la compatibilité old/new names.
- Les fonctions de renommage sont dans `mvpqaic_22_frontend_sheet_rename_migration_core.gs`.

## Ordre
1. Installer `mvpqaic_11_p1_prompt_quality_core.gs` version alias-only.
2. Installer `mvpqaic_22_frontend_sheet_rename_migration_core.gs`.
3. Lancer `MVPQAIC_FrontendRenameMigrationStatus()`.
4. Lancer `MVPQAIC_FrontendRenameMigrationDryRun()`.
5. Si clean, lancer `MVPQAIC_FrontendRenameMigrationApplySafe()`.
6. Contrôler `MVPQAIC_PromptQualityCoreStatus()` et `MVPQAIC_PromptAdaptiveLoopStatus()`.

## Safety
No delete, no hide, no overwrite, no menu mutation, no trigger mutation, no broker, no order, no sizing, no secret.

## Source 13: `docs/FINAL/fusion_inbox_R6/RUNBOOK/RUNBOOK_MVP_QAIC_P2T_FINAL_CLEAN_UI_BEFORE_REPROCESS_1.1.0_SAFE.md`

# 🛠️ MVP QAIC — P2-T Final Clean UI Before Reprocess — 1.1.0

## Statut
`SAFE_READY_FOR_INSTALL`

## Scripts à remplacer
- `scripts/mvpqaic_11_p1_prompt_quality_core.gs`
- `scripts/mvpqaic_23_gpt_response_intake_core.gs`

## Objectif
Finaliser les trois onglets avant de relancer un nouveau cycle Gem depuis une base propre :

- `🧭 PROMPT_IMPROVEMENT_QUEUE`
  - ajoute `ai_runtime_name` entre `prompt_id` et `next_prompt_draft` ;
  - fige le bloc `backlog_id / prompt_id / ai_runtime_name` ;
  - conserve `next_prompt_draft` visible immédiatement après ;
  - force hauteurs compactes + CLIP.

- `🧾 DECISION_JOURNAL`
  - `test_datetime` en heure de Paris ;
  - `journal_id`, `payload_id`, `test_datetime` en colonnes compactes ;
  - `ai_runtime_name` placé entre `test_datetime` et `prompt_id` ;
  - forçage des hauteurs sur toutes les lignes de la grille ;
  - CLIP sur toutes les cellules.

- `📘 PROMPT_LIBRARY`
  - `ai_runtime_name` placé entre `contract_id` et `prompt_id` ;
  - ajout `cleanup_action` et `cleanup_reason` pour identifier les lignes à garder / archiver / revoir ;
  - conservation des prompts références verrouillés et des variantes ;
  - aucune suppression.

## Fonctions à lancer après remplacement

```javascript
MVPQAIC_JournalFormatUltimate()
MVPQAIC_PromptWorkflowSheetsOptimize()
```

## Garde-fous
- Aucune suppression.
- Aucun trigger/menu.
- Aucun broker/order/sizing.
- `PROMPT_LIBRARY` : nettoyage signalé par colonnes, pas appliqué automatiquement.

## Source 14: `docs/FINAL/fusion_inbox_R6/RUNBOOK/🧭 RUNBOOK_MVP_QAIC_APPSHEET_MANUAL_BUILD_0.6.2.md`

# 🧭 Runbook — MVP QAIC AppSheet & contrôles manuels — 0.6.2 REAL FUSION REPAIR

> **Statut :** `DRAFT_FOR_HUMAN_VALIDATION`  
> **Mode :** `HUMAN_REVIEW_ONLY`  
> **AppSheet :** build manuel non déployé.

## 1. Contrôle Data / Tables

| Table | Permission cible | Delete | Statut |
|---|---|---|---|
| SEARCH_COCKPIT | Read-only | OFF | OK |
| LEXIQUE_MASTER | Read-only | OFF | OK |
| PROMPT_LEXIQUE_BRIDGE | Read-only | OFF | REVIEW clé |
| PROMPT_CONTEXT_PACKS | Read-only | OFF | REVIEW clé/colonnes |
| PROMPT_LIBRARY | Read-only | OFF | OK |
| PROMPT_READY_TO_COPY | Read-only | OFF | REVIEW clé |
| PROMPT_RUN_QUEUE | Adds/updates contrôlés | OFF | OK |
| RESPONSE_INTAKE_QUEUE | Adds/updates contrôlés | OFF | OK |
| JOURNAL_APPEND_QUEUE | Adds/updates contrôlés ou read-only selon test | OFF | OK |
| DECISION_JOURNAL | Read-only | OFF | OK |

## 2. Contrôle UX / Views

| Vue | Source | Check |
|---|---|---|
| MVP QAIC Home | SEARCH_COCKPIT | Recherche visible |
| Lexique | LEXIQUE_MASTER | Consultation terme/méthode/signal |
| Prompts Ready | PROMPT_READY_TO_COPY | Prompt copiable |
| Run Queue | PROMPT_RUN_QUEUE | Prompt + réponse visible |
| Decision Journal | DECISION_JOURNAL | Audit read-only |

## 3. Contrôle workflow manuel

| Étape | Action | Résultat attendu |
|---|---|---|
| 1 | Ouvrir Run Queue | prompt_to_copy visible |
| 2 | Copier prompt | Envoi manuel vers Gem/ChatGPT |
| 3 | Coller réponse | Response Intake / champ réponse |
| 4 | Revue blockers | Missing data et blockers visibles |
| 5 | Journaliser | Decision Journal read-only après append |

## 4. Contrôle futur Portfolio/Broker

| Étape | Autorisé maintenant | Autorisé plus tard |
|---|---|---|
| Portfolio Revolut X read-only | Oui, à construire | Oui |
| Alertes risque | Oui | Oui |
| Manual Trade Ticket | Oui | Oui |
| Paper trading | Préparation | Oui |
| Dry-run broker | Non AppSheet / oui QAIC Python futur | Oui après gates |
| Ordre réel | Non | Seulement projet séparé gated |
| TP/SL/trailing live | Non | Seulement QAIC Python/backend sécurisé |

## 5. Réponse obligatoire si blocker

```text
BLOCKED / REVIEW_REQUIRED
missing_data = ...
blockers = ...
no_order_no_sizing = TRUE
```

## Source 15: `docs/FINAL/fusion_inbox_R6/README/README_MVP_QAIC_P3E_RISK_PLAYBOOK_POSITION_ACTION_SIMPLE_APPLY_1.4.5_SAFE.md`

# 🛠️ MVP QAIC — P3-E Risk Playbook Position Action Simple Apply — 1.4.5 SAFE

## Objectif

Résoudre le blocage `BLOCKED_TARGET_HEADER_NOT_FOUND` sur les 10 lignes approuvées `RISK_PLAYBOOK!position_action`.

## Cause

`🧪 LEXIQUE_GAP_AUDIT` pointe vers `RISK_PLAYBOOK.position_action`, mais la colonne `position_action` n’existe pas encore dans la table source `RISK_PLAYBOOK`.

## Solution simple

- créer uniquement la colonne source manquante `position_action` dans `RISK_PLAYBOOK` si elle n’existe pas ;
- appliquer uniquement les lignes déjà marquées `review_decision = APPROVE_APPLY` ;
- écrire uniquement dans les cellules vides ;
- ne jamais écrire directement dans `📚 LEXIQUE_MASTER` ;
- reconstruire `📚 LEXIQUE_MASTER` et `🔎 SEARCH_COCKPIT` seulement si au moins une ligne est appliquée.

## Fonctions

```javascript
MVPQAIC_P3E_RiskPlaybookPositionActionStatus()
MVPQAIC_P3E_RiskPlaybookPositionActionDryRun()
MVPQAIC_P3E_RiskPlaybookPositionActionApplySafe()
```

## Séquence recommandée

```javascript
MVPQAIC_P3E_RiskPlaybookPositionActionStatus()
MVPQAIC_P3E_RiskPlaybookPositionActionDryRun()
MVPQAIC_P3E_RiskPlaybookPositionActionApplySafe()
```

Puis relancer l’audit :

```javascript
MVPQAIC_P3A_LexiqueExistingGapAuditRun()
```

## Sécurité

- HUMAN_REVIEW_ONLY
- NO broker / order / sizing
- NO secret
- NO delete / hide / menu / trigger mutation
- NO generated master direct apply
- no overwrite
- applies only `APPROVE_APPLY`

<!-- R16F2H6_PROCESS_LOCK_START -->
## 🛠️ R16F2H6 — Reflex runtime/process live lock

Live version: v0.2.7  
Policy ID: `R16F2H4_REFLEX_RUNTIME_POLICY_LOCK`  
Readiness Policy ID: `R16F2H6_REFLEX_READINESS_ANTI_LOOP_POLICY`  
Updated: 2026-06-30 23:41:31 UTC

Validated process now locked:

- Reflex-only runtime preview.
- Docker pinned preview with full tracked HEAD copy outside repo.
- Container ports `3000/8000`; Windows preview ports `3055/8055`.
- Mandatory `REFLEX_POLICY_GUARD_OK=True` and `REFLEX_READINESS_POLICY_GUARD_OK=True` before future runners.
- Anti-loop readiness: max wait, max two identical log tails, internal/host port diagnostic, stop container on failure.
- Reference `.md` generated for validated technical process.
- Relevant `docs/FINAL` deliverables updated through marked fusion blocks.
- Transient logs/reports remain in `_RUN_REPORTS`; FINAL receives only promoted reference content.
<!-- R16F2H6_PROCESS_LOCK_END -->

<!-- R16F2H7I_RUNNER_HARDENING_START -->
## 🧱 R16F2H7I — Runner hardening process lock

Policy ID: `R16F2H7I_REFLEX_RUNNER_HARDENING_PROCESS_LOCK`
Context: MVP QAIC web architecture UI process final fused

### Règles obligatoires pour tout runner futur

- aucun runner sans timeout dur sur chaque sous-commande native.
- aucun docker run sans image preflight.
- aucun docker run sans port preflight.
- aucun docker exec si container non running.
- aucune full copy avec Copy-Item fichier par fichier.
- aucun ZIP sans self-check de structure.
- aucun rapport transitoire dans docs/.

### Contrat d'exécution

- Toute sous-commande native doit être appelée avec timeout dur, sortie capturée, exit code contrôlé.
- `docker run` doit être précédé d'un contrôle image pinned + contrôle ports host.
- `docker exec` est interdit si le container n'est pas `running`.
- La copie full HEAD doit utiliser `git archive HEAD` + extraction tar, jamais `Copy-Item` fichier par fichier.
- Chaque ZIP livré doit contenir un self-check de structure avant action réelle.
- Les rapports de run et diagnostics transitoires vont sous `_RUN_REPORTS`, jamais sous `docs/`.
- Les docs de référence et docs FINAL ne reçoivent que du contenu validé/fusionné.

### Guards requis

- `REFLEX_POLICY_GUARD_OK=True`
- `REFLEX_READINESS_POLICY_GUARD_OK=True`
- `REFLEX_RUNNER_HARDENING_POLICY_GUARD_OK=True`
<!-- R16F2H7I_RUNNER_HARDENING_END -->

