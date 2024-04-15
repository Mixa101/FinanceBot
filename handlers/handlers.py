from aiogram.types import Message
from aiogram import Router, F
from settings import Register, consumption_state, income_state, set_goal_state
from aiogram.fsm.context import FSMContext
from handlers.income_handlers import income_router
from handlers.output_handlers import output_router
from handlers.consumption_handlers import cons_router
from handlers.start_handler import start_router
from handlers.goal_handler import goal_router

# Опять же роутеры классная штука
router = Router()
# добавляем все роутеры
router.include_router(income_router)
router.include_router(cons_router)
router.include_router(output_router)
router.include_router(start_router)
router.include_router(goal_router)

# хендлер в случаях где ввод неправильный точнее введено было не число
@income_router.message(income_state.choosing_amount, F.text)
@cons_router.message(consumption_state.choosing_amount, F.text)
@goal_router.message(set_goal_state.sum_goal, F.text)
@start_router.message(Register.choosing_budget ,F.text)
async def incorrect_register(message: Message, state: FSMContext):
    await message.answer('please enter correct numbers!')