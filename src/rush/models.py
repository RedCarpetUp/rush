from dataclasses import dataclass
from typing import Optional

from pydantic import EmailStr
from pydantic.dataclasses import dataclass as py_dataclass
from sqlalchemy import Column, ForeignKey, Integer, MetaData, String, Table, Text, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import mapper, relationship, sessionmaker

Base = declarative_base()


class AuditMixin(Base):
    __abstract__ = True
    id = Column(Integer, primary_key=True)
    performed_by = Column(Integer, nullable=True)


class User(AuditMixin):
    __tablename__ = "users"
    user_id = Column(Integer, primary_key=True)
    name = Column(String(50))
    email = Column(String(100))
    fullname = Column(String(50))
    nickname = Column(String(12))


@py_dataclass
class AuditMixinPy:
    id: int
    performed_by: int


@py_dataclass
class UserPy(AuditMixinPy):
    user_id: str
    name: str
    email: str
    fullname: str
    nickname: str
