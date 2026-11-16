from telebot.asyncio_handler_backends import State, StatesGroup

class UserRegistration(StatesGroup):
    wait_name = State()
    wait_call = State()