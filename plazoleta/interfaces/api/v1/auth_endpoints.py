from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from exceptions.exception_handler import InvalidRequest
from database.database import database_conn
from adapters.auth import Auth


auth_router = APIRouter(
    prefix="/api/v1/auth",
    tags=["auth"],
    responses={404: {"description": "Not found"}}
)


async def get_db_session() -> AsyncSession:
    async for session in database_conn.get_db():
        yield session


@auth_router.post('/token')
async def generate_token(
        form_data: OAuth2PasswordRequestForm = Depends(),
        db: AsyncSession = Depends(get_db_session)
):
    auth_services = Auth(db)
    user = await auth_services.authenticate(
        email=form_data.username,
        password=form_data.password
    )
    if not user:
        raise InvalidRequest(
            status_code=401, detail='Invalid username or password')
    return auth_services.create_token(user)
