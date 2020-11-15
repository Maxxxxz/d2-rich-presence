import sys
import tkinter as tk
from tkinter import filedialog
import Modules.Pages as Pages

import webbrowser

WIDTH = 400
HEIGHT = 400
APPNAME = "Max's Rich Presence"
ABOUT_URL = "https://github.com/Maxxxxz/d2-rich-presence/blob/master/README.md"
REPO_URL = "https://github.com/Maxxxxz/d2-rich-presence"

class Application(tk.Frame):

    selectedFiles = []

    def __init__(self, master=None):
        master.title("{}".format(APPNAME))                                  #change title here
        master.geometry("{}x{}".format(WIDTH, HEIGHT))            #change window size here
        master.resizable(width=False, height=False)               #resizable?
        tk.Frame.__init__(self, master, relief=tk.GROOVE)
        self.menubar = tk.Menu(self)

        self.contentFrame = tk.Frame(master, width=100, height=100)
        self.contentFrame.pack(anchor=tk.NW, fill=tk.BOTH, expand=True)

        self.pages = []         # initialize pages list

        self.addContent(self.contentFrame)

        self.menus = []         # initialize menus list

        self.addMenus(self.menus)

        for page in self.pages:     # place all pages
            page.place(in_=self.contentFrame, x=0, y=0, relwidth=1, relheight=1)

        self.pages[0].show()

        master.config(menu=self.menubar)

        # self.bind_all("<Control-Key-0>", self.pages[0].show)    # main menu
        # self.bind_all("<Control-Key-1>", self.pages[1].show)    # Page 2

        self.bind_all("<Control-Key-w>", lambda _: self.master.quit())    # Quit Application

    def addMenus(self, menus=None):  #add menu items here

        self.menus.append(tk.Menu(self.menubar, tearoff=0))

        self.menubar.add_cascade(label="File", menu=menus[0])

        menus[0].add_command(label="Exit", command=self.master.quit)

        self.menus.append(tk.Menu(self.menubar, tearoff=0))

        self.menubar.add_cascade(label="Help", menu=menus[1])
        menus[1].add_command(label="About", command=lambda: webbrowser.open(ABOUT_URL))
        menus[1].add_command(label="View the repo", command=lambda: webbrowser.open(REPO_URL))

        # menus.append(tk.Menu(self.menubar, tearoff=0))  # create dropdown menu View

        # self.menubar.add_cascade(label="Pages", underline=0, menu=menus[1])
        # menus[1].add_command(label="Main Menu", command=self.pages[0].lift, accelerator="Control+0")
        # menus[1].add_command(label="Page 1", command=self.pages[1].lift, accelerator="Control+1")

        # self.menus.append(tk.Menu(self.menubar, tearoff=0))



    def clearSelections(self):
        self.selectedFiles.clear()

    def addContent(self, contentFrame=None):                        #add content to contentFrame here
        self.pages.append(Pages.Menu(WIDTH))

def handleArgs():
    pass

if __name__ == "__main__":
    handleArgs()
    root = tk.Tk()
    application = Application(root)
    application.pack()
    root.mainloop()