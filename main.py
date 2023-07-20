import asyncio
import re
from os import getenv

import openai
from aiogram import Bot, Dispatcher, F, Router
from aiogram.enums.chat_action import ChatAction
from aiogram.filters import Command
from aiogram.types import Message
from dotenv import load_dotenv

load_dotenv()
TELEGRAM_BOT_TOKEN = getenv('TELEGRAM_BOT_TOKEN')
WHITE_LIST_IDS = getenv('WHITE_LIST_IDS').split(', ')
CHIMERA_API_KEY = getenv('CHIMERA_API_KEY')
GPT_ENGINE = getenv('GPT_ENGINE')


openai.api_key = CHIMERA_API_KEY
openai.api_base = 'https://chimeragpt.adventblocks.cc/v1'
router: Router = Router()

bot: Bot = Bot(token=TELEGRAM_BOT_TOKEN)
dp: Dispatcher = Dispatcher()
dp.include_router(router)


async def create_chat_completion(message):
    return await openai.ChatCompletion.acreate(
        model=GPT_ENGINE, messages=[{'role': 'user', 'content': message}]
    )


@router.message(Command(commands=['start']))
async def process_start_command(message: Message):
    """Команда старт."""
    result: bool = await bot.send_chat_action(
        chat_id=message.from_user.id, action=ChatAction.TYPING
    )
    if str(message.from_user.id) not in WHITE_LIST_IDS:
        msg = 'Тебя нет в списках на вписках!'
        await message.answer(msg)
        return

    msg = 'Напиши любое сообщение боту чтобы обратиться к ChatGPT!'
    await message.answer(msg)


@router.message(F.content_type == 'text')
async def process_text_message(message: Message):
    """Принимает текстовые сообщения."""
    if str(message.from_user.id) not in WHITE_LIST_IDS:
        return
    result: bool = await bot.send_chat_action(
        chat_id=message.from_user.id, action=ChatAction.TYPING
    )
    try:
        msg = await create_chat_completion(message.text)
        msg = msg.choices[0].message.content
    except openai.error.APIError as e:
        detail_pattern = re.compile(r'{"detail":"(.*?)"}')
        match = detail_pattern.search(e.user_message)
        if match:
            msg = match.group(1)
        else:
            msg = e.user_message

    await message.answer(text=msg)


async def main():
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
