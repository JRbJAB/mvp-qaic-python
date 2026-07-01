# 🧱 MVP QAIC — Runner Hardening Process LIVE v0.2.8

Policy ID: `R16F2H7I_REFLEX_RUNNER_HARDENING_PROCESS_LOCK`
Mode: `LIVE_PROCESS_LOCK`

## ✅ Process runner validé

- ✅ aucun runner sans timeout dur sur chaque sous-commande native.
- ✅ aucun docker run sans image preflight.
- ✅ aucun docker run sans port preflight.
- ✅ aucun docker exec si container non running.
- ✅ aucune full copy avec Copy-Item fichier par fichier.
- ✅ aucun ZIP sans self-check de structure.
- ✅ aucun rapport transitoire dans docs/.
- ✅ aucun commit/tag/push apres tests echoues.
- ✅ aucun runner pack sans self-test.
- ✅ aucun chemin payload ZIP avec emoji.
- ✅ aucun patch PowerShell inline long.
- ✅ Codex requis apres deux echecs repetes sur le meme workstream.

## 🚦 Gates obligatoires avant runtime

```text
REFLEX_POLICY_GUARD_OK=True
REFLEX_READINESS_POLICY_GUARD_OK=True
REFLEX_RUNNER_HARDENING_POLICY_GUARD_OK=True
ZIP_STRUCTURE_OK=True
FULL_HEAD_COPY_METHOD=git_archive_head_tar_extract
DOCKER_IMAGE_PREFLIGHT_OK=True
DOCKER_PORT_PREFLIGHT_OK=True
NO_COMMIT_TAG_PUSH_AFTER_FAILED_TESTS_REQUIRED=True
RUNNER_PACK_SELF_TEST_REQUIRED=True
ZIP_PAYLOAD_PATHS_EMOJI_FREE_REQUIRED=True
INLINE_LONG_POWERSHELL_PATCH_FORBIDDEN=True
CODEX_REQUIRED_AFTER_TWO_REPEATED_WORKSTREAM_FAILURES=True
```

## 🛑 Stop conditions

- Image Docker pinned absente.
- Port preview occupé sans cleanup explicitement autorisé.
- Container non running avant `docker exec`.
- Deux log tails identiques sans diagnostic nouveau.
- Rapport transitoire tenté sous `docs/`.
- ZIP sans structure attendue.
- Tests echoues avant commit/tag/push.
- Runner pack genere sans self-test.
- Chemin payload ZIP avec emoji.
- Patch PowerShell inline long.
- Troisieme tentative non-Codex apres deux echecs repetes sur le meme workstream.

## 📁 Rangement

- Rapports de run: `C:\JRb_TRADING_OS\_RUN_REPORTS\MVP_QAIC_PY`
- Copies runtime: `C:\JRb_TRADING_OS\_RUNTIME_PINNED`
- Docs validées: `docs/RUNTIME`, `docs/PROCESS`, `docs/FINAL`

## 🧾 Statut

`OK_R16F2H7I_RUNNER_HARDENING_PROCESS_LOCKED`
