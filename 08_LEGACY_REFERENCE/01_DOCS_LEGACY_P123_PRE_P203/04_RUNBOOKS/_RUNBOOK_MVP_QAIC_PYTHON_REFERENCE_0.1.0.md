# 🧰 Runbook MVP QAIC Python Reference 0.1.0

## ▶️ Démarrer un lot

1. Lire le README, le CDC, l’architecture et la procédure.
2. Déclarer `SOURCE_OF_TRUTH`, `SCOPE` et les drapeaux de sécurité.
3. Vérifier que le travail utilise seulement des artefacts locaux autorisés.
4. Confirmer que la phase demandée autorise l’action.
5. Refuser toute donnée secrète ou instruction live non approuvée.

## ✅ Contrôles P0

- La racine de travail est confirmée.
- Tous les dossiers de référence sont présents.
- Les sept livrables P0.7.6 sont présents.
- Le JSON du manifeste est syntaxiquement valide.
- Aucun fichier Python exécutable, dépôt Git, appel réseau ou mutation live n’est créé.
- Le rapport contient un arbre compact et les limites de validation.

## 🚦 Matrice d’autorisation

| Action | Par défaut | Condition future |
|---|---|---|
| Lire un export local approuvé | Autorisé | provenance tracée |
| Générer un rapport local | Autorisé | aucune donnée sensible |
| Appeler Google/API réseau | Interdit | hors P0, procédure dédiée |
| Écrire dans Sheets/live | Interdit | P6 + `GO` humain explicite |
| Exécuter Apps Script/clasp | Interdit | procédure distincte approuvée |
| Broker, ordre, sizing, Revolut | Interdit | hors périmètre MVP |

## 🧯 Incident et rollback

Arrêter le traitement, préserver le manifeste et les preuves, marquer la sortie invalide, isoler les artefacts en sandbox sans les exécuter, et confirmer que la source est inchangée. Ne jamais supprimer pour « nettoyer ». Toute restauration future doit suivre un plan pré-approuvé.

## 🧾 Clôturer un lot

```text
STATUS: COMPLETE | PARTIAL | BLOCKED
SOURCE_OF_TRUTH: chemin/version/empreinte
SCOPE: phase et domaines
ACTIONS_DONE: actions locales vérifiées
OUTPUTS_CREATED: chemins exacts
SAFETY_FLAGS: interdictions respectées
BLOCKERS: limites ou écarts
NEXT: prochaine porte de contrôle
```
