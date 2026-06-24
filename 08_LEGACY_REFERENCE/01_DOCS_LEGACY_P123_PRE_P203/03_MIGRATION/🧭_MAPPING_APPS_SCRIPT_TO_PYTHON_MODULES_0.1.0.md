# 🐍 MVP QAIC — Référence Python

**Version :** P0.7.6 / 0.1.0  
**Statut :** référence documentaire, lecture seule  
**Périmètre :** Lexique / Knowledge Base / WebApp en priorité

## 🎯 Finalité

`MVP_QAIC_PY` prépare une migration future et progressive du MVP Google Sheets / Apps Script / WebApp vers une architecture compatible Python. Le MVP actuel reste la source fonctionnelle prioritaire pour le Lexique, la KB et la WebApp. Cette arborescence ne remplace, ne déploie et ne modifie aucun composant live.

La future couche Python doit permettre :

- l’ingestion structurée de sources exportées ;
- la validation par contrats explicites ;
- des tests reproductibles ;
- une CLI locale en lecture seule ;
- la génération de rapports locaux ;
- des workflows contrôlés d’export/import.

Le moteur QAIC avancé demeure séparé. Son raccordement éventuel intervient uniquement en phase P7, via un bridge optionnel et contractualisé.

## 🧭 Principes

1. La source de vérité métier reste explicitement identifiée pour chaque lot.
2. Toute migration commence par un inventaire et des contrats, jamais par une réécriture implicite.
3. Les sorties Python sont locales et en lecture seule jusqu’à un `GO` humain explicite.
4. Les fonctions MVP et moteur avancé restent découplées.
5. Chaque phase produit des preuves, contrôles et conditions de rollback.

## 🚧 Limites absolues

- aucun auto-trading ;
- aucune exécution broker ;
- aucun sizing ;
- aucune API Revolut dans la référence MVP ;
- aucune écriture live sans `GO` explicite ;
- aucun secret dans les sources, contrats, journaux ou rapports ;
- aucune suppression ou mutation des sources Google.

## 🗺️ Parcours documentaire

- CDC : `../01_CDC/_CDC_MVP_QAIC_PYTHON_MIGRATION_0.1.0.md`
- Architecture cible : `../02_ARCHITECTURE/_ARCHITECTURE_MVP_QAIC_PYTHON_TARGET_0.1.0.md`
- Procédure : `../03_MIGRATION/_PROCEDURE_MIGRATION_MVP_QAIC_VERS_PYTHON_0.1.0.md`
- Mapping : `../03_MIGRATION/_MAPPING_APPS_SCRIPT_TO_PYTHON_MODULES_0.1.0.md`
- Runbook : `../04_RUNBOOKS/_RUNBOOK_MVP_QAIC_PYTHON_REFERENCE_0.1.0.md`

## 📦 Phases

| Phase | Objet | Sortie attendue |
|---|---|---|
| P0 | Référence | Documentation et garde-fous |
| P1 | Miroir d’inventaire | Cartographie des sources, sans mutation |
| P2 | Contrats de données | Schémas, règles et exemples |
| P3 | Squelette package | Structure non exécutable validée |
| P4 | CLI read-only | Rapports locaux uniquement |
| P5 | Tests | Unitaires, contrats, intégration hors live |
| P6 | Export/import | Workflow réversible avec validation humaine |
| P7 | Bridge QAIC optionnel | Interface séparée, désactivée par défaut |

## 🧾 Format batch standard

```text
STATUS
SOURCE_OF_TRUTH
SCOPE
ACTIONS_DONE
OUTPUTS_CREATED
SAFETY_FLAGS
BLOCKERS
NEXT
```

## 🔐 Règle de décision

Toute ambiguïté concernant une source, un schéma, une destination ou une autorisation bloque la mutation. La collecte documentaire et les contrôles locaux peuvent continuer ; toute action live exige une revue humaine et un `GO` traçable.
