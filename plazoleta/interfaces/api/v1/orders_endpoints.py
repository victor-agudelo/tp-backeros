from fastapi import APIRouter, Query, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from database.database import database_conn
from aplication.services.order_services import OrderServices
from interfaces.schemas.client_schemas import ClientCreation, ClientBase
from interfaces.schemas.order_schemas import OrderBase

from adapters.auth import Auth


orders_router = APIRouter(
    prefix="/api/v1/orders",
    tags=["orders"],
    responses={404: {"description": "Not found"}}
)


async def get_db_session() -> AsyncSession:
    async for session in database_conn.get_db():
        yield session


@orders_router.get('/all-restaurants')
async def get_all_restaurants(
        page: int = Query(1, ge=1),
        page_size: int = Query(10, ge=1, le=50),
        client: ClientBase = Depends(Auth.get_current_user),
):
    order_services = OrderServices()

    return await order_services.get_all_restaurants(page, page_size)


@orders_router.get('/platos-activos/{idRestaurante}')
async def get_active_dishes(
        idRestaurante: int,
        page: int = Query(1, ge=1),
        page_size: int = Query(10, ge=1, le=50),
        category: str = Query(None)
):
    order_services = OrderServices()
    return await order_services.get_active_dishes(idRestaurante, page, page_size, category)


@orders_router.get('/order/{orderId}')
async def get_order(
        orderId: str,
        client: ClientBase = Depends(Auth.get_current_user)
):
    order_services = OrderServices()

    return await order_services.get_order(orderId, client.idCliente)


@orders_router.post('/new-order')
async def create_new_order(
        new_order: OrderBase,
        client: ClientBase = Depends(Auth.get_current_user)
):
    order_services = OrderServices()

    return await order_services.post_new_order(new_order, client)


@orders_router.patch('/cancel-order/{orderId}')
async def cancel_order(
        orderId: str,
        client: ClientBase = Depends(Auth.get_current_user)
):
    order_services = OrderServices()

    return await order_services.cancel_order(orderId, client)
