# MVP QAIC Reflex Fast Gate R6A â€” Runbook

## Commande standard

```powershell
$people = [char]::ConvertFromUtf32(0x1F465)
$chart  = [char]::ConvertFromUtf32(0x1F4C8)

$repo = [IO.Path]::Combine(
  "G:\Mon Drive",
  "$people JULIEN [Perso]",
  "$chart Trading JRb",
  "Solutions & Dev (Trading JRb)",
  "MVP_QAIC_PY"
)

powershell -NoProfile -ExecutionPolicy Bypass -File "$repo\scripts\REFLEX_FAST_GATE.ps1" -Route "/cdc-dev-tracker"
```

## Si 404

Ne pas toucher npm/bun. Patch `app.add_page` ou le registry route.

## Si frontend deps

Relancer le start script avec `-CleanWeb`, ou laisser le fast gate utiliser le start script R5L/R5M.

## Si vieux runtime

Le fast gate reconstruit automatiquement un runtime frais depuis HEAD.

## Statut attendu

`STATUS=OK_R6A_REFLEX_FAST_GATE_RUNTIME_ROUTE_UP`