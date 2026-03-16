from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_session
from app.query_schemas import ReportQuery, SyncPeriodQuery, get_report_query, get_sync_period_query
from app.schemas import CurrencyStats, ReportResponse, SyncPeriodResponse
from app.service import get_report, sync_period

api_router = APIRouter(prefix="/api", tags=["api"])


@api_router.post("/sync/period", response_model=SyncPeriodResponse)
async def api_sync_period(
    query: SyncPeriodQuery = Depends(get_sync_period_query),
    session: AsyncSession = Depends(get_session),
):
    if query.start_date > query.end_date:
        raise HTTPException(status_code=400, detail="start_date must be <= end_date")
    try:
        count = await sync_period(
            session, query.start_date, query.end_date, query.currencies
        )
        return SyncPeriodResponse(
            synced=count,
            start_date=query.start_date,
            end_date=query.end_date,
            currencies=query.currencies,
        )
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"Sync failed: {e!s}") from e


@api_router.get("/report", response_model=ReportResponse)
async def api_report(
    query: ReportQuery = Depends(get_report_query),
    session: AsyncSession = Depends(get_session),
):
    if query.start_date > query.end_date:
        raise HTTPException(status_code=400, detail="start_date must be <= end_date")
    report = await get_report(
        session, query.start_date, query.end_date, query.currencies
    )
    return ReportResponse(
        start_date=query.start_date,
        end_date=query.end_date,
        currencies={k: CurrencyStats(**v) for k, v in report.items()},
    )
