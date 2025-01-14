import pytest
from sqlalchemy import Column, Integer, String, select
from sqlalchemy.ext.asyncio import AsyncSession
from utils.paginator import PaginatorRepository
from database.database import database_conn


# Modelo de prueba
class TestModel(database_conn.base):
    __tablename__ = "test_model"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)

@pytest.fixture(scope="module", autouse=True)
async def populate_test_data(async_session: AsyncSession):
    async with async_session.begin():
        async_session.add_all([TestModel(name=f"Item {i}") for i in range(1, 51)])


@pytest.mark.asyncio
async def test_paginate_query(async_session: AsyncSession):
    repository = PaginatorRepository(async_session)

    # Configura la consulta base
    query = select(TestModel)
    page = 2
    page_size = 10

    # Ejecuta la consulta paginada
    result = await repository.paginate_query(query, page=page, page_size=page_size)

    # Validaciones
    assert result["total"] == 50  # Total de elementos
    assert result["page"] == page  # Página actual
    assert result["page_size"] == page_size  # Tamaño de página
    assert len(result["items"]) == page_size  # Cantidad de elementos en la página
    assert result["items"][0].name == "Item 11"  # Primer elemento de la página 2

@pytest.mark.asyncio
async def test_paginate_query_empty(async_session: AsyncSession):
    repository = PaginatorRepository(async_session)

    # Configura una consulta que no devuelva resultados
    query = select(TestModel).where(TestModel.name == "Nonexistent")
    page = 1
    page_size = 10

    # Ejecuta la consulta
    result = await repository.paginate_query(query, page=page, page_size=page_size)

    # Validaciones
    assert result["total"] == 0  # Total de elementos debe ser 0
    assert result["page"] == page
    assert result["page_size"] == page_size
    assert len(result["items"]) == 0  # Sin elementos en la consulta
