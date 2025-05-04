from asyncio import run

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

from app.handlers import router
from app.logger import log
from config import TELEGRAM_BOT_TOKEN


async def main() -> None:
    log.info('Запуск бота')

    bot: Bot = Bot(token=TELEGRAM_BOT_TOKEN)
    storage: MemoryStorage = MemoryStorage()
    dp: Dispatcher = Dispatcher(storage=storage)
    dp.include_router(router)

    await dp.start_polling(bot)


if __name__ == '__main__':
    try:
        run(main())
    except KeyboardInterrupt:
        ...
