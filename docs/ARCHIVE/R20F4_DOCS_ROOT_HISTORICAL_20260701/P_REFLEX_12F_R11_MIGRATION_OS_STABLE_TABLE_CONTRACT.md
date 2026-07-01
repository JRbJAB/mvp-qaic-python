# P_REFLEX_12F_R11_MIGRATION_OS_STABLE_TABLE_CONTRACT

Purpose: stop micro-fixes by introducing a stable Python migration OS contract.

Rules:
- Preserve the legacy 15 migration tracker rows.
- Preserve table UX: Type / Source / Cible / % / Statut.
- Use the global matrix as a live input, but never display the raw 2794 rows in Mission Control.
- Group/deduplicate Apps Script functions.
- Keep `/migration/global` only as drill-down.
- No server start by batch.
- Runtime hot sync only.
