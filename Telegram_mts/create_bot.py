from aiogram import Bot 
from aiogram.dispatcher import Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage

storage  = MemoryStorage()

bot = Bot(token = "5688739893:AAEx7ai8SXsM4THmnLwm8P9S9P81GoVmO10")
dp  = Dispatcher(bot, storage=storage)