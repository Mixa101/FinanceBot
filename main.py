from aiogram import types, Dispatcher, Bot, F
import asyncio
from handlers.main_router import router, not_exists_routers
from config import config

bot = Bot(token=config.bot_token.get_secret_value())

dp = Dispatcher()


async def main():
    dp.include_router(router)
    dp.include_router(not_exists_routers)
    await dp.start_polling(bot)
    

if __name__=='__main__':
    asyncio.run(main())