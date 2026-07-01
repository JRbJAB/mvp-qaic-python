# Reflex Pinned Hub Recovered Source Path

This directory is a controlled replacement source build path for:

`jrb-reflex-pinned-hub:py312-node22-reflex096p1`

It is not evidence of the original image build provenance. H8A found no tracked Dockerfile or compose source candidate for the existing local pinned image, so H8B restores a reviewable tracked source path for future operator-controlled rebuilds.

Contract:

- Policy: `R16F2H4_REFLEX_RUNTIME_POLICY_LOCK`
- Python: `3.12`
- Node: `22`
- Reflex: `0.9.6.post1`
- Default selector mode: dry-run, no build
- Runtime startup command: intentionally absent

Dry-run selector:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File scripts\H8B_REFLEX_DOCKER_BUILD_SELECTOR_NO_RUNTIME.ps1
```

Operator-controlled build command printed by the selector:

```powershell
docker build -f docker\reflex-pinned-hub\Dockerfile -t jrb-reflex-pinned-hub:py312-node22-reflex096p1 docker\reflex-pinned-hub
```

To execute that build, the operator must pass the explicit selector flag:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File scripts\H8B_REFLEX_DOCKER_BUILD_SELECTOR_NO_RUNTIME.ps1 -Build
```

Reports are written only under:

`C:\JRb_TRADING_OS\_RUN_REPORTS\MVP_QAIC_PY`
