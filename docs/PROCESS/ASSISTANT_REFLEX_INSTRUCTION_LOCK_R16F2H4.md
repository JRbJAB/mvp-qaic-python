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
