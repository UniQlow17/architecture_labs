from datetime import date

from pydantic import BaseModel


class SyncPeriodResponse(BaseModel):
    synced: int
    start_date: date
    end_date: date
    currencies: list[str]
