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
