from telebot import types

def create_inline_kb(buttons: dict, row_width: int = 1) -> types.InlineKeyboardMarkup:
    markup = types.InlineKeyboardMarkup(row_width=row_width)
    kb_buttons = [
        types.InlineKeyboardButton(text=text, callback_data=data)
        for text, data in buttons.items()
    ]
    markup.add(*kb_buttons)
    return markup

def create_inline_kb_to_menu() -> types.InlineKeyboardMarkup:
    markup = types.InlineKeyboardMarkup(row_width=1)
    markup.add(types.InlineKeyboardButton('Назад в меню', callback_data='back_to_menu'))
    return markup