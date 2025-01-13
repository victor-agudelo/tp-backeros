from sqlalchemy.orm import Session

from interfaces.schemas.user_schemas import UserBase, UserCreation
from exceptions.exception_handler import InvalidRequest
from adapters.user_repository import UserRepository


class UserServices:
    def __init__(self, db: Session):
        self.db = db
        self.user_repository = UserRepository(db)


    async def create_user(self, user, current_user):
        old_user = await self.user_repository.user_by_email(user.correo)

        if old_user:
            raise InvalidRequest(status_code=400, detail="El usuario ya existe")

        roles_available = self.get_add_roles(current_user.rol)
        if user.rol not in roles_available:
            raise InvalidRequest(status_code=400, detail="No tiene permisos para agregar este rol")

        if current_user.rol == "propietario":
            user.idRestaurante = current_user.idUsuario

        await self.user_repository.create_user(user)

        return UserBase(**user.__dict__)

    @staticmethod
    def get_add_roles(rol):
        roles_available = {
            "admin": ["propietario"],
            "propietario": ["empleado"],
        }

        return roles_available.get(rol, [])
