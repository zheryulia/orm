"""Создание БД для приложения такси."""
from enum import Enum
from sqlalchemy import (
     Column,
     create_engine,
     INT,
     Boolean,
     TIMESTAMP,
     ForeignKey,
     VARCHAR
     )
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy_utils import ChoiceType

engine = create_engine('postgresql://postgres:12345@127.0.0.1:5432/taxi')

Base = declarative_base()


class Driver(Base):
    """Таблица Водители."""

    __tablename__ = 'drivers'

    id = Column(INT, primary_key=True, autoincrement=True, comment="ID водителя")
    name = Column(VARCHAR(30), nullable=False, comment="Имя водителя")
    car = Column(VARCHAR(30), nullable=False, comment="Авто водителя")

    @property
    def serialize(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "car": self.car
        }


class Client(Base):
    """Таблицы Клиенты."""

    __tablename__ = 'clients'

    id = Column(INT, primary_key=True, autoincrement=True, comment="ID клиента")
    name = Column(VARCHAR(30), nullable=False, comment="Имя клиента")
    is_vip = Column(Boolean, nullable=False, comment="VIP клиент?")

    @property
    def serialize(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "is_vip": self.is_vip
        }


class StatusType(Enum):
    """Состояния заявки."""

    not_accepted = "not_accepted"
    in_progress = "in_progress"
    cancelled = "cancelled"
    done = "done"


class Order(Base):
    """Таблица Заказы."""

    __tablename__ = 'orders'

    id = Column(INT, primary_key=True, autoincrement=True, comment="ID заказа")
    address_from = Column(VARCHAR(30), nullable=False, comment="Адрес отправки")
    address_to = Column(VARCHAR(30), nullable=False, comment="Адрес прибытия")
    client_id = Column(INT, ForeignKey('clients.id', ondelete='CASCADE'), nullable=False,
                       comment="ID клиента")
    driver_id = Column(INT, ForeignKey('drivers.id', ondelete='CASCADE'), nullable=False,
                       comment="ID водителя")
    date_created = Column(TIMESTAMP, nullable=False, comment="Дата создания заказа")
    status = Column(ChoiceType(StatusType, impl=VARCHAR(20)),
                    nullable=False, default=StatusType.not_accepted)
    clients = relationship("Client")
    drivers = relationship("Driver")

    @property
    def serialize(self) -> dict:
        return {
            "id": self.id,
            "address_from": self.address_from,
            "address_to": self.address_to,
            "client_id": self.client_id,
            "driver_id": self.driver_id,
            "date_created": self.date_created,
            "status": self.status
        }


if __name__ == "__main__":
    Base.metadata.create_all(engine)