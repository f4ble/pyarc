from tkinter import *
from factory import Factory
Config = Factory.get('Config')
from ark.thread_handler import ThreadHandler
from ark.gui.tasks import GuiTasks
from ark.gui.control import Control
import time

class PyArcGui(Frame):
    gui_title = "pyarc - Rcon for Ark Survival"
    gui_size = "1200x700"

    def __init__(self, master):
        Frame.__init__(self,master)
        self.pack(fill=BOTH, expand=1)
        self.create_widgets()
        ThreadHandler.create_thread(GuiTasks.loop)



    def create_widgets(self):
        self.feedback = Text(self,width=100,height=40,wrap=WORD)
        self.feedback.place(x=0,y=0)

        Label(self,text="Command:", width=10).place(y=650,x=0)
        self.command = Entry(self, width=120)
        self.command.bind('<Return>',Control.process_input)
        self.command.place(y=650,x=80)




        Label(self,text="Server version:", width=20, anchor=W).place(y=0,x=810)
        self.server_version = Label(self,text="[Unknown]", width=20, anchor=W, relief=GROOVE)
        self.server_version.place(y=0,x=960)

        Label(self,text="Server address:", width=20, anchor=W).place(y=25,x=810)
        self.server_info = Label(self,text=Config.rcon_host, width=20, anchor=W, relief=GROOVE)
        self.server_info.place(y=25,x=960)

        Label(self,text="Config file:", width=20, anchor=W).place(y=50,x=810)
        self.config_file = Label(self,text=Config.filename, width=20, anchor=W, relief=GROOVE)
        self.config_file.place(y=50,x=960)

        Label(self,text="Last keepalive:", width=20, anchor=W).place(y=75,x=810)
        self.last_keepalive = Label(self,text="Never", width=20, anchor=W, relief=GROOVE)
        self.last_keepalive.place(y=75,x=960)

        Label(self,text="Last server response:", width=20, anchor=W).place(y=100,x=810)
        self.last_serverresponse = Label(self,text="Never", width=20, anchor=W, relief=GROOVE)
        self.last_serverresponse.place(y=100,x=960)

        Label(self,text="Last player activity:", width=20, anchor=W).place(y=125,x=810)
        self.last_player_activity = Label(self,text="Never", width=20, anchor=W, relief=GROOVE)
        self.last_player_activity.place(y=125,x=960)

        Label(self,text="Active threads:", width=20, anchor=W).place(y=150,x=810)
        self.active_threads = Label(self,text="", width=20, anchor=W, relief=GROOVE)
        self.active_threads.place(y=150,x=960)


        Label(self,text="List of players:").place(y=400,x=810)
        self.player_list = Listbox(self, relief=SUNKEN, height=10, width=40)
        self.player_list.insert(END,'[Not available]')
        self.player_list.place(y=425,x=810)

        Button(text='Restart Now',command=self.ev_restart_now, bg='#666', fg="#EEE").place(y=600,x=810)
        Button(text='Restart 60min',command=lambda:self.ev_restart_min(60), bg='#666', fg="#EEE").place(y=600,x=900)
        Button(text='Restart 30min',command=lambda:self.ev_restart_min(30), bg='#666', fg="#EEE").place(y=600,x=990)
        Button(text='Restart 10min',command=lambda:self.ev_restart_min(10), bg='#666', fg="#EEE").place(y=600,x=1080)

    def write(self,message):
        self.feedback.insert(END,message)

    def log(self,message):
        self.feedback.insert(END,message + "\n")

    def is_online(self):
        #self.log('Not connected to RCON')
        return True

    def ev_restart_min(self,minutes):
        if not self.is_online():
            return False

        from ark.rcon import Rcon
        Rcon.delayed_restart(minutes)

    def ev_restart_now(self):
        if not self.is_online():
            return False

        self.log('Restart button pressed')
        from ark.rcon import Rcon
        Rcon.callback_restart()
