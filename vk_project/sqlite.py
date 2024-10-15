import sqlite3



class vk_db:

    def __init__(self):
        self.start()

    def start(self):
        with sqlite3.connect("vk.db") as con:
            self.c = con.cursor()

            self.c.execute("""CREATE TABLE IF NOT EXISTS songs (
                song_id TEXT PRIMARY KEY,
                song_info TEXT NOT NULL
                           
                length TEXT NOT NULL
            )
""")
            
    def connect_db(self):
        self.db = sqlite3.connect('vk.db')
        
        

    def insert(self,attr1,attr2,attr3):
        # db = sqlite3.connect('vk.db')
        # c = db.cursor()

        self.c.execute(f"INSERT INTO songs VALUES('{attr1}', '{attr2}, '{attr3}')")

        # db.commit()

        # db.close()

    def close_conn(self):
        self.db.commit()
        self.db.close()

#starttest = sqtest()
#starttest.add()

# def starft(self):
#         db = sqlite3.connect('vk.db')
#         cur = db.cursor()

#         cur.execute("""CREATE TABLE IF NOT EXISTS songs (
#             band TEXT PRIMARY KEY NOT NULL,
#             name TEXT NOT NULL          
#         )""")
#         cur.execute(f"INSERT INTO songs VALUES('{self.name}', '{self.name2}')")
#         db.commit()

#         db.close()
#         print("fff")
