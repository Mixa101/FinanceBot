from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker
from data.models import Base

engine = create_engine('sqlite:///test.db')
Base.metadata.create_all(engine)
Session =  sessionmaker(bind=engine)

