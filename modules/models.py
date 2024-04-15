from sqlalchemy import (Integer, String, MetaData, \
                        Column, Date)

from sqlalchemy.ext.declarative import declarative_base
from datetime import date
""" ЗДЕСЬ НАХОДЯТСЯ ВСЕ МОДЕЛИ БАЗЫ ДАННЫХ """


# используется для ORM как базовый класс таблиц
Base = declarative_base()

#Таблица для доходов
class Incomes(Base):
    __tablename__ = 'incomes'
    sid = Column(Integer, primary_key=True)
    id = Column(Integer, nullable=False)
    incomes = Column(Integer, nullable=False)
    data = Column(Date,default = date.today())

#Таблица для расходов
class Consumptions(Base):
    sid = Column(Integer, primary_key=True)
    __tablename__ = 'consumptions'
    id = Column(Integer, nullable=False)
    consumptions = Column(Integer, nullable=False)
    reason = Column(String(255), nullable=False)
    data = Column(Date,default= date.today())
    
# Таблица для пользователя 
class Finances(Base):
    sid = Column(Integer, primary_key=True)
    __tablename__ = 'finances'
    id = Column(Integer, nullable=False)
    moneys = Column(Integer)
    goal = Column(String, nullable=True)
    goal_sum = Column(Integer, nullable=True)