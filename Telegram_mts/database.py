import sqlite3

# Получаем информацию по unique_id
def get_info(unique_id):
    conn = sqlite3.connect('mts_adress.db')
    c = conn.cursor()
    c.execute("SELECT * FROM mts_adress WHERE unique_id LIKE (?)", (unique_id,))
    items = c.fetchall()
    for item in items:
         print(item) 
    print("Command executed succesfully!")
    conn.commit()
    conn.close()
    