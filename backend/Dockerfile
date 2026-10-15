# syntax=docker/dockerfile:1

# ============================================================
# Stage: builder — общая база с зависимостями и исходниками
# ============================================================
FROM ghcr.io/astral-sh/uv:python3.14-bookworm-slim AS builder

ENV UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy \
    UV_PYTHON_DOWNLOADS=never

WORKDIR /app

RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync --frozen --no-dev --group prod --no-install-project

COPY pyproject.toml uv.lock README.md ./
COPY src ./src
COPY alembic.ini ./
COPY alembic ./alembic

RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-dev --group prod

# ============================================================
# Stage: dev — для локальной разработки с hot-reload
# ============================================================
FROM builder AS dev

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PATH="/app/.venv/bin:$PATH" \
    APP_ENV=local

WORKDIR /app

RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --group dev --group prod

RUN apt-get update && apt-get install -y --no-install-recommends \
        curl \
        git \
        procps \
        iputils-ping \
        vim \
    && rm -rf /var/lib/apt/lists/*

EXPOSE 8000

CMD ["uvicorn", "app.main:create_app", \
     "--factory", \
     "--host", "0.0.0.0", \
     "--port", "8000", \
     "--reload", \
     "--reload-dir", "/app/src", \
     "--log-level", "debug"]

# ============================================================
# Stage: runtime — минимальный прод-образ
# ============================================================
FROM python:3.14-slim-bookworm AS runtime

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONFAULTHANDLER=1 \
    PATH="/app/.venv/bin:$PATH" \
    APP_ENV=production

RUN apt-get update && apt-get install -y --no-install-recommends \
        ca-certificates \
    && rm -rf /var/lib/apt/lists/*

RUN groupadd --gid 1000 app \
    && useradd --uid 1000 --gid app --create-home --shell /bin/bash app

WORKDIR /app

COPY --from=builder --chown=app:app /app /app

RUN mkdir -p /app/media /app/logs && chown -R app:app /app/media /app/logs

USER app

EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=5s --start-period=15s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://127.0.0.1:8000/health/live', timeout=3)" || exit 1

CMD ["gunicorn", "app.main:create_app()", \
     "--worker-class", "uvicorn.workers.UvicornWorker", \
     "--workers", "4", \
     "--bind", "0.0.0.0:8000", \
     "--access-logfile", "-", \
     "--error-logfile", "-", \
     "--log-level", "info", \
     "--timeout", "60", \
     "--graceful-timeout", "30", \
     "--forwarded-allow-ips", "*"]
