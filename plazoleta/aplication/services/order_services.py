import os
import json
import httpx

from datetime import datetime
from dotenv import load_dotenv, find_dotenv

from exceptions.exception_handler import InvalidRequest

from interfaces.schemas.restaurant_schemas import ClientRestaurant
from interfaces.schemas.order_schemas import FulllOrder


load_dotenv(find_dotenv())


class OrderServices:

    async def get_all_restaurants(self, page: int, page_size: int):
        try:
            BASE_URL = os.getenv("API_USUARIOS")
            FULL_URL = f"{BASE_URL}/restaurants/all-restaurants"
            params = {
                "page": page,
                "page_size": page_size
            }

            headers={"accept": "application/json"}

            async with httpx.AsyncClient() as client:
                response = await client.get(FULL_URL, params=params, headers=headers)

            if response.status_code != 200:
                raise InvalidRequest(
                    status_code=response.status_code,
                    detail=f"Error al obtener los restaurantes: {response.text}"
                )
            final_response = response.json()
            if final_response["restaurants"]:
                final_response["restaurants"] = [ClientRestaurant(**restaurant) for restaurant in final_response["restaurants"]]

            return final_response

        except httpx.RequestError as e:
            raise InvalidRequest(status_code=500, detail=f"Error al obtener los restaurantes: {e}")

    async def get_active_dishes(self, owner_id, page: int = 1, page_size: int = 10, category=None):
        try:
            BASE_URL = os.getenv("API_USUARIOS")
            FULL_URL = f"{BASE_URL}/dishes/platos-activos/{owner_id}"

            if category:
                params = {
                    "page": page,
                    "page_size": page_size,
                    "category": category
                }
            else:
                params = {
                    "page": page,
                    "page_size": page_size
                }

            headers = {"accept": "application/json"}

            async with httpx.AsyncClient() as client:
                response = await client.get(FULL_URL, params=params, headers=headers)

            if response.status_code != 200:
                raise InvalidRequest(
                    status_code=response.status_code,
                    detail=f"Error al obtener los restaurantes: {response.text}"
                )
            return response.json()
        except httpx.RequestError as e:
            raise InvalidRequest(status_code=500, detail=f"Error al obtener los platos del restaurante: {e}")


    async def get_order(self, order_id, client_id):
        try:
            BASE_URL = os.getenv("API_TRAZABILIDAD")
            FULL_URL = f"{BASE_URL}/pedidos/order-by-id/{order_id}"

            headers = {"accept": "application/json"}

            async with httpx.AsyncClient() as client:
                response = await client.get(FULL_URL, headers=headers)

            if response.status_code != 200:
                raise InvalidRequest(
                    status_code=response.status_code,
                    detail=f"Error al obtener la orden: {response.text}"
                )

            return response.json()

        except httpx.RequestError as e:
            raise InvalidRequest(status_code=500, detail=f"Error al obtener la información de la orden: {e}")



    async def post_new_order(self, new_order, client):
        active_orders = await self.__get_active_orders(client.idCliente)

        if active_orders and active_orders["estado"] == "Pendiente":
            raise InvalidRequest(status_code=400, detail=f"Hay ordenes activas en el momento")

        full_new_order = FulllOrder(
            **new_order.__dict__,
            cliente_id=client.idCliente,
            Celular=client.Celular,
            estado="Pendiente",
            pedidoRealizadoTimestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        )

        try:
            BASE_URL = os.getenv("API_TRAZABILIDAD")
            FULL_URL = f"{BASE_URL}/pedidos/new-order"

            headers = {
                "accept": "application/json",
                "Content-Type": "application/json"
            }

            async with httpx.AsyncClient() as client:
                response = await client.post(FULL_URL, json=full_new_order.__dict__, headers=headers)

            if response.status_code != 200:
                raise InvalidRequest(
                    status_code=response.status_code,
                    detail=f"Error al enviar el pedido al restaurante: {response.content}"
                )

            return response.text#"Pedido enviado"

        except httpx.RequestError as e:
            raise InvalidRequest(status_code=500, detail=f"Error de conexion: {e}")

    async def cancel_order(self, order_id, client):
        pending_orders = await self.__get_active_orders(client.idCliente)

        if not pending_orders:
            raise InvalidRequest(status_code=400, detail=f"Lo sentimos, tu pedido ya está en preparación y no puede cancelarse")

        if pending_orders.get("pedido_id") != order_id:
            raise InvalidRequest(status_code=400,
                                 detail=f"Lo sentimos, tu pedido ya está en preparación o finalizado y no puede cancelarse")

        try:
            BASE_URL = os.getenv("API_TRAZABILIDAD")
            FULL_URL = f"{BASE_URL}/pedidos/order/{order_id}/Cancelada"

            headers = {"accept": "application/json"}

            async with httpx.AsyncClient() as client:
                response = await client.patch(FULL_URL, headers=headers)

            if response.status_code != 200:
                raise InvalidRequest(
                    status_code=response.status_code,
                    detail=f"Error al cancelar el pedido: {response.text}"
                )

            return "Orden cancelada"

        except httpx.RequestError as e:
            raise InvalidRequest(status_code=500, detail=f"Error de conexion: {e}")

    async def __get_active_orders(self, client_id, estado="Pendiente"):
        try:
            BASE_URL = os.getenv("API_TRAZABILIDAD")
            FULL_URL = f"{BASE_URL}/pedidos/order/{client_id}"

            headers = {
                "accept": "application/json",
                "Content-Type": "application/json"
            }
            params = {
                "estado": estado
            }


            async with httpx.AsyncClient() as client:
                response = await client.get(FULL_URL, headers=headers, params=params)

            if response.status_code != 200:
                raise InvalidRequest(
                    status_code=response.status_code,
                    detail=f"Error en la consulta del servicio: {response.content}"
                )

            return json.loads(response.text)

        except httpx.RequestError as e:
            raise InvalidRequest(status_code=500, detail=f"Error de conexion: {e}")
