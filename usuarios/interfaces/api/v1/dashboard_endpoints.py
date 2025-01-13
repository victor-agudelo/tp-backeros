from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from database.database import database_conn

from interfaces.schemas.user_schemas import UserBase
from aplication.services.dashboard_services import DashboardServices

from adapters.auth import Auth

dashboard_router = APIRouter(
    prefix="/api/v1/dashboard",
    tags=["dashboard"],
    responses={404: {"description": "Not found"}}
)


async def get_db_session() -> AsyncSession:
    async for session in database_conn.get_db():
        yield session


@dashboard_router.get('/order-times')
async def get_all_orders(
        user: UserBase = Depends(Auth.get_current_user),
        page: int = Query(1, ge=1),
        page_size: int = Query(10, ge=1, le=50)
):
    dashboard_services = DashboardServices()
    return await dashboard_services.get_all_orders(page, page_size, user)


@dashboard_router.get('/employees')
async def get_employee_summary(
        user: UserBase = Depends(Auth.get_current_user),
        page: int = Query(1, ge=1),
        page_size: int = Query(10, ge=1, le=50)
):
    dashboard_services = DashboardServices()
    return await dashboard_services.get_employee_sumary(page, page_size, user)