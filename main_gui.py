#! python3
# this is main GUI window for audio player

import tkinter as tk
from tkinter import filedialog
import player
import database
import os
import psutil
import random
import time
from threading import Thread
import multiprocessing
import search




class GUI:

    volume=50  # initial volume when program start and then keeps the actual volume refference
    current_track=""
    timepattern = "{0:02d}:{1:02d}" # time pattern for clock display
    max_lines_playlist=27  # maximum lines to show into playlist
    index_playing=None
    colors_list = ['#A9A9A9', '#9AAEB0', '#8AB2B8', '#7BB7BF', '#6CBCC6', '#5CC0CD', '#4DC5D5',
                   '#3DC9DC', '#2ECEE3', '#1FD3EA', '#0FD7F2', '#00DCF9'] # sequence for eq color bars from bottom to up
    thread_list=[]
    
    def __init__(self, player, database):
        self.player = player
        self.db = database
        player.parent=self
        self.root=tk.Tk()
        self.root.resizable(False,False)
        # self.root.overrideredirect("True") # hide main window top right buttons
        self.root.title("Audio Player 1.0")
        self.root.attributes('-alpha', 1)
        self.root.geometry("490x780+500+200")
        self.root.configure(background="#D1D3D4") #"#4D5151"
        self.create_console_frame()
        self.create_playlist_frame()
        # self.create_eq_display()
        
        self.root.mainloop()
        

    def check_baterry_status(self):
        battery = psutil.sensors_battery()
        if battery.power_plugged:
            self.battery_status=13
        else:
            self.battery_status = battery.percent * 0.13
        return self.battery_status
        
    def create_console_frame(self):
        self.repeat_status= tk.BooleanVar()
        self.shuffle_status= tk.BooleanVar()
        self.autoplay_status= tk.BooleanVar()
        self.battery_status= tk.IntVar()
        self.mute_status= tk.IntVar()
        self.eq_status=tk.BooleanVar()
        self.eq_status.set(False)
        self.paused_status=tk.BooleanVar()
        self.paused_status.set(False)
        self.show_eq_animation=tk.BooleanVar() # with this variable control the anination from top right corner. EQ animation
        self.show_eq_animation.set(False)
        
        
        frame=tk.Frame(self.root, width=490, height=220,bd=0)
        
        self.autoplay_icon= tk.PhotoImage(file="Icons\\autoplay_icon.gif")
        self.repeat_icon= tk.PhotoImage(file="Icons\\repeat_icon.gif")
        self.eq_icon = tk.PhotoImage(file="Icons\\eq_icon.gif")
        self.shuffle_icon = tk.PhotoImage(file="Icons\\shuffle_icon.gif")
        self.frame_bg_icon = tk.PhotoImage(file="Icons\\console_bg_icon.gif")
        self.autoplay_over_icon = tk.PhotoImage(file="Icons\\autoplay_over_icon.gif")
        self.repeat_over_icon= tk.PhotoImage(file="Icons\\repeat_over_icon.gif")
        self.eq_over_icon = tk.PhotoImage(file="Icons\\eq_over_icon.gif")
        self.shuffle_over_icon = tk.PhotoImage(file="Icons\\shuffle_over_icon.gif")
        self.eq_on_icon = tk.PhotoImage(file="Icons\\eq_on_icon.gif")
        self.eq_off_icon = tk.PhotoImage(file="Icons\\eq_off_icon.gif")
        self.autoplay_on_icon = tk.PhotoImage(file="Icons\\autoplay_on_icon.gif")
        self.autoplay_off_icon = tk.PhotoImage(file="Icons\\autoplay_off_icon.gif")
        self.shuffle_on_icon = tk.PhotoImage(file="Icons\\shuffle_on_icon.gif")
        self.shuffle_off_icon = tk.PhotoImage(file="Icons\\shuffle_off_icon.gif")
        self.repeat_on_icon = tk.PhotoImage(file="Icons\\repeat_on_icon.gif")
        self.repeat_off_icon = tk.PhotoImage(file="Icons\\repeat_off_icon.gif")
        self.mute_off_icon = tk.PhotoImage(file="Icons\\mute_off_icon.gif")
        self.mute_on_icon = tk.PhotoImage(file="Icons\\mute_on_icon.gif")
        self.wireless_on_icon = tk.PhotoImage(file="Icons\\wireless_on_icon.gif")
        self.wireless_off_icon = tk.PhotoImage(file="Icons\\wireless_off_icon.gif")
        self.database_on_icon = tk.PhotoImage(file="Icons\\database_on_icon.gif")
        self.database_off_icon = tk.PhotoImage(file="Icons\\database_off_icon.gif")
        self.play_status_icon=tk.PhotoImage(file="Icons\\play_status_icon.png")
        self.stop_status_icon=tk.PhotoImage(file="Icons\\stop_status_icon.png")
        self.pause_status_icon=tk.PhotoImage(file="Icons\\pause_status_icon.png")
        
        self.prev_icon = tk.PhotoImage(file="Icons\\prev_icon.gif")
        self.ffback_icon = tk.PhotoImage(file="Icons\\ffback_icon.gif")
        self.play_icon = tk.PhotoImage(file="Icons\\play_icon.gif")
        self.pause_icon = tk.PhotoImage(file="Icons\\pause_icon.gif")
        self.stop_icon = tk.PhotoImage(file="Icons\\stop_icon.gif")
        self.ffw_icon = tk.PhotoImage(file="Icons\\ffw_icon.gif")
        self.next_icon = tk.PhotoImage(file="Icons\\next_icon.gif")

        self.mute_icon = tk.PhotoImage(file="Icons\\mute_icon.gif")
        self.unmute_icon = tk.PhotoImage(file="Icons\\unmute_icon.gif")
        self.vol_down_icon = tk.PhotoImage(file="Icons\\vol_down_icon.gif")
        self.vol_up_icon = tk.PhotoImage(file="Icons\\vol_up_icon.gif")
        self.close_icon = tk.PhotoImage(file="Icons\\close_icon.gif")
        
        self.prev_over_icon = tk.PhotoImage(file="Icons\\prev_over_icon.gif")
        self.ffback_over_icon = tk.PhotoImage(file="Icons\\ffback_over_icon.gif")
        self.play_over_icon = tk.PhotoImage(file="Icons\\play_over_icon.gif")
        self.pause_over_icon = tk.PhotoImage(file="Icons\\pause_over_icon.gif")
        self.stop_over_icon = tk.PhotoImage(file="Icons\\stop_over_icon.gif")
        self.ffw_over_icon = tk.PhotoImage(file="Icons\\ffw_over_icon.gif")
        self.next_over_icon = tk.PhotoImage(file="Icons\\next_over_icon.gif")
        self.frequency_icon= tk.PhotoImage(file="Icons\\frequnecy_icon.gif")

        self.mute_over_icon = tk.PhotoImage(file="Icons\\mute_over_icon.gif")
        self.unmute_over_icon = tk.PhotoImage(file="Icons\\unmute_over_icon.gif")
        self.vol_down_over_icon = tk.PhotoImage(file="Icons\\vol_down_over_icon.gif")
        self.vol_up_over_icon = tk.PhotoImage(file="Icons\\vol_up_over_icon.gif")
        self.close_over_icon = tk.PhotoImage(file="Icons\\close_over_icon.gif")
        self.playlist_icon= tk.PhotoImage(file="Icons\\playlist_icon.gif")
        self.playlist_over_icon= tk.PhotoImage(file="Icons\\playlist_over_icon.gif")
        self.frequency_over_icon= tk.PhotoImage(file="Icons\\frequnecy_over_icon.gif")
        
        self.canvas_console=tk.Canvas(frame,width=490, height=220, highlightthickness=0)
        
        self.autoplay_label = tk.Label(frame, text="autoplay_status_label", image=self.autoplay_icon, bd=0)
        self.repeat_label = tk.Label(frame, text="repeat_status_label", image=self.repeat_icon, bd=0)
        self.eq_label = tk.Label(frame, text="eq_status_label", image=self.eq_icon, bd=0)
        self.shuffle_label = tk.Label(frame, text="shuffle_status_label", image=self.shuffle_icon, bd=0)
        self.eq_status_label = tk.Label(frame, text="eq_off", image=self.eq_off_icon, bd=0)
        self.repeat_status_label = tk.Label(frame, text="repeat_off", image=self.repeat_off_icon, bd=0)
        self.shuffle_status_label = tk.Label(frame, text="shuffle_off", image=self.shuffle_off_icon, bd=0)
        self.autoplay_status_label = tk.Label(frame, text="autoplay_off", image=self.autoplay_off_icon, bd=0)
        self.mute_status_label = tk.Label(frame, text="mute_off", image=self.mute_off_icon, bd=0)
        self.wireless_status_label = tk.Label(frame, text="wireless_on", image=self.wireless_on_icon, bd=0)
        self.database_status_label = tk.Label(frame, text="database_on", image=self.database_on_icon, bd=0)
        self.prev_icon_label = tk.Label(frame, text="prev", image=self.prev_icon, bd=0)
        self.ffback_icon_label = tk.Label(frame, text="ffback", image=self.ffback_icon, bd=0, )
        self.play_icon_label = tk.Label(frame, text="play", image=self.play_icon, bd=0)
        self.pause_icon_label = tk.Label(frame, text="pause", image=self.pause_icon, bd=0)
        self.stop_icon_label = tk.Label(frame, text="stop", image=self.stop_icon, bd=0)
        self.ffw_icon_label = tk.Label(frame, text="ffw", image=self.ffw_icon, bd=0)
        self.next_icon_label = tk.Label(frame, text="next", image=self.next_icon, bd=0)

        self.close_icon_label = tk.Label(frame, text="close", image=self.close_icon, bd=0)
        self.mute_icon_label = tk.Label(frame, text="mute", image=self.mute_icon, bd=0)
        self.unmute_icon_label = tk.Label(frame, text="unmute", image=self.unmute_icon, bd=0)
        self.vol_down_icon_label = tk.Label(frame, text="voldown", image=self.vol_down_icon, bd=0)
        self.vol_up_icon_label = tk.Label(frame, text="volup", image=self.vol_up_icon, bd=0)
        self.playlist_icon_label = tk.Label(frame, text="playlist", image=self.playlist_icon, bd=0)
        self.frequency_icon_label=tk.Label(frame, text = "frequency", image=self.frequency_icon, bd=0)
        
        self.canvas_console.create_image(0,0,image= self.frame_bg_icon, anchor="nw")
        self.canvas_console.create_window(18,175, window=self.autoplay_label, anchor="nw")
        self.canvas_console.create_window(174,175, window=self.repeat_label, anchor="nw")
        self.canvas_console.create_window(122,175, window=self.eq_label, anchor="nw")
        self.canvas_console.create_window(70,175, window=self.shuffle_label, anchor="nw")
       
        self.canvas_console.create_window(192,61, window=self.eq_status_label, anchor="nw")
        self.canvas_console.create_window(192,43, window=self.repeat_status_label, anchor="nw")
        self.canvas_console.create_window(192,25, window=self.shuffle_status_label, anchor="nw")
        self.canvas_console.create_window(218,44, window=self.autoplay_status_label, anchor="nw")
        self.canvas_console.create_window(247,44, window=self.mute_status_label, anchor="nw")
        self.canvas_console.create_window(218,61, window=self.wireless_status_label, anchor="nw")
        self.canvas_console.create_window(245,61, window=self.database_status_label, anchor="nw")
        self.canvas_console.create_window(20,146, window=self.prev_icon_label, anchor="nw")
        self.canvas_console.create_window(52,146, window=self.ffback_icon_label, anchor="nw")
        self.canvas_console.create_window(84,146, window=self.play_icon_label, anchor="nw")
        self.canvas_console.create_window(116,146, window=self.pause_icon_label, anchor="nw")
        self.canvas_console.create_window(148,146, window=self.stop_icon_label, anchor="nw")
        self.canvas_console.create_window(180,146, window=self.ffw_icon_label, anchor="nw")
        self.canvas_console.create_window(212,146, window=self.next_icon_label, anchor="nw")
        self.canvas_console.create_window(294,146, window=self.vol_down_icon_label, anchor="nw")
        self.canvas_console.create_window(440,146, window=self.vol_up_icon_label, anchor="nw")
        self.canvas_console.create_window(290,175, window=self.mute_icon_label, anchor="nw")
        self.canvas_console.create_window(326,175, window=self.unmute_icon_label, anchor="nw")
        self.canvas_console.create_window(440,175, window=self.close_icon_label, anchor="nw")
        self.canvas_console.create_window(402,175, window=self.playlist_icon_label, anchor="nw")
        self.canvas_console.create_window(362,175, window=self.frequency_icon_label, anchor="nw")
       
       
        
        
        self.volume_rectangle = self.canvas_console.create_rectangle(335, 156, 335 + self.volume, 161, fill="#6D6E71",
                                                                    width=0)
        
        self.clock=self.canvas_console.create_text( 44, 54 ,anchor="nw", text="00:00", font="DS-Digital 20", fill="#00DCF9")
        self.songname=self.canvas_console.create_text(245, 90, anchor="center", text="[None]", font=("Rounded LED Board-7", 6), fill="#00DCF9") #Rounded LED Board-7,Modern LED Board-7,Repetition Scrolling,Times Square,Segment14,Beware,neuropolitical rg
        self.progress_bar=self.canvas_console.create_rectangle(30,105,30,109,fill="#00DCF9",width=0 )
        self.battery_bar=self.canvas_console.create_rectangle(252,31,252+self.check_baterry_status(),36,fill="#00DCF9",width=0 )
        self.player_status=self.canvas_console.create_image(30, 62, image=self.stop_status_icon, anchor="nw")
        
        
        self.prev_icon_label.bind("<Enter>", self.mouse_over)
        self.ffback_icon_label.bind("<Enter>", self.mouse_over)
        self.play_icon_label.bind("<Enter>", self.mouse_over)
        self.pause_icon_label.bind("<Enter>", self.mouse_over)
        self.stop_icon_label.bind("<Enter>", self.mouse_over)
        self.ffw_icon_label.bind("<Enter>", self.mouse_over)
        self.next_icon_label.bind("<Enter>", self.mouse_over)
        self.mute_icon_label.bind("<Enter>", self.mouse_over)
        self.unmute_icon_label.bind("<Enter>", self.mouse_over)
        self.vol_down_icon_label.bind("<Enter>", self.mouse_over)
        self.vol_up_icon_label.bind("<Enter>", self.mouse_over)
        self.close_icon_label.bind("<Enter>", self.mouse_over)
        self.playlist_icon_label.bind("<Enter>", self.mouse_over)
        self.frequency_icon_label.bind("<Enter>", self.mouse_over)
        
        self.prev_icon_label.bind("<Leave>", self.mouse_out)
        self.ffback_icon_label.bind("<Leave>", self.mouse_out)
        self.play_icon_label.bind("<Leave>", self.mouse_out)
        self.pause_icon_label.bind("<Leave>", self.mouse_out)
        self.stop_icon_label.bind("<Leave>", self.mouse_out)
        self.ffw_icon_label.bind("<Leave>", self.mouse_out)
        self.next_icon_label.bind("<Leave>", self.mouse_out)
        self.mute_icon_label.bind("<Leave>", self.mouse_out)
        self.unmute_icon_label.bind("<Leave>", self.mouse_out)
        self.vol_down_icon_label.bind("<Leave>", self.mouse_out)
        self.vol_up_icon_label.bind("<Leave>", self.mouse_out)
        self.close_icon_label.bind("<Leave>", self.mouse_out)
        self.playlist_icon_label.bind("<Leave>", self.mouse_out)
        self.frequency_icon_label.bind("<Leave>", self.mouse_out)

        self.repeat_label.bind("<Enter>", self.mouse_over)
        self.eq_label.bind("<Enter>", self.mouse_over)
        self.shuffle_label.bind("<Enter>", self.mouse_over)
        self.autoplay_label.bind("<Enter>", self.mouse_over)

        self.repeat_label.bind("<Leave>", self.mouse_out)
        self.eq_label.bind("<Leave>", self.mouse_out)
        self.shuffle_label.bind("<Leave>", self.mouse_out)
        self.autoplay_label.bind("<Leave>", self.mouse_out)

        self.vol_down_icon_label.bind("<Button-1>", self.decrease_volume)
        self.vol_up_icon_label.bind("<Button-1>", self.increase_volume)
        self.mute_icon_label.bind("<Button-1>", self.mute_volume)
        self.unmute_icon_label.bind("<Button-1>", self.unmute_volume)
        self.repeat_label.bind("<Button-1>", self.activate_repeat)
        self.eq_label.bind("<Button-1>", self.activate_eq)
        self.shuffle_label.bind("<Button-1>", self.activate_shuffle)
        self.autoplay_label.bind("<Button-1>", self.activate_autoplay)
        self.play_icon_label.bind("<Button-1>", self.unpause)
        self.ffw_icon_label.bind("<Button-1>", self.ffw)
        self.ffback_icon_label.bind("<Button-1>", self.ffback)
        self.prev_icon_label.bind("<Button-1>", self.previous_track)
        self.next_icon_label.bind("<Button-1>", self.next_track)
        self.close_icon_label.bind("<Button-1>", self.close_app)
        self.playlist_icon_label.bind("<Button-1>", self.playlist_show)
        self.pause_icon_label.bind("<Button-1>", self.pause)
        self.stop_icon_label.bind("<Button-1>", self.stop)

        """ here we create all litlle frame boxes for eq animation and put them into a dictionary"""
        self.frame_dict = {}
        for width in range(12):
            self.list_frame = []
            for height in range(12):
                frame_name = tk.Frame(frame, width=10, height=3, bg=self.colors_list[height])
                self.list_frame.append(frame_name)
            self.frame_dict.setdefault(width, self.list_frame)
        
        self.canvas_console.pack()
        frame.place(x=0,y=0, anchor="nw")
        
    def create_playlist_frame(self):
        self.playlist_show_status=tk.BooleanVar()
        self.playlist_show_status.set(True)
        self.playlist_frame_0 = tk.Frame(self.root, width=490, height=560, bd=0)
        
        self.add_item_icon = tk.PhotoImage(file="Icons\\add_item_icon.gif")
        self.add_folder_icon = tk.PhotoImage(file="Icons\\add_folder_icon.gif")
        self.remove_folder_icon = tk.PhotoImage(file="Icons\\folder_remove_icon.gif")
        self.up_scroll_icon = tk.PhotoImage(file="Icons\\scroll_btn_up.gif")
        self.down_scroll_icon = tk.PhotoImage(file="Icons\\scroll_btn_down.gif")
        self.total_songs_info_icon= tk.PhotoImage(file="Icons\\total_song_info.gif")

        self.add_item_over_icon = tk.PhotoImage(file="Icons\\add_item_over_icon.gif")
        self.add_folder_over_icon = tk.PhotoImage(file="Icons\\add_folder_over_icon.gif")
        self.remove_folder_over_icon = tk.PhotoImage(file="Icons\\folder_remove_over_icon.gif")
        self.up_scroll_over_icon = tk.PhotoImage(file="Icons\\scroll_btn_up_over.gif")
        self.down_scroll_over_icon = tk.PhotoImage(file="Icons\\scroll_btn_down_over.gif")
      
        self.find_icon=tk.PhotoImage(file="Icons\\find_icon.gif")
        self.find_over_icon=tk.PhotoImage(file="Icons\\find_over_icon.gif")
        self.playlist_background = tk.PhotoImage(file="Icons\\playlist_bg_icon.gif")
        self.canvas_playlist= tk.Canvas( self.playlist_frame_0, width=489, height=560, bd=0, highlightthickness=0)
        
        self.add_folder_icon_label = tk.Label( self.playlist_frame_0, text="add_folder", image=self.add_folder_icon, bd=0)
        self.remove_folder_icon_label = tk.Label( self.playlist_frame_0, text="remove_folder", image=self.remove_folder_icon, bd=0)
        self.add_file_icon_label = tk.Label( self.playlist_frame_0, text="add_file", image=self.add_item_icon, bd=0)
        self.scroll_up_icon_label = tk.Label( self.playlist_frame_0, text="scroll_up", image= self.up_scroll_icon, bd=0)
        self.scroll_down_icon_label = tk.Label( self.playlist_frame_0, text="scroll_down", image= self.down_scroll_icon, bd=0)
        self.find_icon_label = tk.Label( self.playlist_frame_0, text="find", image= self.find_icon, bd=0)
        self.total_songs_info= tk.Label( self.playlist_frame_0, text="total_songs_info", image=self.total_songs_info_icon, bd=0)
        
        
        self.playlist_frame = tk.Frame(self.playlist_frame_0, width=417, height=460, bd=0, background="#A7A9AC")
        self.canvas_playlist.create_image(0,0,image=self.playlist_background, anchor="nw")
        self.canvas_playlist.create_window(20, 515, window=self.add_folder_icon_label, anchor="nw")
        self.canvas_playlist.create_window(75, 515, window=self.remove_folder_icon_label, anchor="nw")
        self.canvas_playlist.create_window(130, 515, window=self.add_file_icon_label,anchor="nw" )
        self.canvas_playlist.create_window(185, 515, window=self.find_icon_label,anchor="nw" )
        self.canvas_playlist.create_window(450, 40, window= self.scroll_up_icon_label,anchor="nw" )
        self.canvas_playlist.create_window(450, 491, window=self.scroll_down_icon_label,anchor="nw" )
        self.canvas_playlist.create_window(296, 515, window= self.total_songs_info,anchor="nw" )
        
        self.playlist_bar = self.canvas_playlist.create_rectangle(459,70, 463, 70,fill="#6D6E71", width=0 )# playlist side scrolling bar full
        self.canvas_frame = self.canvas_playlist.create_window(25, 45, window=self.playlist_frame, anchor="nw")
        self.playlist_frame.grid_propagate(0)
        
        self.canvas_playlist.place(x=0,y=0, anchor="nw")

        self.add_file_icon_label.bind("<Button-1>", self.add_song_file)
        # self.remove_item_icon_label.bind("<Button-1>", self.remove_song_file)
        self.remove_folder_icon_label.bind("<Button-1>", self.clear_all_songs)
        self.add_folder_icon_label.bind("<Button-1>", self.add_song_folder)
        self.scroll_up_icon_label.bind("<Button-1>", self.scroll_up_playlist)
        self.scroll_down_icon_label.bind("<Button-1>", self.scroll_down_playlist)
        self.find_icon_label.bind("<Button-1>", self.open_search_window)

        self.add_file_icon_label.bind("<Enter>", self.mouse_over)
        # self.remove_item_icon_label.bind("<Enter>", self.mouse_over)
        self.add_folder_icon_label.bind("<Enter>", self.mouse_over)
        self.remove_folder_icon_label.bind("<Enter>", self.mouse_over)
        self.scroll_up_icon_label.bind("<Enter>", self.mouse_over)
        self.scroll_down_icon_label.bind("<Enter>", self.mouse_over)
        self.find_icon_label.bind("<Enter>", self.mouse_over)

        self.add_file_icon_label.bind("<Leave>", self.mouse_out)
        # self.remove_item_icon_label.bind("<Leave>", self.mouse_out)
        self.add_folder_icon_label.bind("<Leave>", self.mouse_out)
        self.remove_folder_icon_label.bind("<Leave>", self.mouse_out)
        self.scroll_up_icon_label.bind("<Leave>", self.mouse_out)
        self.scroll_down_icon_label.bind("<Leave>", self.mouse_out)
        self.find_icon_label.bind("<Leave>", self.mouse_out)

        self.playlist_frame_0.place(x=0, y=220, anchor="nw")
    
        self.populate_list()

    def moving_frame(self,column_no=None):
        """ this is the eq animation pattern for all threads that is going to be created"""
        while self.show_eq_animation.get() :
            if column_no in range(0,3) or column_no in range(9,12):
                max_height = random.randint(0, 5)
            else:
                max_height = random.randint(5, 12)
            object=[]
            for frame in range(max_height):
                time.sleep(0.06)
                a =self.canvas_console.create_window(287+ (column_no * 14), 73- (frame * 4), window=self.frame_dict[column_no][frame], anchor="nw", tags=str(frame))
                # self.frame_dict[column_no][frame].place(x=2 + (column_no * 14), y=47 - (frame * 4), anchor="nw")
                object.append(a)
            for a in reversed(object):
                time.sleep(0.05)
                self.canvas_console.delete(a)

    def start_animation(self):
        """from here all animation threads are created and started"""
        self.show_eq_animation.set(True)
        for column in range(0, 12):
            thread = Thread(target=self.moving_frame, daemon=True, kwargs=dict(column_no=column))
            self.thread_list.append(thread)

        for thread in self.thread_list:
            thread.start()
            

    def stop_animation(self,event):
        self.show_eq_animation.set(False)
        self.thread_list.clear()
    
    def activate_repeat(self,event):
        if  self.repeat_status_label.cget("text")=="repeat_off":
            self.repeat_status_label.config(image=self.repeat_on_icon, text="repeat_on")
            self.show_message_info("Repeat status ON")
            self.repeat_status.set(True)
        else:
            self.repeat_status_label.config(image=self.repeat_off_icon, text="repeat_off")
            self.show_message_info("Repeat status OFF")
            self.repeat_status.set(False)
    
    def activate_eq(self,event):
        if self.eq_status_label.cget("text") == "eq_off":
            self.eq_status_label.config(image=self.eq_on_icon, text="eq_on")
            self.eq_status.set(True)
        else:
            self.eq_status_label.config(image=self.eq_off_icon, text="eq_off")
            self.eq_status.set(False)
           
    
    def activate_shuffle(self,event):
        if self.shuffle_status_label.cget("text") == "shuffle_off":
            self.shuffle_status_label.config(image=self.shuffle_on_icon, text="shuffle_on")
            self.show_message_info("Shuffle status ON")
            self.shuffle_status.set(True)
        else:
            self.shuffle_status_label.config(image=self.shuffle_off_icon, text="shuffle_off")
            self.show_message_info("Shuffle status OFF")
            self.shuffle_status.set(False)
         
    def activate_autoplay(self,event):
        if self.autoplay_status_label.cget("text") == "autoplay_off":
            self.autoplay_status_label.config(image=self.autoplay_on_icon, text="autoplay_on")
            self.show_message_info("Autoplay status ON")
            self.autoplay_status.set(True)
        else:
            self.autoplay_status_label.config(image=self.autoplay_off_icon, text="autoplay_off")
            self.show_message_info("Autoplay status OFF")
            self.autoplay_status.set(False)
            
            
    def decrease_volume(self,event):
        """function for volume down"""
        if self.volume-10>=0 :
            self.volume-= 10
            position = self.canvas_console.coords(self.volume_rectangle)[2] -10
            self.canvas_console.coords(self.volume_rectangle, 335, 156, position, 161)
            value = self.volume / 100
            self.player.set_volume(value)
            self.check_mute_status_label()
            self.show_message_info("Decreased Volume")

    def increase_volume(self,*args) :
        """function for volume up"""
        
        if self.volume + 10 < 101:
            self.volume += 10
            position=self.canvas_console.coords(self.volume_rectangle)[2] + 10
            self.canvas_console.coords(self.volume_rectangle, 335,156, position,161)
            value=self.volume/100
            self.player.set_volume(value)
            self.check_mute_status_label()
            self.show_message_info("Increased Volume")
            
    def mute_volume(self,*args):
        """function for volume mute"""
        self.volume=0
        self.canvas_console.coords(self.volume_rectangle, 335, 156, 335, 161)
        value = self.volume / 100
        self.player.set_volume(value)
        self.check_mute_status_label()
        self.show_message_info("Mute Volume")
        

    def unmute_volume(self,*args):
        """function for volume un-mute"""
        self.volume = 20
        self.canvas_console.coords(self.volume_rectangle, 335, 156, 335+self.volume, 161)
        value = self.volume / 100
        self.player.set_volume(value)
        self.check_mute_status_label()
        self.show_message_info("Unmute Volume")
        
    def check_mute_status_label(self):
        """checking player volume and updating console icon label """
        if self.volume==0:
            self.mute_status_label.configure(text="mute_on", image=self.mute_on_icon)
        else:
            self.mute_status_label.configure(text="mute_off", image=self.mute_off_icon)
            
    
    def double_click_song(self, event):
        """event to start when double click on a playlist song"""
        if self.index_playing != None: # change to initial fg color for actual playing song before moving to next one
            for i in self.labels[ self.index_playing]:
                i.configure(fg="#f0f0f5")
        self.index_playing= event.widget.grid_info()["row"]
        self.current_track = self.db.return_path( self.index_playing)
       
        self.play_song()

    def next_track(self, event):
        """checking if next track index is available, if is then next track is playing if not nothing happens"""
        try :
            if  self.index_playing +1 <= len(self.labels.keys()): # change to initial fg color for actual playing song before moving to next one
                for i in self.labels[self.index_playing]:
                    i.configure(fg="#f0f0f5")
                self.index_playing += 1
                self.current_track = self.db.return_path( self.index_playing)
                self.show_message_info("Playing Next Song")
                self.play_song()
        except:
            pass
       
    def previous_track(self, event):
        """checking if previous track index is available, if is then next track is playing if not nothing happens"""
        try :
            if self.index_playing  -1 > 0:
                for i in self.labels[self.index_playing]: # change to initial fg color for actual playing song before moving to previous one
                    i.configure(fg="#f0f0f5")
                self.index_playing -= 1
                self.current_track = self.db.return_path( self.index_playing)
                self.show_message_info("Playing Previous Song")
                self.play_song()
        except:
            pass
    
    def shuffle_playing(self):
        global all_indexes
        all_indexes=[]
        for label in self.labels.keys():
            all_indexes.append(label)
        if len(all_indexes)!= 0:
            random_choice=random.choice(all_indexes)
            self.index_playing = random_choice
            self.current_track = self.db.return_path( self.index_playing)
            self.play_song()
            all_indexes.remove(random_choice)
        
    def play_song(self):
        self.player.start_play_thread()
        if not self.show_eq_animation.get():
            self.show_eq_animation.set(True)
            self.start_animation()
        filename = os.path.basename(str(self.current_track))
        filename = filename[0:49]  # maximum characters to display on canvas console
        self.canvas_console.itemconfig(self.songname, text=filename)
        for i in self.labels[ self.index_playing]: # define foreground color for song that is playing into playlist
            i.configure(fg="#404040")
        self.canvas_console.coords(self.progress_bar, 30, 105, 30, 109)
        self.canvas_console.itemconfigure(self.player_status, image=self.play_status_icon)
        self.update_clock_progress_bar()
     
    def ffw(self,evet):
        # TODO figure it out how to seek song position
        self.player.ffw_song()

    def ffback(self, event):
        # TODO figure it out how to seek song position
        self.player.ffback_song()
        
    def pause(self,event):
        self.paused_status.set(True)
        self.player.pause_song()
        self.stop_animation(event=None)
        self.canvas_console.itemconfigure(self.player_status, image=self.pause_status_icon)
        self.show_message_info("Paused")
    
    def stop(self, event):
        self.stop_animation(event=None)
        self.player.stop_song()
        self.canvas_console.itemconfigure(self.player_status, image=self.stop_status_icon)
        self.show_message_info("Unpaused")
        
    def unpause(self,event):
        try:
            if self.paused_status:
                self.start_animation()
                self.player.unpause_song()
                self.paused_status.set(False)
                self.canvas_console.itemconfigure(self.player_status, image=self.play_status_icon)
                
        except:
            pass
        
        
    def update_clock_progress_bar(self):
        song_duration= self.player.song_lenght_time()
        current_time=self.player.actual_song_position()
        currtimemin = int(current_time / 60)
        currtimesec = int(current_time % 60)
        currtimestrng = self.timepattern.format(currtimemin, currtimesec)
        self.canvas_console.itemconfig(self.clock, text=currtimestrng)
        self.canvas_console.coords(self.battery_bar,252,31,252+self.check_baterry_status(),36)
       
        rate=round(430/song_duration,4) # rate wich updates progress bar
        position= 30+ (rate*current_time)
        if position <=460:
            self.canvas_console.coords(self.progress_bar,30,105,position,109)
        self.root.update()
        if current_time>song_duration-1: # define what happens when current song is over playing
            if self.autoplay_status.get() : # play next track from playlist
                self.next_track(event=None)
            elif self.repeat_status.get():  # play same track on repeat
                self.play_song()
            elif self.shuffle_status.get():  # play random track from playlist
                self.shuffle_playing()
            else:
                self.reset_console_frame() # nohting to play afther song is over playing
        else:
            self.canvas_console.after(1000, self.update_clock_progress_bar)
            # self.canvas_console.after(2000, self.test_after)
      
    def reset_console_frame(self):
        """when a song is finished playing console frame is reseting clock,progressbar,stops aninmation and title values"""
        self.canvas_console.coords(self.progress_bar, 30, 105, 30, 109)
        self.canvas_console.itemconfig(self.clock, text="00:00")
        self.canvas_console.itemconfig(self.songname, text="Nothig playing")
        self.canvas_console.itemconfigure(self.player_status, image=self.stop_status_icon)
        self.stop_animation(event=None)
        
    def mouse_over(self, event):
        """control events for mouse over buttons"""
        event_dict = {"prev": self.prev_over_icon , "ffback":self.ffback_over_icon , "next" : self.next_over_icon, "mute":self.mute_over_icon, "ffw": self.ffw_over_icon,
                      "unmute": self.unmute_over_icon, "volup":self.vol_up_over_icon, "voldown": self.vol_down_over_icon, "autoplay_status_label": self.autoplay_over_icon,
                      "repeat_status_label":self.repeat_over_icon, "eq_status_label":self.eq_over_icon,"shuffle_status_label":self.shuffle_over_icon, "play":self.play_over_icon,
                      "pause":self.pause_over_icon,"stop":self.stop_over_icon,"close":self.close_over_icon,"add_file":self.add_item_over_icon,"add_folder":self.add_folder_over_icon,
                      "remove_folder":self.remove_folder_over_icon,"scroll_up":self.up_scroll_over_icon,"scroll_down":self.down_scroll_over_icon, "playlist": self.playlist_over_icon, "find":self.find_over_icon,
                      "frequency":self.frequency_over_icon}
        if event.widget.cget("text") in event_dict.keys() :
            name = event_dict[event.widget.cget("text")]
            event.widget.configure(image=name)
        
    def mouse_out(self, event):
        """initialize default state image for  buttons"""
        event_dict = {"prev": self.prev_icon, "ffback": self.ffback_icon, "next": self.next_icon, "mute": self.mute_icon, "ffw": self.ffw_icon,
                      "unmute": self.unmute_icon, "volup": self.vol_up_icon, "voldown": self.vol_down_icon, "autoplay_status_label": self.autoplay_icon,
                      "repeat_status_label": self.repeat_icon, "eq_status_label": self.eq_icon,
                      "shuffle_status_label": self.shuffle_icon, "play": self.play_icon, "pause": self.pause_icon, "stop": self.stop_icon,
                      "close": self.close_icon, "add_file": self.add_item_icon, "add_folder": self.add_folder_icon,
                      "remove_folder": self.remove_folder_icon, "scroll_up": self.up_scroll_icon, "scroll_down": self.down_scroll_icon,"playlist": self.playlist_icon, "find":self.find_icon,
                      "frequency": self.frequency_icon}
        if event.widget.cget("text") in event_dict.keys():
            name = event_dict[event.widget.cget("text")]
            event.widget.configure(image=name)

    def add_song_folder(self,event):
        """adding an entire folder to the playlist and to playlist database"""
        path= tk.filedialog.askdirectory()
        if path:
            path_files = []
            for folder,subfolder,files in os.walk(path):
                for file in files:
                    if file.endswith(".mp3") or file.endswith(".wav") or file.endswith(".ogg"):
                        path_files.append(os.path.join(folder,file))
            for item in path_files:
                self.db.insert_song(item)
        self.playlist_frame.destroy()
        self.create_playlist_frame()
        self.populate_list()
        
            
    def populate_list(self):
        """connect to playlist database and updates playlist frame with all songs"""
        list = self.db.fetch_data()
        self.labels={} # dictionary with all playlist labels, key is the index from database
        index=[]
        song_name=[]
        length = []
        path=[]
        self.playlist_top_limit=1
        self.playlist_bottom_limit=27
        if len(list)<28:
            self.canvas_playlist.coords(self.playlist_bar, 459, 70, 463,480 )
        else:
            playlist_pages=len(list)//27  # number of playlist pages divided by maximum number of song that can be showed into playlist item
            self.rate= 410/playlist_pages # rate to update playlist bar coords
            self.canvas_playlist.coords(self.playlist_bar, 459, 70, 463,70 + self.rate )  # playlist side scrolling bar full
            
        for item in list:
            index.append(item[0])
            song_name.append(item[1])
            length.append(item[3])
            path.append(item[2])
        for index_label, name_label, duration_label in zip(index, song_name, length):
            l1 = tk.Label( self.playlist_frame, text=index_label, bg="#A7A9AC", anchor=tk.W, width=3, height=0, pady=0,
                          font=("Verdana", 8), fg="#f0f0f5")
            l2 = tk.Label(  self.playlist_frame, text=name_label, bg="#A7A9AC", anchor=tk.W, width=50, height=0, pady=0, padx=0,
                          font=("Verdana", 8), fg="#f0f0f5")
            l3 = tk.Label(  self.playlist_frame, text=duration_label, bg="#A7A9AC", anchor=tk.W, width=0, pady=0, height=0,
                          font=("Verdana", 8), fg="#f0f0f5")
            
            l1.grid(row=int(index_label), column=0)
            l2.grid(row=int(index_label), column=1)
            l3.grid(row=int(index_label), column=3)
            self.labels[index_label] = (l1, l2, l3,)
            
            
            l1.bind("<Enter>", self.playlist_item_color_in)
            l2.bind("<Enter>", self.playlist_item_color_in)
            l3.bind("<Enter>", self.playlist_item_color_in)
            
            l1.bind("<Leave>", self.playlist_item_color_out)
            l2.bind("<Leave>", self.playlist_item_color_out)
            l3.bind("<Leave>", self.playlist_item_color_out)
            
            l1.bind("<Button-1>", self.double_click_song)
            l2.bind("<Button-1>", self.double_click_song)
            l3.bind("<Button-1>", self.double_click_song)

            l1.bind("<MouseWheel>", self.mouse_scroll)
            l2.bind("<MouseWheel>", self.mouse_scroll)
            l3.bind("<MouseWheel>", self.mouse_scroll)
            
        for key,item in self.labels.items(): # when playlist is populated allways shows songs from 1 to 27, the other ones are removed from grid
            if  not (key >= self.playlist_top_limit and key <= self.playlist_bottom_limit):
                for label in item:
                    label.grid_remove()
                    
    def add_song_file(self, event):
        """add a song file to playlist and database """
        filename = tk.filedialog.askopenfilename(filetypes=[("All suported", ".mp3 .wav .ogg"), ("All files", "*.*")])
        if filename:
            self.db.insert_song(filename)
        self.playlist_frame.destroy()
        self.create_playlist_frame()
        self.populate_list()
        

    def remove_song_file(self, event):
        """remove a song file from playlist and database"""
        pass

    def clear_all_songs(self, event):
        """remove all records from database and from main app playlist"""
        self.db.empty_database()
        self.playlist_frame.destroy()
        self.create_playlist_frame()
        self.populate_list()
        
    def playlist_item_color_in (self, event):
        """change color for playlist item when mouse is over"""
        try:
            event.widget.configure(bg="#00DCF9")
            position = event.widget.grid_info()["row"]
            self.labels[position][1].configure(bg="#00DCF9")
            self.labels[position][2].configure(bg="#00DCF9")
            self.labels[position][0].configure(bg="#00DCF9")
        except:
            pass

    def playlist_item_color_out (self, event):
        """change color for playlist item when mouse is not-over"""
        try:
            event.widget.configure(bg="#5D5E61")
            position = event.widget.grid_info()["row"]
            self.labels[position][1].configure(bg="#A7A9AC")
            self.labels[position][2].configure(bg="#A7A9AC")
            self.labels[position][0].configure(bg="#A7A9AC")
        except:
             pass
        
    def scroll_up_playlist(self, event):
        """define event for pressing the button for pressing up button playlist"""
        if self.playlist_top_limit !=1 :  # dont allow to go up if it's allready showing first playlist page
            position = self.canvas_playlist.coords(self.playlist_bar)[3] - self.rate
            self.canvas_playlist.coords(self.playlist_bar, 459, 70, 463, position)  # playlist side scrolling bar fill according playlist page
            self.playlist_top_limit -= 27
            self.playlist_bottom_limit -= 27
            for key, item in self.labels.items():
                if not (key >= self.playlist_top_limit and key <= self.playlist_bottom_limit):
                    for label in item:
                        label.grid_remove()
                else:
                    for label in item:
                        label.grid()
        
    def scroll_down_playlist(self, event):
        """define event for pressing the button for pressing down button playlist"""
        if self.playlist_bottom_limit <= len(self.labels.keys()): # dont allow to go down if it's allready showing last  playlist page
            position = self.canvas_playlist.coords(self.playlist_bar)[3] +self.rate
            self.canvas_playlist.coords(self.playlist_bar, 459, 70, 463, position)  # playlist side scrolling bar fill according playlist page
            self.playlist_top_limit+=27
            self.playlist_bottom_limit+=27
            for key, item in self.labels.items():
                if not (key >= self.playlist_top_limit and key<= self.playlist_bottom_limit):
                   for label in item:
                       label.grid_remove()
                else:
                    for label in item:
                        label.grid()
                        
    def mouse_scroll(self,event):
        if event.delta == 120:
            self.scroll_up_playlist(event=None)
        else:
            self.scroll_down_playlist(event=None)
    
    def playlist_show(self, event):
        """from here playlist is hidden or showed"""
        if self.playlist_show_status.get():
            self.playlist_frame_0.place_forget()
            self.playlist_show_status.set(False)
            self.root.geometry("490x220")
        else:
            self.playlist_frame_0.place(x=0, y=220, anchor="nw")
            self.playlist_show_status.set(True)
            self.root.geometry("490x780")
            
    def open_search_window(self, event):
        """open the search window from here"""
        search_window = search.Find_Song(self.root)
        
        
    def show_message_info(self, message):
        self.canvas_console.delete("info-message") # before showing a new message delete the old on if still is showing
        self.canvas_console.create_text(235, 121, anchor="center", text=message,
                                       font=("Rounded LED Board-7", 6), fill="#00DCF9", tags="info-message")
        self.canvas_console.after(1500, lambda: self.canvas_console.delete("info-message"))
        
    def close_app(self,event):
        self.root.destroy()
 
if __name__=="__main__":
    playerObject = player.Player()
    playlistObject = database.Database("playlist.db")
    app = GUI(playerObject,playlistObject)
