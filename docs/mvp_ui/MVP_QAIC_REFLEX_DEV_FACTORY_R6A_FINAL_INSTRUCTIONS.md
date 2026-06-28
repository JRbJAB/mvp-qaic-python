# MVP QAIC Reflex Dev Factory R6A â€” Instructions finales

## Objectif

Stabiliser le dÃ©veloppement Reflex MVP QAIC pour migrer/activer des cockpits rapidement sans rÃ©pÃ©ter les mÃªmes erreurs serveur, route 404, vieux runtime, npm/bun/rolldown ou faux commit OK.

## RÃ¨gles non nÃ©gociables

- Reflex conservÃ©.
- Aucun test runtime sur un vieux dossier par dÃ©faut.
- Toujours tester depuis `git archive HEAD` vers un runtime frais hors Drive.
- Commit/tag/push uniquement aprÃ¨s gate OK.
- Aucun deploy public.
- Aucun broker/order/sizing.
- Aucun write Sheet/BigQuery.
- Human-review only.

## Process cockpit rapide

Un cockpit = 3 Ã©tapes :

1. Page + route source.
2. `scripts/REFLEX_FAST_GATE.ps1 -Route "/route-cible"`.
3. Commit/tag/push seulement si la route rÃ©pond HTTP OK.

## Diagnostic standard

- `404` avec `/` en `200` = problÃ¨me de route/app registry, pas serveur.
- erreur npm/bun/rolldown = problÃ¨me frontend deps, pas page Python.
- syntax/import error = patch Python uniquement.
- vieux runtime = relancer fresh HEAD, pas modifier code.

## Interdits process

- Ne plus utiliser `P_REFLEX_06C_20260625_200632` comme runtime par dÃ©faut pour routes rÃ©centes.
- Ne plus empiler plusieurs corrections sans gate.
- Ne plus crÃ©er de faux OK si probe HTTP KO.
- Ne plus modifier les scripts serveur pour une 404 route.

## Gate unique

Commande standard :

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File "$repo\scripts\REFLEX_FAST_GATE.ps1" -Route "/cdc-dev-tracker"
```

Mode source/runtime sans dÃ©marrer serveur :

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File "$repo\scripts\REFLEX_FAST_GATE.ps1" -Route "/cdc-dev-tracker" -NoRuntimeStart
```

## Next

Utiliser R6A comme base pour migrer les cockpits suivants :

- CDC Dev Tracker
- Global Migration Matrix
- Prompt Review Cockpit
- Portfolio Human Review Cockpit