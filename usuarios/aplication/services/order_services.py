import os
import json
import httpx

from datetime import datetime
from dotenv import load_dotenv, find_dotenv

from exceptions.exception_handler import InvalidRequest
from utils.random_generator import combination
from utils.message_creator import MessageCreator
from utils.sender import MessageSender

from interfaces.schemas.order_schemas import OrderResponse


load_dotenv(find_dotenv())


class OrderServices:

    async def get_all_orders(self, estado, user, page: int = 1, page_size: int = 10):
        try:
            BASE_URL = os.getenv("API_TRAZABILIDAD")
            FULL_URL = f"{BASE_URL}/pedidos/all-orders/{user.idRestaurante}/{estado}"
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
                    detail=f"Error al obtener los pedidos: {response.text}"
                )
            final_response = response.json()

            return final_response

        except httpx.RequestError as e:
            raise InvalidRequest(
                status_code=500, detail=f"Error al obtener los pedidos: {e}")

    async def patch_active_order(self, pedido_id, user):
        try:
            BASE_URL = os.getenv("API_TRAZABILIDAD")
            FULL_URL = f"{BASE_URL}/pedidos/order/{pedido_id}/En-Preparacion"

            headers = {"accept": "application/json"}

            params = {
                "empleado": user.correo
            }

            async with httpx.AsyncClient() as client:
                response = await client.patch(FULL_URL, headers=headers, params=params)

            if response.status_code != 200:
                raise InvalidRequest(
                    status_code=response.status_code,
                    detail=f"Error al asignar el pedido: {response.text}"
                )

            return response.text

        except httpx.RequestError as e:
            raise InvalidRequest(
                status_code=500, detail=f"Error al realizar la conexion: {e}")

    async def finish_order(self, pedido_id):
        try:
            BASE_URL = os.getenv("API_TRAZABILIDAD")
            FULL_URL = f"{BASE_URL}/pedidos/order/{pedido_id}/Listo"

            headers = {"accept": "application/json"}

            async with httpx.AsyncClient() as client:
                response = await client.patch(FULL_URL, headers=headers)

            if response.status_code != 200:
                raise InvalidRequest(
                    status_code=response.status_code,
                    detail=f"Error al finalizar el pedido: {response.text}"
                )

            response_json = json.loads(response.text)
            receipt_code = combination.generate_code()

            await self.__assign_deliver_code(response_json.get("pedido_id"), receipt_code)

            message = MessageCreator(response_json, receipt_code)
            # sender = MessageSender(...).send_message()

            return "Message sent"  # sender

        except httpx.RequestError as e:
            raise InvalidRequest(
                status_code=500, detail=f"Error al realizar la conexion: {e}")

    async def deliver_order(self, pedido_id, code):
        try:
            BASE_URL = os.getenv("API_TRAZABILIDAD")
            FULL_URL = f"{BASE_URL}/pedidos/end-order/{pedido_id}"

            headers = {"accept": "application/json"}

            params = {
                "code": code
            }

            async with httpx.AsyncClient() as client:
                response = await client.patch(FULL_URL, headers=headers, params=params)

            if response.status_code != 200:
                raise InvalidRequest(
                    status_code=response.status_code,
                    detail=f"Error al entregar el pedido: {response.text}"
                )

            return response.text

        except httpx.RequestError as e:
            raise InvalidRequest(
                status_code=500, detail=f"Error al realizar la conexion: {e}")

    async def __assign_deliver_code(self, order_id, code):
        try:
            BASE_URL = os.getenv("API_TRAZABILIDAD")
            FULL_URL = f"{BASE_URL}/pedidos/order/{order_id}"

            headers = {"accept": "application/json"}

            params = {"code": code}

            async with httpx.AsyncClient() as client:
                response = await client.patch(FULL_URL, headers=headers, params=params)

            if response.status_code != 200:
                raise InvalidRequest(
                    status_code=response.status_code,
                    detail=f"Error al asignar el codigo: {response.text}"
                )

            return response.text
        except httpx.RequestError as e:
            raise InvalidRequest(
                status_code=500, detail=f"Error al realizar la conexion: {e}")
