import passlib.hash

from sqlalchemy import Column, Integer, String, ForeignKey

from sqlalchemy.orm import relationship

from database.database import database_conn


class Clientes(database_conn.base):
    __tablename__ = "clients"

    idCliente = Column(Integer, primary_key=True,
                       autoincrement=True, nullable=False)
    Nombre = Column(String(100), nullable=False)
    Apellido = Column(String(100), nullable=False)
    DocumentoDeIdentidad = Column(Integer, unique=True, index=True)
    Celular = Column(String(13), nullable=False)
    correo = Column(String(100), nullable=False)
    idRol = Column(Integer, nullable=False)
    claveEncriptada = Column(String(100), nullable=False)

    def verify_password(self, clave: str):
        return passlib.hash.bcrypt.verify(clave, self.claveEncriptada)
