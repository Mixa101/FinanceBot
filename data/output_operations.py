from data.data_getters import get_incomes, get_cons, get_cons_sum_fitlered_by_reasons
from collections import defaultdict
from datetime import datetime, timedelta
from modules.functions import calculate_percent

def filter_by_days(model):
    today = datetime.now().date()
    last_week = today - timedelta(days=7)
    
    filtered_model = [i for i in model if last_week <= i.date <= today]
    return filtered_model

def group_dates(model):
    grouped = defaultdict(int)
    for i in model:
        date_str = i.date.strftime('%Y-%m-%d')
        grouped[date_str] += i.sum
    return grouped

def group_reasons(id):
    reasons = get_cons_sum_fitlered_by_reasons(id)
    cons = get_cons(id)
    cons = sum([i.sum for i in cons])
    result = calculate_percent(reasons, cons)
    return result
    
def calculate_avg_income(id):
    incomes = get_incomes(id)
    sum_of_incomes = sum([i.sum for i in incomes])
    filtered_incomes = filter_by_days(incomes)
    sum_of_dates = group_dates(filtered_incomes)
    avg_income = sum([j for i, j in sum_of_dates.items()]) // 7
    result = [avg_income, sum_of_incomes]
    return result

def calculate_avg_cons(id):
    cons = get_cons(id)
    sum_of_cons = sum([i.sum for i in cons])
    filtered_cons = filter_by_days(cons)
    sum_of_dates = group_dates(filtered_cons)
    avg_cons = sum([j for i, j in sum_of_dates.items()]) // 7
    result = [avg_cons, sum_of_cons]
    return result