from aiogram import Router, F
from aiogram.types import Message, ReplyKeyboardRemove
from models import Consumptions, Finances, Incomes
from data_base import Session
from sqlalchemy import func
from aiogram.exceptions import TelegramBadRequest
from aiogram.utils.formatting import Text, Bold, as_list, Italic, as_section

output_router = Router()
# Хендлер вывода бюджета здесь все просто и понятно
@output_router.message(F.text == 'show my money')
async def show_money_cmd(message:Message):
    output_text = []
    with Session() as session:
        user = session.query(Finances).filter(Finances.id == message.from_user.id).first()
        goal_money = user.goal_sum - user.moneys
        budget = Text('you\'re budget is ', Bold(user.moneys))
        if goal_money > 0:
            goal_text = Text('for reach the goal you need ', Bold(goal_money))
        else:
            goal_text = Text('you have all moneys to buy your goal')
            
        output_text = as_list(budget, goal_text, sep='\n')

    await message.answer(**output_text.as_kwargs())
        
# Хендлер для вывода расходов
@output_router.message(F.text.lower() == 'show consumption')
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
            # await message.answer(f'''ваш средний расход в неделю: {avg_per_week}''')
            avg_text = Text('Средний расход в неделю: ', Bold(avg_per_week))
        # если дело не дошло до 7 дней
        except IndexError:
            avg_text = Text('Ещё нет расходов в неделю')
        
        # сумма расходов прикольная штука генератор списков
        try:
            sum_cons = sum(sublist[1] for sublist in cons)
            if sum_cons != 0:
                cons_text = Text('Общий расход: ', Bold(sum_cons))
            # вывод расхода сортируя по причинам
            else:
                cons_text = Text('Расходов ещё нет!')
            cons = session.query(Consumptions.reason,func.sum(Consumptions.consumptions)).group_by(Consumptions.reason).all()
            for item in range(len(cons)):
                rsn_cons[cons[item][0]] = cons[item][1]
            output = '\n'.join(f'{key} : {value}' for key, value in rsn_cons.items())
            out = Text(Bold(output))
            output_text = as_list(avg_text, cons_text, out, sep='\n')
            await message.answer(**output_text.as_kwargs())
        except TelegramBadRequest:
            await message.answer('вы ещё не ввели расходы')
            
            
# хендлер для вывода доходов здесь почти так же как у расходов
@output_router.message(F.text.lower() == 'show incomes')
async def show_incomes_cmd(message: Message):
    with Session() as session:
        avg_per_week = 0
        text_income = 'Средний доход в неделю '
        incomes = session.query(Incomes.data, func.sum(Incomes.incomes)).group_by(Incomes.data).all()
        try:
            for item in range(7):
                avg_per_week += incomes[item][1]
            
            avg_per_week = round(avg_per_week / 7)
            text_income = Text(text_income + Bold(str(avg_per_week)))
        except IndexError:
            text_income = Text('Нету дохода в неделю')
        summary = Text('Общая сумма доходов: ', Bold(sum(sublist[1] for sublist in incomes)))
        output_text = as_list(text_income, summary, sep='\n')
        await message.answer(**output_text.as_kwargs())