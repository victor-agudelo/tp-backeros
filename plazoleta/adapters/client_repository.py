from sqlalchemy.orm import Session
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends


from database.database import database_conn
from domain.models.clientes import Clientes


async def get_db_session() -> AsyncSession:
    async for session in database_conn.get_db():
        yield session


class ClientRepository:
    def __init__(self,  db: Session):
        self.db = db

    async def client_by_email(self, email):
        stmt = select(Clientes).where(Clientes.correo == email)
        result = await self.db.execute(stmt)
        return result.scalars().first()


    async def current_client(self, payload, db: AsyncSession = Depends(get_db_session)):
        stmt = select(Clientes).where(Clientes.correo == payload['correo'])
        result = await db.execute(stmt)
        scalar_result = result.scalars().first()
        return scalar_result

    async def create_client(self, new_client):
        self.db.expire_all()
        client = Clientes(**new_client.dict())
        self.db.add(client)
        await self.db.commit()