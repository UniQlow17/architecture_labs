# Используем образ с uv для быстрой установки зависимостей
FROM python:3.11-slim

WORKDIR /app

# uv для установки зависимостей
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

# Копируем зависимости
COPY pyproject.toml uv.lock* ./
RUN uv sync --frozen --no-dev --no-install-project

# Копируем код приложения
COPY alembic.ini ./
COPY migrations ./migrations
COPY app ./app

# Устанавливаем проект в окружение uv
RUN uv sync --frozen --no-dev

ENV PATH="/app/.venv/bin:$PATH"
ENV PYTHONPATH=/app
# Вывод логов без буферизации (важно для Docker)
ENV PYTHONUNBUFFERED=1

# По умолчанию — запуск приложения
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
