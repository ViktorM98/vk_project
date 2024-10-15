import sqlite3
import database_connector as db_connector
conn = sqlite3.connect(':memory:')
cursor = conn.cursor()

def memory_database_init():

    cursor.execute("""CREATE TABLE IF NOT EXISTS songs (
                            song_id TEXT,
                            music_group TEXT,
                            music_name TEXT,
                            lenght TEXT
                )""")
# Подключение, создание бд из вк на сервере

def read_more_data(offset):

    cursor.execute(f"SELECT * FROM songs LIMIT 6 OFFSET {offset}")
    rows = cursor.fetchall()
    return rows

def add_data(data):
    for song in data:
         cursor.execute("INSERT INTO songs VALUES(?,?,?,?)",(song[0],song[1],song[2],song[3] ))
         print("memory_database файл, add_data:", song)
    conn.commit()
    print("data successfully added to mem. database")
