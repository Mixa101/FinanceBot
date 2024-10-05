from aiogram import F, types, Router
from data.data_setters import set_income, set_consumption
from data.data_getters import user_exists
from aiogram.fsm.context import FSMContext
from modules.states import Income, Consumption
from aiogram.filters import StateFilter
from modules.keyboards import main_keyboard

operational_routers = Router()
# operational_routers.message.filter(lambda message: user_exists(message))

@operational_routers.message(F.text == 'Добавить доход')
async def income(message : types.Message, state : FSMContext):
    await message.answer('Введите доход', reply_markup=types.ReplyKeyboardRemove())
    await state.set_state(Income.enter_sum_of_income)

@operational_routers.message(lambda x: x.text.isdigit() ,StateFilter("Income:enter_sum_of_income"))
async def add_income(message: types.Message, state: FSMContext):
    set_income(message.from_user.id, int(message.text))
    await message.answer("succesfully add new income!", reply_markup=main_keyboard)
    await state.clear()

@operational_routers.message(F.text == 'Добавить расход')
async def consumption(message : types.Message, state: FSMContext):
    await message.answer('введите расход', reply_markup=types.ReplyKeyboardRemove())
    await state.set_state(Consumption.enter_sum_of_cons)

@operational_routers.message(lambda x: x.text.isdigit() ,StateFilter("Consumption:enter_sum_of_cons"))
async def reason_of_cons(message : types.Message, state: FSMContext):
    await state.update_data(sum_of_cons = int(message.text))
    await message.answer('Введите причину расхода')
    await state.set_state(Consumption.enter_reason_of_cons)

@operational_routers.message(StateFilter("Consumption:enter_reason_of_cons"))
async def add_consumption(message : types.Message, state: FSMContext):
    state_data = await state.get_data()
    sum_of_cons = state_data.get('sum_of_cons')
    set_consumption(message.from_user.id, int(sum_of_cons), message.text)
    await message.answer('успешно! добавлен новый расход!', reply_markup=main_keyboard)
    await state.clear()

@operational_routers.message(StateFilter("Consumption:enter_sum_of_cons"), StateFilter("Income:enter_sum_of_income"))
async def wrong_enter(message: types.Message, state: FSMContext):
    await message.answer(f"{message.text} не является числом!")