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
