from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import declarative_base
from sqlalchemy.exc import SQLAlchemyError


from config.db_config import database_config


class Database:
    def __init__(self):
        self.database_url = database_config.database_url
        self.engine = create_async_engine(self.database_url, echo=True)
        self.session = async_sessionmaker(
            bind=self.engine,
            expire_on_commit=False,
            class_=AsyncSession
        )
        self.base = declarative_base()

    async def get_db(self):
        async with self.session() as session:
            try:
                yield session
            finally:
                await session.close()

    async def get_ping(self):
        try:
            async with self.engine.connect():
                return True
        except SQLAlchemyError as e:
            print(f"Error de conexión: {e}")
            return False
        finally:
            await self.shutdown()

    async def shutdown(self):
        await self.engine.dispose()


database_conn = Database()
