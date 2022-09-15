from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove

b1 = KeyboardButton('/Инструкция')
b2 = KeyboardButton('/Проверки рядом со мной', request_location=True)
b3 = KeyboardButton('/Мои_проверки')

kb_client = ReplyKeyboardMarkup(resize_keyboard=True)

kb_client.row(b3, b1).add(b2)