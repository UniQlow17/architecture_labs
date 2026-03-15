# Лабораторная работа 1. Трёхзвенная клиент–серверная архитектура

## Описание задания

Реализован программный комплекс с **трёхзвенной архитектурой**:

- **Клиент** — браузерное SPA (React), интерфейс пользователя.
- **Сервер приложений** — REST API на FastAPI, бизнес-логика и аутентификация.
- **Сервер БД** — PostgreSQL, персистентное хранилище данных.

Клиент общается с сервером **только через API** (HTTP/REST). Взаимодействие с БД выполняется только на стороне сервера приложений.

Реализовано:

- Аутентификация пользователей (JWT).
- Авторизация по ролям: **admin**, **moderator**, **viewer** с разными правами (просмотр, создание/редактирование, удаление).
- API описано в OpenAPI (Swagger); документация доступна по `/docs` и в статическом файле.

---

## Стек технологий

| Звено | Технологии |
|-------|------------|
| **Клиент** | React 18, TypeScript, Vite, React Router |
| **Сервер приложений** | Python 3.11+, FastAPI, SQLAlchemy 2 (async), JWT (python-jose), bcrypt |
| **БД** | PostgreSQL 15 |
| **Инфраструктура** | Docker, Docker Compose, Alembic (миграции) |

---

## Документация API

- **OpenAPI (JSON):** [docs/openapi.json](docs/openapi.json)
- При запущенном API: Swagger UI — `http://localhost:8000/docs`, ReDoc — `http://localhost:8000/redoc`

---

## Запуск

### Вариант 1: Docker Compose (рекомендуется)

1. Скопируйте переменные окружения:
   ```bash
   cp .env.example .env
   ```
   При необходимости отредактируйте `.env` (пароли, порты, `SECRET_KEY`, `VITE_API_URL`).

2. Запустите все сервисы:
   ```bash
   docker compose up -d
   ```

3. После старта:
   - **Фронтенд:** http://localhost:8080 (порт задаётся через `FRONT_PORT` в `.env`)
   - **API:** http://localhost:8000
   - **БД:** порт из `POSTGRES_PORT` (по умолчанию 5432)

Миграции выполняются автоматически при первом запуске (сервис `migrate`).

### Вариант 2: Локальный запуск (для разработки)

1. Установите зависимости и настройте окружение:
   ```bash
   uv sync
   cp .env.example .env
   ```
   В `.env` укажите `POSTGRES_HOST=localhost` и параметры БД.

2. Запустите PostgreSQL (локально или через Docker):
   ```bash
   docker compose up -d db
   ```

3. Примените миграции:
   ```bash
   alembic upgrade head
   ```

4. Запустите API:
   ```bash
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```

5. В отдельном терминале запустите фронтенд:
   ```bash
   cd front_app && npm install && npm run dev
   ```
   Фронтенд будет доступен по адресу, который выведет Vite (обычно http://localhost:5173). Убедитесь, что в `.env` указан `VITE_API_URL=http://localhost:8000` для сборки/прокси к API.
