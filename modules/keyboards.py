from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder
from data.output_operations import group_reasons

main_keyboard = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='Добавить доход'), KeyboardButton(text='Добавить расход')],
    [KeyboardButton(text='Показать бюджет')],
    [KeyboardButton(text='Показать расходы'), KeyboardButton(text='Показать доходы')]
])
def create_reason_keyboard(id):
    reasons = group_reasons(id)
    reason_buttons = [KeyboardButton(text=i)for i in reasons]
    reason_builder = ReplyKeyboardBuilder()
    reason_builder.row(*reason_buttons, width = 4)
    return reason_builder