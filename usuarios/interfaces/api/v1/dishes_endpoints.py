from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from database.database import database_conn
from interfaces.schemas.user_schemas import UserBase
from interfaces.schemas.dish_schemas import DishBase, DishPatch
from aplication.services.dish_services import DishServices

from adapters.auth import Auth

dishes_router = APIRouter(
    prefix="/api/v1/dishes",
    tags=["dishes"],
    responses={404: {"description": "Not found"}}
)


async def get_db_session() -> AsyncSession:
    async for session in database_conn.get_db():
        yield session


@dishes_router.post('/plato')
async def create_dish(
        new_dish: DishBase,
        user: UserBase = Depends(Auth.get_current_user),
        db: AsyncSession = Depends(get_db_session)
):
    dish_services = DishServices(db)
    return await dish_services.create_dish(user, new_dish)


@dishes_router.get('/platos')
async def get_all_dishes(
        user: UserBase = Depends(Auth.get_current_user),
        db: AsyncSession = Depends(get_db_session)
):
    dish_services = DishServices(db)
    return await dish_services.get_all_dishes(user)


@dishes_router.patch('/modificar-plato/{idPlato}')
async def update_dish(
        idPlato: int,
        dish_info: DishPatch,
        user: UserBase = Depends(Auth.get_current_user),
        db: AsyncSession = Depends(get_db_session)
):
    dish_services = DishServices(db)
    return await dish_services.update_dish(user, idPlato, dish_info)


@dishes_router.patch('/estado-plato/{idPlato}')
async def enable_dish(
        idPlato: int,
        user: UserBase = Depends(Auth.get_current_user),
        db: AsyncSession = Depends(get_db_session)
):
    dish_services = DishServices(db)
    return await dish_services.enable_dish(user, idPlato)

@dishes_router.get('/platos-activos/{idRestaurante}')
async def get_active_dishes(
        idRestaurante: int,
        page: int = Query(1, ge=1),
        page_size: int = Query(10, ge=1, le=50),
        category: str = Query(None),
        db: AsyncSession = Depends(get_db_session)
):
    dish_services = DishServices(db)
    return await dish_services.get_active_dishes(idRestaurante, page, page_size, category)

