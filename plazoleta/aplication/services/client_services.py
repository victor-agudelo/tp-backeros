from sqlalchemy.orm import Session

from exceptions.exception_handler import InvalidRequest
from adapters.client_repository import ClientRepository

from interfaces.schemas.client_schemas import FullClientCreation
from utils.random_password import password_generator


class ClientServices:
    def __init__(self, db: Session = None):
        self.db = db
        self.client_repository = ClientRepository(db)

    async def create_client(self, client):
        old_client = await self.client_repository.client_by_email(client.correo)

        if old_client:
            raise InvalidRequest(
                status_code=400, detail="El cliente ya existe")

        client_password = "1"  # password_generator.create_new_password()

        new_client = FullClientCreation(
            **client.__dict__,
            claveEncriptada=client_password,
            idRol=1
        )

        await self.client_repository.create_client(new_client)

        return client
