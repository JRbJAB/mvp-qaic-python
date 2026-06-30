# 🛠️ MVP QAIC — Comparatif CLASP/Git Export 0.1.1 vs QAIC V25 V5.4.4

## Décision

Le fichier MVP QAIC 0.1.0 était une base fonctionnelle, mais plus légère que le modèle QAIC V25. La version 0.1.1 reprend les garde-fous structurants du script QAIC : chemin projet borné, RUN-* + latest, audit de garde fonctions, Git local, CSV unique importable, pull CLASP read-only et interdiction explicite de push/clone/exécution live.

## Points repris du modèle QAIC

- Chemin projet par défaut borné, sans scan global `G:\Mon Drive`.
- Dossier `RUN-yyyymmdd-hhmmss` pour chaque export.
- CSV latest séparé du run d’audit.
- Audit de fonctions publiques critiques.
- Log `clasp_pull_output.txt`.
- Log `git_status_after_commit.txt`.
- Résumé JSON exploitable.
- Git local dans le miroir Apps Script.
- Aucun `clasp push`, aucun `clasp clone`.
- Export CSV consolidé importable dans Sheets.

## Différences volontaires

- Le MVP QAIC reste plus simple que QAIC V25 : pas de garde spécifique MarketScores / AlphaSignal / chaîne V25.
- Pas de BigQuery, pas d’agent, pas de portefeuille réel, pas de broker.
- Les guards P1-G/registry sont partiellement optionnels pour ne pas bloquer si le live n’a pas encore été remplacé.
- La couche registry cible `MVPQAIC_SCRIPT_REGISTRY` et `⬇️ MVPQAIC_CLASP_IMPORTS`, pas les onglets V25.

## Statut recommandé

Utiliser `MVPQAIC_CLASP_GIT_EXPORT_ANALYSIS.ps1` version `0.1.1_QAIC_INSPIRED_PINNED_PATH_SAFE` à la place de la 0.1.0.
