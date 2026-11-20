from telebot import types
from loader import bot
from states import UserAddGame
from datetime import date, timedelta, datetime
from database import save_game
from .inline_keyboards import create_inline_kb
from .menu import menu_handler

CLUBS = {
    'panda': 'Панда',
    'grizzly': 'Гризли',
    'taktika': 'Тактика'
}

GAME_TYPE = {
    'open': 'Открытая',
    'close': 'Закрытая'
}

DATE_OFFSET = {
    'today': 0,
    'yesterday': 1
}

def normalize_data(club, game_type):
    return CLUBS.get(club, club), GAME_TYPE.get(game_type, game_type)

@bot.callback_query_handler(func=lambda callback: callback.data == 'game_add') # Добавление новой игры (ДАТА)
async def game_date_choose_handler(callback):
    user_id = callback.from_user.id
    chat_id = callback.message.chat.id

    markup = create_inline_kb({
        'Сегодня': 'game_date_today',
        'Вчера': 'game_date_yesterday',
        'Ввести дату...': 'game_date_mine'
    })

    await bot.set_state(user_id, UserAddGame.wait, chat_id)
    await bot.edit_message_text('Когда была игра ?', user_id, callback.message.message_id, reply_markup=markup)

@bot.callback_query_handler(func=lambda callback: callback.data.startswith('game_date_')) # Выбор ДАТЫ по нажатию кнопки
async def game_date_callback_handler(callback):
    choose = callback.data.split('_')[-1]
    user_id = callback.from_user.id
    chat_id = callback.message.chat.id
    msg_id = callback.message.message_id

    if choose == 'mine': # Если выбрали свой вариант переходим к вводу
            await bot.set_state(user_id, UserAddGame.wait_date, chat_id)
            await bot.edit_message_text('Отправьте вашу дату в формате (ДД.ММ.ГГГГ)', user_id, msg_id)
            return

    else: # Иначе к следующему шагу
        days_ago = DATE_OFFSET[choose]
        async with bot.retrieve_data(user_id, chat_id) as data:
            data['date'] = date.today() - timedelta(days=days_ago)

    markup = create_inline_kb({
        'PANDA': 'game_club_panda',
        'GRIZZLY': 'game_club_grizzly',
        'ТАКТИКА': 'game_club_taktika',
        'Свой вариант..': 'game_club_mine'
    })

    await bot.edit_message_text('В каком клубе была игра ?', user_id, msg_id, reply_markup=markup)

@bot.message_handler(state=UserAddGame.wait_date, content_types=['text']) # Шаг для ввода своей ДАТЫ
async def game_date_enter_handler(message):
    user_id = message.from_user.id
    chat_id = message.chat.id
    form = ("%d-%m-%Y", "%d.%m.%Y")
    game_date = None

    for frm in form: # Проверяем корректность формы даты
        try:
            game_date = datetime.strptime(message.text.strip(), frm)
            break
        except ValueError:
            continue

    if game_date is None: # Если данные корректны - продолжаем
        await bot.send_message(user_id, 'Ошибка !\nВводите корректное время и в формате ДД-ММ-ГГГГ')
        return

    async with bot.retrieve_data(user_id, chat_id) as data: # Сохраняем данные о дате
        data['date'] = game_date.date()

    await bot.set_state(user_id, UserAddGame.wait, chat_id) # Убираем состояние ожидания даты

    markup = create_inline_kb({
        'PANDA': 'game_club_panda',
        'GRIZZLY': 'game_club_grizzly',
        'ТАКТИКА': 'game_club_taktika',
        'Свой вариант..': 'game_club_mine'
    })

    await bot.send_message(user_id, 'В каком клубе была игра ?', reply_markup=markup)

@bot.callback_query_handler(func=lambda callback: callback.data.startswith('game_club_')) # Выбор КЛУБА по нажатию кнопки
async def game_club_set_handler(callback):
    choose = callback.data.split('game_club_')[-1]
    user_id = callback.from_user.id
    chat_id = callback.message.chat.id
    msg_id = callback.message.message_id

    if choose == 'mine': # Если выбрали свой вариант переходим к вводу
        await bot.set_state(user_id, UserAddGame.wait_club, chat_id)

        await bot.edit_message_text('Введите ваш клуб..', user_id, msg_id)

        return

    else: # Иначе к следующему шагу
        async with bot.retrieve_data(user_id, chat_id) as data:
            data['club'] = choose

        markup = create_inline_kb({
            'Открытая': 'game_type_open',
            'Закрытая': 'game_type_close'
        })

        await bot.edit_message_text('Выберите тип игры:', user_id, msg_id, reply_markup=markup)

@bot.message_handler(state=UserAddGame.wait_club, content_types=['text']) # Шаг для ввода своего КЛУБА
async def game_club_choose(message):
    user_id = message.from_user.id
    chat_id = message.chat.id
    club = message.text

    async with bot.retrieve_data(user_id, chat_id) as data:
        data['club'] = club

    await bot.set_state(user_id, UserAddGame.wait, chat_id)

    markup = create_inline_kb({
        'Открытая': 'game_type_open',
        'Закрытая': 'game_type_close'
    })
    
    await bot.send_message(user_id, 'Выберите тип игры:', reply_markup=markup)

@bot.callback_query_handler(func=lambda callback: callback.data.startswith('game_type_')) # Выбор ТИПА ИГРЫ по нажатию кнопки
async def game_type_set_handler(callback):
    user_id = callback.from_user.id
    chat_id = callback.message.chat.id
    choose = callback.data.split('_')[-1]

    async with bot.retrieve_data(user_id, chat_id) as data: # Достаем все данные и записываем их в переменные
        game_date = data['date']
        club, game_type = normalize_data(data['club'], choose)

    await bot.delete_state(user_id, chat_id) # Убираем статус ожидания чего-либо

    await save_game(user_id, game_date, club, game_type) # Сохраняем все данные

    # Сообщаем о успешном сохранении и возвращаемся в меню
    await bot.edit_message_text('Сохранено !', user_id, callback.message.message_id)
    await menu_handler(callback.message)