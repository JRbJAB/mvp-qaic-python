# P_REFLEX_12F_R16_MIGRATION_OS_COMPAT_FINAL_FIX

Final compatibility fix after R15: restore every R9B/R10/R11 marker and keep Migration OS stable.

- `migration_os.py` owns data contract and backward-compatible symbols.
- `migration_tracker.py` owns Reflex table rendering only.
- Legacy 15 rows are preserved.
- Visible rows are deduplicated and limited to essential entries.
- Raw 2738 function index entries are not displayed in Mission Control.
