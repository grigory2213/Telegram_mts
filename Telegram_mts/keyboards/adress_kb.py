from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove

b1 = KeyboardButton('/Назначить')
b2 = KeyboardButton('/Меню')

kb_adress = ReplyKeyboardMarkup(resize_keyboard=True)

kb_adress.add(b1).add(b2)