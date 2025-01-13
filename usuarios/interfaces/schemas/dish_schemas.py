from pydantic import BaseModel, model_validator


class DishBase(BaseModel):
    Nombre: str
    Precio: int
    Descripcion: str
    UrlImagen: str | None = None
    categoria: str

    @model_validator(mode="after")
    def validate_price(self):
        if self.Precio <= 0:
            raise ValueError("El precio no puede ser inferior a 0")
        return self


class FullDish(DishBase):
    idRestaurante: int
    estado: bool = True


class DishResponse(FullDish):
    idPlato: int


class DishPatch(BaseModel):
    Precio: int | None
    Descripcion: str | None


