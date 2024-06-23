from aiogram.fsm.state import State, StatesGroup


class ChatGPTStates(StatesGroup):
    waiting_for_response = State()
