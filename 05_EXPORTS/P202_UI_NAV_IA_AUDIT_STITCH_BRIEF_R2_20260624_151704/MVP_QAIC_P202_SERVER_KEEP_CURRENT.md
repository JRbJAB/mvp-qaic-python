# MVP QAIC — Garder le serveur ouvert et à jour

## Principe

Garde une fenêtre PowerShell dédiée au serveur : MVP QAIC SERVER.
Ne développe pas dans cette fenêtre.

## Lancer sans pull

powershell -NoExit -ExecutionPolicy Bypass -File "C:\Users\Julie\Documents\JRb-Dev\MVP_QAIC_PY_WORK_20260623_192901\00_OPERATOR_SHORTCUTS\START_MVP_QAIC_SERVER_CURRENT.ps1"

## Mettre à jour puis relancer

powershell -NoExit -ExecutionPolicy Bypass -File "C:\Users\Julie\Documents\JRb-Dev\MVP_QAIC_PY_WORK_20260623_192901\00_OPERATOR_SHORTCUTS\START_MVP_QAIC_SERVER_CURRENT.ps1" -Pull

## Stopper

powershell -ExecutionPolicy Bypass -File "C:\Users\Julie\Documents\JRb-Dev\MVP_QAIC_PY_WORK_20260623_192901\00_OPERATOR_SHORTCUTS\STOP_MVP_QAIC_SERVER_8080.ps1"

## Vérifier

powershell -ExecutionPolicy Bypass -File "C:\Users\Julie\Documents\JRb-Dev\MVP_QAIC_PY_WORK_20260623_192901\00_OPERATOR_SHORTCUTS\STATUS_MVP_QAIC_SERVER_8080.ps1"

## Règle

Après chaque batch qui modifie l'UI : Ctrl+C dans le serveur, puis relancer.
Ne considère jamais qu'un serveur déjà ouvert est automatiquement à jour.
