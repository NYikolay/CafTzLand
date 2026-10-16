# Реализация тестового задания ВитАй Ворлд

**Основной стек:** Next.js (frontend), FastAPI (backend), Postgres, Nginx (прокси)  
**ИИ агент:** OpenCode (к сожалению на данный момент подписки клода у меня нету, но с ним я работаю)  
**Модель:** DeepSeek V4.1 Flash

## Реализованы следующие фичи:
1. Landing PAGE согласно ТЗ
2. REST API с Admin панелью
3. Пересылка оформленного заказа в Telegram чат с ботом
4. Проект задеплоен на личный VPS сервер, получен SSL сертификат

**Выбор стека** (в частности backend на FastAPI) обоснован желанием показать навык. Само собой текущая реализация такой простой задачи является оверхедом и всё можно сделать проще, но упор был на другое.  
Самым идеальным вариантом реализации такой простой задачи (если она реальна) является дефолтный MPA (Django, PHP, в целом и Next.js подойдёт) - для лендинга этого достаточно

## Работа с агентом:

Логи сессий можно найти в директории `opencode_session`

Весь принцип работы построен на подходе Subagent-Driven Development и использовании навыка superpowers. В первую очередь пишется спецификация и план, далее идёт реализация с использованием субагентов  
Работа не ведётся в одной сессии, каждая новая фича - отдельная сессия. При небольшом контекстном окне после написании спеки и плана делается compact контекста и выполняется реализация в этой же сессии.  
Разбивка на сессии обоснована уменьшением интеллекта агента (в частности LLM модели) по меры роста контекстного окна.

## Процесс создания проекта:
1. Дизайн был сформирован в бесплатном агенте Figma согласно тз. Пару правок было сделано руками.
2. Для работы с фигмой был использован локальный MCP. Через Desktop приложение
3. Далее реализация скелета бэка и фронта. 
4. Разбил проект на более-менее мелкие задачи (в логах сессий можно увидеть).

Ошибок как таковых агент не допускал, проект всегда запускался с первого раза. Благодаря SDD и TDD агент чётко понимает что ему делать, сам себя ревьюит и задаёт вопросы когда чего-то не понимает. Количество ошибок минимально, главное чётко описать задачу  
Чтобы реализовать такой простой backend было достаточно дать агенту посмотреть дизайн и пару наводящих фактов.

## Деплой (production)

Требуется: Docker + Compose на сервере, DNS A-записи `tzkvvit.site` и `www.tzkvvit.site` → IP сервера.

```bash
# 1. Окружение
cp .env.prod.example .env.prod   # заполнить секреты: openssl rand -hex 32

# 2. Сборка и запуск (проект kvarta-prod)
docker compose --env-file .env.prod -f compose.prod.yaml up -d --build --wait
docker compose --env-file .env.prod -f compose.prod.yaml ps
docker compose --env-file .env.prod -f compose.prod.yaml logs -f backend

# 3. Первый сертификат Let's Encrypt (заменить <email>; nginx уже слушает :80)
docker compose --env-file .env.prod -f compose.prod.yaml run --rm --entrypoint certbot certbot \
  certonly --webroot -w /var/www/certbot \
  -d tzkvvit.site -d www.tzkvvit.site \
  --email <email> --agree-tos --no-eff-email

# 4. SSL: добавить 443 server-блок в nginx/default.conf
#    (ssl_certificate /etc/letsencrypt/live/tzkvvit.site/fullchain.pem;
#     proxy_pass http://frontend:3000 — включая /api/lead: BFF сам проксирует
#     в backend внутри сети; напрямую API — только /api/v1/ → http://backend:8000)
docker compose --env-file .env.prod -f compose.prod.yaml exec nginx nginx -s reload

# Остановка (тома с данными сохраняются)
docker compose --env-file .env.prod -f compose.prod.yaml down
```

- `NEXT_PUBLIC_SITE_URL` инлайнится в HTML на этапе сборки: смена домена требует пересборки frontend.
- Сервис `certbot` обновляет сертификаты каждые 12 часов, но nginx нужно перезагрузить, чтобы он подхватил новый сертификат: `docker compose --env-file .env.prod -f compose.prod.yaml exec nginx nginx -s reload` (например, из cron раз в неделю).
- Dev-стек: `cp backend/.env.example backend/.env` (заполнить креды) и `docker compose up -d --build` (порт frontend — 3000, backend — 8000).

**Ссылка на сайт:** ...  
**Админ панель:** ...  
**Бот:** ...

**Пароль и логин от админки:** ....

Ссылка на пример моего prod проекта - [https://миноксидил.бел/](https://миноксидил.бел/). Также был собран по большей части агентом за пару дней