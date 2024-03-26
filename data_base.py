from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker

from app.models import Base

# создаем связь с БД
engine = create_engine("###")
Session = sessionmaker(bind=engine)

Base.metadata.create_all(engine)