from fastapi import APIRouter, Query, Depends
from typing import List, Optional

from database.database import database

from aplication.services.order_services import OrderServices
from interfaces.schemas.pedidos_schemas import FulllOrder


pedidos_router = APIRouter(
    prefix="/api/v1/pedidos",
    tags=["pedidos"],
    responses={404: {"description": "Not found"}}
)


@pedidos_router.post('/new-order')
async def create_new_order(
        order: FulllOrder,
        db=Depends(database.get_database)
):
    order_services = OrderServices(database=db)
    return await order_services.create_order(order)


@pedidos_router.get('/all-orders/order-time/{restaurante_id}/')
async def get_all_orders_by_status(
        restaurante_id: int,
        page: int = Query(1, ge=1),
        page_size: int = Query(10, ge=1, le=50),
        db=Depends(database.get_database)
):
    order_services = OrderServices(database=db)

    return await order_services.get_orders(restaurante_id, page, page_size)


@pedidos_router.get('/all-orders/employees/{restaurante_id}/')
async def get_all_orders_by_status(
        restaurante_id: int,
        page: int = Query(1, ge=1),
        page_size: int = Query(10, ge=1, le=50),
        db=Depends(database.get_database)
):
    order_services = OrderServices(database=db)

    return await order_services.get_employees_rates(restaurante_id, page, page_size)


@pedidos_router.get('/all-orders-by-status/{restaurante_id}/{estado}')
async def get_all_orders_by_status(
        restaurante_id: int,
        estado: str,
        page: int = Query(1, ge=1),
        page_size: int = Query(10, ge=1, le=50),
        db=Depends(database.get_database)
):
    order_services = OrderServices(database=db)

    return await order_services.get_orders_by_status(restaurante_id, estado, page, page_size)


@pedidos_router.get('/order/{clientId}')
async def get_order_by_client_id(
        clientId: int,
        estado: Optional[str] = Query(default=None),
        db=Depends(database.get_database)
):
    order_services = OrderServices(database=db)
    return await order_services.get_order_by_client_id(clientId, estado)


@pedidos_router.get('/order-by-id/{pedidoId}')
async def get_order_by_order_id(
        pedidoId: str,
        db=Depends(database.get_database)
):
    order_services = OrderServices(database=db)
    return await order_services.get_order_by_order_id(pedidoId)


@pedidos_router.patch('/order/{orderId}/{estado}')
async def update_order(
        orderId: str,
        estado: str,
        empleado: str = Query(default=None),
        db=Depends(database.get_database)
):
    order_services = OrderServices(database=db)

    return await order_services.update_current_order(orderId, estado, empleado)


@pedidos_router.patch('/order/{orderId}')
async def asign_deliver_code(
        orderId: str,
        code: str = Query(),
        db=Depends(database.get_database)
):
    order_services = OrderServices(database=db)

    return await order_services.assign_code(orderId, code)


@pedidos_router.patch('/end-order/{orderId}')
async def order_delivered(
        orderId: str,
        code: str = Query(),
        db=Depends(database.get_database)
):
    order_services = OrderServices(database=db)

    return await order_services.finish_order(orderId, code)