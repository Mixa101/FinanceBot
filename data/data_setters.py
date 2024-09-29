from data.models import Users, Incomes, Consumptions
from data.config_data import engine, Session

def set_user(id, budget):
    with Session() as session:
        user = Users(user_id=id, budget=budget)
        session.add(user)
        session.commit()
    return 0

def set_income(id, sum_of_inc : int):
    with Session() as session:
        income = Incomes(user_id = id, sum = sum_of_inc)
        user = session.query(Users).filter_by(user_id = id).first()
        user.budget += sum_of_inc
        session.add(income)
        session.commit()

def set_consumption(id, sum_of_cons : int, reason):
    with Session() as session:
        consumption = Consumptions(user_id = id, sum = sum_of_cons, reason = reason)
        user = session.query(Users).filter_by(user_id = id).first()
        user.budget -= sum_of_cons
        session.add(consumption)
        session.commit()