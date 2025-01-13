from motor.motor_asyncio import AsyncIOMotorClient

from config.app_config import database_config


class Database:
    def __init__(self):
        self.client = AsyncIOMotorClient(database_config.MONGODB_URL)
        self.database = self.client[database_config.DATABASE_NAME]

    def get_database(self):
        return self.database


database = Database()
