from fastapi import APIRouter, Query, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from database.database import database_conn
from aplication.services.client_services import ClientServices
from interfaces.schemas.client_schemas import ClientBase

from adapters.auth import Auth


clients_router = APIRouter(
    prefix="/api/v1/clients",
    tags=["clients"],
    responses={404: {"description": "Not found"}}
)

async def get_db_session() -> AsyncSession:
    async for session in database_conn.get_db():
        yield session


@clients_router.post('/client')
async def create_client(
        new_client: ClientBase,
        db: AsyncSession = Depends(get_db_session)
):
    client_services = ClientServices(db)
    return await client_services.create_client(new_client)
