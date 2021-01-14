# Destiny 2 Rich Presence
A Destiny 2 Rich Presence

# About
I created this because I really enjoy using Discord Rich Presence 
functionality when I can. Destiny 2 is a fun MMO-FPS that I find
myself playing a lot in my free time. It doesn't have good Discord 
integration yet, so I decided to make it myself! This uses Bungie's
API for all Destiny related requests, and pypresence for the rich 
presence aspect. The rest is done by me.

# Plans
I'd like to turn this into an executable once I verify it works
the way I want it to. I'll take suggestions on software to use
to do this in the meantime.

I would also like to support showing the number of
members/maximum number of members in a given team to display in
Discord as well, but as of now it seems that might be a little
too farfetched for the Bungie API. Here's hoping we get an
endpoint that allows for this.

# Install

First, clone this repo (or download it):

```bash
git clone https://github.com/Maxxxxz/d2-rich-presence.git
```

# Run

```bash
python RichPresenceWindow.py
```

# To create the Executable

```bash
pyinstaller --onefile .\RichPresenceWindow.py
```

# To Do

* Create a Virtual Environment to (hopefully) lower exe size

# Dependencies

* Python (building this with 3.8.3)
    * PyPresence
    * PyInstaller (to build exe)
    * ...