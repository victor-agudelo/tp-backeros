import uuid

from datetime import datetime
from pydantic import BaseModel, Field
from typing import Optional, Dict


class Pedido(BaseModel):
    pedido_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    cliente_id: int = Field(..., example=1)
    Celular: str = Field(..., example="+573333333333")
    restaurante_id: int = Field(..., example=1)
    platos: Dict[str, int] = Field(..., example={"plato": 1})
    estado: str = Field(..., example="Pendiente")
    pedidoRealizadoTimestamp: datetime = Field(
        ..., example="2025-01-09T08:23:42")
    empleadoAsignado: Optional[str] = Field(
        default=None, example="Homero Simpson")
    pedidoEnPreparacionTimestamp: Optional[datetime] = Field(
        default=None, example="2025-01-09T08:23:42")
    pedidoListoTimestamp: Optional[datetime] = Field(
        default=None, example="2025-01-09T08:23:42")
    entregado: bool = Field(default=False, examples=[True, False])
    codigoEntrega: Optional[str] = Field(default=None, example="0123")
