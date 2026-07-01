# 🛠️ MVP QAIC — Reflex Runtime & Process Live Reference

Live version: v0.2.7
Policy ID: R16F2H4_REFLEX_RUNTIME_POLICY_LOCK
Readiness Policy ID: R16F2H6_REFLEX_READINESS_ANTI_LOOP_POLICY
Updated: 2026-06-30 23:41:31 UTC

## 🔒 Runtime lock

Reflex preview is locked to Docker pinned + full tracked HEAD copy outside repo + Reflex dev mode.

```text
Container frontend: 3000
Container backend: 8000
Windows preview frontend: 3055
Windows preview backend: 8055
```

## 🧯 Anti-loop readiness lock

Future runners must not loop indefinitely on repeated log tails.

```text
MAX_WAIT_SECONDS=420
MAX_IDENTICAL_LOG_TAIL_REPEATS=2
APP_RUNNING_MARKER_REQUIRED=True
INTERNAL_PORT_DIAGNOSTIC_REQUIRED=True
STOP_CONTAINER_ON_FAILURE=True
```

## 🧭 Documentation fusion lock

For every validated technical process:

1. generate a reference `.md` document;
2. update the relevant `docs/FINAL` live deliverable;
3. use emoji headings in final-facing markdown when useful;
4. keep transient reports under `_RUN_REPORTS`;
5. commit only after guards/tests/staged review.

## ✅ Current validated evidence

- H4 runtime policy was sealed and pushed.
- H5B baseline preview passed with HTTP root ready and route gate OK.
- H6 readiness policy passed guard and tests.

## 🚫 Explicitly forbidden

- NiceGUI fallback for this Reflex chain.
- `.web` source patch as a validation strategy.
- `--env prod`, `--single-port`, `reflex export`, or minimal allowlist as primary preview.
- unbounded log polling.
- reports written into final docs folders without explicit promotion.

<!-- R16F2H7I_RUNNER_HARDENING_START -->
## 🧱 R16F2H7I — Runner hardening process lock

Policy ID: `R16F2H7I_REFLEX_RUNNER_HARDENING_PROCESS_LOCK`
Context: MVP QAIC Reflex runtime process live

### Règles obligatoires pour tout runner futur

- aucun runner sans timeout dur sur chaque sous-commande native.
- aucun docker run sans image preflight.
- aucun docker run sans port preflight.
- aucun docker exec si container non running.
- aucune full copy avec Copy-Item fichier par fichier.
- aucun ZIP sans self-check de structure.
- aucun rapport transitoire dans docs/.

### Contrat d'exécution

- Toute sous-commande native doit être appelée avec timeout dur, sortie capturée, exit code contrôlé.
- `docker run` doit être précédé d'un contrôle image pinned + contrôle ports host.
- `docker exec` est interdit si le container n'est pas `running`.
- La copie full HEAD doit utiliser `git archive HEAD` + extraction tar, jamais `Copy-Item` fichier par fichier.
- Chaque ZIP livré doit contenir un self-check de structure avant action réelle.
- Les rapports de run et diagnostics transitoires vont sous `_RUN_REPORTS`, jamais sous `docs/`.
- Les docs de référence et docs FINAL ne reçoivent que du contenu validé/fusionné.

### Guards requis

- `REFLEX_POLICY_GUARD_OK=True`
- `REFLEX_READINESS_POLICY_GUARD_OK=True`
- `REFLEX_RUNNER_HARDENING_POLICY_GUARD_OK=True`
<!-- R16F2H7I_RUNNER_HARDENING_END -->

