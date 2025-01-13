import os

from dotenv import load_dotenv, find_dotenv
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from sqlalchemy.future import select
from jwt import encode, decode
from sqlalchemy.ext.asyncio import AsyncSession

from exceptions.exception_handler import InvalidRequest
from database.database import database_conn
from domain.models.usuarios import Usuario
from interfaces.schemas.user_schemas import FullUser, UserId
from config.app_settings import app_settings


load_dotenv(find_dotenv())

async def get_db_session() -> AsyncSession:
    async for session in database_conn.get_db():
        yield session



class Auth:
    def __init__(self, db: Session):
        self.db = db

    async def get_user_by_email(
            self,
            email: str
    ):
        stmt = select(Usuario).where(Usuario.correo == email)
        result = await self.db.execute(stmt)
        return result.scalars().first()


    async def authenticate(
            self,
            email: str,
            password: str
    ):
        user = await self.get_user_by_email(email)

        if not user:
            return False
        if not user.verify_password(password):
            return False

        return user

    def create_token(
            self,
            user: Usuario
    ):
        user_schema = FullUser(**user.__dict__)

        token = encode(
            payload=user_schema.dict(),
            key=app_settings.JWT_SECRET,
            algorithm=app_settings.ALGORITHMS
        )

        return dict(
            access_token=token,
            token_type="bearer"
        )

    @staticmethod
    async def get_current_user(
            token: str = Depends(OAuth2PasswordBearer(tokenUrl=os.getenv("TOKEN_URL_V1"))),
            db: AsyncSession = Depends(get_db_session)

    ):
        try:
            payload = decode(
                jwt=token,
                key=app_settings.JWT_SECRET,
                algorithms=[app_settings.ALGORITHMS]
            )

            stmt = select(Usuario).where(Usuario.correo == payload['correo'])
            result = await db.execute(stmt)
            scalar_result = result.scalars().first()
            return UserId(**scalar_result.__dict__)
        except Exception as e:
            print(e)
            raise InvalidRequest(status_code=401, detail='Credenciales invalidas')
