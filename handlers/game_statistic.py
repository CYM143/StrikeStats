from loader import bot
from telebot import types
from .inline_keyboards import create_inline_kb_to_menu
from database import get_user_games
from collections import Counter

def get_statistic(games: tuple):
    if not games:
        return None
    
    types_count = Counter(game[4] for game in games)
    clubs = (Counter(game[3] for game in games)).most_common()

    return {
        'total_games': len(games),
        'open_games': types_count['Открытая'],
        'close_games': types_count['Закрытая'],
        'clubs': clubs,
        'favorite_club': clubs[0],
        'last_date': games[-1][2]
    }

@bot.callback_query_handler(func=lambda callback: callback.data == 'game_statistic')
async def games_statistic_handler(callback):
    user_id = callback.from_user.id

    games = await get_user_games(user_id)
    data = get_statistic(games)

    if data is None:
        await bot.edit_message_text('У вас ешё нет добавленных игр, добавтьте их через главное меню !', user_id, callback.message.message_id)
        return

    clubs_list = "\n".join(f" - {club}: {count}" for club, count in data['clubs'])

    msg = f"""<b>Статистика по всем играм:</b>

<i>Общее кол-во игр</i> - {data['total_games']}
 - Открытые: {data['open_games']}
 - Закрытые: {data['close_games']}

Любимый клуб - <b>{data['favorite_club'][0]}</b>
Список клубов по посещаемости: 
{clubs_list}

 
Дата последней игры - {data['last_date']}
"""
    markup = create_inline_kb_to_menu()

    await bot.edit_message_text(msg, user_id, callback.message.message_id, parse_mode='HTML', reply_markup=markup)