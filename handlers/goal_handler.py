from aiogram import Router, F, types
from aiogram.types import ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext
from settings import set_goal_state, TypeFilter
from modules.data_base import Session
from modules.models import Finances
import modules.keyboards as kb
"""
    ЗДЕСЬ НАХОДИТСЯ ОБРАБОТЧИК ДЛЯ ДОБАВЛЕНИЯ НОВОЙ ЦЕЛИ
"""

# Роутер
goal_router = Router()

# начало установки цели
@goal_router.message(F.text.lower() == 'set a goal')
async def goal_handler(message: types.Message, state: FSMContext):
    await state.set_state(set_goal_state.choosing_goal)
    await message.answer('введите цель:', reply_markup=ReplyKeyboardRemove())

# второй шаг
@goal_router.message(set_goal_state.choosing_goal, F.text)
async def set_goal(message: types.Message, state: FSMContext):
    await state.update_data(goal = message.text)
    await state.set_state(set_goal_state.sum_goal)
    await message.answer(f'отлично, сумма для достижения цели: ')

# третий финальный шаг
@goal_router.message(set_goal_state.sum_goal, TypeFilter())
async def set_sum_goal(message: types.Message, state:FSMContext):
    await state.update_data(sum_goal = int(message.text))
    with Session() as session:
        goals = await state.get_data()
        user = session.query(Finances).filter(Finances.id == message.from_user.id).first()
        user.goal = goals['goal']
        user.goal_sum = goals['sum_goal']
        session.commit()
        await message.answer(f'отлично новая цель поставлена!', reply_markup=kb.main_keyboard)