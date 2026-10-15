# syntax=docker/dockerfile:1

# ============================================================
# Stage: builder — общая база с зависимостями и исходниками
# ============================================================
FROM python:3.14-slim-bookworm AS builder

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    POETRY_VIRTUALENVS_IN_PROJECT=1 \
    POETRY_NO_INTERACTION=1

WORKDIR /app

RUN pip install --no-cache-dir "poetry==2.5.1"

COPY pyproject.toml poetry.lock ./

RUN --mount=type=cache,target=/root/.cache \
    poetry install --only main --no-root

COPY src ./src
COPY alembic.ini ./
COPY alembic ./alembic

RUN --mount=type=cache,target=/root/.cache \
    poetry install --only main

# ============================================================
# Stage: dev — для локальной разработки с hot-reload
# ============================================================
FROM builder AS dev

ENV PATH="/app/.venv/bin:$PATH" \
    APP_ENV=local

RUN apt-get update && apt-get install -y --no-install-recommends \
        curl \
        git \
        procps \
        iputils-ping \
        vim \
    && rm -rf /var/lib/apt/lists/*

RUN --mount=type=cache,target=/root/.cache \
    poetry install --with dev

WORKDIR /app

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
