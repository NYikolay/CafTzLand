# VitaiWorld Backend

FastAPI-скелет в DDD-слоях (src-layout). Бизнес-логики пока нет — каркас: health-эндпоинты, конверт ошибок, middlewares, admin-панель, миграции.
Стек: Python 3.14, Poetry, async SQLAlchemy 2.1 + asyncpg, Alembic, pydantic-settings, sqladmin; aiogram подключён как будущая заготовка.

## Запуск (из каталога `backend/`, docker compose)

```bash
cp .env.example .env   # при первом запуске; .env не коммитить
docker compose up -d --build   # db → migrate (alembic) → app (dev-образ, hot-reload)
docker compose logs -f app     # логи (uvicorn --reload)
docker compose down            # остановить
```

Приложение — http://localhost:8000 (`/health/live`, `/health/ready`, `/docs`, `/admin`).
Сервис `migrate` накатывает `alembic upgrade head` и завершается; `app` ждёт его.

## Проверки и разработка (Poetry)

```bash
poetry install                      # зависимости (dev-группа входит по умолчанию)
poetry run pytest                   # тесты (реальная БД не нужна)
poetry run mypy                     # типы (strict)
poetry run ruff check .             # линт
poetry run ruff format --check .    # проверка формата (автофикс: без --check)
poetry run alembic upgrade head --sql  # offline-проверка миграций без БД
```

Запуск без docker: `poetry run uvicorn app.main:create_app --factory --app-dir src --reload` (Postgres — `docker compose up -d db`).

## Структура

- `src/app/domain/` — модели и исключения, без внешних зависимостей
- `src/app/application/` — use cases и ports (Protocol)
- `src/app/infrastructure/` — Settings, engine/sessionmaker/probe, логирование
- `src/app/presentation/` — FastAPI-слой: health, ошибки, middlewares, admin
- `tests/` зеркалит слои; `alembic/versions/` исключён из ruff и mypy
- `compose.yaml` — сервисы db (postgres:18), migrate (разовый прогон alembic), app (dev-таргет с volume на `./src`)

## Конвенции

- Зависимости только внутрь: presentation → application → domain; infrastructure реализует ports.
- Тесты без реальной БД: подмены (test doubles) + httpx `ASGITransport`.
- Все настройки — через `Settings` (pydantic-settings, UPPER_CASE env); новые переменные добавлять и в `.env.example`.
- Ошибки API — единый конверт `{"error": {"code": ..., "message": ...}}` (`presentation/errors.py`).
- Mypy strict (`disallow_untyped_defs`) — все функции аннотированы; плагин pydantic включён.
- Перед завершением любой задачи: `pytest`, `mypy`, `ruff check .`, `ruff format --check .` — всё зелёное.
- Спеки и планы фич — в `../docs/superpowers/specs/` и `../docs/superpowers/plans/` (вне git).

## Не трогать без отдельной задачи

- `Dockerfile` — Poetry (multi-stage: builder/dev/runtime), без uv; зависимости ставятся по `poetry.lock`, проект — editable (hot-reload через volume `./src`). Не переводить обратно на uv.
- Капы `requires-python >=3.14,<3.15` и `pydantic <2.14` диктует aiogram 3.31 — не расширять без его апгрейда.
- `.env`, `.venv/`, `.ruff_cache/`, `media/*` (кроме `.gitkeep`) не коммитить.
