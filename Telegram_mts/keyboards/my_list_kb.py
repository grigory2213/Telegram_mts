from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove

b1 = KeyboardButton('/Заполнить анкету по проверке')
b2 = KeyboardButton('/Снять_себя_с_проверки')

kb_list = ReplyKeyboardMarkup(resize_keyboard=True)

kb_list.add(b1).add(b2)