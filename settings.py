from aiogram.fsm.state import StatesGroup, State
from aiogram import types
from aiogram.filters import Filter
from aiogram.utils.formatting import Text, Bold, Italic

""" создаем машины состояний """

# Состояние регистраций
class Register(StatesGroup):
    choosing_budget = State()

# Состояние ввода дохода
class income_state(StatesGroup):
    choosing_amount = State()

# Состояние ввода расхода
class consumption_state(StatesGroup):
    choosing_amount = State()
    choosing_reason = State()

# Состояние ставки цели!
class set_goal_state(StatesGroup):
    choosing_goal = State()
    sum_goal = State()

#создание кастомного фильтра для фильтраций по типу данных 
class TypeFilter(Filter):    #Filter находится в aiogram.filters
    key = 'is_integer'
    
    async def __call__(self, message: types.Message) -> bool:
        try:
            int(message.text)
            return True
        except:
            return False

def goal_counter(avg_inc, avg_cons, budget, goal_cost):
    needed_cost = goal_cost - budget
    if needed_cost > 0:
        avg_pls = avg_inc - avg_cons
        return needed_cost // avg_pls
    else:
        return 'Ты че быкуешь?'
    