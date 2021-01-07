import os.path
from os import path

import json


APIKEY = None
MEMBERSHIPTYPE = None
MEMBERID = None
# CURRENTSEASONHASH = None

def start():

    if path.exists("./saved/info.json"):
        getInfoJson()
    else:
        print("does not exist")
        



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


    if partialInfo:
        pass
        # Now, do stuff that initializes the window to getinfo section

    # CURRENTSEASONHASH = data["current-season-hash"]
