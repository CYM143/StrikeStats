from telebot import types
from loader import bot
from database import get_user_info
from .inline_keyboards import create_inline_kb

@bot.message_handler(commands=['menu'])
async def menu_handler(message):
    user_id = message.chat.id
    user_id, user_name, user_call = await get_user_info(user_id)

    welcome_msg = f"{user_name}, c возвращением !\nДобро пожаловать в главное меню, выберите действие..."

    markup = create_inline_kb({
        'Статистика игр': 'game_statistic',
        'Добавить игру': 'game_add',
        'Настройки': 'settings',
        'О программе': 'about_program'
    })

    await bot.send_message(user_id, welcome_msg, reply_markup=markup)