from aiogram import Router, F
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext
from settings import income_state, TypeFilter
from models import Incomes, Finances
from data_base import Session
import keyboards as kb

income_router = Router()
# Хендлер для ввода нового дохода
@income_router.message(F.text.lower() == 'income')
async def income_cmd(message:Message, state: FSMContext):
    await message.answer(f'enter your income:', reply_markup=ReplyKeyboardRemove())
    await state.set_state(income_state.choosing_amount)# переводим машину состояний для ввода дохода

# в случае правильного ввода 
@income_router.message(
    income_state.choosing_amount, # так мы фильтруем по состояниям
    TypeFilter() # использовал для фильтра по типу данных int
)
async def income_amount(message: Message, state: FSMContext):
    with Session() as session:
        new_income = Incomes(id=message.from_user.id, incomes=int(message.text))# создаем новый обьект дохода
        await message.answer('Succesfuly added new income')
        session.add(new_income) # добавляем в бд
        user = session.query(Finances).filter(Finances.id == message.from_user.id).first()
        user.moneys += int(message.text) # обновляем бюджет
        session.commit()
        await message.answer(f'your new budget: {user.moneys}', reply_markup=kb.main_keyboard)
    await state.clear() # и под конец очищаем машину состояний