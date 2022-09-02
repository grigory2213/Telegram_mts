from aiogram import types, Dispatcher
from create_bot import dp, bot
from keyboards import kb_client

async def command_start(message: types.Message):
    await bot.send_message(message.from_user.id, 'Приветсвуем вас в боте Profpoint_mts!', reply_markup=kb_client)

async def command_info(message: types.Message):
    await bot.send_message(message.from_user.id, 'Информацию по оплате уточняйте по телефону.')


def register_handlers_client(dp : Dispatcher):
    dp.register_message_handler(command_start, commands = ['start', 'help'])
    dp.register_message_handler(command_info, commands = ['Оплата'])