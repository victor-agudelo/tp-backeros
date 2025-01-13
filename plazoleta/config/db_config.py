import os
from dotenv import load_dotenv, find_dotenv
from sqlalchemy.engine import URL

load_dotenv(find_dotenv())


class BasicConfig:
    def __init__(self):
        self.drivername = "mysql+aiomysql"
        self.username = os.getenv("DB_USER")
        self.password = os.getenv("DB_PASSWORD")
        self.host = os.getenv("DB_HOST")
        self.port = os.getenv("DB_PORT")
        self.database = os.getenv("DB_NAME")
        self.database_url = URL.create(
            drivername=self.drivername,
            username=self.username,
            password=self.password,
            host=self.host,
            port=self.port,
            database=self.database
        )


database_config = BasicConfig()
