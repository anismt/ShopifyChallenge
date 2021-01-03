import sqlite3
import pdb

conn=sqlite3.connect('picDB.db')
conn.text_factory = str
cursor = conn.cursor()


def create_pic_table():
   cursor.execute("""
   CREATE TABLE IF NOT EXISTS pic_table
   (id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
   name TEXT,
   data BLOP)
   """)

def create_keyword_table():
   cursor.execute("""
   CREATE TABLE IF NOT EXISTS keyword_table
   (id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
   keyword TEXT,
   picture_id INT,
   FOREIGN KEY (picture_id) REFERENCES pic_table(id))
   """)
 


def add_pic(name,data,keyword):
   
   cursor.execute("""
   INSERT INTO pic_table (name, data) VALUES (?,?)""", (name, data))
 
   picture_id = cursor.execute("""SELECT id FROM pic_table WHERE name=? and data=?""", [name, data]).fetchone()[0]

   cursor.execute("""
   INSERT INTO keyword_table (keyword, picture_id) VALUES (?,?)""", (keyword, picture_id))
 

def search_table():
   cursor.execute("""
   SELECT pic_table.name, pic_table.data
   FROM pic_table
   INNER JOIN keyword_table
   ON keyword_table.picture_id = pic_table.id
   """)

# pdb.set_trace()

create_pic_table()
create_keyword_table()


name = 'Sunflower'
with open('sunflower.jpg','rb') as f:
   data= f.read()
keyword = "flower"

add_pic(name,data,keyword)


search_table()






conn.commit()
cursor.close()
conn.close()
