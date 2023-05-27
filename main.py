import asyncio
import io
from os import getenv

import openai
from aiogram import Bot, Dispatcher, F, Router
from aiogram.enums.chat_action import ChatAction
from aiogram.filters import Command
from aiogram.methods import SendChatAction
from aiogram.types import Message, Voice
from dotenv import load_dotenv
from pydub import AudioSegment

load_dotenv()
TELEGRAM_BOT_TOKEN = getenv("TELEGRAM_BOT_TOKEN")
WHITE_LIST_IDS = getenv("WHITE_LIST_IDS").split(", ")
OPENAI_API_KEY = getenv("OPENAI_API_KEY")
GPT_ENGINE = getenv("GPT_ENGINE")


openai.api_key = OPENAI_API_KEY
router: Router = Router()


async def create_chat_completion(message):
    return await openai.ChatCompletion.acreate(
        model=GPT_ENGINE, messages=[{"role": "user", "content": message}]
    )


async def audio_to_text(file_path: str) -> str:
    """Принимает путь к аудио файлу, возвращает текст файла."""
    with open(file_path, "rb") as audio_file:
        transcript = await openai.Audio.atranscribe("whisper-1", audio_file)
    return transcript["text"]


async def save_voice_as_mp3(bot: Bot, voice: Voice) -> str:
    """Скачивает голосовое сообщение и сохраняет в формате mp3."""
    voice_file_info = await bot.get_file(voice.file_id)
    voice_ogg = io.BytesIO()
    await bot.download_file(voice_file_info.file_path, voice_ogg)
    voice_mp3_path = f"voice_files/voice-{voice.file_unique_id}.mp3"
    AudioSegment.from_file(voice_ogg, format="ogg").export(
        voice_mp3_path, format="mp3"
    )
    return voice_mp3_path


@router.message(Command(commands=["start"]))
async def process_start_command(message: Message):
    """Команда старт."""
    await SendChatAction(
        chat_id=message.from_user.id, action=ChatAction.TYPING
    )
    if str(message.from_user.id) not in WHITE_LIST_IDS:
        msg = "Тебя нет в списках на вписках!"
        await message.answer(msg)
        return

    msg = "Напиши любое сообщение боту чтобы обратиться к ChatGPT!"
    await message.answer(msg)


@router.message(F.content_type == "text")
async def process_text_message(message: Message):
    """Принимает текстовые сообщения."""
    if str(message.from_user.id) not in WHITE_LIST_IDS:
        return
    await SendChatAction(
        chat_id=message.from_user.id, action=ChatAction.TYPING
    )
    try:
        msg = await create_chat_completion(message.text)
        msg = msg.choices[0].message.content
    except openai.error.RateLimitError:
        msg = "Достигнут предел скорости. Ограничение: 3 запроса в минуту. Пожалуйста, повторите попытку через 20 секунд."
    except Exception as e:
        msg = f"Ошибка: {e}"
    await message.answer(text=msg)


@router.message(F.content_type == "voice")
async def process_voice_message(message: Message, bot: Bot):
    """Принимает все голосовые сообщения и транскрибирует их в текст."""
    if str(message.from_user.id) not in WHITE_LIST_IDS:
        return
    await SendChatAction(
        chat_id=message.from_user.id, action=ChatAction.TYPING
    )
    voice_path = await save_voice_as_mp3(bot, message.voice)
    transcripted_voice_text = await audio_to_text(voice_path)

    if transcripted_voice_text:
        # await message.reply(text=transcripted_voice_text)
        await SendChatAction(
            chat_id=message.from_user.id, action=ChatAction.TYPING
        )
        try:
            msg = await create_chat_completion(transcripted_voice_text)
            msg = msg.choices[0].message.content
        except openai.error.RateLimitError:
            msg = "Достигнут предел скорости. Ограничение: 3 запроса в минуту. Пожалуйста, повторите попытку через 20 секунд."
        except Exception as e:
            msg = f"Ошибка: {e}"
        await message.answer(text=msg)


async def main():
    bot: Bot = Bot(token=TELEGRAM_BOT_TOKEN)
    dp: Dispatcher = Dispatcher()
    dp.include_router(router)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
