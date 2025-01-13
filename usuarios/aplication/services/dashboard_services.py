import os
import json
import httpx


from exceptions.exception_handler import InvalidRequest


class DashboardServices:

    async def get_all_orders(self, page, page_size, user):
        if user.rol != "propietario":
            raise InvalidRequest(
                status_code=401, detail="No tiene permisos para ver los datos")

        try:
            BASE_URL = os.getenv("API_TRAZABILIDAD")
            FULL_URL = f"{BASE_URL}/pedidos/all-orders/order-time/{user.idUsuario}/"

            headers = {"accept": "application/json"}

            params = {
                "page": page,
                "page_size": page_size
            }

            async with httpx.AsyncClient() as client:
                response = await client.get(FULL_URL, headers=headers, params=params)

            if response.status_code != 200:
                raise InvalidRequest(
                    status_code=response.status_code,
                    detail=f"Error al obtener la informacion: {response.text}"
                )

            return json.loads(response.text)

        except httpx.RequestError as e:
            raise InvalidRequest(
                status_code=500, detail=f"Error al realizar la conexion: {e}")

    async def get_employee_sumary(self, page, page_size, user):
        if user.rol != "propietario":
            raise InvalidRequest(
                status_code=401, detail="No tiene permisos para ver los datos")

        try:
            BASE_URL = os.getenv("API_TRAZABILIDAD")
            FULL_URL = f"{BASE_URL}/pedidos/all-orders/employees/{user.idUsuario}/"

            headers = {"accept": "application/json"}

            params = {
                "page": page,
                "page_size": page_size
            }

            async with httpx.AsyncClient() as client:
                response = await client.get(FULL_URL, headers=headers, params=params)

            if response.status_code != 200:
                raise InvalidRequest(
                    status_code=response.status_code,
                    detail=f"Error al obtener la informacion: {response.text}"
                )

            return json.loads(response.text)

        except httpx.RequestError as e:
            raise InvalidRequest(
                status_code=500, detail=f"Error al realizar la conexion: {e}")
