import os
import json

from dotenv import load_dotenv, find_dotenv
from fastapi.security import OAuth2PasswordBearer

load_dotenv(find_dotenv())


class Settings:
    JWT_SECRET = os.getenv('JWT_SECRET')
    ALGORITHMS = os.getenv('ALGORITHMS')


app_settings = Settings()