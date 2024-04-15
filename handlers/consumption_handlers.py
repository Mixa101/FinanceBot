from aiogram import Router, F
from settings import consumption_state, TypeFilter
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext
from modules.data_base import Session
import modules.keyboards as kb
from modules.functions import add_consumption

"""
        ЗДЕСЬ НАХОДИТСЯ ОБРАБОТЧИК РАСХОДА
"""
# используем списки для создания динамической клавиатуры
consumption_reasons = ['regular cons', 'ethernet', 'credit', 'food']

# роутер
cons_router = Router()

# хендлер для ввода расхода
@cons_router.message(F.text.lower() == 'consumption')
async def consumption_cmd(message: Message, state: FSMContext):
    await state.set_state(consumption_state.choosing_amount)
    await message.answer('введите новый расход:', reply_markup=ReplyKeyboardRemove())

#в случае правильного ввода 
@cons_router.message(consumption_state.choosing_amount, TypeFilter())
async def choosing_amount(message: Message, state: FSMContext):
    await state.set_state(consumption_state.choosing_reason)
    await state.update_data(cons_amount=int(message.text)) # загружаем в оперативку расход
    # создаем динамическую клавиатуру на основе consumotion_reasons для того чтоб было удобно считать расходы
    await message.answer('отлично теперь укажите причину расхода:',
                         reply_markup=kb.make_row_keyboard(consumption_reasons)) 

# в случае правильного ввода
@cons_router.message(consumption_state.choosing_reason, F.text.in_(consumption_reasons))
async def choosing_reason(message: Message, state: FSMContext):
    await state.update_data(cons_reason = message.text) # загружаем в оперативку
    cons = await state.get_data() # получаем данные из оперативки
    balance = add_consumption(cons, message.from_user.id)
    await message.answer(f'ваш бюджет: {balance}', reply_markup=kb.main_keyboard)
    
    await state.clear()