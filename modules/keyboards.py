from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder

main_keyboard = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='Добавить доход'), KeyboardButton(text='Добавить расход')],
    [KeyboardButton(text='Показать бюджет')],
    [KeyboardButton(text='Показать расходы'), KeyboardButton(text='Показать доходы')]
])