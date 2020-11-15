import tkinter as tk

class Page(tk.Frame):
    def __init__(self):
        tk.Frame.__init__(self)
    def show(self, event=None):
        self.lift()

#   Main menu
class Menu(Page):
    def __init__(self, w):
        Page.__init__(self)
        label = tk.Label(self, text="Max's Destiny 2 Rich Presence App")
        label.place(x=(w/2), y=25, anchor="center")  # Place label at top of screen
