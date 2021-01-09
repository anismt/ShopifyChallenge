import sqlite3
import pdb
import base64
import os


from PIL import Image


conn=sqlite3.connect('picDB.db')
conn.text_factory = str
cursor = conn.cursor()

def create_pic_table():
   cursor.execute("""
   CREATE TABLE IF NOT EXISTS pic_table
   (id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
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

def add_pic(data):
   cursor.execute("""
   INSERT INTO pic_table (data) VALUES (?)""", [data])
   conn.commit()

def add_folder_of_pics(folder):

   for pic in os.listdir(folder):

      if pic == ".DS_Store":
         continue

      data = pic   
      keyword = raw_input("Lets add a keyword to the photo " + data + ": ")

      final_data = folder + "/" + data
      
      add_pic(final_data)
      add_keyword(final_data,keyword)


      conn.commit()

def add_keyword(data,keyword):

   picture_id = cursor.execute("""SELECT id FROM pic_table WHERE data=?""", [data]).fetchone()[0]

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

def pic_table_length():
   tab_len = cursor.execute("""
   SELECT pic_table.data
   FROM pic_table
   """)
   lis = []

   for x in tab_len:
      lis.append(x[0])

   conn.commit()
   return lis

def keyword_table_length():
   tab_len = cursor.execute("""
   SELECT keyword_table.keyword
   FROM keyword_table
   """)
   
   lis = []
   
   for x in tab_len:
      lis.append(x[0])
   
   conn.commit()
   return lis


def display_pictures(keyword):
   
   for i in range(0,len(search_table(keyword))):
   
      img = Image.open(search_table(keyword)[i][0])
      img.show()

def display_specific_pic(pic_id):
   img = Image.open(pic_id)
   img.show()

if __name__ == "__main__":

   create_pic_table()
   create_keyword_table()
   keyword_list = []


   # print("Welcome to the Picture Show! Here you will be able to add pictures, attach keywords to those pictures and then later search for those pictures.")

   next_pic = ""
   data = ""
   choice = ""
   what_pic = ""

   while(choice != "e"):
      choice = raw_input("Type s - search, a - add picture, f - add folder of pictures, k - adding more keywords or e to exit: ").lower()

      if choice == "s":
         
         if len(pic_table_length()) == 0:
            print("There are no pictures in the database to search from!")
         else:
            keyword = raw_input("What is a keyword for your picture(s) (Yellow): ")

            if keyword not in keyword_table_length():
               print("There are no pictures with " + keyword + " as their keywords!")
            else:
               if len(search_table(keyword)) == 1:
                  display_specific_pic(keyword)
               else:
                  for i in range(0,len(search_table(keyword))):
                     print(search_table(keyword)[i][0])
                  while(what_pic != "all" or what_pic != "d"):
                     what_pic = raw_input("What picture would you like to open, type all for all photos:, or d for done: ").lower()
                     if what_pic != "all":
                        display_specific_pic(what_pic)
                  if what_pic == "all":
                     display_pictures(keyword)
      if choice == "a":

         data = raw_input("What is the photo file name path (e.g. sunflower.jpg, PicFolder/moon.jpg): ")
         if data in pic_table_length():
            print("This picture is already in the database!")
         else:
            add_pic(data)
            keyword = raw_input("Lets add a keyword to the photo " + data + ": ")
            add_keyword(data,keyword)
         
      if choice == "k":
         if len(pic_table_length()) == 0:
            print("There are no pictures to add keywords to!")
         else:
            print(pic_table_length())
            data = raw_input("What is the photo path, select from above (e.g. sunflower.jpg, PicFolder/moon.jpg): ")
            if data not in pic_table_length():
               print("There are no pictures like " + data + " in the database!")
            else:
               keyword_list = list(map(str, raw_input("Put in all the keywords seperated by a space (for moon.jpg - Lune Round White) : ").split()))         
               for i in keyword_list:
                  add_keyword(data,i)

      if choice == "f":
         folder = raw_input("What is the pathway to your folder: ")
         add_folder_of_pics(folder)   
   print("Thank you for coming to the Picture Show! Good Day!")

   cursor.close()
   conn.close()