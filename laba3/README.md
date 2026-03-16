# Лабораторная работа 3. Синхронизация и отчёты по курсу чешской кроны

Сервис автоматически забирает курсы валют с сайта Чешского национального банка (ČNB), сохраняет их в БД и отдаёт отчёты по выбранным валютам через REST API.

---

## Стек

| Категория | Технологии |
|-----------|------------|
| Язык | Python 3.11+ |
| Web | FastAPI, Uvicorn |
| БД | PostgreSQL, SQLAlchemy 2 (async + asyncpg) |
| Миграции | Alembic |
| Планировщик | APScheduler (AsyncIOScheduler) |
| HTTP-клиент | httpx |
| Конфиг | pydantic-settings, .env |
| Сборка/запуск | Docker, docker-compose, uv |

---

## Функционал

1. **Автоматическая синхронизация по расписанию**  
   Ежедневная загрузка курсов на текущую дату. Время запуска задаётся cron-выражением (по умолчанию каждый день в 00:01). Список валют настраивается в конфиге.

2. **Синхронизация за период**  
   API `POST /api/sync/period` с параметрами `start_date`, `end_date` и опционально `currencies`. Подтягиваются данные из ежедневного и годового источников ČNB, пропуски обрабатываются.

3. **Отчёт по курсам**  
   API `GET /api/report` возвращает за указанный период для каждой выбранной валюты минимум, максимум и среднее значение курса (для 1 единицы валюты). Формат — JSON. При отсутствии данных по валюте поля `min`/`max`/`avg` могут быть `null`.

4. **Опциональная загрузка истории при старте**  
   При `SYNC_HISTORY_YEARS_BACK > 0` при старте приложения один раз подгружается история курсов за указанное число лет.

---

## Запуск

### Локально (с уже поднятой PostgreSQL)

```bash
# Зависимости
uv sync

# Миграции
uv run alembic upgrade head

# Запуск
uv run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Docker

```bash
cp .env.example .env
# при необходимости отредактировать .env

docker compose up -d
```

Приложение: http://localhost:8000  
Документация API: http://localhost:8000/docs

---

## Конфигурация (.env)

| Переменная | Описание | По умолчанию |
|------------|----------|--------------|
| `DB_HOST`, `DB_PORT`, `DB_USER`, `DB_PASSWORD`, `DB_NAME` | Подключение к PostgreSQL | localhost, 5432, postgres, postgres, cnb |
| `SYNC_CRON` | Cron для ежедневной синхронизации (минута час день месяц день_недели) | `1 0 * * *` (00:01) |
| `SYNC_CURRENCIES` | Коды валют через запятую | EUR,USD,GBP,CHF,PLN |
| `SYNC_HISTORY_YEARS_BACK` | Лет истории для подгрузки при старте (0 — не подгружать) | 0 |
| `CNB_DAILY_URL`, `CNB_YEAR_URL` | URL ежедневного и годового файлов ČNB | стандартные |

---

## API (кратко)

- **POST /api/sync/period**  
  Параметры: `start_date`, `end_date`, `currencies` (опционально). Синхронизирует курсы за период.

- **GET /api/report**  
  Параметры: `start_date`, `end_date`, `currencies` (опционально). Возвращает JSON с полями `min`, `max`, `avg` по каждой валюте.

---

## Структура проекта

```
laba3/
├── app/
│   ├── main.py              # Точка входа FastAPI
│   ├── api/
│   │   ├── __init__.py
│   │   └── routes.py        # Эндпоинты /api/sync/period, /api/report
│   ├── core/
│   │   ├── __init__.py
│   │   ├── config.py        # Настройки (pydantic-settings)
│   │   ├── database.py      # AsyncSession, фабрика сессий
│   │   └── logger.py
│   ├── models/
│   │   ├── __init__.py
│   │   ├── base.py
│   │   └── exchange_rate.py # Модель курса (дата, валюта, курс за 1 ед.)
│   ├── query_schemas/       # Query-параметры и dependency для API
│   │   ├── __init__.py
│   │   ├── report.py
│   │   └── sync_period.py
│   ├── schemas/             # Pydantic-модели ответов/запросов
│   │   ├── __init__.py
│   │   ├── report.py        # ReportResponse, CurrencyStats
│   │   └── sync.py          # SyncPeriodResponse
│   ├── service/
│   │   ├── __init__.py
│   │   └── exchange_rates.py # sync_daily, sync_period, get_report
│   └── utils/
│       ├── __init__.py
│       ├── currencies.py    # Нормализация списка валют
│       ├── lifespan.py      # Lifespan: БД, планировщик, история
│       ├── scheduler.py     # APScheduler, cron, ежедневная задача
│       └── cnb/
│           ├── __init__.py
│           ├── client.py    # fetch_daily, fetch_year, fetch_period (httpx)
│           └── parser.py   # Парсинг daily.txt / year.txt ČNB
├── migrations/              # Alembic
│   ├── env.py
│   ├── script.py.mako
│   └── versions/
├── .env.example
├── alembic.ini
├── docker-compose.yml       # postgres, migrate, app
├── Dockerfile
├── Dockerfile.migrate
├── pyproject.toml
└── README.md
```
