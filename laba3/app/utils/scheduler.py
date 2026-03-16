from datetime import date

from app.core import logger
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger

from app.core.config import settings
from app.core.database import async_session_factory
from app.service import sync_daily, sync_period


async def run_history_sync_if_configured() -> None:
    """Однократная синхронизация истории при старте, если задано SYNC_HISTORY_YEARS_BACK."""
    if settings.sync_history_years_back <= 0:
        return
    end = date.today()
    start = date(end.year - settings.sync_history_years_back, 1, 1)
    async with async_session_factory() as session:
        try:
            count = await sync_period(session, start, end, settings.sync_currencies)
            logger.info(f"Synced {count} exchange rates for period {start} to {end}")
            await session.commit()
        except Exception:
            await session.rollback()


async def _scheduled_sync_job() -> None:
    logger.info("Starting daily sync job")
    async with async_session_factory() as session:
        try:
            await sync_daily(session, date.today(), settings.sync_currencies)
            await session.commit()
        except Exception:
            await session.rollback()
            raise


def _parse_cron(cron: str) -> dict:
    parts = cron.strip().split()
    if len(parts) != 5:
        return {"minute": "1", "hour": "0", "day": "*", "month": "*", "day_of_week": "*"}
    return {
        "minute": parts[0],
        "hour": parts[1],
        "day": parts[2],
        "month": parts[3],
        "day_of_week": parts[4],
    }


def start_scheduler(scheduler: AsyncIOScheduler | None = None) -> AsyncIOScheduler:
    if scheduler is None:
        scheduler = AsyncIOScheduler()
    cron_params = _parse_cron(settings.sync_cron)
    logger.info(f"Adding daily sync job with cron: {cron_params}")
    scheduler.add_job(
        _scheduled_sync_job,
        CronTrigger(**cron_params),
        id="cnb_daily_sync",
        replace_existing=True,
    )
    scheduler.start()
    return scheduler
