import sqlite3
import pdb

conn=sqlite3.connect('picDB.db')
conn.text_factory = str
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS pic_table
(id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
name TEXT,
data BLOP)
""")
 
cursor.execute("""
CREATE TABLE IF NOT EXISTS keyword_table
(id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
keyword TEXT,
picture_id INT,
FOREIGN KEY (picture_id) REFERENCES pic_table(id))
""")
 

name = 'Sunflower'
with open('sunflower.jpg','rb') as f:
   data= f.read()
 
cursor.execute("""
INSERT INTO pic_table (name, data) VALUES (?,?)""", (name, data))
 
keyword = 'flower'

picture_id = cursor.execute("""SELECT id FROM pic_table WHERE name=? and data=?""", [name, data]).fetchone()[0]
# pdb.set_trace()
cursor.execute("""
INSERT INTO keyword_table (keyword, picture_id) VALUES (?,?)""", (keyword, picture_id))
 
search_results = cursor.execute("""
SELECT pic_table.name, pic_table.data
FROM pic_table
INNER JOIN keyword_table
ON keyword_table.picture_id = pic_table.id
""")

# pdb.set_trace()

conn.commit()
cursor.close()
conn.close()
