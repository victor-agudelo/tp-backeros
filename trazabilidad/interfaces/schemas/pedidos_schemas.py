from datetime import datetime
from pydantic import BaseModel, model_validator
from typing import Dict, Optional


class OrderBase(BaseModel):
    restaurante_id: int
    platos: Dict[str, int]
    cliente_id: int
    Celular: str

    @model_validator(mode="after")
    def validate_client_id(self):
        if self.cliente_id < 0:
            raise ValueError("Cliente no es valido")
        return self

    @model_validator(mode="after")
    def validate_restaurant_id(self):
        if self.restaurante_id < 0:
            raise ValueError("Restaurante no es valido")
        return self

    @model_validator(mode="after")
    def validate_dishes(self):
        if not self.platos:
            raise ValueError("Platos no validos")
        return self


class FulllOrder(OrderBase):
    pedido_id: str
    estado: str
    pedidoRealizadoTimestamp: str | datetime
    empleadoAsignado: Optional[str]

    @model_validator(mode="after")
    def validate_status(self):
        if self.estado not in ("Pendiente", "En-Preparacion", "Listo", "Cancelada"):
            raise ValueError("Estado no es valido")
        return self

    @model_validator(mode="after")
    def validate_order_date(self):
        try:
            if isinstance(self.pedidoRealizadoTimestamp, datetime):
                return self
            else:
                self.pedidoRealizadoTimestamp = datetime.strptime(
                    self.pedidoRealizadoTimestamp, "%Y-%m-%d %H:%M:%S")
                return self
        except:
            raise ValueError("Fecha no valida")


class FinalOrder(FulllOrder):
    pedidoEnPreparacionTimestamp: str | datetime | None
    pedidoListoTimestamp: str | datetime | None
    entregado: bool


class OrderResponse(BaseModel):
    message: str
    order_id: str
