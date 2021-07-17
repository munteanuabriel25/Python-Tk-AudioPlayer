import tkinter as tk
from tkinter import ttk
from database import Database

class Find_Song:
    def __init__(self,root):
        
        self.root=root
        self.create_window()
        self.database = Database("playlist.db")
        
    def create_window(self):
        self.window=tk.Toplevel(self.root)
        self.window.geometry("490x200+500+500")
        self.window.title("Search song")
        
        self.place_contents()
        
        
    def place_contents(self):
        self.entry_var=tk.StringVar()
        self.entry_var.trace("w", self.show_message)
        
        self.frame_0=tk.Frame(self.window, width= 490, height=200, bd=0 )
        self.search_background= tk.PhotoImage(file="Icons\\search_window.gif")
        self.label= tk.Label(image=self.search_background)
        self.label.photo=self.search_background
       
        self.search_canvas= tk.Canvas(self.frame_0, width=490, height=200, bd=0,highlightthickness=0)
        self.results_frame = tk.Frame(self.frame_0,  width=429, height=123, bd=0, background="#A7A9AC")  # intra 7 labeluri cu numele melodiilor

        self.search_canvas.create_image(0, 0, image=self.search_background, anchor="nw")
        self.entry = tk.Entry(self.frame_0,width=20, bd=0, bg="#A7A9AC",  font=("Verdana", 12), foreground="white", textvariable=self.entry_var)#6D6E71
        
        
        self.search_canvas.create_window(150,17, window=self.entry, anchor="nw")
        self.search_canvas.create_window(30,48, window= self.results_frame, anchor="nw")
        
   
        self.results_frame.grid_propagate(0)
        self.frame_0.place(x=0, y=0, anchor="nw")
        
        self.search_canvas.pack()
        self.create_labels()
        
    def show_message(self,*args):
        self.reset_labels()
        string=self.entry_var.get()
        result=self.database.search_song(string)
        index=0
        for position in result:
            if index <=6 :
                self.all_labels[index][0].configure(text=position[0])
                self.all_labels[index][1].configure(text=position[1])
                index = index + 1
            else:
                break
        
              
        
    def create_labels(self):
        """from here results are placed on the top level window"""
        self.all_labels={}
        for i in range (7):
            index_label = tk.Label(self.results_frame, text="", bg="#A7A9AC", anchor=tk.W, width=3, height=0, pady=0,
                          font=("Verdana", 8), fg="#f0f0f5")
            song_name = tk.Label(self.results_frame, text="", bg="#A7A9AC", anchor=tk.W, width=57, height=0, pady=0,
                          padx=0,
                          font=("Verdana", 8), fg="#f0f0f5")
            self.all_labels[i]= (index_label,song_name)
        for index , labels in self.all_labels.items():
            labels[0].grid(row=int(index), column=0)
            labels[1].grid(row=int(index), column=1)

        self.bind_labels()
   
    def reset_labels(self):
        """from here, labels text are deleted and then waiting for another search to beginn"""
        for label in self.all_labels.values():
                label[0].configure(text="")
                label[1].configure(text="")
            
    def bind_labels(self):
        for i in range (7):
            for j in range(2):
                self.all_labels[i][j].bind("<Enter>", self.playlist_item_color_in)
                self.all_labels[i][j].bind("<Leave>", self.playlist_item_color_out)
                self.all_labels[i][j].bind("<Button-1>", self.click_on_item)
                   
    def playlist_item_color_in(self,event):
        position = event.widget.grid_info()["row"]
        self.all_labels[position][0].configure(bg="#00DCF9")
        self.all_labels[position][1].configure(bg="#00DCF9")
        
        
    def playlist_item_color_out(self, event):
        position = event.widget.grid_info()["row"]
        self.all_labels[position][0].configure(bg="#A7A9AC")
        self.all_labels[position][1].configure(bg="#A7A9AC")
        
    def click_on_item(self,event):
        """from here selected song is played through the main app"""
        row = event.widget.grid_info()["row"]
        print("Start playing song name :" + self.all_labels[row][1].cget("text"))
        return row