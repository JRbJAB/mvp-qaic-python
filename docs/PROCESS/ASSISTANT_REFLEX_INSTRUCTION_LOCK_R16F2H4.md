# Assistant Instruction Lock - MVP QAIC Reflex

Policy ID: R16F2H4_REFLEX_RUNTIME_POLICY_LOCK

Every future MVP QAIC Reflex / UI preview / runtime / Docker response must contain:
POLICY_ID=R16F2H4_REFLEX_RUNTIME_POLICY_LOCK
REFLEX_POLICY_GUARD_REQUIRED=True

Assistant rules:

1. Read and apply config/reflex_runtime_policy.json.
2. Use only Reflex dev + Docker pinned + full tracked HEAD copy + ports 3055/8055 for primary UI preview.
3. Never propose --env prod, --single-port, reflex export, or a minimal allowlist as primary UI preview.
4. Require REFLEX_POLICY_GUARD_OK=True before any future runner.
5. Never patch the real repo before visual validation.
6. Never commit/tag/push without explicit human approval.
7. Cite official Reflex documentation for any Reflex command/config change.
8. If a policy conflict appears: stop and run readonly audit first.

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
Context: Assistant Reflex instruction lock

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

