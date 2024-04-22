from telebot import types

async def buttons_creation():
     markup = types.InlineKeyboardMarkup()
     button_a = types.InlineKeyboardButton(text="A", callback_data="A")
     button_b = types.InlineKeyboardButton(text="B", callback_data="B")
     button_c = types.InlineKeyboardButton(text="C", callback_data="C")
     markup.add(button_a, button_b, button_c)
     return markup