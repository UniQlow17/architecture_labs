from datetime import date
from decimal import Decimal

from sqlalchemy import Date, Numeric, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base


class ExchangeRate(Base):
    __tablename__ = "exchange_rates"
    __table_args__ = (UniqueConstraint("rate_date", "currency_code", name="uq_exchange_rates_date_currency"),)

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    rate_date: Mapped[date] = mapped_column(Date, nullable=False, index=True)
    currency_code: Mapped[str] = mapped_column(String(3), nullable=False, index=True)
    rate_per_unit: Mapped[Decimal] = mapped_column(Numeric(20, 6), nullable=False)

    def __repr__(self) -> str:
        return f"ExchangeRate({self.rate_date!r}, {self.currency_code!r}, {self.rate_per_unit!r})"
