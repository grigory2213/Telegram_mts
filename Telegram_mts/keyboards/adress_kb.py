from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove

b1 = KeyboardButton('/Назначить')

kb_adress = ReplyKeyboardMarkup(resize_keyboard=True)

kb_adress.add(b1)