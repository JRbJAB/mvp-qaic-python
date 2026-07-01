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
```

## Décision opérationnelle

Aucun runner Reflex / Docker / runtime ne doit être proposé ou exécuté sans respecter cette politique.
