from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from interfaces.schemas.user_schemas import UserBase
from database.database import database_conn
from aplication.services.order_services import OrderServices

from adapters.auth import Auth

orders_router = APIRouter(
    prefix="/api/v1/orders",
    tags=["orders"],
    responses={404: {"description": "Not found"}}
)

async def get_db_session() -> AsyncSession:
    async for session in database_conn.get_db():
        yield session


@orders_router.get('/all-orders/{estado}')
async def get_all_orders(
        estado: str,
        page: int = Query(1, ge=1),
        page_size: int = Query(10, ge=1, le=50),
        user: UserBase = Depends(Auth.get_current_user),
):
    order_services = OrderServices()

    return await order_services.get_all_orders(estado, user, page, page_size)


@orders_router.patch('/take-order/{pedidoId}')
async def take_order(
        pedidoId: str,
        user: UserBase = Depends(Auth.get_current_user)
):
    order_services = OrderServices()

    return await order_services.patch_active_order(pedidoId, user)


@orders_router.patch('/end-order/{pedidoId}')
async def finish_order(
        pedidoId: str,
        user: UserBase = Depends(Auth.get_current_user)
):
    order_services = OrderServices()

    return await order_services.finish_order(pedidoId)

@orders_router.patch('/deliver-order/{pedidoId}')
async def deliver_order(
        pedidoId: str,
        code: str,
        user: UserBase = Depends(Auth.get_current_user)
):
    order_services = OrderServices()

    return await order_services.deliver_order(pedidoId, code)
