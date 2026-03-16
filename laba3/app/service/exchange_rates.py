"""Сервис синхронизации и отчётов по курсам валют."""
from datetime import date
from decimal import Decimal

from sqlalchemy import and_, func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import ExchangeRate
from app.utils.cnb import fetch_daily, fetch_period


async def sync_daily(
    session: AsyncSession, rate_date: date, currencies: list[str] | None = None
) -> int:
    rows = await fetch_daily(rate_date, currencies)
    return await _upsert_rates(session, rows)


async def sync_period(
    session: AsyncSession,
    start_date: date,
    end_date: date,
    currencies: list[str] | None = None,
) -> int:
    rows = await fetch_period(start_date, end_date, currencies)
    return await _upsert_rates(session, rows)


async def _upsert_rates(
    session: AsyncSession,
    rows: list[tuple[date, str, Decimal]],
) -> int:
    if not rows:
        return 0
    for rate_date, currency_code, rate_per_unit in rows:
        stmt = select(ExchangeRate).where(
            ExchangeRate.rate_date == rate_date,
            ExchangeRate.currency_code == currency_code,
        )
        result = await session.execute(stmt)
        existing = result.scalar_one_or_none()
        if existing:
            existing.rate_per_unit = rate_per_unit
        else:
            session.add(
                ExchangeRate(
                    rate_date=rate_date,
                    currency_code=currency_code,
                    rate_per_unit=rate_per_unit,
                )
            )
    return len(rows)


async def get_report(
    session: AsyncSession,
    start_date: date,
    end_date: date,
    currencies: list[str],
) -> dict[str, dict[str, float | None]]:
    report: dict[str, dict[str, float | None]] = {}
    for code in currencies:
        q = (
            select(
                func.min(ExchangeRate.rate_per_unit).label("min_rate"),
                func.max(ExchangeRate.rate_per_unit).label("max_rate"),
                func.avg(ExchangeRate.rate_per_unit).label("avg_rate"),
                func.count(ExchangeRate.id).label("cnt"),
            )
            .where(
                and_(
                    ExchangeRate.currency_code == code,
                    ExchangeRate.rate_date >= start_date,
                    ExchangeRate.rate_date <= end_date,
                )
            )
        )
        r = await session.execute(q)
        row = r.one_or_none()
        if row and row.cnt and row.cnt > 0:
            report[code] = {
                "min": float(row.min_rate),
                "max": float(row.max_rate),
                "avg": round(float(row.avg_rate), 6),
            }
        else:
            report[code] = {"min": None, "max": None, "avg": None}
    return report
