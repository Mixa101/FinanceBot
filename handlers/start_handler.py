from aiogram import types, Router
from aiogram.filters import Command, StateFilter
from data.data_getters import user_exists
from data.data_setters import set_user
from aiogram.fsm.context import FSMContext
from modules.states import Register
from modules.keyboards import main_keyboard

start_router = Router()

@start_router.message(Command('start'))
async def start_handler(message: types.Message, state: FSMContext):
    # Проверяем существует ли пользователь
    if user_exists(message):
        await message.answer("Вы уже зарегестрированы!", reply_markup=main_keyboard)
        return 0
    
    # дальше регистрируем
    else:
        await message.answer('введите бюджет: ')
        await state.set_state(Register.enter_budget)


@start_router.message(lambda x: x.text.isdigit() ,StateFilter("Register:enter_budget"))
async def enter_budget(message: types.Message, state: FSMContext):
    set_user(message.from_user.id, int(message.text))
    await message.reply('успешная регистрация!', reply_markup=main_keyboard)
    await state.clear()


@start_router.message(StateFilter("Register:enter_budget"))
async def wrong_budget(message: types.Message, state: FSMContext):
    await message.answer(f"'{message.text}' не является числом, бюджет состоит из цифр!")