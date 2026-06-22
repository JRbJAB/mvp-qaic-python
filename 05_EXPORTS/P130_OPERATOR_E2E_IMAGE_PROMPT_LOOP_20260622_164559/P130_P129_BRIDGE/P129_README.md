
# P129-R1 Image To Prompt Manual Transcription Bridge

P129 bridges P128 manual transcription into a P124-compatible portfolio input file.

Runtime fix:
- Latest P128 discovery is done inside Python using Path objects.
- It cannot degrade to `LATEST_P128_DIR=G`.

It does not OCR images.
It does not automatically extract visual data.
It does not invent portfolio quantities, prices, values, or balances.
