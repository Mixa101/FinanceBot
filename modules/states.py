from aiogram.fsm.state import StatesGroup, State

class Register(StatesGroup):
    enter_budget = State()

class Income(StatesGroup):
    enter_sum_of_income = State()

class Consumption(StatesGroup):
    enter_sum_of_cons = State()
    enter_reason_of_cons = State()