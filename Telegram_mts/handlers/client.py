
from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher.filters import Text
from create_bot import  dp, bot

from data_base import sqlite_db

from keyboards import kb_client
from keyboards import kb_adress
from keyboards import kb_reg, kb_list


async def command_menu(message: types.Message):
    await bot.send_message(message.from_user.id, 'Приветсвуем вас в боте Profpoint_mts!', reply_markup=kb_client)
    
async def command_info(message: types.Message):
    await bot.send_message(message.from_user.id, '''
    Приветствуем вас в боте Profpoint_mts! Бот позволяет найти ближайшие свободные проверки и назначить себя на их выполнение.
Для того, что бы бот работал корректно - используйте предлагаемые варианты ответов или комманды /start(для возврата к началу) или отмена(для отмены предыдущих действий).
                           
Рекомендуем использовать смартфон или планшет, для того, что бы бот мог предлагать вам ближайшие к вам адреса.
После того, как вы выберите проверки, которые планируете выполнить - они зарезервируются за вами на 48 часов.
Вы можете снять с себя проверку, но не более 3х раз. Если вы не выполните проверки в течении 48 часов и не отмните их до истечения этого времени - вы будете забанены.
                           
После выполнения закрепленной за вами проверки - вы можете заполнить анкету прямо в боте. Если вы делаете это со смартфона - убедитесь, что записи с диктофона сохранены как файл(на айфон).
                            
Если у вас остались вопросы по работе бота - свяжитесь с нами по команде /Поддержка.
                           
Спасибо! И желаем Удачи.
    ''', reply_markup=kb_client)
    await message.reply_document('BQACAgIAAxkBAAIGy2MkP3jei5iO869ZNqQnOvSSfMDrAAL3IAACWvUpSUPM9QfkM4EuKQQ')
    await message.reply_document('BQACAgIAAxkBAAIGh2MkNgpLF9ARx_JUR_-P4NUgXnW0AALFIAACWvUpScOeJyNT06GOKQQ')
    
    
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
        
class FSMassignation(StatesGroup):
    number_state = State()

async def take_one(message: types.Message):
    await FSMassignation.number_state.set()
    await message.reply('Напишите номер проверки:')
    
#Ловим первый ответ и пишем в словарь
async def number(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    number = int(message.text)
        
    result =  sqlite_db.sql_add_number(user_id, number)    
    await message.reply(result, reply_markup=kb_client)    
    await state.finish()


async def test(message: types.Message):
    global user_id
    user_id = message.from_user.id
    # print(user_id)
    reply1 = sqlite_db.get_mylist(user_id)
    # print(reply1)
    if len(reply1) == 0:
        await bot.send_message(message.from_user.id, 'Вы не назначены ни на одну проверку', reply_markup=kb_client)
    else:    
        await bot.send_message(message.from_user.id, 'Вы назначены на следующие проверки: ', reply_markup=kb_list)
        for i in reply1:
            await bot.send_message(message.from_user.id, f'{i} : {reply1[i]}')

class FSMremove(StatesGroup):
    number_state = State()

async def remove(message: types.Message):
    await FSMremove.number_state.set()
    await message.reply('Напишите номер проверки, от которой хотите отказаться:')
    
    
#Ловим ответ и удаляем проверку у пользователя
async def remove_number(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    number = int(message.text)
        
    result =  sqlite_db.sql_remove_number(user_id, number)    
    await message.reply(result, reply_markup=kb_client)    
    await state.finish()




#####################################################РЕГИСТРАЦИЯ#########################################################

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
    await message.reply('Спасибо! Теперь вы заргистрированы', reply_markup=kb_client)    
    await state.finish()

#@dp.message_handler(state="*", commands ='отмена')
async def cancel_handler(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return
    await state.finish()
    await message.reply('OK')    


#####################################################ЗАПОЛНЕНИЕ_АНКЕТЫ#########################################################

class FSMfilling(StatesGroup):
    number = State()
    date = State()
    time = State()
    audio = State()
    photo = State()

async def command_fill(message: types.Message):
    await FSMfilling.number.set()
    await message.reply('Напишите номер проверки:')
         
#Ловим первый ответ и пишем в словарь
async def getting_number(message: types.Message, state: FSMfilling):
    async with state.proxy() as data_check:
        data_check['user_id'] = message.from_user.id
        data_check['number'] = int(message.text)
        
    await FSMfilling.next()
    await message.reply('Дата проверки. Формат 12.12.2022.')

#Ловим второй ответ
async def getting_date(message: types.Message, state: FSMfilling):
    async with state.proxy() as data_check:
        data_check['date'] = message.text
    await FSMfilling.next()
    await message.reply('Время проверки. Формат 17:30')

#Ловим третий ответ
async def getting_time(message: types.Message, state: FSMfilling):
    async with state.proxy() as data_check:
        data_check['time'] = message.text
    await FSMfilling.next()
    await message.reply('Прикрепите аудиофайл проверки.')
    
#Ловим четвертый ответ
async def getting_audio(message: types.Message, state: FSMfilling):
    async with state.proxy() as data_check:
        data_check['audio'] = message.audio.file_id
    await FSMfilling.next()
    await message.reply('Прикрепите фото зала.')
    
#Ловим пятый ответ 
async def getting_photo(message: types.Message, state: FSMfilling):
    async with state.proxy() as data_check:
        data_check['photo'] = message.photo[0].file_id
    await sqlite_db.sql_add_check(state)    
    await message.reply(f'Спасибо! Анкета {data_check["number"]} -- заполнена!', reply_markup=kb_client)    
    await state.finish()

#@dp.message_handler(state="*", commands ='отмена')
async def cancel_handler(message: types.Message, state: FSMfilling):
    current_state = await state.get_state()
    if current_state is None:
        return
    await state.finish()
    await message.reply('OK') 
    
async def scan_message(message: types.Message):
    document_id = message.document.file_id
    file_info = await bot.get_file(document_id)
    print(f'file_id: {file_info.file_id}')
    print(f'file_path: {file_info.file_path}')
    print(f'file_size: {file_info.file_size}')
    print(f'file_unique_id: {file_info.file_unique_id}')


def register_handlers_client(dp : Dispatcher):
    dp.register_message_handler(command_start, commands = ['start', 'help'])
    dp.register_message_handler(command_menu, commands = ['Меню'])
    dp.register_message_handler(scan_message, content_types=['document'])
    dp.register_message_handler(test, commands = ['Мои_проверки'])
    dp.register_message_handler(command_info, commands = ['Инструкция'])
    dp.register_message_handler(location_request, commands=['Проверки рядом со мной'])
    dp.register_message_handler(location_give, content_types=["location"])
    
    dp.register_message_handler(take_one, commands=['Назначить'], state = None)
    dp.register_message_handler(number, state = FSMassignation.number_state)
    dp.register_message_handler(remove, commands=['Снять_себя_с_проверки'], state = None)
    dp.register_message_handler(remove_number, state = FSMremove.number_state)
    
    dp.register_message_handler(command_fill, commands = ['Заполнить_анкету'], state = None)
    dp.register_message_handler(cancel_handler,Text(equals='отмена', ignore_case=True), state="*")
    dp.register_message_handler(getting_number, state = FSMfilling.number)
    dp.register_message_handler(getting_date, state = FSMfilling.date)
    dp.register_message_handler(getting_time, state = FSMfilling.time)
    dp.register_message_handler(getting_audio, content_types=['audio'], state = FSMfilling.audio)
    dp.register_message_handler(getting_photo, content_types=['photo'], state = FSMfilling.photo)
    
def register_handlers_registration(dp : Dispatcher):
    dp.register_message_handler(cm_start, commands = ['Регистрация'], state = None)
    dp.register_message_handler(cancel_handler,Text(equals='отмена', ignore_case=True), state="*")
    dp.register_message_handler(getting_name, state = FSMregistration.name)
    dp.register_message_handler(getting_surname, state = FSMregistration.surname)
    dp.register_message_handler(getting_email, state = FSMregistration.email)