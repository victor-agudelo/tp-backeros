import os
import json

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv, find_dotenv

from interfaces.api.v1.pedido_endpoint import pedidos_router

load_dotenv(find_dotenv())


def app_constructor():
    app = FastAPI(
        title="Trazabilidad API",
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
        pedidos_router,
    )

    for router in routers:
        app.include_router(router)

    return app