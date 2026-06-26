# P_REFLEX_12F_R17_POLICY_DUAL_CONTRACT_FINAL

R17 final fix: resolve contradictory R11 equality and R14 substring policy tests with a dual-compatible string policy marker, without changing UI behavior.

- `migration_os.py` owns data contract and backward-compatible symbols.
- `migration_tracker.py` owns Reflex table rendering only.
- Legacy 15 rows are preserved.
- Visible rows are deduplicated and limited to essential entries.
- Raw 2738 function index entries are not displayed in Mission Control.
