from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.dialects.mysql import INTEGER
from sqlalchemy.orm import mapped_column


Base = declarative_base()
metadata = Base.metadata


class EquipmentType(Base):
    """Описание базы данный Тип оборудования"""
    __tablename__ = 'equipment_type'

    id = Column(INTEGER(11), primary_key=True)
    type_name = Column(String(255))
    mask = Column(String(255))


class Equipment(Base):
    """Описание базы данный Оборудования"""
    __tablename__ = 'equipment'

    id = Column(INTEGER(11), primary_key=True)
    code_equipment_type = mapped_column(ForeignKey("equipment_type.id"))
    serial_number = Column(String(255), unique=True)
