# MVP QAIC — Final Reference Seal v0.2.6

Generated: 20260630_202410

## Status

`OK_FINAL_REFERENCE_v0.2.6_VERIFIED`

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

