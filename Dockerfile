FROM python:3.14-slim AS build
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

WORKDIR /app

COPY pyproject.toml uv.lock /app

# Install dependencies
RUN uv sync \
        --frozen \
        --no-dev \
        --no-install-project

# Copy the project into the image
ADD . /app/

# Sync the project
RUN uv sync \
        --frozen \
        --no-dev

FROM python:3.14-slim

ENV PATH=/app/.venv/bin:$PATH \
    PYTHONUNBUFFERED=1

RUN groupadd -r app
RUN useradd -r -d /app -g app -N app

STOPSIGNAL SIGINT

WORKDIR /app

ARG GIT_SHA=unknown-sha
ARG GIT_REF=unknown-ref

ENV \
  GIT_SHA="${GIT_SHA}" \
  GIT_REF="${GIT_REF}"

COPY --from=build --chown=app:app /app /app

RUN my-script --help
