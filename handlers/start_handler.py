from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext
from modules.models import Finances
from modules.data_base import Session
import modules.keyboards as kb
from settings import Register, TypeFilter

start_router = Router()

@start_router.message(Command('start'))
async def cmd_start(message: Message, state: FSMContext):
    #открываем базу данных и проверяем существует ли наш юзер
    with Session() as session:
        user = session.query(Finances).all()
        for item in user:
            #если существует то закрываем функцию и отправляем сообщение об этом
            if message.from_user.id == item.id:
                await message.answer('Вы уже зарегестрированы!', reply_markup=kb.main_keyboard)
                return 0
        # в случае новой регистраций мы добавляем нашего юзера в БД
        new_user = Finances(id=message.from_user.id, moneys = 0)
        session.add(new_user)
        session.commit()
    await message.answer('успешная регистрация, введите ваш бюджет :', reply_markup=ReplyKeyboardRemove())
    await state.set_state(Register.choosing_budget)

#используя машины состояний мы вводим начальный бюджет юзера
@start_router.message(Register.choosing_budget,
                TypeFilter())
async def register(message: Message, state: FSMContext):
    moneys = int(message.text)
    with Session() as session:
        user = session.query(Finances).filter(Finances.id == message.from_user.id).first()
        user.moneys = moneys
        session.commit()
    await message.answer(f'отлично ваш бюджет : {moneys}', reply_markup=kb.main_keyboard)
    await state.clear()