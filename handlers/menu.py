from telebot import types
from loader import bot
from database import get_user_info, load_user_message_id, remove_user_message_id, save_user_message_id
from .inline_keyboards import create_inline_kb

async def build_main_menu(user_id: int, chat_id: int) -> tuple:
    await bot.delete_state(user_id, chat_id)
    _, user_name, _ = await get_user_info(user_id)

    welcome_msg = f"{user_name}, c возвращением !\nДобро пожаловать в главное меню, выберите действие..."
    
    markup = create_inline_kb({
        'Статистика игр': 'game_statistic',
        'Добавить игру': 'game_add',
        'Настройки': 'settings',
        'О программе': 'about_program'
    })

    return welcome_msg, markup

@bot.message_handler(commands=['menu'])
async def menu_command_handler(message):
    user_id = message.from_user.id
    chat_id = message.chat.id

    await remove_user_message_id(user_id)

    welcome_msg, markup = await build_main_menu(user_id, chat_id)

    bot_msg = await bot.send_message(chat_id, welcome_msg, reply_markup=markup)
    await bot.delete_message(chat_id, message.message_id)
    await save_user_message_id(user_id, bot_msg.message_id)

async def menu_handler(message):
    user_id = message.from_user.id
    chat_id = message.chat.id
    msg_id = await load_user_message_id(user_id)

    welcome_msg, markup = await build_main_menu(user_id, chat_id)
    
    await bot.edit_message_text(welcome_msg, chat_id, msg_id,  reply_markup=markup)


@bot.callback_query_handler(func=lambda callback: callback.data == 'back_to_menu')
async def back_to_menu_handler(callback):
    user_id = callback.from_user.id
    chat_id = callback.message.chat.id

    welcome_msg, markup = await build_main_menu(user_id, chat_id)

    await bot.edit_message_text(welcome_msg, chat_id, callback.message.message_id, reply_markup=markup)