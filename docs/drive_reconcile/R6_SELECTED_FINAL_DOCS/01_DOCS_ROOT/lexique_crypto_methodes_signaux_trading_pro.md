# 🚀 Lexique Crypto, Méthodes & Signaux Trading — Guide Pro Quotidien

> **Objectif :** livrable Markdown opérationnel pour une utilisation quotidienne et pour poser l’architecture d’un futur outil fonctionnel de support à la décision crypto/trading.

> ⚠️ Contenu éducatif et informatif uniquement. Les signaux décrits sont des cadres d’analyse, pas des garanties.

---

## 📌 Table des matières

1. 🧠 Philosophie générale  
2. ₿ Lexique crypto essentiel  
3. 📈 Lexique trading & market structure  
4. 🧬 Lexique DeFi, Web3, NFT, on-chain  
5. 🔥 Types de tokens et profils de risque  
6. 🗓️ Méthode d’analyse quotidienne  
7. 📊 Indicateurs techniques à afficher  
8. 🎯 Méthodes de signaux trading  
9. ⚡ Signaux sur tokens très volatils  
10. 🛡️ Gestion du risque et position sizing  
11. 🧮 Scoring crypto sur 100  
12. 🧾 Templates opérationnels  
13. 🏗️ Architecture d’un outil fonctionnel de support  
14. 🧱 Schémas de données  
15. 🤖 Pseudo-code moteur de signaux  
16. 🧪 Backtesting conceptuel  
17. 🖥️ Dashboard idéal  
18. ✅ Checklists quotidiennes  
19. ⚠️ Disclaimers  

---

# 1. 🧠 Philosophie générale

Le marché crypto est dominé par **la liquidité**, **le momentum**, **les narratifs**, **les flux institutionnels**, **l’effet de levier** et **la psychologie de foule**.

Le but n’est pas de prédire avec certitude. Le but est de construire un système qui répond chaque jour à trois questions :

| Question | Objectif |
|---|---|
| **Où est le risque ?** | Identifier supports, volatilité, liquidité, invalidation |
| **Où est l’opportunité ?** | Détecter momentum, rotation, accumulation, catalyseurs |
| **Quelle taille engager ?** | Adapter l’exposition au contexte BTC et au cash disponible |

> **Un bon trade n’est pas celui qui gagne toujours. C’est celui dont le risque est défini avant l’entrée.**

---

# 2. ₿ Lexique crypto essentiel

| Terme | Définition | Utilisation pratique |
|---|---|---|
| **Bitcoin / BTC** | Première crypto, actif directeur du marché | Baromètre global du risque |
| **Ethereum / ETH** | Blockchain smart contracts dominante | Indicateur DeFi/Web3 |
| **Altcoin** | Toute crypto hors BTC | Plus volatile, dépend souvent de BTC |
| **Stablecoin** | Token indexé sur une monnaie fiat | Réserve de cash, protection, arbitrage |
| **USDC / USDT** | Stablecoins majeurs | Sortie temporaire du risque |
| **Market Cap** | Prix x supply en circulation | Taille relative d’un projet |
| **FDV** | Valorisation si tous les tokens étaient en circulation | Détecte survalorisation/dilution |
| **Circulating Supply** | Tokens actuellement en circulation | Impacte market cap et liquidité |
| **Max Supply** | Offre maximale possible | Important pour rareté/inflation |
| **Tokenomics** | Structure économique du token | Débloquages, dilution, incentives |
| **Narratif** | Thème dominant du marché | IA, RWA, DePIN, L2, memes |
| **Catalyseur** | Événement pouvant provoquer un mouvement | Listing, upgrade, ETF, partenariat |
| **Listing** | Ajout sur exchange | Peut augmenter liquidité et visibilité |
| **Unlock** | Déblocage de tokens | Peut créer pression vendeuse |
| **Burn** | Destruction de tokens | Peut réduire supply |
| **Emission** | Création de nouveaux tokens | Dilution potentielle |

---

# 3. 📈 Lexique trading & market structure

## Structure de marché

| Terme | Définition | Signal pratique |
|---|---|---|
| **Support** | Zone où les acheteurs défendent | Achat potentiel si confirmation |
| **Résistance** | Zone où les vendeurs dominent | TP ou attente breakout |
| **Breakout** | Cassure d’une résistance | Achat possible si volume confirmé |
| **Breakdown** | Cassure d’un support | Réduction ou stop |
| **Retest** | Retour sur une zone cassée | Meilleure entrée que FOMO |
| **Higher High / HH** | Nouveau sommet supérieur | Structure haussière |
| **Higher Low / HL** | Creux supérieur | Accumulation possible |
| **Lower High / LH** | Sommet inférieur | Faiblesse |
| **Lower Low / LL** | Creux inférieur | Tendance baissière |
| **MSS** | Market Structure Shift | Changement potentiel de tendance |
| **CHoCH** | Change of Character | Premier signe de retournement |
| **Liquidity Sweep** | Chasse aux stops avant retournement | Fréquent sur cryptos volatiles |
| **Fakeout** | Fausse cassure | Danger si rejet rapide |

## Ordres

| Terme | Définition | Utilisation |
|---|---|---|
| **Market Order** | Achat/vente immédiat | Rapide, mais slippage possible |
| **Limit Order** | Achat/vente à prix défini | Préférable pour entrée propre |
| **Stop Loss / SL** | Niveau d’invalidation | Protège le capital |
| **Take Profit / TP** | Niveau de prise de profit | Sécurise les gains |
| **Trailing Stop** | Stop suiveur | Laisse courir tout en protégeant |
| **DCA** | Achat par paliers | Réduit mauvais timing |
| **Scale in** | Entrer progressivement | Adapté aux marchés volatils |
| **Scale out** | Sortir progressivement | TP1, TP2, TP3 |

## Concepts avancés

| Terme | Définition | Utilité |
|---|---|---|
| **Order Block** | Zone potentielle d’accumulation/distribution | Zone de réaction |
| **Fair Value Gap / FVG** | Déséquilibre de prix | Zone de retour possible |
| **Liquidity Pool** | Zone où s’accumulent les stops | Cible fréquente du marché |
| **Open Interest / OI** | Valeur des positions dérivées ouvertes | Mesure levier |
| **Funding Rate** | Coût longs/shorts en perps | Détecte excès de biais |
| **Liquidation Cascade** | Liquidations forcées en chaîne | Accélération violente |
| **Short Squeeze** | Shorts forcés de racheter | Hausse rapide |
| **Long Squeeze** | Longs liquidés | Chute rapide |

---

# 4. 🧬 Lexique DeFi, Web3, NFT, on-chain

| Terme | Définition | Signal |
|---|---|---|
| **TVL** | Total Value Locked dans un protocole | Utilisation/attraction de liquidité |
| **Yield Farming** | Recherche de rendement DeFi | Risque smart contract |
| **Staking** | Blocage de tokens contre récompense | Rendement + lock-up |
| **Restaking** | Réutilisation du staking | Risque systémique accru |
| **AMM** | Market maker automatisé | Base des DEX |
| **LP Token** | Token reçu en fournissant de la liquidité | Exposition double |
| **Impermanent Loss** | Perte relative d’un LP vs hold | Risque des pools |
| **Active Addresses** | Adresses actives | Adoption/utilisation |
| **Exchange Inflows** | Entrées vers exchanges | Risque vente |
| **Exchange Outflows** | Sorties des exchanges | Accumulation potentielle |
| **Whale Wallets** | Gros portefeuilles | Influence possible |
| **Holder Distribution** | Répartition des holders | Concentration = risque |
| **Airdrop** | Distribution de tokens | Catalyseur ou pression vendeuse |
| **Snapshot** | Capture des wallets | Souvent lié aux airdrops |
| **NFT Floor** | Prix minimum d’une collection NFT | Santé marché NFT |
| **Mint** | Création d’un token/NFT | Événement de lancement |

---

# 5. 🔥 Types de tokens et profils de risque

| Type | Exemples | Potentiel | Risque | Usage |
|---|---|---:|---:|---|
| **Core** | BTC, ETH | Moyen | Faible à moyen | Base portefeuille |
| **Large-cap L1** | SOL, SUI, NEAR | Moyen à élevé | Moyen | Swing / rotation |
| **DeFi solide** | AAVE, UNI, ONDO | Moyen à élevé | Moyen | Narratif sectoriel |
| **RWA** | ONDO, TRU | Élevé | Moyen à très élevé | Narratif institutionnel |
| **IA / DePIN** | RENDER, FET, AI, HONEY | Élevé | Élevé | Rotation narrative |
| **DEX / Perps** | HYPE, JUP, OSMO | Élevé | Élevé | Momentum sectoriel |
| **Microcaps** | SQD, SPK, B3 | Très élevé | Très élevé | Trades courts |
| **Memecoins** | PEPE, WIF, BONK, DEGEN | Extrême | Extrême | Spéculation rapide |
| **Top gainers 24h** | STG, TRU, SQD | Très élevé | Très élevé | Momentum/scalp |

## Définition d’un token très volatil

| Critère | Seuil indicatif |
|---|---:|
| Variation 24h | > ±8% |
| Variation 7j | > ±20% |
| Volume 24h en hausse | > +50% |
| Market cap | Petite à moyenne |
| Spread | Large ou variable |
| Dépendance au narratif | Forte |
| Réaction à BTC | Amplifiée |
| Risque de mèche | Élevé |

---

# 6. 🗓️ Méthode d’analyse quotidienne

## Routine en 15 minutes

| Étape | Question | Action |
|---|---|---|
| **1. BTC** | BTC tient-il ses zones clés ? | Définir risk-on/risk-off |
| **2. ETH** | ETH confirme-t-il BTC ? | Vérifier breadth |
| **3. Dominance BTC** | Capital vers BTC ou alts ? | Rotation ou défense |
| **4. Volume marché** | Mouvement confirmé ? | Éviter faux pumps |
| **5. Heatmap** | Quels secteurs performent ? | Identifier narratif |
| **6. Watchlist** | Volume + momentum ? | Préparer ordres |
| **7. Risk budget** | Combien risquer aujourd’hui ? | Limiter taille |
| **8. Journal** | Quelle décision et pourquoi ? | Éviter impulsivité |

## Mode marché

| Condition BTC | Mode | Stratégie |
|---|---|---|
| BTC > EMA 200 daily + HH/HL | 🟢 **Risk-on** | Alts, momentum, swing |
| BTC en range stable | 🟡 **Neutral** | Trades courts, TP rapides |
| BTC sous supports clés | 🔴 **Risk-off** | Cash, BTC léger, éviter microcaps |
| BTC capitulation + volume extrême | 🟠 **Contrarian prudent** | Micro-DCA, pas all-in |
| BTC breakout confirmé | 🚀 **Expansion** | Scale-in progressif |

---

# 7. 📊 Indicateurs techniques à afficher

## Noms à chercher dans Revolut X / TradingView

| Indicateur simplifié | Nom exact à chercher | Réglage courant |
|---|---|---|
| **EMA** | **Moving Average Exponential** | 20 / 50 / 200 |
| **SMA** | **Moving Average** | 50 / 100 / 200 |
| **RSI** | **Relative Strength Index** | 14 |
| **MACD** | **MACD** | 12 / 26 / 9 |
| **Volume** | **Volume** | Standard |
| **ATR** | **Average True Range** | 14 |
| **Bandes Bollinger** | **Bollinger Bands** | 20 / 2 |
| **VWAP** | **VWAP** ou **Volume Weighted Average Price** | Session |

## Setup recommandé

| Usage | Timeframe | Indicateurs |
|---|---|---|
| **BTC direction marché** | 4H + Daily | EMA 50/200, RSI, Volume |
| **Swing alts** | 1H + 4H | EMA 20/50/200, RSI, MACD, Volume |
| **Tokens volatils** | 15m + 1H | EMA 20/50, RSI, Volume, ATR |
| **Entrée précise** | 5m + 15m | EMA 20, Volume, RSI |
| **Gestion SL** | 1H | ATR 14 + supports |

## Lecture rapide

| Signal | Lecture | Action |
|---|---|---|
| Prix > EMA 20 | Momentum court terme positif | Achat possible |
| EMA 20 > EMA 50 | Structure courte favorable | Setup plus propre |
| Prix < EMA 200 | Marché fragile | Taille réduite |
| RSI 50–70 | Momentum sain | Zone favorable |
| RSI > 70 | Surachat | Éviter FOMO / prendre profit |
| MACD croise haut | Momentum reprend | Confirmation |
| Volume hausse sur bougie verte | Achat crédible | Signal positif |
| Volume faible pendant pump | Hausse fragile | Prudence |

---

# 8. 🎯 Méthodes de signaux trading

## Signal A — Breakout confirmé 🚀

| Condition | Exigence |
|---|---|
| Prix casse résistance | Oui |
| Volume supérieur moyenne | Oui |
| RSI > 50 | Oui |
| MACD haussier | Idéal |
| Retest réussi | Entrée optimale |
| SL | Sous résistance cassée |
| TP | 1R / 2R / 3R |

## Signal B — Pullback sur tendance 🧲

| Condition | Exigence |
|---|---|
| Tendance haussière | Prix > EMA 50 |
| Retour vers EMA 20/50 | Oui |
| RSI reste > 40–45 | Oui |
| Volume vendeur diminue | Oui |
| Bougie de réaction | Oui |
| SL | Sous creux du pullback |

## Signal C — Reversal après capitulation 🩸

| Condition | Exigence |
|---|---|
| Forte baisse récente | Oui |
| Volume extrême | Oui |
| Mèche basse | Oui |
| RSI < 30 puis retour > 35/40 | Oui |
| Confirmation 1H/4H | Obligatoire |
| SL | Sous plus bas capitulation |

## Signal D — Range trading 📦

| Zone | Action |
|---|---|
| Support du range | Achat si réaction |
| Milieu du range | Éviter entrée |
| Résistance du range | TP / vente partielle |
| Cassure support | Stop |
| Cassure résistance + retest | Breakout trade |

## Signal E — Momentum token volatil ⚡

| Condition | Pondération |
|---|---:|
| Variation 24h positive contrôlée | +15 |
| Volume 24h en forte hausse | +20 |
| Prix tient EMA 20 1H | +15 |
| RSI entre 50 et 70 | +15 |
| BTC stable | +15 |
| Narratif actif | +10 |
| Pas de grande mèche haute | +10 |

| Score | Décision |
|---:|---|
| **> 75** | Setup intéressant |
| **60–75** | Watch / petite taille |
| **45–60** | Surveillance |
| **< 45** | Éviter |

---

# 9. ⚡ Signaux sur tokens très volatils

## Signaux positifs

| Signal | Pourquoi c’est important |
|---|---|
| Volume 24h > volume moyen | Mouvement suivi |
| Prix maintient le pump 3–6h | Moins pump-and-dump |
| Pullback < 30–40% du pump | Consolidation saine |
| Retest d’une résistance cassée | Entrée plus propre |
| RSI refroidit de 75 vers 55–60 | FOMO réduit |
| BTC stable ou positif | Favorise les alts |
| Plusieurs exchanges listent | Meilleure liquidité |
| Narratif clair | Soutien psychologique |

## Signaux de danger

| Signal | Interprétation |
|---|---|
| +50% à +100% en 24h | Risque FOMO élevé |
| Grande mèche haute | Distribution possible |
| Volume chute pendant hausse | Mouvement fragile |
| Spread élevé | Sortie difficile |
| Market cap très faible | Manipulation possible |
| Pump sans actualité | Risque de piège |
| BTC casse support | Microcaps chutent plus |
| Unlock imminent | Pression vendeuse possible |

## Règles d’entrée

| Situation | Action |
|---|---|
| Token déjà +50% 24h | Attendre pullback |
| Token +10–25% avec volume | Surveiller entrée |
| Pullback support + RSI > 50 | Achat possible |
| Breakout sans volume | Éviter |
| BTC sous stress | Taille divisée par 2 ou 3 |

---

# 10. 🛡️ Gestion du risque et position sizing

## Formule

```text
Taille de position = Montant risqué / Distance entre entrée et SL
```

Exemple :

```text
Capital = 1 000 $
Risque par trade = 1% = 10 $
Entrée = 1,00 $
SL = 0,90 $
Risque par token = 0,10 $
Taille = 10 / 0,10 = 100 tokens
Valeur position = 100 $
```

## Risque conseillé

| Type d’actif | Risque max par trade |
|---|---:|
| BTC | 1–2% |
| ETH / large-cap | 0,75–1,5% |
| Mid-cap | 0,5–1% |
| Token volatil | 0,25–0,75% |
| Microcap / meme | 0,10–0,50% |

## Prise de profit standard

| Niveau | Action |
|---|---|
| **TP1** | Vendre 30–40% |
| **TP2** | Vendre 25–35% |
| **TP3** | Vendre 15–25% |
| **Runner** | Garder 5–15% |
| **Après TP1** | Remonter SL proche entrée |
| **Après TP2** | Remonter SL vers TP1 |
| **Après TP3** | Stop suiveur |

---

# 11. 🧮 Scoring crypto sur 100

| Catégorie | Points |
|---|---:|
| Momentum technique | 20 |
| Volume / liquidité | 15 |
| Structure de marché | 15 |
| Narratif | 15 |
| Fondamental / utilité | 10 |
| Tokenomics | 10 |
| On-chain / adoption | 5 |
| Unlock / dilution | 5 |
| Corrélation BTC | 5 |

| Score | Décision |
|---:|---|
| **85–100** | Setup fort |
| **70–84** | Setup intéressant |
| **55–69** | Watchlist |
| **40–54** | Micro-position seulement |
| **< 40** | Éviter |

## Exemple

```markdown
Token : HYPE
Momentum : 17/20
Volume : 14/15
Structure : 11/15
Narratif : 14/15
Fondamental : 8/10
Tokenomics : 6/10
On-chain/adoption : 4/5
Unlock/dilution : 3/5
Corrélation BTC : 3/5
Score total : 80/100
Décision : achat progressif possible si BTC stable
```

---

# 12. 🧾 Templates opérationnels

## Template analyse token

```markdown
## Analyse Token

Token :
Prix actuel :
Market cap :
Volume 24h :
Variation 24h :
Variation 7j :
Narratif :
Type : Core / L1 / DeFi / IA / RWA / Meme / Microcap

### Structure
Support principal :
Résistance principale :
Tendance 1H :
Tendance 4H :
Tendance Daily :

### Indicateurs
EMA 20 :
EMA 50 :
EMA 200 :
RSI :
MACD :
Volume :
ATR :

### Plan
Entrée :
SL :
TP1 :
TP2 :
TP3 :
% cession :
Taille position :
Risque max :

### Verdict
Score :
Décision :
Invalidation :
```

## Template journal de trade

```markdown
## Journal de trade

Date :
Token :
Direction :
Prix d’entrée :
Taille :
SL :
TP1 :
TP2 :
TP3 :
Risque en $ :
Risque en % portefeuille :

Pourquoi j’entre ?
1.
2.
3.

Qu’est-ce qui invalide le trade ?
1.
2.

Résultat :
Leçon :
Erreur évitable :
```

## Template plan quotidien

```markdown
# Plan du jour

## Marché global
BTC :
ETH :
Dominance BTC :
Mode marché : Risk-on / Neutral / Risk-off

## Watchlist
1.
2.
3.
4.
5.

## Opportunités
Token :
Setup :
Entrée :
SL :
TP1 :
TP2 :
TP3 :
Taille :

## Risques
Support BTC critique :
News :
Unlocks :
Volatilité :
Liquidations :

## Décision
Acheter :
Attendre :
Réduire :
Cash :
```

---

# 13. 🏗️ Architecture d’un outil fonctionnel de support

## Objectif outil

Créer un assistant qui permet de :

- 📥 Importer une watchlist
- 🔍 Scanner les tokens
- 📊 Calculer momentum, volume, volatilité
- 🧠 Générer un score
- 🎯 Proposer entrée, SL, TP1/TP2/TP3
- 🛡️ Calculer taille de position
- 📝 Générer un journal de trade
- 🔔 Envoyer des alertes
- 📈 Suivre la performance

## Modules

| Module | Fonction |
|---|---|
| **Market Data Engine** | Prix, volume, variation |
| **Technical Engine** | EMA, RSI, MACD, ATR |
| **Risk Engine** | SL, position sizing, exposition |
| **Scoring Engine** | Score sur 100 |
| **Narrative Engine** | IA, RWA, DePIN, meme, L1, DeFi |
| **Portfolio Engine** | Allocation, cash, concentration |
| **Alert Engine** | Alertes prix et signaux |
| **Trade Journal** | Décisions et résultats |
| **Backtest Engine** | Test des règles |
| **Dashboard UI** | Vue quotidienne |

## Architecture logique

```text
[Data Sources]
     |
     v
[Market Data Engine] ---> [Technical Engine]
     |                         |
     v                         v
[Token Database] ---> [Scoring Engine]
     |                         |
     v                         v
[Risk Engine] ----------> [Signal Generator]
     |                         |
     v                         v
[Portfolio Engine] ---> [Dashboard + Alerts]
     |
     v
[Trade Journal + Analytics]
```

---

# 14. 🧱 Schémas de données

## Token

```json
{
  "symbol": "HYPE",
  "name": "Hyperliquid",
  "category": ["DEX", "Perps", "DeFi"],
  "price": 57.74,
  "market_cap": 14600000000,
  "volume_24h": 1050000000,
  "change_24h": -5.54,
  "change_7d": -20.25,
  "risk_level": "high",
  "narrative": "perp_dex",
  "exchange_available": true
}
```

## TechnicalSignal

```json
{
  "symbol": "HYPE",
  "timeframe": "1h",
  "ema20": 58.20,
  "ema50": 56.90,
  "ema200": 61.40,
  "rsi14": 54.3,
  "macd_signal": "bullish_cross",
  "atr14": 2.10,
  "volume_status": "above_average",
  "trend_status": "recovering"
}
```

## TradePlan

```json
{
  "symbol": "HYPE",
  "entry_zone": [56, 58],
  "stop_loss": 51.5,
  "tp1": 62,
  "tp1_sell_percent": 35,
  "tp2": 68,
  "tp2_sell_percent": 35,
  "tp3": 75,
  "tp3_sell_percent": 20,
  "runner_percent": 10,
  "max_position_usd": 35,
  "risk_usd": 3.5,
  "status": "watch"
}
```

---

# 15. 🤖 Pseudo-code moteur de signaux

## Scoring momentum

```python
def momentum_score(token):
    score = 0

    if 5 <= token.change_24h <= 25:
        score += 15
    elif token.change_24h > 25:
        score += 8
    elif token.change_24h < -10:
        score += 5

    if token.volume_change_24h > 50:
        score += 20

    if 50 < token.rsi < 70:
        score += 15
    elif token.rsi >= 70:
        score += 5

    if token.price > token.ema20:
        score += 10

    if token.ema20 > token.ema50:
        score += 10

    if token.btc_context == "stable":
        score += 15

    if token.has_clear_narrative:
        score += 15

    return min(score, 100)
```

## Génération SL/TP

```python
def generate_trade_plan(entry, atr, volatility_type):
    if volatility_type == "high":
        sl = entry - (1.5 * atr)
    elif volatility_type == "extreme":
        sl = entry - (2.0 * atr)
    else:
        sl = entry - (1.2 * atr)

    risk = entry - sl

    return {
        "entry": entry,
        "sl": sl,
        "tp1": entry + (1.2 * risk),
        "tp2": entry + (2.0 * risk),
        "tp3": entry + (3.0 * risk),
        "sell_plan": {
            "tp1": 35,
            "tp2": 35,
            "tp3": 20,
            "runner": 10
        }
    }
```

## Position sizing

```python
def position_size(portfolio_value, risk_percent, entry, stop_loss):
    risk_amount = portfolio_value * risk_percent
    risk_per_unit = abs(entry - stop_loss)

    if risk_per_unit == 0:
        return None

    units = risk_amount / risk_per_unit
    position_value = units * entry

    return {
        "units": units,
        "position_value": position_value,
        "risk_amount": risk_amount
    }
```

---

# 16. 🧪 Backtesting conceptuel

## À tester

| Élément | Question |
|---|---|
| Entrées EMA/RSI | Le signal produit-il un avantage ? |
| TP1/TP2/TP3 | Les prises partielles améliorent-elles le résultat ? |
| SL ATR | Stop trop serré ou trop large ? |
| Filtre BTC | Performance meilleure quand BTC stable ? |
| Filtre volume | Volume améliore-t-il la qualité ? |
| Timeframe | 15m, 1H, 4H : lequel fonctionne le mieux ? |

## Métriques

| Métrique | Définition |
|---|---|
| Win rate | % trades gagnants |
| Profit factor | Gains bruts / pertes brutes |
| Max drawdown | Pire baisse du capital |
| Average R | Gain/perte moyen en unités de risque |
| Expectancy | Gain moyen attendu par trade |
| Slippage | Écart prix théorique/exécuté |

```text
Expectancy = (Win Rate x Gain Moyen) - (Loss Rate x Perte Moyenne)
```

---

# 17. 🖥️ Dashboard idéal

| Bloc | Contenu |
|---|---|
| **Market Regime** | BTC mode, ETH mode, dominance, fear/greed |
| **Watchlist Score** | Tokens classés par score |
| **Signals** | Buy / Watch / Avoid |
| **Risk Panel** | Exposition, cash, risque ouvert |
| **Trade Plans** | Entrée, SL, TP1/TP2/TP3 |
| **Alerts** | Prix clés et invalidations |
| **Journal** | Trades actifs et clôturés |

## Exemple

```markdown
## Dashboard du jour

### Market Regime
BTC : Neutral/Risk-off
ETH : Weak
Mode : Cash dominant + micro-trades

### Top Watchlist
1. HYPE — Score 80 — Watch/Buy small
2. ONDO — Score 76 — Buy on pullback
3. SQD — Score 72 — Momentum trade
4. SPK — Score 69 — Watch
5. JUP — Score 58 — Hold/recovery only

### Alertes
- BTC > 65 500 $ : reprise progressive
- BTC < 60 000 $ : suspendre volatils
- HYPE > 62 $ : TP1
- ONDO < 0,325 $ : invalidation
```

---

# 18. ✅ Checklists quotidiennes

## Avant marché

```markdown
- [ ] BTC au-dessus ou sous zones clés ?
- [ ] ETH confirme-t-il ?
- [ ] Dominance BTC en hausse ou baisse ?
- [ ] Volume global en hausse ?
- [ ] Top gainers : pump sain ou FOMO ?
- [ ] Tokens avec volume anormal ?
- [ ] News ou unlocks importants ?
- [ ] Cash disponible ?
- [ ] Risque maximal du jour défini ?
```

## Avant d’acheter

```markdown
- [ ] Je connais mon entrée
- [ ] Je connais mon SL
- [ ] Je connais TP1, TP2, TP3
- [ ] Le ratio risk/reward est acceptable
- [ ] BTC n’est pas en breakdown
- [ ] Le volume confirme
- [ ] Je n’achète pas une mèche euphorique
- [ ] La taille est adaptée
- [ ] J’ai écrit la raison du trade
```

## Après TP1

```markdown
- [ ] Vendre 30–40%
- [ ] Remonter SL vers entrée
- [ ] Ne pas rajouter par euphorie
- [ ] Vérifier BTC
```

---

# 19. ⚡ Glossaire express

| Terme | Sens rapide |
|---|---|
| **FOMO** | Acheter par peur de rater |
| **FUD** | Peur/incertitude/doute |
| **Pump** | Hausse rapide |
| **Dump** | Baisse rapide |
| **Whale** | Gros investisseur |
| **Bagholder** | Position perdante conservée |
| **Airdrop** | Distribution de tokens |
| **Unlock** | Déblocage de tokens |
| **Slippage** | Différence prix attendu/exécuté |
| **Spread** | Écart achat/vente |
| **Liquidity** | Facilité d’acheter/vendre |
| **Narrative** | Thème dominant du marché |
| **Alpha** | Signal/information avec avantage potentiel |
| **Risk-on** | Marché favorable aux actifs risqués |
| **Risk-off** | Marché défensif |
| **R:R** | Risk/reward |
| **1R** | Unité de risque |
| **Breakout** | Cassure haussière |
| **Breakdown** | Cassure baissière |
| **Retest** | Test d’une zone cassée |
| **DCA** | Achat progressif |
| **Scalp** | Trade très court |
| **Swing** | Trade sur plusieurs jours/semaines |
| **Spot** | Achat réel sans levier |
| **Perp** | Contrat perpétuel |
| **Funding** | Paiement entre longs/shorts |
| **OI** | Open Interest |
| **TVL** | Total Value Locked |

---

# 20. ⚠️ Disclaimers

Ce document est fourni à des fins **éducatives, analytiques et informatives** uniquement.  
Il ne constitue pas un conseil financier, une recommandation personnalisée, une incitation à acheter/vendre, ni une garantie de performance.

Les marchés crypto sont volatils. Les performances passées ne préjugent pas des performances futures. Toute décision d’investissement doit être prise après recherche personnelle, gestion du risque et compréhension des pertes potentielles.

Pour les graphiques, alertes et indicateurs avancés, un outil comme [TradingView](https://www.tradingview.com/?aff_id=138872) peut être utilisé comme support d’analyse.

---

## 🧩 Version opérationnelle courte

```text
1. Regarder BTC
2. Définir mode marché
3. Scanner volume + momentum
4. Éviter FOMO
5. Attendre pullback ou breakout confirmé
6. Définir entrée, SL, TP1, TP2, TP3
7. Calculer taille
8. Placer alertes
9. Journaliser
10. Respecter le plan
```

## 🧠 Mantra

> **Cash = optionnalité.  
> SL = survie.  
> TP = discipline.  
> Journal = progression.  
> Taille = contrôle.**
