from asyncio import run
from logging import INFO, basicConfig, getLogger

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

from app.handlers import router
from config import TELEGRAM_BOT_TOKEN

basicConfig(
    level=INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
)
logger = getLogger(__name__)


async def main() -> None:
    logger.info('Запуск бота')

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
