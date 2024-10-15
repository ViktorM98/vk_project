import sqlite3

con = sqlite3.connect("vk.db")
cur = con.cursor()

def database_init():
    cur.execute("""CREATE TABLE IF NOT EXISTS songs (
                           song_id TEXT,
                           music_group TEXT,
                           music_name TEXT,
                           lenght TEXT
            )""")
    
def read_data():
    return cur.execute("""SELECT * FROM songs""").fetchall()

def read_more_data(offset):
    
    return cur.execute(f"""SELECT * FROM songs LIMIT 6 OFFSET {offset}""").fetchall()


def get_data():
    database_init()
    return read_data()

def get_more_data(offset):
    database_init()
    return read_more_data(offset)


if __name__ == "__main__":
    get_data()