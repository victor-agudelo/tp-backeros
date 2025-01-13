from sqlalchemy.orm import Session
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends


from database.database import database_conn
from domain.models.usuarios import Usuario


async def get_db_session() -> AsyncSession:
    async for session in database_conn.get_db():
        yield session


class UserRepository:
    def __init__(self,  db: Session):
        self.db = db

    async def user_by_email(self, email):
        stmt = select(Usuario).where(Usuario.correo == email)
        result = await self.db.execute(stmt)
        return result.scalars().first()


    async def current_user(self, payload, db: AsyncSession = Depends(get_db_session)):
        stmt = select(Usuario).where(Usuario.correo == payload['correo'])
        result = await db.execute(stmt)
        scalar_result = result.scalars().first()
        return scalar_result

    async def create_user(self, new_user):
        user = Usuario(**new_user.dict())
        self.db.add(user)
        await self.db.commit()