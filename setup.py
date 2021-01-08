import os.path
from os import path

import json


APIKEY = None
MEMBERSHIPTYPE = None
MEMBERID = None
# CURRENTSEASONHASH = None

def start():

    if path.exists("./saved/info.json"):
        return getInfoJson()
    else:
        print("no save info found!")
        



def getInfoJson():
    
    global APIKEY
    global MEMBERSHIPTYPE
    global MEMBERID
    
    with open("./saved/info.json") as f:
        data = json.load(f)
    
    partialInfo = False

    APIKEY = data["api-key"]

    if APIKEY == "" or None:
        print("malformed API Key") # more info on fixing; close application

    MEMBERSHIPTYPE = data["membership-type"]
    
    if MEMBERSHIPTYPE == "":
        partialInfo = True

    MEMBERID = data["member-id"]

    if MEMBERID == "":
        partialInfo = True


    if partialInfo: # startFresh will be set to true
        return True
    else:           # startFresh will be set to false, information is present
        return False
        # Now, do stuff that initializes the window to getinfo section

    # CURRENTSEASONHASH = data["current-season-hash"]
