from sqlalchemy import (Integer, String, MetaData, Column, Date)
from sqlalchemy.ext.declarative import declarative_base
from datetime import date

Base = declarative_base()

class Incomes(Base):
    __tablename__ = 'incomes'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, nullable=False)
    sum = Column(Integer, nullable=False)
    date = Column(Date, default=date.today())

class Consumptions(Base):
    __tablename__ = 'consumptions'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, nullable=False)
    sum = Column(Integer, nullable=False)
    reason = Column(String(255), nullable=False)
    date = Column(Date, default= date.today())

class Users(Base):
    __tablename__ = 'Users'
    id = Column(Integer, primary_key = True)
    user_id = Column(Integer, nullable=False)
    budget = Column(Integer)
    