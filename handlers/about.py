from loader import bot
from .inline_keyboards import create_inline_kb_to_menu
import requests, re

repo_url = 'https://api.github.com/repos/CYM143/StrikeStats/commits'

@bot.callback_query_handler(func=lambda callback: callback.data == 'about_program')
async def about_handler(callback):
    user_id = callback.from_user.id
    chat_id = callback.message.chat.id

    request = (requests.get(repo_url).json())[0]['commit']['message']
    version = re.search(r'\d.\d.\d+[a-z]?', request)
    msg = f'''Приложение для отслеживание посещенных игр

Раработано - MrValViL (CYM143)
Текущая версия - v{version.group()}

<a href="https://github.com/CYM143/StrikeStats">Исходный код</a>
    '''

    markup = create_inline_kb_to_menu()

    await bot.edit_message_text(msg, chat_id, callback.message.message_id, reply_markup=markup, parse_mode="HTML")