from config import config
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from handlers.handlers import router
import asyncio, logging

# включаем логирование чтобы не пропустить важные сообщения
logging.basicConfig(level=logging.INFO)
# обьект бота
bot = Bot(token=config.bot_token.get_secret_value())
# диспетчер
dp = Dispatcher(storage=MemoryStorage())


#полинг бота
async def main():
    #роутеры классная штука
    dp.include_router(router)
    await dp.start_polling(bot)

if __name__=='__main__':
    asyncio.run(main())
    