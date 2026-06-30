# 🚀 Instructions Projet — MVP QAIC Process Governance 0.7.3

> **Projet :** 🛠️ MVP QAIC — Crypto Signal OS  
> **Version :** `0.7.3_PROCESS_GOVERNANCE_BATCH_MAXI_FAST_FUSE`  
> **Date :** 2026-06-20  
> **Statut :** `ACTIVE_SUPERSEDE_RULES`  
> **S'applique à :** toutes les phases MVP QAIC après 0.7.2.

---

## 1. Règle ferme de développement

```text
DEV_MODE = BATCH_MAXI_PLUS_PLUS_PLUS_ONLY
STEP_MODE = FAST_AND_FUSE
MICRO_PATCHES = FORBIDDEN_BY_DEFAULT
CHAT_TRUNCATION = FORBIDDEN_BY_DEFAULT
ZIP_REQUIRED_IF_LONG = TRUE
```

Traduction opérationnelle :

```text
Pas de micro-corrections isolées.
Pas de tunnel d'audit inutile.
Pas de mini-batchs répétitifs.
Pas de réponses longues tronquées.
Pas de collage énorme si un ZIP est plus sûr.
```

---

## 2. Batch Maxi +++ only

Toute prochaine étape doit être conçue comme un batch complet :

```text
1. audit borné
2. correction/fusion
3. validation
4. rangement
5. statut final
6. next action claire
```

Un batch MVP doit grouper les corrections mineures compatibles.

Exemples autorisés :

```text
PxxA_AUDIT_AND_FUSION_DOCS_MAXI
PxxB_APPLY_AND_VERIFY_WEBAPP_MAXI
PxxC_LEXIQUE_REVIEW_AND_REGISTRY_MAXI
```

Exemples interdits :

```text
PxxA_micro_fix_title
PxxB_micro_fix_readme
PxxC_micro_check_again
PxxD_same_audit_again
```

---

## 3. Mode Fast & Fuse

La règle **Fast & Fuse** veut dire :

```text
FAST = éviter la sur-validation répétitive quand les preuves existent.
FUSE = fusionner dans les documents/modules existants plutôt que créer des branches parallèles.
```

Application :

```text
- si un document existe, créer une version fusionnée complète, pas une synthèse séparée ;
- si une correction touche plusieurs docs, produire un pack unique ;
- si plusieurs erreurs mineures sont détectées, les intégrer dans un même batch ;
- si une preuve live existe déjà, ne pas relancer trois audits équivalents ;
- si un ancien document reste utile, le marquer historique/superseded plutôt que le supprimer.
```

---

## 4. Règle anti-réponse tronquée ChatGPT

Pour les chats/prochaines réponses :

```text
NO_TRUNCATED_FINAL = TRUE
NO_PARTIAL_CODE_BLOCK_IF_LONG = TRUE
NO_HALF_SCRIPT = TRUE
NO_LONG_DOC_INLINE_IF_ZIP_BETTER = TRUE
```

Si une réponse risque d'être longue :

```text
- produire un résumé court dans le chat ;
- générer un ZIP ou un fichier .md ;
- mettre les gros contenus dans le livrable ;
- fournir les liens et le statut ;
- ne jamais couper un script ou un document au milieu.
```

Format recommandé :

```text
Résumé court
+ statut
+ fichiers générés / rangés
+ liens
+ next action
```

---

## 5. Règle de scope MVP / QAIC maintenue

```text
MVP = Lexique / KB / WebApp pédagogique
QAIC = calculs / trading analytics / portefeuille / Revolut API
```

Interdits MVP :

```text
NO_REVOLUT_API_IN_MVP
NO_TRADING_ENGINE_IN_MVP
NO_PORTFOLIO_ENGINE_IN_MVP
NO_ORDER_IN_MVP
NO_SIZING_IN_MVP
NO_BROKER_EXECUTION_IN_MVP
```

---

## 6. Règle documentaire

Tous les docs résiduels antérieurs restent historiques mais ne pilotent plus le process.

```text
0.7.3_PROCESS_GOVERNANCE_BATCH_MAXI_FAST_FUSE
  > 0.7.2_REAL_FULL_SOURCE_FUSION_SCOPE_SPLIT
  > 0.6.2_REAL_FUSION_REPAIR
```

---

## 7. Règle de réponse assistant

Pour toute future demande MVP QAIC :

```text
- répondre en français ;
- être direct ;
- éviter les explications inutiles ;
- utiliser batch maxi par défaut ;
- ne pas demander confirmation quand la suite logique est sûre ;
- annoncer clairement ce qui est fait / pas fait ;
- si livrable volumineux : ZIP obligatoire ;
- jamais de promesse de travail différé ;
- jamais de "je reviens vers toi plus tard" sans action terminée.
```

---

## 8. Statut actif

```text
PROCESS_GOVERNANCE_0.7.3 = ACTIVE
BATCH_MAXI_PLUS_PLUS_PLUS_ONLY = TRUE
FAST_AND_FUSE = TRUE
ANTI_TRUNCATION_ZIP_RULE = TRUE
```
