import tkinter as tk
from tkinter import *
import json

import webbrowser
import os
import setup

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
        self.RPC = RPC
        self.hideFT = True
        self.max = 6
        # label = tk.Label(self, text="Max's Destiny 2 Rich Presence App")
        # label.place(x=(w/2), y=25, anchor="center")  # Place label at top of screen
        bottomFrame = tk.Frame(self, height=250)
        # bottomFrame.grid_configure()

        

        
        self.startUpdateButton = tk.Button(self, text="Start Updating", 
            command=self.updatePressed
            )
        # startUpdateButton.place(x=(w/2), y=(w/2), anchor="center")
        self.startUpdateButton.pack(side=BOTTOM)
        bottomFrame.pack(side=BOTTOM)

        ###############

        self.toggleFTButton = tk.Button(bottomFrame, text="Fireteam Size: Hidden", command=self.toggleHideFT)
        self.toggleFTButton.grid(row=1, column=2)

        vcmdCUR = (self.register(self.validateCur), '%P')

        self.curSizeSB = tk.Spinbox(bottomFrame, from_=1, to_=12, increment=1, validate="key", validatecommand=vcmdCUR, width=5)
        self.curSizeSB.grid(row=1, column=3)

        slashLabel = tk.Label(bottomFrame, text="/")
        slashLabel.grid(row=1, column=4)

        vcmdMAX = (self.register(self.validateMax), '%P')
        var = tk.IntVar(self)
        var.set(self.max)

        self.maxSizeSB = tk.Spinbox(bottomFrame, from_=1, to_=12, increment=1, validate="key", validatecommand=vcmdMAX, textvariable=var, width=5)
        self.maxSizeSB.grid(row=1, column=5)

        # self.startUpdateButton.grid(row=3, column=3)

        ###############

        # Force update button?

        stateTextBox = tk.Text(self, state=DISABLED)
        stateTextBox.pack(side=TOP)
        # stateTextBox.config(state=DISABLED)
        self.RPC.setUpdateBox(stateTextBox)

        # getinfoButton = tk.Button(self, text="get info", command= RPC.test)
        # getinfoButton.place(x=(w/2), y=(w/2) - 50, anchor="center")

        # printPresence = tk.Button(self, text="print presence", command= RPC.printPresence)
        # printPresence.place(x=(w/2), y=(w/2) - 100, anchor="center")
    
    def updatePressed(self):
        self.RPC.startUpdate()
        self.startUpdateButton.config(state=DISABLED)

    def validateCur(self, cur):
        if cur.isnumeric() and (cur <= str(self.max)):
            self.RPC.state.setSize(cur)
            return True
        # else:
        return False

    def validateMax(self, cur):
        if cur.isnumeric():
            self.max = cur
            self.RPC.state.setMaxSize(self.max)
            self.curSizeSB.config(to_=self.max)
            return True
        else:
            return False

    def toggleHideFT(self):
        self.hideFT = not self.hideFT
        self.RPC.state.hideFT = self.hideFT

        if self.hideFT:
            self.toggleFTButton.config(text="Fireteam Size: Hidden")
        else:
            self.toggleFTButton.config(text="Fireteam Size: Visible")

        # Should I change the fireteam spinboxes to -1?
        # if self.hideFT:
        #     self.


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
            # data["api-key"] = KEY,       # Should I grab this from github?
            data["membership-type"] = PLATFORM_DEFINITION[plat]         # Just use the number
            data["member-id"] = ID                                      # Keep as string

            setup.MEMBERSHIPTYPE = PLATFORM_DEFINITION[plat]
            setup.MEMBERID = ID

            path = "./saved/info.json"

            if not os.path.exists(path):
                os.makedirs("saved", exist_ok=True)
                file = open(path, 'w+')
                file.close()

            with open(path, "w") as f:
                json.dump(data, f)
            
            self.app.pages[0].show()



#   Make Pages for each system login (ie, pc page, ps page, xbox page, etc)
