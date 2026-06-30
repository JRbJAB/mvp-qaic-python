# R18B Drive root desktop.ini archive resume

- Scope: local sync Drive root Windows noise only.
- No delete, no reset, no git add dot.
- Accepts prior R18 failed-report residue and UI/config dirty only.
- Moves `desktop.ini` from Drive root to `99_ARCHIVES/R18B_ROOT_DESKTOP_INI_NOISE_*` when possible.
- If Windows recreates `desktop.ini`, the report marks it explicitly; no false clean claim.
