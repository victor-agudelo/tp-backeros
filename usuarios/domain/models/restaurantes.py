from sqlalchemy import Column, Integer, String, Boolean, ForeignKey

from sqlalchemy.orm import relationship

from database.database import database_conn
from domain.models.platos import Platos


class Restaurantes(database_conn.base):
    __tablename__ = "restaurants"

    idRestaurante = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    Nombre = Column(String(50), nullable=False)
    NIT = Column(Integer, nullable=False)
    Direccion = Column(String(100), nullable=False)
    TelefonoRestaurante = Column(String(13), nullable=False)
    UrlLogo = Column(String(150), nullable=False)
    DocumentoDeIdentidadPropietario = Column(Integer, nullable=False)
    estado = Column(Boolean, nullable=False, default=True)

    usuarios = relationship("Usuario", back_populates="restaurante")
    platos = relationship("Platos", back_populates="restaurante")