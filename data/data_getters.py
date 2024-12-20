from data.config_data import engine, Session
from data.models import Users, Incomes, Consumptions
from aiogram.filters import BaseFilter
from aiogram.types import Message
from sqlalchemy import func

def user_exists(message : Message) -> bool:
    with Session() as session:
        user = session.query(Users).filter(Users.user_id == message.from_user.id).first()
        if user:
            return True
        else:
            return False

class UserExists(BaseFilter):
    def __init__(self, filter_type):
        self.filter_type = filter_type
    
    async def __call__(self, message : Message):
        with Session() as session:
            user = session.query(Users).filter(Users.user_id == message.from_user.id).first()
        if self.filter_type == 'for_exist':
            return user is not None
        
        elif self.filter_type == 'for_not_exist':
            return user is None
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

def get_cons_sum_fitlered_by_reasons(id):
    with Session() as session:
        cons_sum = session.query(Consumptions.reason, func.sum(Consumptions.sum)).filter(Consumptions.user_id == id).group_by(Consumptions.reason).all()
    
    cons_dict = {reason : amount for reason, amount in cons_sum}
    return cons_dict