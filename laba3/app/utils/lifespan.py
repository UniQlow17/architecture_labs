import asyncio
from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.utils.scheduler import run_history_sync_if_configured, start_scheduler

scheduler = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    global scheduler
    scheduler = start_scheduler()
    asyncio.create_task(run_history_sync_if_configured())
    yield
    if scheduler:
        scheduler.shutdown(wait=False)
