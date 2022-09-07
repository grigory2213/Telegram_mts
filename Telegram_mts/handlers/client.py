from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher.filters import Text
from create_bot import  dp, bot

from data_base import sqlite_db

from keyboards import kb_client
from keyboards import kb_adress
from keyboards import kb_reg


async def command_menu(message: types.Message):
    await bot.send_message(message.from_user.id, 'Приветсвуем вас в боте Profpoint_mts!', reply_markup=kb_client)

async def command_info(message: types.Message):
    await bot.send_message(message.from_user.id, 'Информацию по оплате уточняйте по телефону.')
    
async def location_request(message: types.Message):
    await bot.send_message(message.from_user.id, 'reply')
    
async def location_give(message: types.Message):
    global reply
    lat = message.location.latitude
    lon = message.location.longitude
    lat1 = lat-0.1
    lat2 = lat+0.1
    lon1 = lon-0.1
    lon2 = lon+0.1
    reply = sqlite_db.get_info(lat1, lat2, lon1, lon2)
    for i in reply:
        await bot.send_message(message.from_user.id, f'{i} : {reply[i]}', reply_markup=kb_adress)

async def take_one(message: types.Message):
    await bot.send_message(message.from_user.id, 'Напишите номер проверки:')


#####################################################РЕГИСТРАЦИЯ################################################

user_id = None

class FSMregistration(StatesGroup):
    name = State()
    surname = State()
    email = State()

async def command_start(message: types.Message):
    global user_id 
    user_id = message.from_user.id
    is_registred = sqlite_db.is_registred(user_id)
    if is_registred != '':
        await bot.send_message(message.from_user.id, f'Добрый день, {is_registred}!', reply_markup=kb_client)
    else:
        await bot.send_message(message.from_user.id, 'Кажется, вы еще не зарегистрированны! Хотите?', reply_markup=kb_reg)
         

#Начинаем диалог регистрации
async def cm_start(message : types.Message):
    await FSMregistration.name.set()
    await message.reply('Напишите свое Имя')
    
#Ловим первый ответ и пишем в словарь
async def getting_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['id'] = message.from_user.id
        data['name'] = message.text
        
    await FSMregistration.next()
    await message.reply('Теперь напишите свою Фамилию')

#Ловим второй ответ
async def getting_surname(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['surname'] = message.text
    await FSMregistration.next()
    await message.reply('Введите ваш email')

#Ловим третий ответ 
async def getting_email(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['email'] = message.text
        
    await sqlite_db.sql_add_commend(state)    
        
    await state.finish()

#@dp.message_handler(state="*", commands ='отмена')
async def cancel_handler(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return
    await state.finish()
    await message.reply('OK')    



def register_handlers_client(dp : Dispatcher):
    dp.register_message_handler(command_start, commands = ['start', 'help'])
    dp.register_message_handler(command_menu, commands = ['Меню'])
    dp.register_message_handler(command_info, commands = ['Оплата'])
    dp.register_message_handler(location_request, commands=['Проверки рядом со мной'])
    dp.register_message_handler(location_give, content_types=["location"])
    dp.register_message_handler(take_one, commands=['Назначить'])
    
def register_handlers_registration(dp : Dispatcher):
    dp.register_message_handler(cm_start, commands = ['Регистрация'], state = None)
    dp.register_message_handler(cancel_handler,Text(equals='отмена', ignore_case=True), state="*")
    dp.register_message_handler(getting_name, state = FSMregistration.name)
    dp.register_message_handler(getting_surname, state = FSMregistration.surname)
    dp.register_message_handler(getting_email, state = FSMregistration.email)