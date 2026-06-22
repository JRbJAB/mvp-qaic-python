# P110B — Human Confirm Canonical Index + Patch Plan

## Decision status

`REVIEW_REQUIRED`

## Top candidate to confirm

- relative_path: `03_DEV/APPS_SCRIPT_PULL_ISOLATED_P57D_20260620_114750/CAND_001/MVPQAIC_Index.html`
- full_path: `G:\Mon Drive\👥 JULIEN [Perso]\📈 Trading JRb\Solutions & Dev (Trading JRb)\📈 QAIC\🛠️ MVP QAIC — Crypto Signal OS\03_DEV\APPS_SCRIPT_PULL_ISOLATED_P57D_20260620_114750\CAND_001\MVPQAIC_Index.html`
- score: `95`
- role: `probable_canonical_apps_script_mirror`

## Confirmation options

- `ACCEPT_TOP_CANDIDATE_AS_CANONICAL` | applies_now=`False` | requires_human=`True`
- `REJECT_TOP_CANDIDATE` | applies_now=`False` | requires_human=`True`
- `SELECT_OTHER_CANDIDATE` | applies_now=`False` | requires_human=`True`
- `NEEDS_MORE_REVIEW` | applies_now=`False` | requires_human=`True`

## Binding patch plan

- **P0 — bind_webapp_pack**: Plan data binding of webapp_pack.json to the confirmed canonical UI shell. apply_now=`False`
- **P0 — bind_context_pack**: Plan context_pack.json binding for lexique/method/prompt context cards. apply_now=`False`
- **P0 — bind_prompt_payload**: Plan prompt_payload.json binding for public human-review prompt flow. apply_now=`False`
- **P1 — preserve_admin_monitor_separation**: Keep ADMIN_MONITOR.html as internal admin/suivi only. apply_now=`False`
- **P0 — keep_public_deploy_blocked**: Do not public deploy until explicit separate authorization. apply_now=`False`

## Forbidden next actions

- `EDIT_INDEX_HTML_NOW`
- `OVERWRITE_INDEX_HTML`
- `GENERATE_PUBLIC_INDEX_HTML`
- `CLASP_PUSH`
- `APPS_SCRIPT_EXECUTION`
- `PUBLIC_DEPLOY_WITHOUT_APPROVAL`
- `BROKER_OR_TRADING_EXECUTION`

## Safety

- HUMAN_CONFIRMATION_REQUIRED
- NO_INDEX_HTML_EDIT
- NO_INDEX_HTML_GENERATION
- NO_PUBLIC_DEPLOY
- NO_CLASP
- NO_APPS_SCRIPT_EXECUTION
- NO_SHEET_WRITE
- NO_BROKER_ORDER_SIZING
