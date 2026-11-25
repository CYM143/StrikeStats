from loader import bot
from .inline_keyboards import create_inline_kb, create_inline_kb_to_menu
from states import UserChangeData
from database import load_user_message_id, change_call_user, change_name_user
import asyncio
from .menu import menu_handler

@bot.callback_query_handler(func=lambda callback: callback.data == 'settings')
async def settings_handler(callback):
    user_id = callback.from_user.id
    chat_id = callback.message.chat.id

    markup = create_inline_kb({
        'Сменить имя': 'change_name',
        'Сменить позывной': 'change_call',
        'Назад в меню': 'back_to_menu'
    })

    await bot.edit_message_text('Меню настроек...', chat_id, callback.message.message_id, reply_markup=markup)



@bot.callback_query_handler(func=lambda callback: callback.data == 'change_name')
async def change_name_callback_handler(callback):
    user_id = callback.from_user.id
    chat_id = callback.message.chat.id

    await bot.set_state(user_id, UserChangeData.wait_name, chat_id)

    markup = create_inline_kb_to_menu()

    await bot.edit_message_text('Пришлите ваше новое имя...', chat_id, callback.message.message_id, reply_markup=markup)

@bot.message_handler(state=UserChangeData.wait_name, content_types=['text'])
async def change_name_handler(message):
    user_id = message.from_user.id
    chat_id = message.chat.id
    name = message.text
    msg_id = await load_user_message_id(user_id)

    await change_name_user(user_id, name)

    await bot.delete_state(user_id, chat_id)

    await bot.edit_message_text('Успешная смена имени !', chat_id, msg_id)
    await bot.delete_message(chat_id, message.message_id)
    await asyncio.sleep(1.5)
    await menu_handler(message)




@bot.callback_query_handler(func=lambda callback: callback.data == 'change_call')
async def change_name_callback_handler(callback):
    user_id = callback.from_user.id
    chat_id = callback.message.chat.id

    await bot.set_state(user_id, UserChangeData.wait_call, chat_id)

    markup = create_inline_kb_to_menu()

    await bot.edit_message_text('Пришлите ваш новый позывной...', chat_id, callback.message.message_id, reply_markup=markup)

@bot.message_handler(state=UserChangeData.wait_call, content_types=['text'])
async def change_name_handler(message):
    user_id = message.from_user.id
    chat_id = message.chat.id
    call = message.text
    msg_id = await load_user_message_id(user_id)

    await change_call_user(user_id, call)

    await bot.delete_state(user_id, chat_id)

    await bot.edit_message_text('Успешная смена позывного !', chat_id, msg_id)
    await bot.delete_message(chat_id, message.message_id)
    await asyncio.sleep(1.5)
    await menu_handler(message)