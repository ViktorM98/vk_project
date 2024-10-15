import sqlite3
attr1 = 'hyunfdfya'
attr2 = 'hayffa'
attr3 = 'vfdfc'
# with sqlite3.connect("some.db") as con:
#     c = con.cursor()

#     c.execute("""CREATE TABLE IF NOT EXISTS songs (
#               song_id TEXT,
#               song_info TEXT,
#               lenght TEXT
#     )""")
    

#     c.execute("INSERT INTO songs VALUES(?,?,?)",(attr1,attr2,attr3))

con = sqlite3.connect("some.db")
c = con.cursor()
try:
    c.execute("BEGIN")
    c.execute("INSERT INTO songs VALUES(?,?,?)",(attr1,attr2,attr3))

    c.execute("COMMIT")
except:
    c.execute("ROLLBACK")

c.close()
