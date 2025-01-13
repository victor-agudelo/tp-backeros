from datetime import datetime
from pydantic import BaseModel, Field, model_validator
from typing import Dict


class OrderBase(BaseModel):
    restaurante_id: int
    platos: Dict[str, int]


class FulllOrder(OrderBase):
    cliente_id: int
    Celular: str
    estado: str
    pedidoRealizadoTimestamp: str
    empleadoAsignado: str | None = None

    @model_validator(mode="after")
    def validate_restaurant_id(self):
        if self.restaurante_id < 0:
            raise ValueError("Restaurante no es valido")
        return self

    @model_validator(mode="after")
    def validate_client_id(self):
        if self.cliente_id < 0:
            raise ValueError("Cliente no es valido")
        return self

    @model_validator(mode="after")
    def validate_status(self):
        if self.estado not in ("Pendiente", "En-Preparacion", "Listo", "Cancelada"):
            raise ValueError("Estado no es valido")
        return self

    @model_validator(mode="after")
    def validate_order_date(self):
        try:
            datetime.strptime(self.pedidoRealizadoTimestamp,
                              "%Y-%m-%d %H:%M:%S")
            return self
        except:
            raise ValueError("Fecha no valida")
