import passlib.hash

from pydantic import BaseModel, model_validator

from utils.email_validator import check_email



class ClientBase(BaseModel):
    Nombre: str
    Apellido: str
    DocumentoDeIdentidad: int
    Celular: str
    correo: str

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


class FullClient(ClientBase):
    idCliente: int


class ClientCreation(ClientBase):
    claveEncriptada: str

    @model_validator(mode="after")
    def password_encrypted(self):
        self.claveEncriptada = passlib.hash.bcrypt.hash(self.claveEncriptada)
        return self


class FullClientCreation(ClientCreation):
    idRol: int | None = 1
