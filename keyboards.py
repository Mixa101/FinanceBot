from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder

# создаем основную клавиатуру 
main_keyboard = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='Income'), KeyboardButton(text='Consumption')],
    [KeyboardButton(text='show my money'), KeyboardButton(text='set a goal')],
    [KeyboardButton(text='Show consumption'), KeyboardButton(text='Show incomes')]
], resize_keyboard=True)

# функция для создания динамической клавиатуры
def make_row_keyboard(items: list[str]) -> ReplyKeyboardMarkup:
    row = [KeyboardButton(text=item) for item in items]
    return ReplyKeyboardMarkup(keyboard=[row], resize_keyboard=True)
