from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class DatabaseSettings(BaseSettings):
    db_host: str = Field(default="localhost", alias="DB_HOST")
    db_port: int = Field(default=5432, alias="DB_PORT")
    db_user: str = Field(default="postgres", alias="DB_USER")
    db_password: str = Field(default="postgres", alias="DB_PASSWORD")
    db_name: str = Field(default="cnb", alias="DB_NAME")

    @property
    def url(self) -> str:
        return (
            f"postgresql+asyncpg://{self.db_user}:{self.db_password}"
            f"@{self.db_host}:{self.db_port}/{self.db_name}"
        )

    @property
    def url_sync(self) -> str:
        return (
            f"postgresql://{self.db_user}:{self.db_password}"
            f"@{self.db_host}:{self.db_port}/{self.db_name}"
        )


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    database: DatabaseSettings = Field(default_factory=DatabaseSettings)
    sync_cron: str = Field(default="1 0 * * *", alias="SYNC_CRON")
    sync_currencies: list[str] = Field(
        default=["EUR", "USD", "GBP", "CHF", "PLN"],
        alias="SYNC_CURRENCIES",
        description="Коды валют через запятую",
    )
    sync_history_years_back: int = Field(default=0, ge=0, le=30, alias="SYNC_HISTORY_YEARS_BACK")
    cnb_daily_url: str = Field(
        default="https://www.cnb.cz/en/financial_markets/foreign_exchange_market/exchange_rate_fixing/daily.txt",
        alias="CNB_DAILY_URL",
    )
    cnb_year_url: str = Field(
        default="https://www.cnb.cz/en/financial_markets/foreign_exchange_market/exchange_rate_fixing/year.txt",
        alias="CNB_YEAR_URL",
    )


settings = Settings()