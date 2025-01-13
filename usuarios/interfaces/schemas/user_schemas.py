import passlib.hash

from pydantic import BaseModel, model_validator
from datetime import date

from utils.email_validator import check_email
from utils.age_calculator import validate_age


class UserBase(BaseModel):
    correo: str
    rol: str
    idRestaurante: int | None = None


class UserId(UserBase):
    idUsuario: int


class FullUser(UserBase):
    DocumentoDeIdentidad: int
    Nombre: str
    Apellido: str
    Celular: str
    fechaNacimiento: date

    @model_validator(mode="after")
    def age_validations(self):
        if validate_age(self.fechaNacimiento) < 18:
            raise ValueError("El usuario debe ser mayor de edad")
        self.fechaNacimiento = self.fechaNacimiento.strftime("%Y-%m-%d")
        return self

    @model_validator(mode="after")
    def email_validations(self):
        if not check_email(self.correo):
            raise ValueError("Correo invalido")
        return self

    @model_validator(mode="after")
    def phone_validations(self):
        if len(self.Celular) == 10:
            if not self.Celular.isdigit():
                raise ValueError("Celular invalido")
            self.Celular = f"+57{self.Celular}"
            return self
        elif len(self.Celular) == 13:
            if not self.Celular.startswith("+57"):
                raise ValueError("Celular invalido")
            if not self.Celular[1:].isdigit():
                raise ValueError("Celular invalido")
            return self
        raise ValueError("Celular invalido")

    @model_validator(mode="after")
    def id_validations(self):
        if not isinstance(self.DocumentoDeIdentidad, int):
            raise ValueError("Documento de identidad invalido")
        if self.DocumentoDeIdentidad <= 0:
            raise ValueError("Documento de identidad invalido")
        return self

    @model_validator(mode="after")
    def rol_validations(self):
        if self.rol not in ["admin", "propietario", "empleado"]:
            raise ValueError("Rol invalido")
        if self.idRestaurante and self.rol == "admin" and self.idRestaurante != 1:
            raise ValueError("Rol invalido")
        if self.idRestaurante and self.rol != "admin" and self.idRestaurante == 1:
            raise ValueError("Rol invalido")
        return self

    @model_validator(mode="after")
    def id_restaurante_validations(self):
        if self.idRestaurante is not None:
            if self.rol != "admin" and self.idRestaurante < 1:
                raise ValueError("Id de restaurante invalido")
        return self


class UserCreation(FullUser):
    claveEncriptada: str

    @model_validator(mode="after")
    def password_encrypted(self):
        self.claveEncriptada = passlib.hash.bcrypt.hash(self.claveEncriptada)
        return self




