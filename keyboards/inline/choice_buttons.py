from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from config import categories
from keyboards.inline.callback_datas import cat_callback

menu = InlineKeyboardMarkup(row_width=1)
buttons = [InlineKeyboardButton(text=el, callback_data=cat_callback.new(cat_text=el)) for el in categories]
for el in buttons:
    menu.insert(el)

return_button = InlineKeyboardButton(text="Вернуться назад", callback_data="cancel")
menu.add(return_button)