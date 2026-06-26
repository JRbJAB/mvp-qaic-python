# P_REFLEX_12F_R15_MIGRATION_OS_BACKCOMPAT_FINAL_SEAL

Final consolidation of the migration tracker stack.

- `migration_os.py` owns data contract and backward-compatible symbols.
- `migration_tracker.py` owns Reflex table rendering only.
- Legacy 15 rows are preserved.
- Visible rows are deduplicated and limited to essential entries.
- Raw 2738 function index entries are not displayed in Mission Control.
