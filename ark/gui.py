from tkinter import *
from factory import Factory
Config = Factory.get('Config')

class PyArcGui(Frame):
    gui_title = "pyarc - Rcon for Ark Survival"
    gui_size = "1200x700"

    def __init__(self, master):
        Frame.__init__(self,master)
        self.pack(fill=BOTH, expand=1)
        self.create_widgets()

    def create_widgets(self):
        self.feedback = Text(self,width=100,height=40,wrap=WORD)
        self.feedback.place(x=0,y=0)

        self.command_label = Label(self,text="Command:", width=10)
        self.command = Entry(self, width=120)
        self.command_label.place(y=650,x=0)
        self.command.place(y=650,x=80)

        self.server_version = Label(self,text="Server version:", width=20, anchor=W)
        self.server_version_value = Label(self,text="[Unknown]", width=20, anchor=W, relief=GROOVE)
        self.server_version.place(y=0,x=810)
        self.server_version_value.place(y=0,x=960)

        self.server_info = Label(self,text="Server address:", width=20, anchor=W)
        self.server_info_value = Label(self,text=Config.rcon_host, width=20, anchor=W, relief=GROOVE)
        self.server_info.place(y=25,x=810)
        self.server_info_value.place(y=25,x=960)


        self.player_list = Label(self,text="List of players:")
        self.player_list.place(y=400,x=810)
        self.player_list_value = Listbox(self, relief=SUNKEN, height=10, width=40)
        self.player_list_value.insert(END,'[Not available]')
        self.player_list_value.place(y=425,x=810)

        self.restart_now = Button(text='Restart Now',command=self.ev_restart_now, bg='#666', fg="#EEE")
        self.restart_now.place(y=600,x=810)

        self.restart_60 = Button(text='Restart 60min',command=lambda:self.ev_restart_min(60), bg='#666', fg="#EEE")
        self.restart_60.place(y=600,x=900)

        self.restart_30 = Button(text='Restart 30min',command=lambda:self.ev_restart_min(30), bg='#666', fg="#EEE")
        self.restart_30.place(y=600,x=990)

        self.restart_10 = Button(text='Restart 10min',command=lambda:self.ev_restart_min(10), bg='#666', fg="#EEE")
        self.restart_10.place(y=600,x=1080)

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
