import sqlite3 as sq
from urllib import response

global base, cur

#Создаем базу данных с пользователями, если ее не существует
def sql_start():
    global base, cur
    base = sq.connect('mts_adress.db')
    cur = base.cursor()
    if base:
        print('Data base connected OK!')
    base.execute('CREATE TABLE IF NOT EXISTS users(id INTEGER NOT NULL, name TEXT, surname TEXT, email TEXT)')
    base.commit
    
# Проверяем, зарегистрирован ли пользователь    
def is_registred(user_id):
    global base, cur
    name = '' 
    result = base.execute("SELECT EXISTS (SELECT * FROM users WHERE id = (?))", (user_id,))
    responce = result.fetchone()[0]
    # print(responce)
    if responce != 0:
        result = base.execute("SELECT * FROM users WHERE id = (?)", (user_id,))
        responce = result.fetchone()
        # print(responce)
        name = responce[1]
    return name

    
async def sql_add_commend(state):
    global base, cur
    async with state.proxy() as data:
        cur.execute("INSERT INTO users VALUES(?,?,?,?)", tuple(data.values()))
        base.commit()

async def sql_add_check(state):
    global base, cur
    async with state.proxy() as data:
        list = tuple(data.values())
        cur.execute("INSERT INTO proverka VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)", tuple(data.values()))
        cur.execute("UPDATE mts_adress SET done = (?) WHERE unique_id = (?)", (list[0], list[1],))
        cur.execute("UPDATE mts_adress SET assigned = 0 WHERE unique_id = (?)", (list[1],))
        base.commit()

def sql_add_number(user_id, number):
    global base, cur
    cur.execute("SELECT * FROM mts_adress WHERE unique_id = (?)", (number,))
    items = cur.fetchall()
    if items == '':
        otvet = 'Точки с таким id не существует'
    else:
        cur.execute("UPDATE mts_adress SET assigned = (?) WHERE unique_id = (?)", (user_id, number,))
        otvet = f'Вы назначены на проверку точки {number}. Пожалуйста выполните проверку в течении 48 часов.'
    base.commit()
    return otvet
    
def sql_remove_number(user_id, number):
    global base, cur
    cur.execute("SELECT * FROM mts_adress WHERE unique_id = (?) AND assigned = (?)", (number, user_id,))
    items = cur.fetchall()
    if items == '':
        otvet = 'Точки с таким id не существует'
    else:
        cur.execute("UPDATE mts_adress SET assigned = 0 WHERE unique_id = (?)", (number,))
        otvet = 'Вы отменили проверку'
    base.commit()
    return otvet


def get_mylist(user_id):
    global base, cur
    cur.execute("SELECT * FROM mts_adress WHERE assigned = (?)", (user_id,))
    items = cur.fetchall()
    adress_dict = {}
    for item in items:
         id = item[0]
         adress = item[4]
         adress_dict[id] = adress
    base.commit()
    return adress_dict
    
    
def get_info(latitude1, latitude2, longitude1, longitude2):
    cur.execute("SELECT * FROM mts_adress WHERE latitude BETWEEN (?) AND (?) AND longitude BETWEEN (?) AND (?) AND assigned = 0 AND done = 0", (latitude1, latitude2, longitude1, longitude2))
    items = cur.fetchall()
    adress_dict = {}
    for item in items:
         id = item[0]
         adress = item[4]
         adress_dict[id] = adress
         
    if adress_dict == '':
        reply = 'Рядом с вами нет свободных проверок.'
    else:
        reply = adress_dict
         
         
    print("Command executed succesfully!")
    base.commit()
    
    return reply
