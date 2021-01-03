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
   conn.commit()


def create_keyword_table():
   cursor.execute("""
   CREATE TABLE IF NOT EXISTS keyword_table
   (id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
   keyword TEXT,
   picture_id INT,
   FOREIGN KEY (picture_id) REFERENCES pic_table(id))
   """)
   conn.commit()

 

def add_pic(name,data,keyword):
   
   cursor.execute("""
   INSERT INTO pic_table (name, data) VALUES (?,?)""", (name, data))
 
   picture_id = cursor.execute("""SELECT id FROM pic_table WHERE name=? and data=?""", [name, data]).fetchone()[0]

   cursor.execute("""
   INSERT INTO keyword_table (keyword, picture_id) VALUES (?,?)""", (keyword, picture_id))
   
   conn.commit()


def search_table(search_keyword):
   name_and_pictures = cursor.execute("""
   SELECT pic_table.name, pic_table.data
   FROM pic_table
   INNER JOIN keyword_table
   ON keyword_table.picture_id = pic_table.id
   WHERE keyword_table.keyword = ?
   """,[search_keyword]).fetchall()

   return name_and_pictures


def get_data_for_picture(file_name):
   with open(file_name,'rb') as f:
      data = f.read()

   return data


if __name__ == "__main__":
   create_pic_table()
   create_keyword_table()

   name = 'Sunflower'
   data = get_data_for_picture("sunflower.jpg")
   keyword = "flower"

   add_pic(name, data, keyword)


   print search_table("flower")[0]

   cursor.close()
   conn.close()
