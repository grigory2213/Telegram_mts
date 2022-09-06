from typing import Text
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram import types, Dispatcher
from create_bot import  dp
from aiogram.dispatcher.filters import Text

class FSMadmin(StatesGroup):
    photo = State()
    name = State()
    description = State()
    price = State()


#Начинаем диалог загрузки нового пункта меню    
#@dp.message_handler(commands='Загрузить', state=None)
async def cm_start(message : types.Message):
    await FSMadmin.photo.set()
    await message.reply('Загрузи фото')
    
#Ловим первый ответ и пишем в словарь
#@dp.message_handler(content_types = ['photo'], state=FSMadmin.photo)
async def load_photo(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['photo'] = message.photo[0].file_id
    await FSMadmin.next()
    await message.reply('Теперь введи название')

#Ловим второй ответ
#@dp.message_handler(state =FSMadmin.name)
async def load_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['name'] = message.text
    await FSMadmin.next()
    await message.reply('Введи описание')

#Ловим третий ответ 
#@dp.message_handler(state =FSMadmin.description)
async def load_description(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['description'] = message.text
    await FSMadmin.next()
    await message.reply("Теперь укажи цену")

#Ловим четвертый ответ
#@dp.message_handler(state =FSMadmin.price)
async def load_price(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['price'] = float(message.text)
        
    async with state.proxy() as data:
        await message.reply(str(data))
        
        
    await state.finish()

#@dp.message_handler(state="*", commands ='отмена')
#@dp.message_handler(Text(equals='отмена', ignore_case=True), state="*")
async def cancel_handler(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return
    await state.finish()
    await message.reply('OK')    

    
    
def register_handlers_admin(dp : Dispatcher):
    dp.register_message_handler(cm_start, commands = ['Загрузить'], state = None)
    dp.register_message_handler(cancel_handler,Text(equals='отмена', ignore_case=True), state="*")
    dp.register_message_handler(load_photo, content_types=['photo'], state = FSMadmin.photo)
    dp.register_message_handler(load_name, state = FSMadmin.name)
    dp.register_message_handler(load_description, state = FSMadmin.description)
    dp.register_message_handler(load_price, state = FSMadmin.price)