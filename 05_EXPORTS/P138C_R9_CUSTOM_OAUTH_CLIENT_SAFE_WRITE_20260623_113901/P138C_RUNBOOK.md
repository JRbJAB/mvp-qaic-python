# P138C — Safe Partial Sheets Write

Status: `P138C_APPLY_REQUESTED`
Safe candidate count: `9`

## Target sheets

- `📘 PROMPT_LIBRARY`: `9` rows

## Write rules

- Explicit GO required.
- Append only or skip duplicate by `migration_id` / `source_hash`.
- No blocked rows.
- No duplicate-review rows.
- No locked-reference overwrite.
- Backup CSV exported before write.
