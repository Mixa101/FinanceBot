from aiogram import Router, F
from aiogram.types import Message, ReplyKeyboardRemove
from modules.models import Consumptions, Finances, Incomes
from modules.data_base import Session
from sqlalchemy import func
from aiogram.exceptions import TelegramBadRequest
from aiogram.utils.formatting import Text, Bold, as_list, Italic
from settings import goal_counter
from aiogram.filters import Command
from modules.functions import output_cons, test, output_income

"""
    ЗДЕСЬ НАХОДИТСЯ ВСЕ ЧТО СВЯЗАНО С ВЫВОДОМ
"""

output_router = Router()
# Хендлер вывода бюджета здесь все просто и понятно
# @output_router.message(Command('test'))
# async def test3(message:Message):
#     output_incomes = output_income(message.from_user.id)
#     await message.answer(**output_incomes.as_kwargs())
    

@output_router.message(F.text == 'show my money')
async def show_money_cmd(message:Message):
    output_text = []
    with Session() as session:
        user = session.query(Finances).filter(Finances.id == message.from_user.id).first()
        # проверка на существующую запись пользователя
        if user:
            # проверяем наличие цели у пользователя
            if user.goal_sum:
                goal_money = user.goal_sum - user.moneys
                # ну здесь все понятно если до цели ещё много
                if goal_money > 0:
                    goal_text = Text('для достижения цели вам надо ещё: ', Bold(goal_money))
                else:
                    goal_text = Text('сегодня же можешь идти покупать')
            # если цель не поставлена
            else:
                goal_text = Text('цели не поставлены')
            budget = Text('ваш бюджет: ', Bold(user.moneys))

            # здесь мы готовим окончательный ответ
            output_text = as_list(budget, goal_text, sep='\n')
            await message.answer(**output_text.as_kwargs())
        # если же запись не сущетсвует 
        else:
            await message.answer('Вы ещё не зарегестрированы пожалуйста введите /start', reply_markup=ReplyKeyboardRemove())

        
# Хендлер для вывода расходов
@output_router.message(F.text.lower() == 'show consumption')
async def show_cons_cmd(message: Message):
    output_consum = output_cons(message.from_user.id)
    await message.answer(**output_consum.as_kwargs())
            
            
# хендлер для вывода доходов здесь почти так же как у расходов
@output_router.message(F.text.lower() == 'show incomes')
async def show_incomes_cmd(message: Message):
    output_incomes = output_income(message.from_user.id)
    await message.answer(**output_incomes.as_kwargs())