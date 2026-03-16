from datetime import date
from decimal import Decimal

import httpx

from app.core.config import settings
from app.utils.cnb.parser import parse_daily_rates, parse_year_rates


async def fetch_daily(
    rate_date: date,
    currencies: list[str] | None = None,
) -> list[tuple[date, str, Decimal]]:
    date_str = rate_date.strftime("%d.%m.%Y")
    url = f"{settings.cnb_daily_url}?date={date_str}"
    async with httpx.AsyncClient(timeout=30.0) as client:
        resp = await client.get(url)
        resp.raise_for_status()
    return parse_daily_rates(resp.text, currencies_filter=currencies)


async def fetch_year(
    year: int,
    currencies: list[str] | None = None,
) -> list[tuple[date, str, Decimal]]:
    url = f"{settings.cnb_year_url}?year={year}"
    async with httpx.AsyncClient(timeout=60.0) as client:
        resp = await client.get(url)
        resp.raise_for_status()
    return parse_year_rates(resp.text, currencies_filter=currencies)


async def fetch_period(
    start_date: date,
    end_date: date,
    currencies: list[str] | None = None,
) -> list[tuple[date, str, Decimal]]:
    result: list[tuple[date, str, Decimal]] = []
    seen: set[tuple[date, str]] = set()
    for year in range(start_date.year, end_date.year + 1):
        try:
            year_data = await fetch_year(year, currencies)
            for d, code, rate in year_data:
                if start_date <= d <= end_date and (d, code) not in seen:
                    seen.add((d, code))
                    result.append((d, code, rate))
        except httpx.HTTPStatusError:
            continue
    result.sort(key=lambda x: (x[0], x[1]))
    return result
