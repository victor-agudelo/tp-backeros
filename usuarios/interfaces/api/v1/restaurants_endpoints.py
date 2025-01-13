from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from database.database import database_conn
from interfaces.schemas.user_schemas import UserBase
from interfaces.schemas.restaurant_schemas import CreateRestaurant
from aplication.services.restaurant_services import RestaurantServices

from adapters.auth import Auth


restaurants_router = APIRouter(
    prefix="/api/v1/restaurants",
    tags=["restaurants"],
    responses={404: {"description": "Not found"}}
)


async def get_db_session() -> AsyncSession:
    async for session in database_conn.get_db():
        yield session


@restaurants_router.post('/new-restaurant')
async def create_restaurant(
        new_restaurant: CreateRestaurant,
        user: UserBase = Depends(Auth.get_current_user),
        db: AsyncSession = Depends(get_db_session)
):
    restaurant_services = RestaurantServices(db)

    return await restaurant_services.create_restaurant(user, new_restaurant)


@restaurants_router.get('/all-restaurants')
async def get_all_restaurants(
        page: int = Query(1, ge=1),
        page_size: int = Query(10, ge=1, le=50),
        db: AsyncSession = Depends(get_db_session)
):
    restaurant_services = RestaurantServices(db)

    return await restaurant_services.get_all_restaurants(page, page_size)
