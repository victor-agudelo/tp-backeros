from sqlalchemy.future import select
from sqlalchemy.orm import Session

from domain.models.platos import Platos
from utils.paginator import PaginatorRepository


class DishRepository:
    def __init__(self,  db: Session):
        self.db = db
        self.paginator = PaginatorRepository(db)

    async def new_dish(self, new_dish):
        plato = Platos(**new_dish.dict())
        self.db.add(plato)
        await self.db.commit()

    async def get_all_dishes(self, owner_id):
        stmt = select(Platos).where(Platos.idRestaurante == owner_id)
        result = await self.db.execute(stmt)
        return result.scalars().all()

    async def get_dish_by_id(self, dish_id):
        stmt = select(Platos).where(Platos.idPlato == dish_id)
        result = await self.db.execute(stmt)
        return result.scalars().first()

    async def update_dish(self, dish):
        await self.db.commit()
        await self.db.refresh(dish)
        return dish

    async def get_active_dishes(self, owner_id, page: int = 1, page_size: int = 10, category=None):
        if category:
            stmt = select(Platos).where(Platos.idRestaurante == owner_id, Platos.estado ==
                                        True, Platos.categoria == category).order_by(Platos.Nombre)
        else:
            stmt = select(Platos).where(Platos.idRestaurante ==
                                        owner_id, Platos.estado == True).order_by(Platos.Nombre)
        return await self.paginator.paginate_query(
            query=stmt,
            page=page,
            page_size=page_size
        )
