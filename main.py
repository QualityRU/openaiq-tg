from asyncio import run

from aiogram import Bot, Dispatcher, F, Router
from aiogram.enums.chat_action import ChatAction
from aiogram.filters import Command
from aiogram.types import Message
from decouple import config
from openai import AsyncOpenAI

TELEGRAM_BOT_TOKEN: str = config('TELEGRAM_BOT_TOKEN')
OPENAI_API_KEY: str = config('OPENAI_API_KEY')
OPENAI_PROJECT: str = config('OPENAI_PROJECT')
GPT_ENGINE: str = config('GPT_ENGINE')

bot: Bot = Bot(token=TELEGRAM_BOT_TOKEN)
dp: Dispatcher = Dispatcher()
router: Router = Router()
dp.include_router(router)


client = AsyncOpenAI(api_key=OPENAI_API_KEY, project=OPENAI_PROJECT)


async def create_chat_completion(message: Message):
    chat_completion = await client.chat.completions.create(
        messages=[
            {
                'role': 'user',
                'content': message,
            }
        ],
        model=GPT_ENGINE,
    )
    return chat_completion


@router.message(Command(commands=['start']))
async def process_start_command(message: Message):
    """Команда старт."""
    result: bool = await bot.send_chat_action(
        chat_id=message.from_user.id, action=ChatAction.TYPING
    )
    # if str(message.from_user.id) not in WHITE_LIST_IDS:
    #     msg = 'Тебя нет в списках на вписках!'
    #     await message.answer(msg)
    #     return

    msg = 'Напиши любое сообщение боту чтобы обратиться к ChatGPT!'
    await message.answer(msg)


@router.message(F.content_type == 'text')
async def process_text_message(message: Message):
    """Принимает текстовые сообщения."""
    # if str(message.from_user.id) not in WHITE_LIST_IDS:
    #     return
    result: bool = await bot.send_chat_action(
        chat_id=message.from_user.id, action=ChatAction.TYPING
    )
    try:
        msg = await create_chat_completion(message.text)
        msg = msg.choices[0].message.content
    except Exception as e:
        msg = e

    await message.answer(text=msg)


async def main():
    await dp.start_polling(bot)


if __name__ == '__main__':
    run(main())
