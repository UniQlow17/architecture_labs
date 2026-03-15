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
- **OpenAPI (YAML):** [docs/openapi.yaml](docs/openapi.yaml)
- При запущенном API: Swagger UI — `http://localhost:8000/docs`, ReDoc — `http://localhost:8000/redoc`

Чтобы обновить статическую документацию в репозитории после изменений API:

```bash
uv run python -m app.utils.export_openapi
```

Скрипт кладёт актуальную схему в `docs/openapi.json` и (при установленном PyYAML) в `docs/openapi.yaml`.

---

## Структура проекта

### Бэкенд (FastAPI, `app/`)

```
app/
├── main.py              # Точка входа: FastAPI-приложение, CORS, подключение роутеров
├── api/
│   ├── auth.py          # Роуты: регистрация, логин (JWT)
│   └── items.py         # Роуты: CRUD элементов с проверкой ролей
├── core/
│   ├── config.py        # Настройки из .env (Pydantic Settings)
│   ├── database.py      # Подключение к PostgreSQL, сессии SQLAlchemy (async)
│   └── constants.py     # Роли (admin, moderator, viewer)
├── models/
│   ├── base.py          # Базовый класс моделей
│   ├── user.py          # Модель пользователя
│   └── item.py          # Модель элемента
├── schemas/
│   ├── auth.py          # Схемы запросов/ответов для логина и регистрации
│   ├── user.py          # Схемы пользователя (создание, ответ)
│   └── item.py          # Схемы элемента (создание, обновление, ответ)
├── crud/
│   ├── user.py          # CRUD для пользователей
│   └── item.py          # CRUD для элементов
└── utils/
    ├── deps.py          # Зависимости: get_current_user, проверка ролей
    ├── jwt.py           # Создание и проверка JWT-токенов
    ├── password.py      # Хэширование паролей (bcrypt)
    └── export_openapi.py # Экспорт OpenAPI в docs/ (JSON/YAML)
```

Рядом с `app/`: `migrations/` (Alembic), `alembic.ini`, `pyproject.toml`.

### Фронтенд (React + Vite, `front_app/`)

```
front_app/
├── index.html
├── package.json
├── vite.config.ts
├── nginx.conf            # Nginx Конфиг
├── Dockerfile
└── src/
    ├── main.tsx          # Точка входа, рендер App
    ├── App.tsx           # Роутер (BrowserRouter), AuthProvider, Layout
    ├── App.css
    ├── types.ts          # Типы (User, Item, роли и т.д.)
    ├── constants/
    │   └── roles.ts      # Константы ролей для UI
    ├── context/
    │   └── AuthContext.tsx  # Состояние авторизации, login/logout
    ├── api/
    │   ├── client.ts     # Axios-инстанс, перехватчик с Bearer-токеном
    │   ├── auth.ts       # Запросы: регистрация, логин
    │   └── items.ts      # Запросы: CRUD элементов
    ├── components/
    │   ├── layout/
    │   │   └── Layout.tsx    # Оболочка: навбар, меню, Outlet для страниц
    │   └── auth/
    │       └── ProtectedRoute.tsx  # Защита маршрутов по роли/авторизации
    └── pages/
        ├── Login.tsx     # Страница входа
        ├── Register.tsx  # Страница регистрации
        └── Items.tsx     # Список/создание/редактирование элементов
```

### Документация и конфигурация

```
docs/
├── openapi.json
└── openapi.yaml
```

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
