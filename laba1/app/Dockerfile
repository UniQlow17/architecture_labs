FROM python:3.11-slim

ENV PYTHONUNBUFFERED=1
ENV POSTGRES_HOST=db

WORKDIR /app

COPY pyproject.toml README.md ./
RUN pip install uv && uv sync --no-dev
COPY app ./app

EXPOSE 8000
CMD ["uv", "run", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
