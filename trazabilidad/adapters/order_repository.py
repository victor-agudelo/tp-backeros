from datetime import datetime
from domain.models.pedido import Pedido

from utils.paginator import MongoPaginatorRepository


class OrderRepository:
    def __init__(self, db):
        self.order_collection = db.pedidos
        self.paginator = MongoPaginatorRepository(self.order_collection)

    async def create_transaction(self, order: Pedido):
        await self.order_collection.insert_one(order.model_dump())

        return order.pedido_id

    async def get_orders(self, restaurant_id, page: int = 1, page_size: int = 10, order = "pedidoRealizadoTimestamp"):
        query = {"restaurante_id": restaurant_id}

        fields = {
            "pedido_id": 1,
            "estado": 1,
            "pedidoRealizadoTimestamp": 1,
            "pedidoListoTimestamp": 1,
            "duracionPreparacion": 1,
            "_id": 0
        }

        add_fields = {
            "$addFields": {
                "duracionPreparacion": {
                    "$cond": {
                        "if": {"$and": ["$pedidoRealizadoTimestamp", "$pedidoListoTimestamp"]},
                        "then": {
                            "$divide": [
                                {"$subtract": ["$pedidoListoTimestamp", "$pedidoRealizadoTimestamp"]},
                                1000 * 60
                            ]
                        },
                        "else": None
                    }
                }
            }
        }

        paginated_result = await self.paginator.paginate_query(
            query=query,
            page=page,
            page_size=page_size,
            order=order,
            fields=fields,
            add_fields=add_fields
        )

        return paginated_result

    async def get_employees_rates(self, restaurant_id, page: int = 1, page_size: int = 10, order = "pedidoRealizadoTimestamp"):
        query = {
            "restaurante_id": restaurant_id,
            "pedidoRealizadoTimestamp": {"$ne": None},
            "pedidoListoTimestamp": {"$ne": None},
            "empleadoAsignado": {"$ne": None}
            }

        add_fields = {
            "$addFields": {
                "duracionPreparacion": {
                    "$cond": {
                        "if": {"$and": ["$pedidoRealizadoTimestamp", "$pedidoListoTimestamp"]},
                        "then": {
                            "$divide": [
                                {"$subtract": ["$pedidoListoTimestamp", "$pedidoRealizadoTimestamp"]},
                                1000 * 60
                            ]
                        },
                        "else": None
                    }
                }
            }
        }

        group_by = {
                "_id": "$empleadoAsignado",
                "tiempoMedio": {"$avg": "$duracionPreparacion"},
                "totalPedidos": {"$sum": 1}
            }

        paginated_result = await self.paginator.paginate_query(
            query=query,
            page=page,
            page_size=page_size,
            order=order,
            add_fields=add_fields,
            group_by=group_by
        )

        return paginated_result

    async def get_orders_by_status(self, restaurant_id, status, page: int = 1, page_size: int = 10, order = "pedidoRealizadoTimestamp"):
        query = {"restaurante_id": restaurant_id, "estado": status}

        paginated_result = await self.paginator.paginate_query(
            query=query,
            page=page,
            page_size=page_size,
            order=order
        )

        paginated_result["items"] = [Pedido(**item) for item in paginated_result["items"]]

        return paginated_result

    async def get_order(self, order_id):
        query = {"pedido_id": order_id}

        return await self.order_collection.find_one(query)

    async def get_order_by_client(self, client_id, estado=None):
        query = {"cliente_id": client_id}
        if estado:
            query["estado"] = estado

        return await self.order_collection.find_one(query)

    async def update_order(self, orderId, estado, empleado = None):

        if estado == "Listo":
            update_fields = {
                "estado": estado,
                "pedidoListoTimestamp": datetime.now()
            }
        elif estado == "En-Preparacion":
            update_fields = {
                "estado": estado,
                "pedidoEnPreparacionTimestamp": datetime.now()
            }
        elif estado == "Cancelada":
            update_fields = {
                "estado": estado,
            }

        if empleado:
            update_fields["empleadoAsignado"] = empleado

        await self.order_collection.update_one(
            {"pedido_id": orderId},
            {"$set": update_fields}
        )

        return await self.get_order(orderId)

    async def update_code_order(self, order_id, code):
        update_fields = {
            "codigoEntrega": code
        }

        await self.order_collection.update_one(
            {"pedido_id": order_id},
            {"$set": update_fields}
        )

    async def update_deliver_status(self, order_id):
        update_fields = {
            "entregado": True
        }

        await self.order_collection.update_one(
            {"pedido_id": order_id},
            {"$set": update_fields}
        )