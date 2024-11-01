from aiogram import Router, F, types
from handlers.start_handler import start_router
from handlers.operations_router import operational_routers
from handlers.output_routers import output_router
from data.data_getters import UserExists

not_found_router = Router()
# not_found_router.message.filter(lambda message: user_exists(message))
user_not_exists = Router()
@user_not_exists.message(UserExists("for_not_exist"))
async def not_exists(message: types.Message):
    await message.answer(f"введите '/start' для начала работы!")

@not_found_router.message()
async def wrong_message(message: types.Message):
    await message.answer(f'извините у меня нет такой команды как "{message.text}"')

router = Router()
router.message.filter(UserExists('for_exist'))
router.include_router(operational_routers)
router.include_router(output_router)
router.include_router(not_found_router)

not_exists_routers = Router()
not_exists_routers.include_router(start_router)
not_exists_routers.include_router(user_not_exists)


