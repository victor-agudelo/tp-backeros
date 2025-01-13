from pydantic import BaseModel, model_validator


class ClientRestaurant(BaseModel):
    Nombre: str
    UrlLogo: str
