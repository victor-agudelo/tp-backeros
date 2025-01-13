from exceptions.exception_handler import InvalidRequest

from domain.models.pedido import Pedido
from adapters.order_repository import OrderRepository
from interfaces.schemas.pedidos_schemas import OrderResponse, FulllOrder, FinalOrder



class OrderServices:
    def __init__(self, database):
        self.db = database
        self.order_repository = OrderRepository(self.db)

    async def create_order(self, order):
        new_order = Pedido(**order.__dict__)
        new_transaction = await self.order_repository.create_transaction(new_order)

        return OrderResponse(
            message="Orden creada con éxito",
            order_id=new_transaction
        )

    async def get_orders(self, restaurant_id, page: int = 1, page_size: int = 10):
        return await self.order_repository.get_orders(restaurant_id, page, page_size)

    async def get_employees_rates(self, restaurant_id, page: int = 1, page_size: int = 10):
        return await self.order_repository.get_employees_rates(restaurant_id, page, page_size, "tiempoMedio")

    async def get_orders_by_status(self, restaurant_id, status, page: int = 1, page_size: int = 10):
        return await self.order_repository.get_orders_by_status(restaurant_id, status, page, page_size)

    async def get_order_by_client_id(self, client_id, estado = None):
        order_by_client = await self.__get_order_by_client_id(client_id, estado)

        if order_by_client:
            return FulllOrder(**order_by_client)
        return []

    async def get_order_by_order_id(self, order_id):
        order_by_order_id = await self.__get_order_by_id(order_id)

        if order_by_order_id:
            return FinalOrder(**order_by_order_id)
        return []

    async def update_current_order(self, orderId, estado, empleado = None):
        if estado not in ("Pendiente", "En-Preparacion", "Listo", "Cancelada"):
            raise InvalidRequest(detail="Estado no es valido")
        current_order = await self.__get_order_by_id(orderId)

        if not current_order:
            raise InvalidRequest(status_code=401, detail="No existe esta orden")

        if current_order.get("estado") == "Cancelada":
            raise InvalidRequest(detail="No es posible actualizar el estado de una orden cancelada")

        order = await self.__update_order(orderId, estado, empleado)

        return FinalOrder(**order)

    async def assign_code(self, order_id, code):
        await self.__update_code_order(order_id, code)

    async def finish_order(self, order_id, code):
        current_order = await self.__get_order_by_id(order_id)

        if not current_order:
            raise InvalidRequest(status_code=401, detail="No existe esta orden")

        if current_order.get('estado') != "Listo":
            raise InvalidRequest(status_code=401, detail="El pedido aun no esta Listo")

        if current_order.get('codigoEntrega') != code:
            raise InvalidRequest(status_code=401, detail="Codigo no coincide")

        await self.__update_deliver_status(order_id)
        return "Pedido finalizado"

    async def __get_order_by_id(self, order_id):
        return await self.order_repository.get_order(order_id)

    async def __get_order_by_client_id(self, client_id, estado = None):
        return await self.order_repository.get_order_by_client(client_id, estado)

    async def __update_order(self, orderId, estado, empleado = None):
        return await self.order_repository.update_order(orderId, estado, empleado)

    async def __update_code_order(self, order_id, code):
        return await self.order_repository.update_code_order(order_id, code)

    async def __update_deliver_status(self, order_id):
        return await self.order_repository.update_deliver_status(order_id)
