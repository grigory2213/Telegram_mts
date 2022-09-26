from aiogram import Bot 
from aiogram.dispatcher import Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage

storage  = MemoryStorage()

bot = Bot(token = "5438493035:AAGoWM_UjtUE8Abnmkt3YjbWmnYGvK5uyv4")
dp  = Dispatcher(bot, storage=storage)