# Tool Registry Changelog

## 2026-06-29 11:37:10 â€” P237B_R4_TOOL_REGISTRY_ROOT_LOCKED_CLEAN_START

- Reprise propre aprÃ¨s nettoyage des artefacts crÃ©Ã©s par erreur sous C:\Users\Julie.
- Ajout d'un garde-fou dur sur C:\JRb_TRADING_OS\MVP_QAIC_PY.
- CrÃ©ation des documents Tool Registry.
- CrÃ©ation des JSON globaux/projet.
- CrÃ©ation du snapshot read-only.
- CrÃ©ation du CSV d'audit.
- CrÃ©ation d'un test de contrat minimal.
- Aucune modification Reflex.
## P237C_ROOT_LOCK_EXPORT_HYGIENE_GUARD — 20260629_132034

- Added root-lock and export hygiene policy.
- Enforced desktop.ini ignore rule.
- Added repository hygiene contract test.
- No Reflex file modification.

## P237C_R2_ROOT_LOCK_EXPORT_HYGIENE_GUARD_UTF8_FIX — 20260629_132608

- Fixed Windows/Python Unicode decode issue in hygiene contract test.
- Replaced implicit cp1252 text decoding with explicit UTF-8 bytes decoding and errors="replace".
- Kept root-lock and export hygiene guard.
- No Reflex file modification.
