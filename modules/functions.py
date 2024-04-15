from modules.data_base import Session
from modules.models import Consumptions, Finances, Incomes
from aiogram.utils.formatting import Text, as_list, Bold
from sqlalchemy import func, desc
from datetime import datetime, timedelta


def change_balance(action, amount, session, user_id):
    if action == '+':
        balance = session.query(Finances).filter(Finances.id == user_id).first()
        balance.moneys += amount
        return balance.moneys
    elif action == '-':
        balance = session.query(Finances).filter(Finances.id == user_id).first()
        balance.moneys -= amount
        return balance.moneys

def get_average(obj : list):
    sum_of = sum(item[0] for item in obj)
    return round(sum_of / len(obj), 1)

def calculate_goal(user_id, average_cons, average_inc, goal_sum):
    average_plus = average_inc - average_cons
    if average_plus <= 0:
        return 'стоит тратить меньше, ваши расходы превышают ваши расходы!'
    else:
        return f'до цели в этом темпе ещё {goal_sum // average_plus} дней поработать'

def add_consumption(data : dict, user_id):
    with Session() as session:
        balance = change_balance('-', data['cons_amount'], session, user_id)
        new_cons = Consumptions(id=user_id,
                                consumptions=data['cons_amount'],
                                reason=data['cons_reason'])
        session.add(new_cons)
        session.commit()
        return balance

def add_incomes(amount, user_id):
    with Session() as session:
        balance = change_balance('+', amount, session, user_id)
        new_income = Incomes(id = user_id,
                             incomes=amount)
        session.add(new_income)
        session.commit()
        return balance

def test(user_id):
    with Session() as session:
        cons = session.query(Consumptions.data).filter(Consumptions.id == user_id).all()
        return '\t==\t'.join(f'{item[0]}' for item in cons)

def output_cons(user_id):
    end_date  = datetime.now()
    start_date = end_date - timedelta(days=7)
    
    with Session() as session:
        balance = session.query(Finances).filter(Finances.id == user_id).first()
        
        consumptions = session.query(func.sum(Consumptions.consumptions), Consumptions.reason).filter(
            Consumptions.id == user_id).group_by(Consumptions.reason).all()
        
        out_cons = '\t ||| \t'.join(f'{item[1]} : {item[0]}' for item in consumptions)
        out_avg_per_week = None
        try:
            avg_per_week = session.query(func.sum(Consumptions.consumptions)).filter(
                Consumptions.data >= start_date, Consumptions.data <= end_date, Consumptions.id == user_id).group_by(Consumptions.data).order_by(
                    desc(Consumptions.data)).all()
            out_avg_per_week = sum(item[0] for item in avg_per_week) // 7
        except:
            out_avg_per_week = 'нету расходов в неделю'
        
        average_cons = get_average(session.query(func.sum(
            Consumptions.consumptions)).filter(Consumptions.id == user_id).group_by(
            Consumptions.data).all())
        average_inc = get_average(session.query(func.sum(
            Incomes.incomes)).filter(Incomes.id == user_id).group_by(
            Incomes.data).all())
        
        goal_text = None
        
        if balance.goal:
            goal_text = Text(calculate_goal(user_id, average_cons, average_inc, balance.goal_sum))
        else:
            goal_text = Text('Цели нет!')
        
        return as_list(Text('причины расходов:\n', Bold(out_cons)),
                       Text('средний расход: ', Bold(average_cons)),
                       Text('средний расход в неделю: ', Bold(out_avg_per_week))
                       ,goal_text ,sep='\n')

def output_income(user_id):
    end_date  = datetime.now()
    start_date = end_date - timedelta(days=7)
    with Session() as session:
        balance = session.query(Finances).filter(Finances.id == user_id).first()
        income = session.query(func.sum(Incomes.incomes)).filter(Incomes.id == user_id).group_by(Incomes.data).all()
        avg_day = get_average(income)
        average_cons = get_average(session.query(func.sum(Consumptions.consumptions)).filter(Consumptions.id == user_id).group_by(Consumptions.data).all())
        average_per_week = None
        try:
            average_per_week = session.query(func.sum(Incomes.incomes)).filter(
                Incomes.data >= start_date, Incomes.data <= end_date, Incomes.id == user_id).group_by(Incomes.data).order_by(
                    desc(Incomes.data)).all()
            average_per_week = sum(item[0] for item in average_per_week) // 7
        except:
            average_per_week = 'нету доходов в неделю'
        
        goal_text = None
        if balance.goal:
            goal_text = Text(calculate_goal(user_id, average_cons, avg_day, balance.goal_sum))
        else:
            goal_text = Text('Цели нет!')
                
        return as_list(Text('средний доход: ', Bold(avg_day)),
                       Text('средний доход в неделю: ', Bold(average_per_week)),
                       Text(goal_text),
                       sep='\n'
                       )