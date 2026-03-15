from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api import auth_router, items_router
from app.core.config import settings

app = FastAPI(
    title="API сервер приложений",
    description=(
        "Трёхзвенная архитектура: клиент ↔ сервер приложений (этот API) ↔ PostgreSQL. "
        "Аутентификация по JWT. Роли: **admin** (полный доступ), **moderator** (создание/редактирование), **viewer** (только чтение)."
    ),
    version="0.1.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router, prefix="/api")
app.include_router(items_router, prefix="/api")


@app.get("/health", tags=["Служебные"])
async def health():
    return {"status": "ok"}
