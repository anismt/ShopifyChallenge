import sqlite3


conn=sqlite3.connect('image.db')
conn.text_factory = str
cursor = conn.cursor()

m = cursor.execute("""

SELECT * FROM my_table
""")

for x in m:
    print(x[2])
    rec_data = x[2]

with open('moon.jpg','wb') as f:
    f.write(rec_data)


conn.commit()

cursor.close()

conn.close()
