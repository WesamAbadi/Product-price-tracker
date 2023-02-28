
import sqlite3

con = sqlite3.connect('trcker.db')
cur = con.cursor()

cur.execute('''CREATE TABLE IF NOT EXISTS trackers
                    (site text, price real)''')

cur.execute('''INSERT INTO trackers VALUES
                    ('shoe2', '30')''')

con.commit()

for row in cur.execute('''SELECT * FROM trackers'''):
    print(row)