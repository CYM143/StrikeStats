from telebot import types
from loader import bot
from states import UserRegistration
from database import search_user, registration_user

@bot.message_handler(commands=['start'])
async def start_handler(message):
    user_id = message.from_user.id

    if await search_user(user_id):
        return

    await bot.set_state(user_id, UserRegistration.wait_name, message.chat.id)
    await bot.send_message(user_id, 'Введите ваше имя:')

@bot.message_handler(state=UserRegistration.wait_name, content_types=['text'])
async def get_name_handler(message):
    user_id = message.from_user.id
    async with bot.retrieve_data(user_id, user_id) as data:
        data['name'] = message.text

    await bot.set_state(user_id, UserRegistration.wait_call, message.chat.id)
    await bot.send_message(user_id, 'Введите ваш позывной:')

@bot.message_handler(state=UserRegistration.wait_call, content_types=['text'])
async def get_name_handler(message):
    user_id = message.from_user.id
    async with bot.retrieve_data(user_id, user_id) as data:
        name = data['name']
        call = message.text

    await registration_user(user_id, name, call)
    await bot.delete_state(user_id, user_id)
    await bot.send_message(user_id, f'{name}, поздравляю с успешной регистрацией !\nТеперь вы можете вносить список своих игр =)')