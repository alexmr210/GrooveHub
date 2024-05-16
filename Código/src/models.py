from time import time
from sqlalchemy import (
    Column,
    ForeignKey,
    Integer,
    PrimaryKeyConstraint,
    String,
)
from sqlalchemy.orm import declarative_base, relationship
from flask_login import UserMixin
from config import config as p
from jwt import encode, decode

### En este fichero se almacenan los modelos de las tablas en la base de datos

Base = declarative_base()


# Tabla usuarios
class User(Base, UserMixin):
    __tablename__ = "usuarios"
    id_usuario = Column(String(255), primary_key=True, nullable=False, unique=True)
    username = Column(String(20), nullable=False)
    contrasena = Column(String(255), nullable=False)
    nombre = Column(String(255), nullable=False)
    correoElectronico = Column(String(255), nullable=False)
    ediciones = relationship("Edicion_Usuario", back_populates="usuario")
    correctPassword = False

    def get_id(self):
        return str(self.id_usuario)

    def get_reset_token(self, expires=500):
        return encode(
            {"reset_password": self.username, "exp": time() + expires},
            key=p.SECRET_KEY,
            algorithm="HS256",
        )

    @staticmethod
    def verify_reset_token(token):
        try:
            username = decode(token, key=p.SECRET_KEY, algorithms=["HS256"])[
                "reset_password"
            ]
            return username
        except Exception as ex:
            raise Exception(ex)


# Tabla artistas
class Artista(Base):
    __tablename__ = "artistas"
    id_artista = Column(String(64), primary_key=True)
    artista = Column(String(255), nullable=False)
    discos = relationship("Disco", back_populates="artista")
    canciones = relationship("Artista_Cancion", back_populates="artista")


# Tabla discos
class Disco(Base):
    __tablename__ = "discos"
    id_disco = Column(String(64), primary_key=True)
    titulo = Column(String(20), nullable=False)
    id_artista = Column(String(64), ForeignKey("artistas.id_artista"))
    artista = relationship("Artista", back_populates="discos")
    ediciones = relationship("Edicion_Disco", back_populates="disco")
    canciones = relationship("Disco_Cancion", back_populates="disco")


# Tabla ediciones_disco
class Edicion_Disco(Base):
    __tablename__ = "ediciones_disco"
    id_edicion = Column(String(64), primary_key=True)
    id_disco = Column(String(64), ForeignKey("discos.id_disco"))
    edicion = Column(String(255), nullable=False)
    agno = Column(Integer, nullable=False)
    pais = Column(String(255), nullable=False)
    disco = relationship("Disco", back_populates="ediciones")
    edicion_usuario = relationship("Edicion_Usuario", back_populates="edicion_disco")


# Tabla ediciones_usuario
class Edicion_Usuario(Base):
    __tablename__ = "ediciones_usuario"
    id_edicion = Column(String(64), ForeignKey("ediciones_disco.id_edicion"))
    id_usuario = Column(String(255), ForeignKey("usuarios.id_usuario"))
    __table_args__ = (
        PrimaryKeyConstraint(id_edicion, id_usuario),
        {},
    )
    edicion_disco = relationship("Edicion_Disco", back_populates="edicion_usuario")
    usuario = relationship("User", back_populates="ediciones")


# Tabla canciones
class Cancion(Base):
    __tablename__ = "canciones"
    id_cancion = Column(String(67), primary_key=True)
    cancion = Column(String(255), nullable=False)
    duracion = Column(String(255), nullable=False)
    artista = relationship("Artista_Cancion", back_populates="cancion")
    disco = relationship("Disco_Cancion", back_populates="cancion")


# Tabla artistas_canciones
class Artista_Cancion(Base):
    __tablename__ = "artistas_canciones"
    id_artista = Column(String(64), ForeignKey("artistas.id_artista"))
    id_cancion = Column(String(64), ForeignKey("canciones.id_cancion"))
    cancion = relationship("Cancion", back_populates="artista")
    artista = relationship("Artista", back_populates="canciones")
    __table_args__ = (
        PrimaryKeyConstraint(id_artista, id_cancion),
        {},
    )


# Tabla discos_canciones
class Disco_Cancion(Base):
    __tablename__ = "discos_canciones"
    id_disco = Column(String(64), ForeignKey("discos.id_disco"))
    id_cancion = Column(String(64), ForeignKey("canciones.id_cancion"))
    cancion = relationship("Cancion", back_populates="disco")
    disco = relationship("Disco", back_populates="canciones")
    __table_args__ = (
        PrimaryKeyConstraint(id_disco, id_cancion),
        {},
    )
