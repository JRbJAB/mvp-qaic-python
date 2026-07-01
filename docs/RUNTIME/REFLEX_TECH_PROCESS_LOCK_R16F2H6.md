# R16F2H6 - Reflex Technical Process Lock

Policy ID: R16F2H4_REFLEX_RUNTIME_POLICY_LOCK
Readiness Policy ID: R16F2H6_REFLEX_READINESS_ANTI_LOOP_POLICY
Live version: v0.2.7
Updated: 2026-06-30 23:41:31 UTC

## Locked runtime foundation

- Reflex only.
- Docker pinned image only for preview gates.
- Full tracked HEAD copy outside the repo.
- Primary preview command remains:

```text
python -m reflex run --env dev --backend-host 0.0.0.0 --backend-port 8000 --frontend-port 3000
```

- Windows preview mapping remains:

```text
host 3055 -> container 3000
host 8055 -> container 8000
```

## Readiness anti-loop lock

Every future Reflex preview runner must print both guards before action:

```text
REFLEX_POLICY_GUARD_OK=True
REFLEX_READINESS_POLICY_GUARD_OK=True
```

Mandatory readiness behavior:

```text
MAX_WAIT_SECONDS=420
MAX_IDENTICAL_LOG_TAIL_REPEATS=2
APP_RUNNING_MARKER_REQUIRED=True
INTERNAL_PORT_DIAGNOSTIC_REQUIRED=True
STOP_CONTAINER_ON_FAILURE=True
```

Forbidden readiness behavior:

- unbounded `LOG_TAIL_START` / `LOG_TAIL_END` loops;
- more than two identical log tails;
- waiting after `App Running` without internal and host port diagnostics;
- silent `RemoteDisconnected` spam;
- dynamic port fallback;
- patching the real repo before visual validation.

## Reference-doc process lock

Every meaningful technical validation must produce or update a reference `.md` document under `docs/RUNTIME` or `docs/PROCESS`.

Every final user-facing process that is relevant to delivery must also be fused into `docs/FINAL`.

Final docs rules:

- Markdown only.
- Emoji headings are allowed and expected in FINAL deliverables.
- Maintain a live version section.
- Prefer marked fusion blocks so future runners update the same section instead of duplicating content.
- Runtime reports, probes, logs and transient files must stay under `_RUN_REPORTS`, not under `docs/drive_reconcile` or `docs/FINAL` unless explicitly promoted as final reference material.

## Seal rule

No commit/tag/push unless:

1. runtime guard passes;
2. readiness guard passes;
3. targeted tests pass;
4. staged files are explicitly listed;
5. final status prints the commit and tag.

<!-- R16F2H7I_RUNNER_HARDENING_START -->
## 🧱 R16F2H7I — Runner hardening process lock

Policy ID: `R16F2H7I_REFLEX_RUNNER_HARDENING_PROCESS_LOCK`
Context: Reflex technical process lock

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
