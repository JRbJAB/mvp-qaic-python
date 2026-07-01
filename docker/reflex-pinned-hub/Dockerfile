# Recovered replacement source path for the MVP QAIC pinned Reflex image.
# This file is not asserted to be the original Dockerfile provenance.
# Target image tag:
# jrb-reflex-pinned-hub:py312-node22-reflex096p1

FROM python:3.12-bookworm

ARG NODE_MAJOR=22
ARG REFLEX_VERSION=0.9.6.post1

LABEL org.opencontainers.image.title="MVP QAIC Reflex pinned hub"
LABEL org.opencontainers.image.description="Recovered replacement source path for pinned Reflex image contract; original provenance is not proven."
LABEL org.opencontainers.image.version="py312-node22-reflex096p1"
LABEL mvp_qaic.policy_id="R16F2H4_REFLEX_RUNTIME_POLICY_LOCK"
LABEL mvp_qaic.recovered_source_path="true"
LABEL mvp_qaic.original_provenance_proven="false"
LABEL mvp_qaic.pinned_image="jrb-reflex-pinned-hub:py312-node22-reflex096p1"

SHELL ["/bin/bash", "-o", "pipefail", "-c"]

RUN apt-get update \
    && apt-get install -y --no-install-recommends ca-certificates curl gnupg \
    && install -d -m 0755 /etc/apt/keyrings \
    && curl -fsSL https://deb.nodesource.com/gpgkey/nodesource-repo.gpg.key \
        | gpg --dearmor -o /etc/apt/keyrings/nodesource.gpg \
    && echo "deb [signed-by=/etc/apt/keyrings/nodesource.gpg] https://deb.nodesource.com/node_${NODE_MAJOR}.x nodistro main" \
        > /etc/apt/sources.list.d/nodesource.list \
    && apt-get update \
    && apt-get install -y --no-install-recommends nodejs \
    && python -m pip install --no-cache-dir --upgrade pip \
    && python -m pip install --no-cache-dir "reflex==${REFLEX_VERSION}" \
    && apt-get purge -y --auto-remove curl gnupg \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /workspace
