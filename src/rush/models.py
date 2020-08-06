from dataclasses import dataclass
from decimal import Decimal as DecimalType
from typing import Optional

import pendulum
from pendulum import DateTime
from pydantic import EmailStr
from pydantic.dataclasses import dataclass as py_dataclass
from sqlalchemy import (
    DECIMAL,
    JSON,
    TIMESTAMP,
    Column,
    ForeignKey,
    Integer,
    MetaData,
    String,
    Table,
    Text,
    create_engine,
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import (
    Session,
    mapper,
    relationship,
    sessionmaker,
)

Base = declarative_base()


def get_current_ist_time():
    return pendulum.now("Asia/Kolkata").replace(tzinfo=None)


class AuditMixin(Base):
    __abstract__ = True
    id = Column(Integer, primary_key=True)
    created_at = Column(TIMESTAMP, default=get_current_ist_time(), nullable=False)
    updated_at = Column(TIMESTAMP, default=get_current_ist_time(), nullable=False)
    performed_by = Column(Integer, default=1, nullable=True)

    @classmethod
    def snapshot(
        cls,
        primary_key: str,
        new_data: dict,
        session: Session,
        skip_columns: tuple = ("id", "created_at", "updated_at"),
    ):
        old_row = (
            session.query(cls)
            .filter(
                getattr(cls, primary_key) == new_data[primary_key],
                getattr(cls, "row_status") == "active",
            )
            .with_for_update(skip_locked=True)
            .one_or_none()
        )
        if old_row:
            old_row.row_status = "inactive"
            session().flush()
        cls_keys = cls.__table__.columns.keys()
        keys_to_skip = [key for key in new_data.keys() if key not in cls_keys]
        new_skip_columns = keys_to_skip + list(skip_columns)
        for column in new_skip_columns:
            new_data.pop(column, None)
        new_obj = cls.new(**new_data)
        session.flush()
        return new_obj


def get_or_create(session, model, defaults=None, **kwargs):
    instance = session.query(model).filter_by(**kwargs).first()
    if instance:
        return instance
    else:
        params = dict((k, v) for k, v in kwargs.items())
        params.update(defaults or {})
        instance = model(**params)
        session.add(instance)
        session.flush()
        return instance


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
    created_at: DateTime
    updated_at: DateTime


@py_dataclass
class UserPy(AuditMixinPy):
    user_id: str
    name: str
    email: str
    fullname: str
    nickname: str
