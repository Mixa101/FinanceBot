from aiogram import Router, F
from settings import consumption_state, TypeFilter
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext
from data_base import Session
from models import Consumptions, Finances
import keyboards as kb

# используем списки для создания динамической клавиатуры
consumption_reasons = ['regular cons', 'ethernet', 'credit', 'food']

# роутер
cons_router = Router()

# хендлер для ввода расхода
@cons_router.message(F.text.lower() == 'consumption')
async def consumption_cmd(message: Message, state: FSMContext):
    await state.set_state(consumption_state.choosing_amount)
    await message.answer('enter consumption:', reply_markup=ReplyKeyboardRemove())

#в случае правильного ввода 
@cons_router.message(consumption_state.choosing_amount, TypeFilter())
async def choosing_amount(message: Message, state: FSMContext):
    await state.set_state(consumption_state.choosing_reason)
    await state.update_data(cons_amount=int(message.text)) # загружаем в оперативку расход
    # создаем динамическую клавиатуру на основе consumotion_reasons для того чтоб было удобно считать расходы
    await message.answer('now enter reason of consumption:', reply_markup=kb.make_row_keyboard(consumption_reasons)) 

# в случае правильного ввода
@cons_router.message(consumption_state.choosing_reason, F.text.in_(consumption_reasons))
async def choosing_reason(message: Message, state: FSMContext):
    await state.update_data(cons_reason = message.text) # загружаем в оперативку
    with Session() as session:
        cons = await state.get_data() # получаем данные из оперативки
        # создаем на основе этих данных новый обьект расхода
        new_cons = Consumptions(id = message.from_user.id, consumptions=cons['cons_amount'], reason=cons['cons_reason']) 
        user = session.query(Finances).filter(Finances.id == message.from_user.id).first()
        user.moneys -= cons['cons_amount'] # обновляем наш бюджет
        session.add(new_cons)
        session.commit()
        await message.answer(f'your new budget is: {user.moneys}', reply_markup=kb.main_keyboard)
    
    await state.clear()