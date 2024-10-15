import sqlite3 

connection = sqlite3.connect("DB.db")

cursor = connection.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS some_db(
               nana TEXT PRIMARY KEY,
               haha TEXT PRIMARY KEY
               
)""")