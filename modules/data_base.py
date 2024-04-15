from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker

# иногда для создания БД приходилось пользоваться этим файлом хотя может еслиб я просто запускал main может и получалось бы но на всяк 

from modules.models import Base

# создаем связь с БД
engine = create_engine("sqlite:///test.db")
Session = sessionmaker(bind=engine)

Base.metadata.create_all(engine)