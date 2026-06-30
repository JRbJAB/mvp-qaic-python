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
