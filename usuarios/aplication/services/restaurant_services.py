from sqlalchemy.orm import Session

from adapters.restaurant_repository import RestaurantRepository
from interfaces.schemas.restaurant_schemas import FullRestaurant, RestaurantBase, PublicRestaurant
from exceptions.exception_handler import InvalidRequest

class RestaurantServices:
    def __init__(self, db: Session):
        self.db = db
        self.restaurant_repository = RestaurantRepository(db)


    async def create_restaurant(
            self,
            current_user,
            restaurant_info
    ):
        if current_user.rol != "admin":
            raise InvalidRequest(status_code=401, detail="No tiene permisos para crear un restaurante")

        propietario_restaurante = await self.restaurant_repository.get_restaurant_owner(restaurant_info.DocumentoDeIdentidadPropietario)
        if not propietario_restaurante:
            raise InvalidRequest(status_code=401, detail="El propietario no existe")
        if propietario_restaurante.rol != "propietario":
            raise InvalidRequest(status_code=401, detail="El rol no es de propietario")

        new_restaurant = FullRestaurant(**restaurant_info.dict(), idRestaurante=propietario_restaurante.idUsuario)
        await self.restaurant_repository.create_new_restaurant(new_restaurant)

        return RestaurantBase(**new_restaurant.__dict__)

    async def get_all_restaurants(self, page: int = 1, page_size: int = 10):
        paginated_data = await self.restaurant_repository.get_all_restaurants(page, page_size)

        return {
            "total": paginated_data["total"],
            "page": paginated_data["page"],
            "page_size": paginated_data["page_size"],
            "restaurants": [
                PublicRestaurant(**restaurant.__dict__) for restaurant in paginated_data["items"]
            ]
        }