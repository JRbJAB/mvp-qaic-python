# 🛠️ MVP QAIC — P2-C Frontend Rename Corrected Standalone

## Statut
SAFE_CORRECTED — ne pas utiliser le pack précédent `MVP_QAIC_P2C_FRONTEND_RENAME_SAFE_FALLBACKS_0.8.0_SAFE`.

## Correction de responsabilité
- `mvpqaic_11_p1_prompt_quality_core.gs` reste le core prompt.
- Il reçoit seulement la compatibilité old/new names.
- Les fonctions de renommage sont dans `mvpqaic_22_frontend_sheet_rename_migration_core.gs`.

## Ordre
1. Installer `mvpqaic_11_p1_prompt_quality_core.gs` version alias-only.
2. Installer `mvpqaic_22_frontend_sheet_rename_migration_core.gs`.
3. Lancer `MVPQAIC_FrontendRenameMigrationStatus()`.
4. Lancer `MVPQAIC_FrontendRenameMigrationDryRun()`.
5. Si clean, lancer `MVPQAIC_FrontendRenameMigrationApplySafe()`.
6. Contrôler `MVPQAIC_PromptQualityCoreStatus()` et `MVPQAIC_PromptAdaptiveLoopStatus()`.

## Safety
No delete, no hide, no overwrite, no menu mutation, no trigger mutation, no broker, no order, no sizing, no secret.
