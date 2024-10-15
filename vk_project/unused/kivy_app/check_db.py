import sqlite3

with sqlite3.connect("vk.db") as con:
    c = con.cursor()
    c.execute("DROP TABLE songs")