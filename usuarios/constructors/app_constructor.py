import os
import json

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv, find_dotenv

from interfaces.api.v1.users_endpoints import users_router
from interfaces.api.v1.restaurants_endpoints import restaurants_router
from interfaces.api.v1.auth_endpoints import auth_router
from interfaces.api.v1.dishes_endpoints import dishes_router
from interfaces.api.v1.orders_endpoints import orders_router
from interfaces.api.v1.dashboard_endpoints import dashboard_router


load_dotenv(find_dotenv())


def app_constructor():
    app = FastAPI(
        title="Usuarios API",
        version="1.0.0"
    )

    origins = json.loads(os.getenv('CORS_ORIGINS'))

    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    routers = (
        auth_router,
        users_router,
        restaurants_router,
        dishes_router,
        orders_router,
        dashboard_router
    )

    for router in routers:
        app.include_router(router)

    return app
