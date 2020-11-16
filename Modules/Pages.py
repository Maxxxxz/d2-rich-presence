import tkinter as tk
from tkinter import *

class Page(tk.Frame):
    def __init__(self):
        tk.Frame.__init__(self)
    def show(self, event=None):
        self.lift()

#   Main menu
class Menu(Page):
    def __init__(self, w, RPC):
        Page.__init__(self)
        label = tk.Label(self, text="Max's Destiny 2 Rich Presence App")
        label.place(x=(w/2), y=25, anchor="center")  # Place label at top of screen
        updateButton = tk.Button(self, text="Update", command= RPC.update)
        updateButton.place(x=(w/2), y=(w/2), anchor="center")

        getinfoButton = tk.Button(self, text="get info", command= RPC.test)
        getinfoButton.place(x=(w/2), y=(w/2) - 50, anchor="center")

#   First Load/Reset Page
class GetInfo(Page):
    def __init__(self, w, RPC):
        Page.__init__(self)
        label = tk.Label(self, text="What platform are you using?")
        label.place(x=(w/2), y=25, anchor="center")  # Place label at top of screen

#   Make Pages for each system login (ie, pc page, ps page, xbox page, etc)
