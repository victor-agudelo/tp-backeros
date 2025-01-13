from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session

from domain.models.usuarios import Usuario
from domain.models.restaurantes import Restaurantes
from utils.paginator import PaginatorRepository


class RestaurantRepository:
    def __init__(self,  db: Session):
        self.db = db
        self.paginator = PaginatorRepository(db)

    async def get_restaurant_owner(self, owner_id):
        stmt = select(Usuario).where(Usuario.DocumentoDeIdentidad == owner_id)
        result = await self.db.execute(stmt)
        return result.scalars().first()

    async def create_new_restaurant(self, new_restaurant):
        restaurant = Restaurantes(**new_restaurant.dict())
        self.db.add(restaurant)
        await self.db.commit()

    async def get_all_restaurants(self, page: int = 1, page_size: int = 10):
        stmt = select(Restaurantes).where(Restaurantes.estado ==
                                          True).order_by(Restaurantes.Nombre)
        return await self.paginator.paginate_query(
            query=stmt,
            page=page,
            page_size=page_size
        )
