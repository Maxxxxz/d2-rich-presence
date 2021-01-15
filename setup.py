import os.path
from os import path

import json

APIKEY = None
MEMBERSHIPTYPE = None
MEMBERID = None
LANG = "en"
# CURRENTSEASONHASH = None

def start():

    if path.exists("./saved/info.json"):
        return getInfoJson()
    else:
        getInfoJson()
        return True

def getInfoJson():
    
    global APIKEY
    global MEMBERSHIPTYPE
    global MEMBERID
    global LANG
    
    partialInfo = False
    
    try:
        with open("./saved/info.json") as f:
            data = json.load(f)
    
            APIKEY = data["api-key"][0]

        if APIKEY == "" or None:
            print("malformed API Key") # more info on fixing; close application

        MEMBERSHIPTYPE = data["membership-type"]
        
        if MEMBERSHIPTYPE == "":
            partialInfo = True

        MEMBERID = data["member-id"]

        if MEMBERID == "":
            partialInfo = True
    
    except:
        partialInfo = True

    if partialInfo: # startFresh will be set to true
        return True
    else:           # startFresh will be set to false, information is present
        return False
        # Now, do stuff that initializes the window to getinfo section

    # CURRENTSEASONHASH = data["current-season-hash"]
