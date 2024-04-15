from aiogram import Router, F
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext
from settings import income_state, TypeFilter
from modules.models import Incomes, Finances
from modules.data_base import Session
import modules.keyboards as kb
from modules.functions import add_incomes

"""
    ЗДЕСЬ НАХОДИТСЯ ОБРАБОТЧИК ДОХОДОВ
"""

income_router = Router()
# Хендлер для ввода нового дохода
@income_router.message(F.text.lower() == 'income')
async def income_cmd(message:Message, state: FSMContext):
    await message.answer(f'введите новый доход:', reply_markup=ReplyKeyboardRemove())
    await state.set_state(income_state.choosing_amount)# переводим машину состояний для ввода дохода

# в случае правильного ввода 
@income_router.message(
    income_state.choosing_amount, # так мы фильтруем по состояниям
    TypeFilter() # использовал для фильтра по типу данных int
)
async def income_amount(message: Message, state: FSMContext):
    with Session() as session:
        balance = add_incomes(int(message.text), message.from_user.id)
        await message.answer('успешно добавлен новый доход')
        await message.answer(f'ваш новый бюджет: {balance}', reply_markup=kb.main_keyboard)
    await state.clear() # и под конец очищаем машину состояний