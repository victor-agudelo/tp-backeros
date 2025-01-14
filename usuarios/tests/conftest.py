import pytest
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from starlette.testclient import TestClient
from typing import Generator, AsyncGenerator
from fastapi import FastAPI
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

from constructors.app_constructor import app_constructor
from database.database import database_conn


def create_test_database():
    admin_user = "postgres"
    admin_password = "admin_password"
    admin_host = "localhost"
    admin_port = "5432"

    db_name = "test_db"

    try:
        conn = psycopg2.connect(
            dbname="postgres",
            user=admin_user,
            password=admin_password,
            host=admin_host,
            port=admin_port
        )
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)

        cursor = conn.cursor()
        cursor.execute(f"DROP DATABASE IF EXISTS {db_name}")
        cursor.execute(f"CREATE DATABASE {db_name} OWNER {admin_user}")
        cursor.close()
        conn.close()

        print(f"Database '{db_name}' created successfully.")

    except Exception as e:
        print(f"An error occurred while creating the test database: {e}")

    return db_name, admin_user, admin_password, admin_host, admin_port


# Configuración de la base de datos
db_name, admin_user, admin_password, db_host, db_port = create_test_database()

SQLALCHEMY_DATABASE_URL = f"postgresql+asyncpg://{admin_user}:{admin_password}@{db_host}:{db_port}/{db_name}"
engine = create_async_engine(SQLALCHEMY_DATABASE_URL, future=True, echo=False)
SessionTesting = sessionmaker(bind=engine, expire_on_commit=False, class_=AsyncSession)


@pytest.fixture(scope="module")
async def app() -> AsyncGenerator[FastAPI, None]:
    async with engine.begin() as conn:
        await conn.run_sync(database_conn.base.metadata.create_all)

    _app = app_constructor()
    yield _app

    async with engine.begin() as conn:
        await conn.run_sync(database_conn.base.metadata.drop_all)


@pytest.fixture(scope="module")
def async_session_factory() -> sessionmaker:
    return sessionmaker(bind=engine, expire_on_commit=False, class_=AsyncSession)


@pytest.fixture(scope="module")
async def async_session(async_session_factory: sessionmaker) -> AsyncGenerator[AsyncSession, None]:
    async with async_session_factory() as session:
        yield session


@pytest.fixture(scope="module")
def client(app: FastAPI, async_session_factory: sessionmaker) -> TestClient:
    async def _get_test_db():
        async with async_session_factory() as session:
            yield session

    app.dependency_overrides[database_conn.get_db] = _get_test_db

    with TestClient(app) as client:
        yield client
