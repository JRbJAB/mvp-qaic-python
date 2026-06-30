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
