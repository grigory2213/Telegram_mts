import sqlite3 as sq
global base, cur

def sql_start():
    global base, cur
    base = sq.connect('mts_adress.db')
    cur = base.cursor()
    if base:
        print('Data base connected OK!')
    base.execute('CREATE TABLE IF NOT EXISTS users(id INTEGER NOT NULL, name TEXT, surname TEXT, email TEXT)')
    base.commit
    
def is_registred(user_id):
    global base, cur
    name = '' 
    result = base.execute("SELECT EXISTS (SELECT * FROM users WHERE id = (?))", (user_id,))
    responce = result.fetchone()[0]
    print(responce)
    if responce != 0:
        result = base.execute("SELECT * FROM users WHERE id = (?)", (user_id,))
        responce = result.fetchone()
        print(responce)
        name = responce[1]
    return name

    
async def sql_add_commend(state):
    async with state.proxy() as data:
        cur.execute("INSERT INTO users VALUES(?,?,?,?)", tuple(data.values()))
        base.commit()


    
def get_info(latitude1, latitude2, longitude1, longitude2):
    cur.execute("SELECT * FROM mts_adress WHERE latitude BETWEEN (?) AND (?) AND longitude BETWEEN (?) AND (?)", (latitude1, latitude2, longitude1, longitude2))
    items = cur.fetchall()
    adress_dict = {}
    for item in items:
         id = item[0]
         adress = item[4]
         adress_dict[id] = adress
         
         
    print("Command executed succesfully!")
    base.commit()
    
    return adress_dict
