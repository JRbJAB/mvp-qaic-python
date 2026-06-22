# P138A — Python Ultimate Process Simplification

Status: `PYTHON_ULTIMATE_PROCESS_SIMPLIFICATION_READY`

## Objectif

Remplacer le process Sheets fragmenté par une migration Python canonique, validée, puis écrite dans Sheets après GO.

## Problèmes du process Sheets d'origine

- prompts répartis dans plusieurs onglets
- variantes, queues, runtime specs et output contracts séparés
- risque de corriger le mauvais prompt
- historique utile mais difficile à exploiter directement
- write Sheets dangereux sans provenance, hash, validation et plan ligne par ligne

## Process cible Python

- read old Sheets base once
- normalize all source tabs into one canonical registry
- hash every source row and prompt body
- deduplicate references and variants
- preserve locked reference prompts
- apply P137 corrections as local candidate, not as blind overwrite
- build a deterministic Sheets write plan
- block write until validation GO
- write to Sheets with run_id/source_hash/migration_status only after approval

## Règles de simplification ultime

- `single_registry`: one canonical PromptMigrationCandidate table
- `single_gate`: P138B validates blockers before any write
- `single_write_plan`: P138C writes only approved rows
- `single_traceability`: source_tab + source_row + source_hash + run_id on every migrated row
- `single_safety_contract`: no broker/order/sizing/auto apply for all prompts

## Politique write Sheets

- `p138a`: `NO_SHEETS_WRITE`
- `p138b`: `NO_SHEETS_WRITE_VALIDATE_ONLY`
- `p138c`: `SHEETS_WRITE_AFTER_EXPLICIT_GO_ONLY`
