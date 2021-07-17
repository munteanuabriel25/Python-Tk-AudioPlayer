
import sqlite3
import os
from mutagen.mp3 import MP3

class Database:
    timepattern = "{0:02d}:{1:02d}"
    
    def __init__(self, db):
        """create a connection to database. If Table does not exists it creates one"""
        self.db=db
        self.connect=sqlite3.connect(self.db) # connecting to database
        self.cursor= self.connect.cursor()
        self.cursor.execute("CREATE TABLE IF NOT EXISTS playlist (id INT PRIMARY KEY, song_name text, song_path text, duration text) ")
        self.check_database_files()
        self.connect.commit()
        
    def check_database_files(self):
        """when program starts is checking if some file where moved from initial location. If finds one, then removes it"""
        self.cursor.execute("SELECT song_path FROM playlist")
        result = self.cursor.fetchall()
        broken_paths=[] # path that dont longer exists into the same directory
        for path in result:
            if not os.path.exists(path[0]):
                broken_paths.append(path[0])
        if broken_paths != []: # remove entire line from databse according to given path
            for path in broken_paths:
                self.remove_song(path)
        self.connect.commit()
        
    def return_path(self,primary_key):
        """returning path song  afther quering from main app index number """
        self.cursor.execute("SELECT song_path FROM playlist WHERE id=?",(primary_key,))
        path=""
        for letter in self.cursor.fetchone()[0]: # setting the plath to the correct output "//"
            if letter == "/":
                path += "\\"
            else:
                path += letter
        return path
        
    def insert_song(self, path):
        """adding a song into playlist, not allowing duplicates"""
        song_name = os.path.basename(path)
        song_name = song_name
        file = MP3(path)
        current_time = file.info.length
        currtimemin = int(current_time / 60)
        currtimesec = int(current_time % 60)
        currtimestrng = self.timepattern.format(currtimemin, currtimesec)
        self.cursor.execute("SELECT song_name FROM  playlist WHERE song_name =?",(song_name,))
        if len(self.cursor.fetchall()) == 0:
            self.cursor.execute("INSERT INTO playlist VALUES(NULL, ?,?,?)",(song_name,path,currtimestrng))
            self.connect.commit()

    
    def fetch_data(self):
        """returning a row with all objects from database"""
        self.cursor.execute("SELECT * FROM playlist")
        rows = self.cursor.fetchall()
        return rows




    def search_song(self, string):
        result_list=[]
        string= string.lower()
        self.cursor.execute("SELECT song_name, id  FROM  playlist" )
        all_songs= self.cursor.fetchall()
        
        for result in all_songs:
            result_1 = result[0].lower()
            if string in result_1:
                result_list.append((result[1],result_1))
        return result_list
        
    def remove_song(self, path):
        self.cursor.execute("DELETE FROM playlist WHERE song_path=?", (path,))
        self.connect.commit()
        
    def empty_database(self):
        """cleans all informations stored into database"""
        self.cursor.execute("DELETE FROM playlist")
        self.connect.commit()
        
    def close_database(self):
        """closing connection to database"""
        self.connect.close()
        
# data=Database("playlist.db")
# data.search_song("body")
