# MVP QAIC — Final Reference Seal v0.2.7



Generated: 20260630_202410



## Status



`OK_FINAL_REFERENCE_v0.2.7_VERIFIED`



## Verified current reference files



- `MVP_QAIC_INSTRUCTIONS_GOVERNANCE_FINAL_FUSED_v0.2.6.md`

- `MVP_QAIC_CDC_CONTRACT_FINAL_FUSED_v0.2.6.md`

- `MVP_QAIC_NOTICE_RUNBOOK_FINAL_FUSED_v0.2.6.md`

- `MVP_QAIC_PROMPT_GEM_WORKFLOW_FINAL_FUSED_v0.2.6.md`

- `MVP_QAIC_LEXIQUE_REFERENCE_FINAL_FUSED_v0.2.6.md`

- `MVP_QAIC_WEB_ARCHITECTURE_UI_PROCESS_FINAL_FUSED_v0.2.6.md`



## Safety



- No deletion.

- No Drive write.

- No `git add .`.

- Previous source/inbox files are preserved as evidence.



<!-- R16F2H6_PROCESS_LOCK_START -->

## 🛠️ R16F2H6 — Reflex runtime/process live lock



Live version: v0.2.7

Policy ID: `R16F2H4_REFLEX_RUNTIME_POLICY_LOCK`

Readiness Policy ID: `R16F2H6_REFLEX_READINESS_ANTI_LOOP_POLICY`

Updated: 2026-06-30 23:41:31 UTC



Validated process now locked:



- Reflex-only runtime preview.

- Docker pinned preview with full tracked HEAD copy outside repo.

- Container ports `3000/8000`; Windows preview ports `3055/8055`.

- Mandatory `REFLEX_POLICY_GUARD_OK=True` and `REFLEX_READINESS_POLICY_GUARD_OK=True` before future runners.

- Anti-loop readiness: max wait, max two identical log tails, internal/host port diagnostic, stop container on failure.

- Reference `.md` generated for validated technical process.

- Relevant `docs/FINAL` deliverables updated through marked fusion blocks.

- Transient logs/reports remain in `_RUN_REPORTS`; FINAL receives only promoted reference content.

<!-- R16F2H6_PROCESS_LOCK_END -->



<!-- R16F2H7I_RUNNER_HARDENING_START -->

## 🧱 R16F2H7I — Runner hardening process lock



Policy ID: `R16F2H7I_REFLEX_RUNNER_HARDENING_PROCESS_LOCK`

Context: MVP QAIC reference final seal



### Règles obligatoires pour tout runner futur



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


### Contrat d'exécution



- Toute sous-commande native doit être appelée avec timeout dur, sortie capturée, exit code contrôlé.

- `docker run` doit être précédé d'un contrôle image pinned + contrôle ports host.

- `docker exec` est interdit si le container n'est pas `running`.

- La copie full HEAD doit utiliser `git archive HEAD` + extraction tar, jamais `Copy-Item` fichier par fichier.

- Chaque ZIP livré doit contenir un self-check de structure avant action réelle.
- Les rapports de run et diagnostics transitoires vont sous `_RUN_REPORTS`, jamais sous `docs/`.
- Les docs de référence et docs FINAL ne reçoivent que du contenu validé/fusionné.
- Aucun commit/tag/push n'est autorisé après tests échoués.
- Aucun runner pack généré ne peut être livré sans self-test.
- Aucun chemin payload ZIP ne doit contenir un emoji.
- Aucun patch PowerShell inline long n'est autorisé.
- Codex est requis après deux échecs répétés sur le même workstream.

### Guards requis

- `REFLEX_POLICY_GUARD_OK=True`
- `REFLEX_READINESS_POLICY_GUARD_OK=True`
- `REFLEX_RUNNER_HARDENING_POLICY_GUARD_OK=True`
- `NO_COMMIT_TAG_PUSH_AFTER_FAILED_TESTS_REQUIRED=True`
- `RUNNER_PACK_SELF_TEST_REQUIRED=True`
- `ZIP_PAYLOAD_PATHS_EMOJI_FREE_REQUIRED=True`
- `INLINE_LONG_POWERSHELL_PATCH_FORBIDDEN=True`
- `CODEX_REQUIRED_AFTER_TWO_REPEATED_WORKSTREAM_FAILURES=True`
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

<!-- BEGIN_R21F_DRIVE_FIRST_REFERENCE_LOCK -->
## R21F_DRIVE_FIRST_REFERENCE_LOCK - 2026-07-01

- DRIVE_LIVE_ACCESS=True
- DRIVE_SOURCE_OF_TRUTH_REQUIRED=True
- READ_CURRENT_REFERENCE_INDEX_BEFORE_PROJECT_BATCH=True
- READ_FINAL_DOCS_BEFORE_PROJECT_BATCH=True
- READ_CDC_TOOL_REGISTRY_UI_TRACKER_REFERENCES_BEFORE_PATCH=True
- NO_MEMORY_ONLY=True
- NO_APPROXIMATION=True
- NO_BATCH_WITHOUT_REFERENTIAL_AUDIT=True
- NO_RUNTIME_OR_CODEX_RUNNER_BEFORE_RELEVANT_REFERENCES_AUDITED=True
- REQUIRED_ORDER=Drive source of truth -> CURRENT_REFERENCE_INDEX -> active final docs -> CDC/tool registry/UI tracker references -> batch plan
- Scope: MVP QAIC / QAIC / QAIT project work.
- Memo: docs/FINAL/R21F_DRIVE_FIRST_REFERENCE_LOCK_MEMO_20260701.md
<!-- END_R21F_DRIVE_FIRST_REFERENCE_LOCK -->
