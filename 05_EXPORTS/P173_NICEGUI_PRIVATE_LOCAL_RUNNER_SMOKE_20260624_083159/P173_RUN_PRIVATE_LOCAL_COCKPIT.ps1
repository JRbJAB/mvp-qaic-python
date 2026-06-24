$ErrorActionPreference = "Stop"
chcp 65001 | Out-Null
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
$OutputEncoding = [System.Text.Encoding]::UTF8

# Private local launch only. Do not change host to 0.0.0.0.
Set-Location -LiteralPath "C:\Users\Julie\Documents\JRb-Dev\MVP_QAIC_PY_WORK_20260623_192901"
python -m mvp_qaic_py.p173_nicegui_private_local_runner --project-root . --host 127.0.0.1 --port 8088 --serve-private
