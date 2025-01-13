import passlib.hash

from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship

from database.database import database_conn
from domain.models.restaurantes import Restaurantes


class Usuario(database_conn.base):
    __tablename__ = "users"
    idUsuario = Column(Integer, primary_key=True, index=True, autoincrement=True)
    correo = Column(String(100), nullable=False)
    DocumentoDeIdentidad = Column(Integer, unique=True, index=True)
    Nombre = Column(String(50), nullable=False)
    Apellido = Column(String(50), nullable=False)
    Celular = Column(String(13), nullable=False)
    fechaNacimiento = Column(Date)
    claveEncriptada = Column(String(100), nullable=False)
    rol = Column(String(50), nullable=False)
    idRestaurante = Column(Integer, ForeignKey("restaurants.idRestaurante"), nullable=False)

    restaurante = relationship("Restaurantes", back_populates="usuarios")

    def verify_password(self, clave: str):
        return passlib.hash.bcrypt.verify(clave, self.claveEncriptada)
