# Codex Sandbox And Workflow Rules

Active workspace: `C:\JRb_TRADING_OS`.

`G:\Mon Drive` is no longer the active Codex workspace. DriveFS/FAT32 failed the Codex `workspace-write` sandbox workflow, while the NTFS workspace under `C:\JRb_TRADING_OS` passed local write and validation requirements.

Operational rules:

- Work only inside the active NTFS workspace for Codex edits and validation.
- Do not use `G:\Mon Drive` for Codex workspace writes.
- Keep tracker work local, private, read-only toward Sheets/BigQuery/Apps Script unless a future batch explicitly authorizes external writes.
- Do not run deploys, broker/order/sizing actions, secret access, or live APIs from tracker validation batches.
