from aiogram import types, Dispatcher
from keyboards import adress_kb
from create_bot import dp, bot
from keyboards import kb_client
from database import get_info

async def command_start(message: types.Message):
    await bot.send_message(message.from_user.id, 'Приветсвуем вас в боте Profpoint_mts!', reply_markup=kb_client)

async def command_info(message: types.Message):
    await bot.send_message(message.from_user.id, 'Информацию по оплате уточняйте по телефону.')
    
async def location_request(message: types.Message):
    await bot.send_message(message.from_user.id, 'reply')
    
async def location_give(message: types.Message):
    lat = message.location.latitude
    lon = message.location.longitude
    lat1 = lat-0.1
    lat2 = lat+0.1
    lon1 = lon-0.1
    lon2 = lon+0.1
    reply = get_info(lat1, lat2, lon1, lon2)
    for i in reply:
        await bot.send_message(message.from_user.id, f'{i} : {reply[i]}')

async def take_one(message: types.Message):
    await bot.send_message(message.from_user.id, 'Введите номер проверки:')


def register_handlers_client(dp : Dispatcher):
    dp.register_message_handler(command_start, commands = ['start', 'help'])
    dp.register_message_handler(command_info, commands = ['Оплата'])
    dp.register_message_handler(location_request, commands=['Проверки рядом со мной'])
    dp.register_message_handler(location_give, content_types=["location"])
    dp.register_message_handler(take_one, commands=['Назначить себе проверку'])