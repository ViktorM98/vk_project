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


def run_process():
    database_init()
    return read_data()

if __name__ == "__main__":
    run_process()