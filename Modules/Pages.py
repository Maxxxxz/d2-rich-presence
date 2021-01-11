import tkinter as tk
from tkinter import *
import json

import webbrowser

MEMID_HELP_PAGE = "https://maxxxxz.github.io/Sandbox/DestinyMembershipID/"

PLATFORM_DEFINITION = {
    "PC": 3,
    "Playstation": 2,
    "XBox": 1,
    "Stadia": 5
}

class Page(tk.Frame):
    def __init__(self):
        tk.Frame.__init__(self)
    def show(self, event=None):
        self.lift()

#   Main menu
class Menu(Page):
    def __init__(self, w, RPC):
        Page.__init__(self)
        # label = tk.Label(self, text="Max's Destiny 2 Rich Presence App")
        # label.place(x=(w/2), y=25, anchor="center")  # Place label at top of screen
        startUpdateButton = tk.Button(self, text="Start Updating", 
            command=RPC.startUpdate
            )
        # startUpdateButton.place(x=(w/2), y=(w/2), anchor="center")
        startUpdateButton.pack(side=BOTTOM)

        # Force update button?

        stateTextBox = tk.Text(self, state=DISABLED)
        stateTextBox.pack(side=TOP)
        # stateTextBox.config(state=DISABLED)
        RPC.setUpdateBox(stateTextBox)

        # getinfoButton = tk.Button(self, text="get info", command= RPC.test)
        # getinfoButton.place(x=(w/2), y=(w/2) - 50, anchor="center")

        # printPresence = tk.Button(self, text="print presence", command= RPC.printPresence)
        # printPresence.place(x=(w/2), y=(w/2) - 100, anchor="center")

#   First Load/Reset Page
class GetInfo(Page):

    def __init__(self, w, RPC, app):
        Page.__init__(self)

        self.PLATFORMS = ["PC", "Playstation", "XBox", "Stadia"]

        self.app = app

        self.topLabel = tk.Label(self, text="Enter your information here.")
        self.topLabel.place(x=(w/2), y=25, anchor="center")  # Place label at top of screen

        self.memTypeLabel = tk.Label(self, text="What platform do you use?")
        self.memTypeLabel.place(x=(w/2), y=55, anchor="center")

        self.curType = tk.StringVar(self)
        self.curType.set(self.PLATFORMS[0])

        self.typeBox = tk.OptionMenu(self, self.curType, *self.PLATFORMS)
        self.typeBox.place(x=(w/2), y=85, anchor="center")


        self.memLabel = tk.Label(self, text="What is your Membership ID?")
        self.memLabel.place(x=(w/2), y=115, anchor="center")

        self.memHelpLabel = tk.Label(self, text="How do I find this? (opens in browser)", fg="grey")
        self.memHelpLabel.bind("<Button-1>", lambda e: self.openMemIDHelp())
        self.memHelpLabel.place(x=(w/2), y=135, anchor="center")

        self.idField = tk.Entry(self)
        self.idField.place(x=(w/2), y=165, anchor="center")
        self.idField.focus_force()


        self.submit = tk.Button(self, text="Submit", command= self.onSubmit )
        self.submit.place(x=(w/2), y=200, anchor="center")

    def openMemIDHelp(self):
        webbrowser.open(MEMID_HELP_PAGE)

    # validate info (check ID and memtype return valid player)
    def onSubmit(self):
        # print("platform is {}".format(self.curType.get()))
        missingInfo = False
        ID = self.idField.get()
        plat = self.curType.get()
        # print("platform is: {} while ID is {}".format(PLATFORM_DEFINITION[plat], ID))

        if(ID == ""):
            missingInfo = True

        if(missingInfo):
            messagebox.showerror(title="Missing Info", message="You are missing required information!")
        else:
            # Try to see if player exists using api, then save if success
            data = {}
            data["api-key"] = "7df97cc02219401fbfa6be6c26069b44",       # Should I grab this from github?
            data["membership-type"] = PLATFORM_DEFINITION[plat]         # Just use the number
            data["member-id"] = ID                                      # Keep as string

            with open("./saved/info.json", "w") as f:
                json.dump(data, f)
            
            self.app.pages[0].show()



#   Make Pages for each system login (ie, pc page, ps page, xbox page, etc)
