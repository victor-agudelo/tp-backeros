
from pydantic import BaseModel, model_validator


class OrderResponse(BaseModel):
    message: str
