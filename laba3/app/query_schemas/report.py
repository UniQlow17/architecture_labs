from datetime import date

from fastapi import HTTPException, Query
from pydantic import BaseModel, Field

from app.core.config import settings
from app.utils.currencies import normalize_currencies


class ReportQuery(BaseModel):
    start_date: date = Field(..., description="Начало периода (YYYY-MM-DD)")
    end_date: date = Field(..., description="Конец периода (YYYY-MM-DD)")
    currencies: list[str] = Field(..., description="Коды валют: EUR,USD,GBP")


def get_report_query(
    start_date: date = Query(..., description="Начало периода (YYYY-MM-DD)"),
    end_date: date = Query(..., description="Конец периода (YYYY-MM-DD)"),
    currencies: list[str] | str | None = Query(None, description="Коды валют (например EUR,USD)"),
) -> ReportQuery:
    cur = normalize_currencies(currencies) if currencies else settings.sync_currencies
    return ReportQuery(start_date=start_date, end_date=end_date, currencies=cur)
