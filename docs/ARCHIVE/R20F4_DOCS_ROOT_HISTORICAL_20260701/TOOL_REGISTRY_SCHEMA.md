# Tool Registry Schema

| Champ | Description |
|---|---|
| tool_id | Identifiant stable et unique |
| name | Nom lisible |
| category | runtime, framework, dev_tool, google_service, project_module, locked_external |
| projects | Projets concernÃ©s |
| version_expected | Version attendue ou politique de version |
| version_detected | Version dÃ©tectÃ©e localement si disponible |
| functional_role | RÃ´le fonctionnel dans MVP QAIC |
| features_used | FonctionnalitÃ©s utilisÃ©es |
| settings | ParamÃ¨tres fonctionnels importants |
| safety_flags | Garde-fous explicites |
| status | ACTIVE_PRIVATE, READONLY_OR_MANUAL, LEGACY_READONLY, REVIEW, BLOCKED |
| last_verified_at | Date de vÃ©rification |
| verification_source | Source de vÃ©rification |

## Invariants

- Une capacitÃ© externe dangereuse doit rester dÃ©sactivÃ©e par dÃ©faut.
- Une intÃ©gration UI Reflex doit Ãªtre sÃ©parÃ©e du registre docs/data.
- Aucun outil ne doit impliquer broker/order/sizing cÃ´tÃ© MVP.