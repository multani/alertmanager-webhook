# Inspired by https://raw.githubusercontent.com/astral-sh/uv-docker-example/refs/heads/main/multistage.Dockerfile
FROM python:3.13-slim AS builder
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

ENV UV_COMPILE_BYTECODE=1 UV_LINK_MODE=copy

# Omit development dependencies
ENV UV_NO_DEV=1

# Disable Python downloads, because we want to use the system interpreter
# across both images.
ENV UV_PYTHON_DOWNLOADS=0

WORKDIR /app
RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync --locked --no-install-project
COPY . /app
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --locked


# This should be the same image as the "builder" one.
FROM python:3.13-slim

ENV PATH=/app/.venv/bin:$PATH \
    PYTHONUNBUFFERED=1

# Setup a non-root user
RUN groupadd --system --gid 999 nonroot \
 && useradd --system --gid 999 --uid 999 --create-home nonroot

WORKDIR /app

# Copy the application from the builder
COPY --from=builder --chown=nonroot:nonroot /app /app

USER nonroot
STOPSIGNAL SIGINT

ARG \
    GIT_SHA=unknown-sha \
    GIT_REF=unknown-ref

ENV \
  GIT_SHA="${GIT_SHA}" \
  GIT_REF="${GIT_REF}"

RUN ["alertmanager-webhook", "--help"]
