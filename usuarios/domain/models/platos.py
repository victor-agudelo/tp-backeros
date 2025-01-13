from sqlalchemy import Column, Integer, String, Boolean, ForeignKey

from sqlalchemy.orm import relationship

from database.database import database_conn


class Platos(database_conn.base):
    __tablename__ = "dishes"

    idPlato = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    Nombre = Column(String(100), nullable=False)
    Precio = Column(Integer, nullable=False)
    Descripcion = Column(String(500), nullable=False)
    UrlImagen = Column(String(150), nullable=False)
    categoria = Column(String(50), nullable=False)
    estado = Column(Boolean, nullable=False, default=True)
    idRestaurante = Column(Integer, ForeignKey("restaurants.idRestaurante"), nullable=False)

    restaurante = relationship("Restaurantes", back_populates="platos")