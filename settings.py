from aiogram.fsm.state import StatesGroup, State
from aiogram import types
from aiogram.filters import Filter

# создаем машины состояний
class Register(StatesGroup):
    choosing_budget = State()

class income_state(StatesGroup):
    choosing_amount = State()

class consumption_state(StatesGroup):
    choosing_amount = State()
    choosing_reason = State()


#создание кастомного фильтра для фильтраций по типу данных 
class TypeFilter(Filter):    #Filter находится в aiogram.filters
    key = 'is_integer'
    
    async def __call__(self, message: types.Message) -> bool:
        try:
            int(message.text)
            return True
        except:
            return False
