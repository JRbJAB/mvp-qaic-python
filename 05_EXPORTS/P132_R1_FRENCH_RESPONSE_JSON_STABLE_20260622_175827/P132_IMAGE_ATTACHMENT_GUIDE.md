
# P132 Image Attachment Guide

Attach the Revolut X screenshot/image directly to GEM with the P132 prompt.

Do not run a separate preliminary OCR/extraction prompt.
The image is part of the main GEM portfolio prompt.

Expected control in final GEM response:
- image_used=true
- image_usage_evidence.status="IMAGE_USED"
- visual_evidence_summary is not empty
- reference_currency="USD"

If not, block or review.
