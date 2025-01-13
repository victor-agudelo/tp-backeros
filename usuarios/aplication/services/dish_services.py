from sqlalchemy.orm import Session

from adapters.dish_repository import DishRepository
from exceptions.exception_handler import InvalidRequest
from interfaces.schemas.dish_schemas import FullDish, DishBase, DishResponse


class DishServices:
    def __init__(self, db: Session):
        self.db = db
        self.dish_repository = DishRepository(db)

    async def create_dish(
            self,
            current_user,
            dish_info
    ):
        if current_user.rol != "propietario":
            raise InvalidRequest(
                status_code=401, detail="No tiene permisos para crear un plato")

        new_dish = FullDish(**dish_info.dict(),
                            idRestaurante=current_user.idUsuario)

        await self.dish_repository.new_dish(new_dish)

        return dish_info

    async def get_all_dishes(self, user):
        if user.rol != "propietario":
            raise InvalidRequest(
                status_code=401, detail="No tiene permisos para ver los platos")

        all_dishes = await self.dish_repository.get_all_dishes(user.idUsuario)

        if all_dishes:
            return [DishResponse(**dish.__dict__) for dish in all_dishes]
        return []

    async def update_dish(self, current_user, dish_id, dish_info):
        if current_user.rol != "propietario":
            raise InvalidRequest(
                status_code=401, detail="No tiene permisos para actualizar un plato")

        dish = await self.dish_repository.get_dish_by_id(dish_id)

        if not dish:
            raise InvalidRequest(status_code=404, detail="El plato no existe")
        if dish.idRestaurante != current_user.idUsuario:
            raise InvalidRequest(
                status_code=401, detail="No tiene permisos para actualizar este plato")

        dish.Precio = dish_info.Precio
        dish.Descripcion = dish_info.Descripcion

        await self.dish_repository.update_dish(dish)

        return DishResponse(**dish.__dict__)

    async def enable_dish(self, current_user, dish_id):
        if current_user.rol != "propietario":
            raise InvalidRequest(
                status_code=401, detail="No tiene permisos para habilitar un plato")

        dish = await self.dish_repository.get_dish_by_id(dish_id)

        if not dish:
            raise InvalidRequest(status_code=404, detail="El plato no existe")
        if dish.idRestaurante != current_user.idUsuario:
            raise InvalidRequest(
                status_code=401, detail="No tiene permisos para habilitar este plato")

        if dish.estado:
            dish.estado = False
        else:
            dish.estado = True

        await self.dish_repository.update_dish(dish)

        return DishResponse(**dish.__dict__)

    async def get_active_dishes(self, owner_id, page: int = 1, page_size: int = 10, category=None):
        paginated_data = await self.dish_repository.get_active_dishes(owner_id, page, page_size, category)

        return {
            "total": paginated_data["total"],
            "page": paginated_data["page"],
            "page_size": paginated_data["page_size"],
            "restaurants": [
                DishResponse(**restaurant.__dict__) for restaurant in paginated_data["items"]
            ]
        }
