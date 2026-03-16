from fastapi import FastAPI

from app.api import api_router
from app.utils.lifespan import lifespan

app = FastAPI(
    title="ČNB Exchange Rates",
    description="Синхронизация и отчёты по курсу чешской кроны (данные ČNB)",
    lifespan=lifespan,
)
app.include_router(api_router)
