
import time
from threading import Thread

import pygame
from mutagen.mp3 import MP3

class Player:
    parent= None
    current_song_length=0 # song length
    current_song_position=0 # song time updated every second
    paused_status= False
    seek_time=40 # time for forwarding in seconds
    start=0
    def __init__(self):
        pygame.init()
        self.myplayer = pygame.mixer
        self.myplayer.init()

    def play_media (self):
        try:
            self.source = self.parent.current_track
            self.myplayer.music.load(self.source)
            self.myplayer.music.play()
        except:
            pass

    def start_play_thread(self):
        """starting thread for each song"""
        player_thread = Thread(target=self.play_media)
        player_thread.start()
        time.sleep(0.2)
        
    def stop_song(self):
        try:
            self.myplayer.music.stop()
        except:
            pass
        
    def pause_song(self):
        self.myplayer.music.pause()

    def unpause_song(self):
        self.myplayer.music.unpause()
            

    def ffw_song(self):
        # TODO here to figure it out how to solve it
        global current_time
        current_time= int(self.myplayer.music.get_pos()/1000)
        print(current_time)
        self.myplayer.music.rewind()
        self.myplayer.music.play(start=current_time+30)
        
        
    def ffback_song(self):
        #TODO here to figure it out how to solve it
        current_time=self.myplayer.music.get_pos()
        self.myplayer.music.set_pos(current_time-self.seek_time)

    def set_volume(self,value):
        """setting player volume and mute / unmute methods"""
        try:
            self.myplayer.music.set_volume(value)
        except:
            pass

    def song_lenght_time(self):
        """return the total song length"""
        try:
            file = MP3(self.source)
            current_song_length = file.info.length
        except:
            current_song_length = 0
        return current_song_length

    def sample_rate(self):
        try:
            file = MP3(self.source)
            rate= file.info.mode
            print(rate)
        except:
            rate=0
        
    
    def actual_song_position(self):
        """return actual time position for music wich is played"""
        try:
            self.current_song_position = self.myplayer.music.get_pos()
            self.current_song_position = round(self.current_song_position/1000,0)
            # print(self.current_song_position)
        except:
            self.current_song_position = 0
        return self.current_song_position
        

if __name__ == '__main__':
    print('a pyglet player class implementation')