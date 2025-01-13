from pydantic import BaseModel, model_validator


class RestaurantBase(BaseModel):
    Nombre: str


class CreateRestaurant(RestaurantBase):
    NIT: int
    Direccion: str
    TelefonoRestaurante: str
    UrlLogo: str | None = None
    DocumentoDeIdentidadPropietario: int
    estado: bool = True

    @model_validator(mode="after")
    def phone_validations(self):
        if len(self.TelefonoRestaurante) == 10:
            if not self.TelefonoRestaurante.isdigit():
                raise ValueError("Celular invalido")
            self.TelefonoRestaurante = f"+57{self.TelefonoRestaurante}"
            return self
        elif len(self.TelefonoRestaurante) == 13:
            if not self.TelefonoRestaurante.startswith("+57"):
                raise ValueError("Celular invalido")
            if not self.TelefonoRestaurante[1:].isdigit():
                raise ValueError("Celular invalido")
            return self
        raise ValueError("Celular invalido")

    @model_validator(mode="after")
    def nit_validations(self):
        if not isinstance(self.NIT, int):
            raise ValueError("NIT invalido")
        if self.NIT <= 0:
            raise ValueError("NIT invalido")
        return self

    @model_validator(mode="after")
    def name_validations(self):
        if self.Nombre.isdigit():
            raise ValueError("Nombre invalido")
        return self


class FullRestaurant(CreateRestaurant):
    idRestaurante: int

    @model_validator(mode="after")
    def id_restaurant_validations(self):
        if self.idRestaurante and self.idRestaurante < 1:
            raise ValueError("Id del restaurante invalido")
        return self


class PublicRestaurant(RestaurantBase):
    NIT: int
    Direccion: str
    TelefonoRestaurante: str
    idRestaurante: int
    UrlLogo: str | None = None
