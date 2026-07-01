# 🛠️ MVP QAIC — Reflex Runtime & Process Live Reference

Live version: v0.2.8
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

<!-- BEGIN_REFLEX_H8I_HARD_PROCESS_LOCK -->
## REFLEX H8I HARD PROCESS LOCK

- Pinned image: `jrb-reflex-pinned-hub:py312-node22-reflex096p1`.
- Pinned Reflex version: `Reflex 0.9.6.post1`.
- Never propose, modify, or launch Reflex commands from memory.
- The real `python -m reflex run --help` output from the pinned image is the only source of truth for CLI flags.
- Authorized command shape: `python -m reflex run --env dev --backend-host 0.0.0.0 --backend-port 8000 --frontend-port 3000`.
- Forbidden flag because it is absent from the real help: `--frontend-host`.
- `--frontend-host` is forbidden and must never appear in an allowed command.
- Required local preview port mappings: `127.0.0.1:3055:3000` and `127.0.0.1:8055:8000`.
- Runtime remains forbidden unless explicitly approved by operator.
- Manual preview URL only after HTTP smoke pass: `http://127.0.0.1:3055/`.
- TCP-only port checks are not success.
- Use temporary runtime copy outside source repo: `C:\JRb_TRADING_OS\_RUNTIME_TMP\`.
- Store evidence under: `C:\JRb_TRADING_OS\_RUN_REPORTS\`.
- No browser open, no public deploy, no provider call, no broker/order/sizing, no Sheet/BQ write, no Apps Script execution, no clasp push.
- After any Reflex failure: stop runtime, capture logs, capture docker inspect, capture command used, capture Reflex version, capture Reflex run help, capture repo status, and do not relaunch.

Required guard constants:

```text
REFLEX_CLI_HELP_CAPTURE_REQUIRED=True
NO_FRONTEND_HOST_FLAG=True
STOP_AND_AUDIT_READONLY
NO_HELP = NO_RUNTIME
HELP_FLAG_MISSING = COMMAND_FORBIDDEN
TCP_ONLY = NOT_PREVIEW_READY
HTTP_FAIL = STOP_AND_DIAG
SOURCE_REPO_DIRTY_AFTER_RUNTIME = RUNTIME_INVALID
PREVIEW_ONLY_AFTER_HTTP_PASS = TRUE
```
<!-- END_REFLEX_H8I_HARD_PROCESS_LOCK -->

## R21B_REFLEX_RUNTIME_CLOSURE - 2026-07-01

- REFLEX_RUNTIME_STATUS=PAUSED
- REFLEX_RUNTIME_RUNNER_CHAIN=STOPPED
- H9H_H9I_H9K_CHAIN=CLOSED_FAILED_NO_COMMIT_ROLLBACK_DONE
- STOP_DEV_PREVIEW_RETRY_AFTER_HTTP_BODY_ZERO=True
- STOP_CODEX_RUNTIME_RUNNER_GENERATION_UNTIL_RUNNER_AUDITED=True
- NO_MICRO_FIX_LOOP=True
- ONE_BATCH_ONE_DECISION=True
- NO_DOCKER_RM_ON_FAILURE=True
- PS51_RUNNER_REVIEW_REQUIRED_BEFORE_EXECUTION=True
- NO_COMMIT_BEFORE_HTTP_PREVIEW_OK=True
- FALLBACK_STATIC_WYSIWYG_ALLOWED=True
- REFLEX_ALLOWED_NEXT_ONLY_AFTER_HUMAN_RUNNER_REVIEW=True
- Memo: docs/FINAL/R21B_REFLEX_RUNTIME_CLOSURE_STRATEGY_AND_INSTRUCTIONS_MEMO_20260701.md
