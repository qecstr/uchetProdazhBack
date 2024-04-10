from app.database import Base
from sqlalchemy import types, Table
from sqlalchemy import Column,Integer


class Finances(Base):
    __tablename__ = 'Finances'

    id = Column(Integer, primary_key=True,index=True)
    date = Column(types.DATE,index=True)
    operation_type = Column(types.TEXT,index=True)
    sum = Column(types.DOUBLE_PRECISION, index=True)
    sender = Column(types.TEXT, index=True)
    comment = Column(types.TEXT, index=True)
    time = Column(types.TIME,index = True)
class Employees(Base):
    __tablename__ = 'Employees'
    id = Column(Integer,primary_key=True,index=True)
    name = Column(types.TEXT,index = True)
    surname = Column(types.TEXT,index = True)
    speciality = Column(types.TEXT,index=True)
    time = Column(types.TIME, index=True)
class Services(Base):
    __tablename__ = 'Services'
    id = Column(Integer,primary_key=True,index=True)
    operation_type = Column(types.TEXT,index=True)
    name = Column(types.TEXT,index=True)
    sum = Column(types.DOUBLE_PRECISION,index=True)
    time = Column(Integer,index=True)


class Calendar(Base):
    __tablename__ = 'Calendar'
    id = Column(Integer,primary_key=True,index=True)
    operation_type = Column(types.TEXT,index=True)
    name = Column(types.TEXT,index=True)
    sum = Column(types.DOUBLE_PRECISION,index=True)
    date = Column(types.DATE,index=True)
    comments = Column(types.TEXT,index=True)
    time = Column(types.TIME,index=True)



