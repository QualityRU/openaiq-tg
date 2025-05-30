from logging import getLogger
from typing import Any, Dict, Union

from aiogram import Bot, F, Router
from aiogram.filters import Command, Filter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from openai import AsyncOpenAI

from app.states import ChatGPTStates
from config import ADMIN_IDS, GPT_ENGINE, OPENAI_API_KEY

logger = getLogger(__name__)

router: Router = Router()
client: AsyncOpenAI = AsyncOpenAI(
    api_key=OPENAI_API_KEY, base_url='https://api.chatanywhere.tech/v1'
)


class IsAdminFilter(Filter):
    async def __call__(self, message: Message) -> bool:
        return message.from_user.id in ADMIN_IDS


async def create_chat_completion(
    message_text: str,
) -> Union[str, Dict[str, Any]]:
    try:
        logger.info(f'Запрос к OpenAI: {message_text}')
        chat_completion = await client.chat.completions.create(
            messages=[
                {
                    'role': 'user',
                    'content': message_text,
                }
            ],
            model=GPT_ENGINE,
        )
        logger.info('Ответ получен от OpenAI')
        return chat_completion
    except Exception as e:
        logger.error(f'Ошибка при запросе к OpenAI: {e}')
        return str(e)


@router.message(Command(commands=['start']), IsAdminFilter())
async def process_start_command(message: Message) -> None:
    """Команда старт."""
    logger.info(f'Команда /start от пользователя: {message.from_user.id}')
    msg: str = 'Напиши любое сообщение боту чтобы обратиться к ChatGPT!'
    await message.answer(msg)


@router.message(F.content_type == 'text', IsAdminFilter())
async def process_text_message(
    message: Message, state: FSMContext, bot: Bot
) -> None:
    """Принимает текстовые сообщения."""
    logger.info(
        f'Сообщение от пользователя {message.from_user.id}: {message.text}'
    )
    current_state = await state.get_state()
    if current_state is not None:
        logger.warning(
            f'Пользователь {message.from_user.id} отправил сообщение, когда предыдущее еще не обработано'
        )
        await message.answer(
            'Пожалуйста, дождитесь ответа на предыдущее сообщение.'
        )
        return

    await state.set_state(ChatGPTStates.waiting_for_response)

    try:
        await bot.send_chat_action(chat_id=message.chat.id, action='typing')

        response = await create_chat_completion(message.text)
        if isinstance(response, str):
            msg = response
        else:
            msg = response.choices[0].message.content
        logger.info(f'Ответ пользователю {message.from_user.id}: {msg}')
    except Exception as e:
        msg = f'Произошла ошибка: {str(e)}'
        logger.error(
            f'Ошибка при обработке сообщения от пользователя {message.from_user.id}: {e}'
        )

    await message.answer(text=str(msg))
    await state.clear()
