
# P131 Real Image Transcription Operator Test

## Goal

Run a real local operator test with a screenshot/image, but keep all interpretation human-reviewed.

## Source context

Latest P128:
`G:\Mon Drive\👥 JULIEN [Perso]\📈 Trading JRb\Solutions & Dev (Trading JRb)\MVP_QAIC_PY\05_EXPORTS\P128_PROMPT_INPUT_IMAGE_CAPTURE_HUMAN_REVIEW_20260622_161704`

Latest P130:
`G:\Mon Drive\👥 JULIEN [Perso]\📈 Trading JRb\Solutions & Dev (Trading JRb)\MVP_QAIC_PY\05_EXPORTS\P130_OPERATOR_E2E_IMAGE_PROMPT_LOOP_20260622_164559`

## Steps

1. Put the real portfolio screenshot/image in `P131_REAL_IMAGE_INBOX`.
2. Open `P131_FILLED_TRANSCRIPTION_OUTBOX/P131_MANUAL_TRANSCRIPTION_REAL_TEST.md`.
3. Fill symbol, quantity, value_eur, unclear rows, and notes manually.
4. Run the P130 command from `P131_OPERATOR_COMMANDS.md`.
5. Continue only if P130 returns `E2E_READY_FOR_GEM_COPY_PASTE`.

## Hard stop

If P130 remains `E2E_WAITING_FOR_MANUAL_TRANSCRIPTION`, the transcription is still incomplete.
If P130 returns `E2E_BLOCKED_REVIEW_REQUIRED`, resolve blockers before GEM.

## Boundaries

No OCR.
No automated visual extraction.
No invented portfolio data.
No Sheets write.
No broker, no order, no sizing.
