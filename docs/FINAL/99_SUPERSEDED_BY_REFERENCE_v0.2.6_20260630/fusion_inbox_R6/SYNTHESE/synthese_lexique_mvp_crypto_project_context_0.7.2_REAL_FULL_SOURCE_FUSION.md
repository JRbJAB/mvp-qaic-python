<!--
REAL FULL SOURCE FUSION 0.7.2
Source original preserved: synthese_lexique_mvp_crypto_project_context.md
Source SHA256: 162b1fe04cf02a56394d0d2f54b4cd6d8f9817c52391a63cf0ee22a5f9c6f5bf
Source lines: 520
Fusion rule: original content is kept, then a scope-split correction block is appended.
No Drive overwrite. No Apps Script run. No clasp push.
-->

# 📚🚀 Synthèse Projet Crypto — Lexique & MVP uniquement

> **Objectif du document :** fournir une synthèse propre, exploitable et prête à intégrer dans un Projet ChatGPT, centrée uniquement sur la partie **Lexique Crypto Méthodes & Signaux Trading Pro** et **Architecture MVP Crypto Lexique-first**.  
> Cette synthèse exclut volontairement la partie portefeuille, positions, achats/ventes et suivi de marché personnel.

---

## 1. 🎯 Vision du projet

Le projet vise à construire un outil crypto quotidien nommé provisoirement :

# 🚀📊 Crypto Signal OS — Lexique-first MVP

L’objectif est de transformer un **lexique crypto professionnel** en **outil fonctionnel de support à la décision**, utilisable dès le début du développement.

Le MVP doit commencer par une base de connaissance solide, structurée et exploitable, avant d’ajouter progressivement les données marché, le scoring, les alertes et le suivi de portefeuille.

---

## 2. 🧠 Principe central : Lexique-first

Le développement doit suivre une approche **Lexique-first**.

Cela signifie que le **Lexique Crypto Méthodes & Signaux Trading Pro** devient le noyau initial du produit.

```text
Lexique Crypto
↓
Knowledge Base
↓
Rules Engine
↓
Scoring Engine
↓
Risk Engine
↓
Dashboard
↓
Journal + Alertes
```

Le MVP doit rester utile même sans automatisation complète des prix en temps réel.  
Dès le Jour 1, l’utilisateur doit pouvoir consulter les termes, méthodes, signaux, règles de risque et playbooks de décision.

---

## 3. 📚 Rôle du Lexique Crypto Méthodes & Signaux Trading Pro

Le lexique est la **base éducative, méthodologique et opérationnelle** du futur outil.

Il doit couvrir :

| Domaine | Contenu attendu |
|---|---|
| **Crypto général** | BTC, altcoins, stablecoins, market cap, dominance, cycles |
| **Trading** | Breakout, pullback, range, support, résistance, momentum |
| **Indicateurs** | RSI, EMA, MACD, Volume, ATR, VWAP, Bollinger Bands |
| **Market structure** | Tendance, consolidation, capitulation, fakeout, retest |
| **Gestion du risque** | SL, TP1/TP2/TP3, position sizing, risk/reward |
| **Tokens volatils** | Volume, liquidité, social momentum, narratif, slippage |
| **On-chain / DeFi** | TVL, staking, DEX, bridges, unlocks, tokenomics |
| **Méthodes quotidiennes** | Checklists, routines, filtres d’achat, filtres de danger |
| **Signaux trading** | Signaux positifs, signaux négatifs, confirmations, invalidations |

---

## 4. 🧩 Transformation du lexique en base structurée

Le lexique Markdown ne doit pas rester un simple document statique.  
Il doit être transformé en **Knowledge Base exploitable**.

### Tables / onglets recommandés

| Table | Fonction |
|---|---|
| **KNOWLEDGE_TERMS** | Définitions crypto et trading |
| **METHOD_LIBRARY** | Méthodes de trading structurées |
| **SIGNAL_LIBRARY** | Signaux positifs, négatifs et neutres |
| **RISK_PLAYBOOK** | Règles de SL, TP, sizing et invalidation |
| **MARKET_REGIME_RULES** | Règles risk-on / risk-off selon BTC |
| **VOLATILITY_RULES** | Règles spécifiques aux tokens volatils |
| **CHECKLISTS** | Routines d’analyse quotidiennes |
| **DECISION_TEMPLATES** | Modèles “acheter / attendre / réduire / éviter” |
| **GLOSSARY_TAGS** | Tags : DeFi, IA, RWA, meme, L1, L2, DePIN, infra |

---

## 5. 🏗️ Architecture MVP Lexique-first

Le MVP doit être conçu comme un outil modulaire.

```text
Utilisateur
↓
Interface Knowledge Base
↓
Recherche / filtres / tags
↓
Méthodes & signaux
↓
Rules Engine
↓
Scoring semi-automatique
↓
Risk Engine TP/SL
↓
Dashboard quotidien
↓
Journal de décision
```

### Modules principaux

| Module | Priorité | Rôle |
|---|---:|---|
| **Knowledge Base** | P0 | Rendre le lexique consultable |
| **Search Engine** | P0 | Rechercher terme, méthode, signal |
| **Signal Library** | P0 | Lister les signaux exploitables |
| **Risk Playbook** | P0 | Appliquer SL, TP1/TP2/TP3, sizing |
| **Method Detail Pages** | P0 | Expliquer chaque méthode |
| **Scoring Engine** | P1 | Noter les setups sur 100 |
| **Dashboard** | P1 | Afficher marché, watchlist, score |
| **Trade Journal** | P1 | Journaliser les décisions |
| **Alert Engine** | P2 | Alertes BTC, token, TP, SL |
| **Portfolio Tracker** | P2 | Suivi allocation plus tard |

---

## 6. 🛠️ Stack technique recommandée

Le MVP doit privilégier une stack Google-native, simple et peu coûteuse au départ.

| Outil | Rôle |
|---|---|
| **Google Sheets** | Base de données MVP |
| **Google Apps Script** | Automatisations, parsing, alertes |
| **Google AppSheet** | Application web/mobile no-code |
| **Looker Studio** | Dashboard visuel |
| **Google Stitch** | Maquettes UI et design system |
| **Google Antigravity** | Génération et orchestration du code |
| **BigQuery** | Historique scalable plus tard |
| **Firebase** | Authentification / temps réel plus tard |
| **Cloud Run** | Backend scalable plus tard |

### Stack MVP initiale conseillée

```text
Google Sheets
+ Apps Script
+ AppSheet
+ Looker Studio
+ Stitch
+ Antigravity
```

---

## 7. 📊 Structure Google Sheets recommandée

```text
CONFIG
TOKENS
MARKET_RAW
INDICATORS
SCORES
PORTFOLIO
TRADES
KNOWLEDGE_TERMS
METHOD_LIBRARY
SIGNAL_LIBRARY
RISK_PLAYBOOK
MARKET_REGIME_RULES
VOLATILITY_RULES
CHECKLISTS
ALERTS
```

### Priorité des onglets au démarrage

| Jour | Onglet | But |
|---:|---|---|
| **J1** | KNOWLEDGE_TERMS | Importer les définitions |
| **J1** | METHOD_LIBRARY | Structurer les méthodes |
| **J1** | SIGNAL_LIBRARY | Créer la bibliothèque de signaux |
| **J1** | RISK_PLAYBOOK | Rendre les règles TP/SL disponibles |
| **J2** | CHECKLISTS | Créer les routines quotidiennes |
| **J2** | CONFIG | Paramètres généraux |
| **J3** | TOKENS | Watchlist initiale |
| **J4** | SCORES | Scoring semi-automatique |
| **J5** | TRADES | Journal de décisions |

---

## 8. 🔎 Fonctionnalités MVP prioritaires

### P0 — Fonctionnel dès le départ

| Fonction | Description |
|---|---|
| **Recherche lexique** | Rechercher un terme crypto/trading |
| **Fiches méthodes** | Voir définition, contexte, signaux, erreurs fréquentes |
| **Bibliothèque signaux** | Accès aux signaux haussiers, baissiers, neutres |
| **Risk Playbook** | Génération manuelle TP1/TP2/TP3/SL |
| **Checklists quotidiennes** | Routine avant achat / avant vente |
| **Décision guidée** | Acheter / attendre / réduire / éviter |

### P1 — Après base lexique

| Fonction | Description |
|---|---|
| **Scoring /100** | Notation semi-auto d’un setup |
| **Dashboard watchlist** | Vue tokens + score + risque |
| **Journal de décision** | Historique des analyses |
| **Tags et filtres** | IA, RWA, meme, DeFi, L1, L2, DePIN |
| **Templates de trade** | Plans structurés avec TP/SL |

### P2 — Évolutions

| Fonction | Description |
|---|---|
| **Données crypto live** | API CoinGecko / CoinMarketCap |
| **Alertes Telegram / email** | Alertes prix, score, TP, SL |
| **Portfolio tracker** | Allocation, cash, P&L |
| **Backtesting simple** | Tester règles sur historique |
| **Mode multi-utilisateur** | Version partagée / publique |

---

## 9. 🧮 Scoring Engine basé sur le lexique

Le scoring doit être alimenté par les règles du lexique.

### Exemple de score /100

| Critère | Points |
|---|---:|
| BTC stable ou haussier | 20 |
| Volume en hausse | 20 |
| Prix au-dessus EMA 20/50 | 15 |
| RSI entre 45 et 65 | 15 |
| Narratif clair | 10 |
| Risk/reward ≥ 2:1 | 20 |

### Interprétation

| Score | Décision |
|---:|---|
| **80–100** | Setup fort |
| **60–79** | Achat possible en petite taille |
| **40–59** | Surveillance uniquement |
| **< 40** | Éviter |

---

## 10. 🛡️ Risk Engine basé sur le lexique

Le Risk Engine doit générer une structure de trade standardisée.

### Format obligatoire

| Élément | Description |
|---|---|
| **Entrée idéale** | Zone d’achat optimale |
| **SL initial** | Niveau d’invalidation |
| **TP1** | Premier objectif |
| **Cession TP1** | % à vendre |
| **TP2** | Deuxième objectif |
| **Cession TP2** | % à vendre |
| **TP3** | Troisième objectif |
| **Cession TP3** | % à vendre |
| **Runner** | Petite position restante |
| **SL2 / SL3** | Stops remontés après TP1/TP2 |

### Règle standard

```text
TP1 : vendre 35%
TP2 : vendre 35%
TP3 : vendre 20%
Runner : garder 10%
Après TP1 : remonter le SL proche du prix d’entrée
Après TP2 : remonter le SL proche de TP1
```

---

## 11. 📈 Indicateurs techniques intégrés au lexique

Les noms doivent être compatibles avec Revolut X / TradingView.

| Nom simplifié | Nom exact à utiliser |
|---|---|
| **EMA** | Moving Average Exponential |
| **RSI** | Relative Strength Index |
| **MACD** | MACD |
| **Volume** | Volume |
| **ATR** | Average True Range |
| **VWAP** | VWAP / Volume Weighted Average Price |
| **Bollinger Bands** | Bollinger Bands |

### Setup standard

| Indicateur | Réglage |
|---|---:|
| Moving Average Exponential | 20 |
| Moving Average Exponential | 50 |
| Moving Average Exponential | 200 |
| Relative Strength Index | 14 |
| MACD | 12 / 26 / 9 |
| Average True Range | 14 |
| Volume | Standard |

---

## 12. 🖥️ Écrans MVP à concevoir dans Stitch

### Écran 1 — Knowledge Home

Objectif : page d’accueil du lexique.

Blocs :
- barre de recherche ;
- catégories principales ;
- méthodes populaires ;
- signaux du jour ;
- accès Risk Playbook ;
- accès Checklists.

### Écran 2 — Term Detail

Objectif : fiche détaillée d’un terme.

Champs :
- définition ;
- catégorie ;
- exemples ;
- signaux liés ;
- erreurs fréquentes ;
- méthodes associées ;
- tags.

### Écran 3 — Method Detail

Objectif : expliquer une méthode de trading.

Champs :
- contexte d’utilisation ;
- signaux requis ;
- invalidation ;
- TP/SL recommandés ;
- erreurs à éviter ;
- checklist.

### Écran 4 — Signal Library

Objectif : bibliothèque des signaux.

Filtres :
- haussier ;
- baissier ;
- neutre ;
- volume ;
- momentum ;
- volatilité ;
- BTC regime ;
- token volatil.

### Écran 5 — Risk Playbook

Objectif : générer une structure TP/SL.

Champs :
- token ;
- prix d’entrée ;
- volatilité ;
- ATR ;
- niveau d’invalidation ;
- TP1/TP2/TP3 ;
- % de cession.

---

## 13. 🤖 Prompts Antigravity recommandés

### Prompt 1 — Parser le lexique

```text
Convertis le fichier Markdown Lexique Crypto Méthodes & Signaux Trading Pro en tables structurées Google Sheets :
- KNOWLEDGE_TERMS
- METHOD_LIBRARY
- SIGNAL_LIBRARY
- RISK_PLAYBOOK
- CHECKLISTS

Chaque entrée doit contenir :
id, title, category, definition, use_case, signals, risks, examples, tags, related_methods.
```

### Prompt 2 — Générer le scoring

```text
Crée un moteur de scoring crypto sur 100 basé sur :
BTC regime, volume, EMA, RSI, MACD, ATR, narratif, liquidité et risk/reward.
Le moteur doit retourner :
score, décision, niveau de risque, raison principale, conditions d’invalidation.
```

### Prompt 3 — Générer TP/SL

```text
Crée une fonction Apps Script qui génère :
entrée idéale, SL, TP1, TP2, TP3, cessions 35/35/20/10, SL2 après TP1, SL3 après TP2.
La fonction doit s’adapter au niveau de volatilité : faible, moyen, élevé, extrême.
```

### Prompt 4 — Créer dashboard AppSheet

```text
Crée une app AppSheet connectée à Google Sheets avec les écrans :
Knowledge Home, Search Term, Method Detail, Signal Library, Risk Playbook, Trade Journal.
Le MVP doit être mobile-first, clair, rapide et orienté décision.
```

---

## 14. 🗓️ Roadmap MVP Lexique-first

| Jour | Objectif | Résultat attendu |
|---:|---|---|
| **J1** | Import lexique | Base consultable |
| **J2** | Structuration tables | Knowledge Base organisée |
| **J3** | AppSheet Knowledge UI | Recherche et fiches |
| **J4** | Signal Library | Signaux filtrables |
| **J5** | Risk Playbook | Génération TP/SL |
| **J6** | Scoring manuel | Score /100 semi-auto |
| **J7** | Dashboard + Journal | Utilisation quotidienne |

---

## 15. ✅ Definition of Done MVP

Le MVP est considéré comme valide si :

| Critère | Statut attendu |
|---|---|
| Lexique consultable | Obligatoire |
| Recherche par terme | Obligatoire |
| Méthodes accessibles | Obligatoire |
| Signaux filtrables | Obligatoire |
| Risk Playbook utilisable | Obligatoire |
| TP1/TP2/TP3 générables | Obligatoire |
| SL et invalidation disponibles | Obligatoire |
| Checklists quotidiennes | Obligatoire |
| Journal de décision | Recommandé |
| Dashboard simple | Recommandé |

---

## 16. 🧭 Instructions projet ChatGPT à intégrer

```md
Tu es un assistant crypto éducatif et analytique spécialisé dans la construction d’un outil Lexique-first nommé Crypto Signal OS.

Priorité du projet :
1. Transformer le Lexique Crypto Méthodes & Signaux Trading Pro en Knowledge Base fonctionnelle.
2. Structurer les termes, méthodes, signaux, playbooks de risque et checklists.
3. Construire un MVP Google-native avec Google Sheets, Apps Script, AppSheet, Looker Studio, Stitch et Antigravity.
4. Rendre le lexique exploitable dès le Jour 1.
5. Utiliser le lexique pour alimenter un scoring engine, un risk engine et un journal de décision.

Les réponses doivent être :
- en français ;
- structurées en Markdown ;
- avec tableaux ;
- avec emojis utiles ;
- orientées action ;
- compatibles avec une architecture MVP.

Pour toute évolution MVP, toujours préciser :
- objectif ;
- modules concernés ;
- structure de données ;
- écrans UI ;
- logique métier ;
- automatisations ;
- priorité P0/P1/P2 ;
- Definition of Done.
```

---

## 17. 🔥 Résumé ultra-court

```md
Projet Lexique & MVP Crypto = construire Crypto Signal OS, un outil quotidien de support crypto basé d’abord sur une Knowledge Base.

Priorité absolue :
rendre le Lexique Crypto Méthodes & Signaux Trading Pro fonctionnel dès le début.

Architecture :
Lexique → Knowledge Base → Rules Engine → Scoring → Risk Engine → Dashboard → Journal + Alertes.

Stack MVP :
Google Sheets + Apps Script + AppSheet + Looker Studio + Stitch + Antigravity.

Modules P0 :
KNOWLEDGE_TERMS, METHOD_LIBRARY, SIGNAL_LIBRARY, RISK_PLAYBOOK, CHECKLISTS.

But :
permettre à l’utilisateur de rechercher un terme, comprendre une méthode, identifier un signal, générer TP/SL et prendre une décision structurée.
```

---

## 18. ⚠️ Cadre d’utilisation

Ce projet est un **outil éducatif et analytique**.  
Il ne doit pas être présenté comme un système garantissant des performances.  
Les signaux et scores servent à structurer la décision, pas à prédire avec certitude le marché.
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

## 6. Impact spécifique sur `SYNTHESE`

Ce document reste source valide pour son contenu historique et structurel, mais ses passages liés à Revolut, portfolio, broker, paper trading, dry-run ou calcul trading sont **superseded** par cette correction 0.7.2.

```text
MVP_SCOPE = LEXIQUE_KB_WEBAPP_ONLY
QAIC_SCOPE = CALC_TRADING_REVOLUT_ENGINE
QAIC_BRIDGE_IN_MVP = OUTPUT_IMPORT_AND_DISPLAY_ONLY
```
