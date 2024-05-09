from time import time
from sqlalchemy import Column, Integer, String, Sequence, Identity
from sqlalchemy.orm import declarative_base
from flask_login import UserMixin
from config import config as p
from jwt import encode, decode

### En este fichero se almacenan los modelos de las tablas en la base de datos

Base = declarative_base()
# table_sequence = Sequence('table_id_seq', start=1)


# Tabla users
class User(Base, UserMixin):
    __tablename__ = "users"
    id = Column(Integer(), Identity(always=True, start=1, increment=1))
    username = Column(String(20), primary_key=True)
    password = Column(String(164), nullable=False)
    email = Column(String(50), nullable=False)
    name = Column(String(20), nullable=False)
    correctPassword = False

    def get_reset_token(self, expires=500):
        return encode(
            {"reset_password": self.username, "exp": time() + expires}, key=p.SECRET_KEY, algorithm="HS256"
        )

    @staticmethod
    def verify_reset_token(token):
        try:
            username = decode(token, key=p.SECRET_KEY, algorithms=['HS256'])["reset_password"]
            return username
        except Exception as ex:
            raise Exception(ex)

