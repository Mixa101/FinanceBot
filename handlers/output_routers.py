from aiogram import types, F, Router
from data.data_getters import get_budget, user_exists
from data.output_operations import calculate_avg_income, calculate_avg_cons

output_router = Router()
# output_router.message.filter(lambda message: user_exists(message))


@output_router.message(F.text == 'Показать бюджет')
async def output_budget(message : types.Message):
    budget = get_budget(message.from_user.id)
    await message.answer(f"ваш бюджет : {budget}")

@output_router.message(F.text == 'Показать доходы')
async def output_incomes(message : types.Message):
    incomes = calculate_avg_income(message.from_user.id)
    await message.answer(f"сумма общего дохода: {incomes[1]}\nсредний доход в неделю: {incomes[0]}")

@output_router.message(F.text == 'Показать расходы')
async def output_cons(message: types.Message):
    cons = calculate_avg_cons(message.from_user.id)
    await message.answer(f"сумма общего расхода: {cons[1]}\nсредний расход в неделю: {cons[0]}")