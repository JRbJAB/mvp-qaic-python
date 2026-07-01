# 🧱 R16F2H7I — Reflex Runner Hardening Policy

Policy ID: `R16F2H7I_REFLEX_RUNNER_HARDENING_PROCESS_LOCK`
Parent policy: `R16F2H4_REFLEX_RUNTIME_POLICY_LOCK`
Readiness policy: `R16F2H6_REFLEX_READINESS_ANTI_LOOP_POLICY`
Status: `LOCKED_FOR_FUTURE_RUNNERS`

## Décision verrouillée

Les erreurs répétées de wrappers, ports, Docker, `Copy-Item`, chemins spéciaux, ZIP mal structuré et boucles d'attente doivent être traitées avant tout runtime.

## Règles obligatoires

- aucun runner sans timeout dur sur chaque sous-commande native.
- aucun docker run sans image preflight.
- aucun docker run sans port preflight.
- aucun docker exec si container non running.
- aucune full copy avec Copy-Item fichier par fichier.
- aucun ZIP sans self-check de structure.
- aucun rapport transitoire dans docs/.
- aucun commit/tag/push apres tests echoues.
- aucun runner pack sans self-test.
- aucun chemin payload ZIP avec emoji.
- aucun patch PowerShell inline long.
- Codex requis apres deux echecs repetes sur le meme workstream.

## Implémentation attendue

| Domaine | Règle imposée |
|---|---|
| Native commands | Timeout dur par sous-commande, capture stdout/stderr, exit code explicite |
| Docker image | Preflight image pinned avant `docker run` |
| Docker ports | Preflight ports host avant `docker run` |
| Docker exec | Autorisé uniquement si container `running` |
| Full HEAD copy | `git archive HEAD` + tar extract uniquement |
| ZIP | Self-check structure avant action |
| Rapports | `_RUN_REPORTS` uniquement pour tout transitoire |
| Docs | `docs/` réservé aux références/final docs validées |
| Git release | Aucun commit/tag/push apres tests echoues |
| Runner pack | Self-test obligatoire avant livraison |
| ZIP payload | Chemins payload sans emoji |
| PowerShell patch | Pas de patch inline long |
| Repeated failures | Codex requis apres deux echecs repetes sur le meme workstream |

## Sorties minimales futures

```text
REFLEX_POLICY_GUARD_OK=True
REFLEX_READINESS_POLICY_GUARD_OK=True
REFLEX_RUNNER_HARDENING_POLICY_GUARD_OK=True
NATIVE_TIMEOUT_REQUIRED=True
DOCKER_IMAGE_PREFLIGHT_REQUIRED=True
DOCKER_PORT_PREFLIGHT_REQUIRED=True
DOCKER_EXEC_RUNNING_REQUIRED=True
FULL_HEAD_COPY_METHOD=git_archive_head_tar_extract
ZIP_STRUCTURE_SELF_CHECK_REQUIRED=True
TRANSIENT_REPORTS_FORBIDDEN_UNDER_DOCS=True
NO_COMMIT_TAG_PUSH_AFTER_FAILED_TESTS_REQUIRED=True
RUNNER_PACK_SELF_TEST_REQUIRED=True
ZIP_PAYLOAD_PATHS_EMOJI_FREE_REQUIRED=True
INLINE_LONG_POWERSHELL_PATCH_FORBIDDEN=True
CODEX_REQUIRED_AFTER_TWO_REPEATED_WORKSTREAM_FAILURES=True
```

## Décision opérationnelle

Aucun runner Reflex / Docker / runtime ne doit être proposé ou exécuté sans respecter cette politique.
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
