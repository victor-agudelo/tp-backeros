from fastapi import APIRouter, Query, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from database.database import database_conn
from aplication.services.user_services import UserServices
from interfaces.schemas.user_schemas import UserBase, UserCreation

from adapters.auth import Auth


users_router = APIRouter(
    prefix="/api/v1/users",
    tags=["users"],
    responses={404: {"description": "Not found"}}
)


async def get_db_session() -> AsyncSession:
    async for session in database_conn.get_db():
        yield session


@users_router.post('/user')
async def create_user(
        new_user: UserCreation,
        user: UserBase = Depends(Auth.get_current_user),
        db: AsyncSession = Depends(get_db_session)
):
    user_services = UserServices(db)
    return await user_services.create_user(new_user, user)
