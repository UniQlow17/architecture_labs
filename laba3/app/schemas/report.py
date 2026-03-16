from datetime import date

from pydantic import BaseModel


class CurrencyStats(BaseModel):
    min: float | None = None
    max: float | None = None
    avg: float | None = None


class ReportResponse(BaseModel):
    start_date: date
    end_date: date
    currencies: dict[str, CurrencyStats]
