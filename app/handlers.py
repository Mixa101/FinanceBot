from aiogram.filters import Command
from aiogram.types import Message
import app.keyboards as kb
from aiogram import Router, F
from data_base import Session
from app.models import *
from settings import Register, TypeFilter, income_state, consumption_state
from aiogram.fsm.context import FSMContext
from aiogram.types import ReplyKeyboardRemove
from sqlalchemy import func

# Опять же роутеры классная штука
router = Router()

# используем списки для создания динамической клавиатуры
consumption_reasons = ['regular cons', 'ethernet', 'credit']

#handler на команду старт (регистрация пользователя)
@router.message(Command('start'))
async def cmd_start(message: Message, state: FSMContext):
    #открываем базу данных и проверяем существует ли наш юзер
    with Session() as session:
        user = session.query(Finances).all()
        for item in user:
            #если существует то закрываем функцию и отправляем сообщение об этом
            if message.from_user.id == item.id:
                await message.answer('You\'re already registered!', reply_markup=kb.main_keyboard)
                return 0
        # в случае новой регистраций мы добавляем нашего юзера в БД
        new_user = Finances(id=message.from_user.id, moneys = 0)
        session.add(new_user)
        session.commit()
    await message.answer('succesful registered now enter your budget:', reply_markup=ReplyKeyboardRemove())
    await state.set_state(Register.choosing_budget)

#используя машины состояний мы вводим начальный бюджет юзера
@router.message(Register.choosing_budget,
                TypeFilter())
async def register(message: Message, state: FSMContext):
    moneys = int(message.text)
    with Session() as session:
        user = session.query(Finances).filter(Finances.id == message.from_user.id).first()
        user.moneys = moneys
        session.commit()
    await message.answer(f'отлично ваш бюджет : {moneys}', reply_markup=kb.main_keyboard)
    await state.clear()

# Хендлер для ввода нового дохода
@router.message(F.text.lower() == 'income')
async def income_cmd(message:Message, state: FSMContext):
    await message.answer(f'enter your income:', reply_markup=ReplyKeyboardRemove())
    await state.set_state(income_state.choosing_amount)# переводим машину состояний для ввода дохода

# в случае правильного ввода 
@router.message(
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

# хендлер для ввода расхода
@router.message(F.text.lower() == 'consumption')
async def consumption_cmd(message: Message, state: FSMContext):
    await state.set_state(consumption_state.choosing_amount)
    await message.answer('enter consumption:', reply_markup=ReplyKeyboardRemove())

#в случае правильного ввода 
@router.message(consumption_state.choosing_amount, TypeFilter())
async def choosing_amount(message: Message, state: FSMContext):
    await state.set_state(consumption_state.choosing_reason)
    await state.update_data(cons_amount=int(message.text)) # загружаем в оперативку расход
    # создаем динамическую клавиатуру на основе consumotion_reasons для того чтоб было удобно считать расходы
    await message.answer('now enter reason of consumption:', reply_markup=kb.make_row_keyboard(consumption_reasons)) 

# в случае правильного ввода
@router.message(consumption_state.choosing_reason, F.text.in_(consumption_reasons))
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
    
# Хендлер вывода бюджета здесь все просто и понятно
@router.message(F.text == 'show my money')
async def show_money_cmd(message:Message):
    with Session() as session:
        user = session.query(Finances).filter(Finances.id == message.from_user.id).first()
        await message.answer(f'you\'re budget is: {user.moneys}')

# Хендлер для вывода расходов
@router.message(F.text.lower() == 'show consumption')
async def show_cons_cmd(message: Message):
    with Session() as session:
        avg_per_week = 0
        rsn_cons = dict()
        # получаем из БД сумму расходов группируя их по дате
        cons = session.query(Consumptions.data, func.sum(Consumptions.consumptions)).group_by(Consumptions.data).all()
        try:
            # Для вывода среднего расхода в неделю
            for item in range(7):
                avg_per_week += cons[item][1]
            
            avg_per_week = round(avg_per_week / 7, 1) # округляем до 1 числа после запятой
            await message.answer(f'''ваш средний расход в неделю: {avg_per_week}''')
        # если дело не дошло до 7 дней
        except IndexError:
            await message.answer('Нету расхода в неделю')
        
        # сумма расходов прикольная штука генератор списков
        sum_cons = sum(sublist[1] for sublist in cons)
        await message.answer(f'Общий расход состовляет: {sum_cons}')
        
        # вывод расхода сортируя по причинам
        cons = session.query(Consumptions.reason,func.sum(Consumptions.consumptions)).group_by(Consumptions.reason).all()
        for item in range(len(cons)):
            rsn_cons[cons[item][0]] = cons[item][1]
        output = [f'{key} : {value}' for key, value in rsn_cons.items()]
        await message.answer('\n'.join(output))

# хендлер для вывода доходов здесь почти так же как у расходов
@router.message(F.text.lower() == 'show incomes')
async def show_incomes_cmd(message: Message):
    with Session() as session:
        avg_per_week = 0
        incomes = session.query(Incomes.data, func.sum(Incomes.incomes)).group_by(Incomes.data).all()
        try:
            for item in range(7):
                avg_per_week += incomes[item][1]
            
            avg_per_week = round(avg_per_week / 7)
            await message.answer(f'Средний доход в неделю {avg_per_week}')
        except IndexError:
            await message.answer(f'Нету дохода в неделю')
        summary = sum(sublist[1] for sublist in incomes)
        await message.answer(f'you\'r incomes sum: {summary}')


# хендлер в случаях где ввод неправильный точнее введено было не число
@router.message(consumption_state.choosing_amount, F.text)
@router.message(Register.choosing_budget, F.text)
@router.message(income_state.choosing_amount, F.text)
async def incorrect_register(message: Message, state: FSMContext):
    await message.answer('please enter correct numbers!')