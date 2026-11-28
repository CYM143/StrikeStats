from loader import bot
from states import UserRegistration
from database import search_user, registration_user, save_user_message_id, load_user_message_id
from .menu import menu_handler, menu_command_handler
import asyncio
from logger import logger

@bot.message_handler(commands=['start'])
async def start_handler(message):
    user_id = message.from_user.id
    chat_id = message.chat.id

    await bot.delete_state(user_id, chat_id)

    if await search_user(user_id):
        await menu_command_handler(message)
        return

    await bot.set_state(user_id, UserRegistration.wait_name, message.chat.id)
    bot_msg = await bot.send_message(user_id, 'Введите ваше имя:')
    await bot.delete_message(user_id, message.message_id)
    await save_user_message_id(user_id, bot_msg.message_id)

@bot.message_handler(state=UserRegistration.wait_name, content_types=['text'])
async def get_name_handler(message):
    user_id = message.from_user.id
    chat_id = message.chat.id
    msg_id = await load_user_message_id(user_id)

    async with bot.retrieve_data(user_id, chat_id) as data:
        data['name'] = message.text

    await bot.set_state(user_id, UserRegistration.wait_call, message.chat.id)
    await bot.delete_message(chat_id, message.message_id)
    await bot.edit_message_text('Введите ваш позывной:', chat_id, msg_id)

@bot.message_handler(state=UserRegistration.wait_call, content_types=['text'])
async def get_name_handler(message):
    user_id = message.from_user.id
    chat_id = message.chat.id
    msg_id = await load_user_message_id(user_id)

    async with bot.retrieve_data(user_id, chat_id) as data:
        name = data['name']
        call = message.text

    await registration_user(user_id, name, call)
    logger.info("New user register succesful")
    await bot.delete_state(user_id, user_id)
    await bot.delete_message(chat_id, message.message_id)
    await bot.edit_message_text(f'{name}, поздравляю с успешной регистрацией !\nТеперь вы можете вносить список своих игр =)', chat_id, msg_id)
    await asyncio.sleep(5)
    await menu_handler(message)