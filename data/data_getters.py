from data.config_data import engine, Session
from data.models import Users, Incomes, Consumptions
from aiogram.types import Message

def user_exists(message : Message) -> bool:
    with Session() as session:
        user = session.query(Users).filter(Users.user_id == message.from_user.id).first()
        if user:
            return True
        else:
            return False

def get_budget(id):
    with Session() as session:
        user = session.query(Users).filter(Users.user_id == id).first()
        return user.budget

def get_incomes(id):
    with Session() as session:
        incomes = session.query(Incomes).filter(Incomes.user_id == id).all()
        return incomes

def get_cons(id):
    with Session() as session:
        cons = session.query(Consumptions).filter(Consumptions.user_id == id).all()
        return cons