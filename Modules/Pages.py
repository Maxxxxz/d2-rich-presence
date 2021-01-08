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
        updateButton = tk.Button(self, text="Start", 
            command=RPC.startUpdate
            )
        updateButton.place(x=(w/2), y=(w/2), anchor="center")

        # getinfoButton = tk.Button(self, text="get info", command= RPC.test)
        # getinfoButton.place(x=(w/2), y=(w/2) - 50, anchor="center")

        printPresence = tk.Button(self, text="print presence", command= RPC.printPresence)
        printPresence.place(x=(w/2), y=(w/2) - 100, anchor="center")

#   First Load/Reset Page
class GetInfo(Page):

    def __init__(self, w, RPC):
        Page.__init__(self)

        self.PLATFORMS = ["PC", "Playstation", "XBox", "Stadia"]

        self.topLabel = tk.Label(self, text="Enter your information here.")
        self.topLabel.place(x=(w/2), y=25, anchor="center")  # Place label at top of screen

        self.memTypeLabel = tk.Label(self, text="What platform do you use?")
        self.memTypeLabel.place(x=(w/2), y=55, anchor="center")

        self.curType = tk.StringVar(self)
        self.curType.set(self.PLATFORMS[0])

        self.typeBox = tk.OptionMenu(self, self.curType, *self.PLATFORMS)
        self.typeBox.place(x=(w/2), y=85, anchor="center")


        self.memLabel = tk.Label(self, text="What is your ID?")
        self.memLabel.place(x=(w/2), y=115, anchor="center")

        self.idField = tk.Entry(self)
        self.idField.place(x=(w/2), y=145, anchor="center")



        self.submit = tk.Button(self, text="Submit", command= self.onSubmit )
        self.submit.place(x=(w/2), y=200, anchor="center")

    # validate info (check ID and memtype return valid player)
    def onSubmit(self):
        print("platform is {}".format(self.curType.get()))

#   Make Pages for each system login (ie, pc page, ps page, xbox page, etc)
