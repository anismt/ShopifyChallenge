import sqlite3
import pdb
import base64

from PIL import Image


conn=sqlite3.connect('picDB.db')
conn.text_factory = str
cursor = conn.cursor()


def create_pic_table():
   cursor.execute("""
   CREATE TABLE IF NOT EXISTS pic_table
   (id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
   name TEXT,
   data TEXT)
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

 

def add_pic(name,data):
   
   cursor.execute("""
   INSERT INTO pic_table (name, data) VALUES (?,?)""", (name, data))
   
   conn.commit()

def add_keyword(name,data,keyword):


   picture_id = cursor.execute("""SELECT id FROM pic_table WHERE name=? and data=?""", [name, data]).fetchone()[0]

   cursor.execute("""
   INSERT INTO keyword_table (keyword, picture_id) VALUES (?,?)""", (keyword, picture_id))

   conn.commit()


def search_table(search_keyword):
   pictures = cursor.execute("""
   SELECT pic_table.data
   FROM pic_table
   INNER JOIN keyword_table
   ON keyword_table.picture_id = pic_table.id
   WHERE keyword_table.keyword = ?
   """,[search_keyword]).fetchall()

   return pictures


def display_pictures(keyword):
   for i in range(0,len(search_table(keyword))):
      img = Image.open(search_table(keyword)[i][0])
      img.show()

if __name__ == "__main__":

   create_pic_table()
   create_keyword_table()
   keyword_list = []

   print("Welcome to the Picture Show! Here you will be able to add pictures, attach keywords to those pictures and then later search for those pictures.")
   print("Let's start off by adding a picture.")

   next_pic = ""
   name = ""
   data = ""
   

   while(next_pic != "n"):

      name = raw_input("What is the name of your picture: ")
      data = raw_input("What is the file name: ")

      add_pic(name,data)

      keyword_list = list(map(str, raw_input("Put in all the keywords: ").split()))

      for i in keyword_list:
         add_keyword(name,data,i)

      next_pic = raw_input("Would you like to add another picture (y/n): ")

      if next_pic == "y":
         continue


   print("Let's search for picture(s) now: ")
   keyword = raw_input("What is a keyword for your picture: ")

   display_pictures(keyword)

   print("Thank you for coming to the Picture Show! Good Day!")

   cursor.close()
   conn.close()
