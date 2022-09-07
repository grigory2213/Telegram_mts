import sqlite3
import pandas as pd

df_adress = pd.read_excel('/Users/user/Desktop/Work/API_profpoint/Telegram_mts/mts_data.xlsx')

# Обработка первоначального файла
df_adress = df_adress.drop(['Бренд ОП', 'Формат салона', 'Юр.лицо', 'Легенда для проверки', 'Предмет для консультации', 'Нас.пункт признак'], axis = 1)
df_adress = df_adress.rename(columns={"Код ОП": "unique_id", "Дивизион МТС": "devision", "Область":"region", "Населённый пункт название": "city", "Адрес Офиса продаж":"adress", "GPS координаты. широта":"latitude", "GPS координаты. долгота":"longitude", "Режим работы":"work_time", "Тип строения":"building"})

#Подключаемся к базе данных mts_adress
conn = sqlite3.connect('mts_adress.db')
c = conn.cursor()

#Создаем табличку с адресами
c.execute(
    """
    CREATE TABLE IF NOT EXISTS mts_adress (
       unique_id INTEGER NOT NULL,
       devision TEXTa,
       region TEXT, 
       city TEXT,
       adress TEXT,
       latitude REAL, 
       longitude REAL,
       work_time TEXT,
       building TEXT,
       PRIMARY KEY(unique_id)
        )
   """
)

#Передаем в таблицу данные из экселевского файла
df_adress.to_sql('mts_adress', conn, if_exists='append', index=False)

conn.commit()

conn.close()