from pypresence import Presence
import time
import requests
import json
import operator

BASE_URL = "https://bungie.net/Platform/Destiny2/"
API_KEY = "7df97cc02219401fbfa6be6c26069b44"
RPC_CLIENT_ID = "777656520518270986"

STEAM_ID_LOOKUP = ""

TEST_ID64 = "76561198020873129"

platform = 3
memID = "4611686018483845808"
charID = 0
my_header = {"X-API-Key": API_KEY}

class D2Presence:
    def __init__(self):
        print("init presence")

        man = requests.get(BASE_URL + "Manifest/")
        self.manifest = man.json()
        # print(j1["Response"]["jsonWorldComponentContentPaths"]['en']['DestinyActivityDefinition'])
        hashes = requests.get("http://bungie.net" + self.manifest["Response"]["jsonWorldComponentContentPaths"]['en']['DestinyActivityDefinition'])
        # for x in j1["Response"]:
        #     print(x)
        # print(j1["Response"]["jsonWorldComponentContentPaths"]["en"]['DestinyDestinationDefinition'])
        self.activity_hashes = hashes.json()

        destin_hashes = requests.get("http://bungie.net" + self.manifest["Response"]["jsonWorldComponentContentPaths"]["en"]['DestinyDestinationDefinition'])
        self.dest_hashes = destin_hashes.json()
        # This gets the name for the activity hash, will also contain the location hash
        # for x in j2:
            # print(j2[x]["destinationHash"])
            # print(j2[x]["displayProperties"]['name'])

        # for x in j3:
        #     print(j3[x]["displayProperties"])

        # t = requests.get(BASE_URL + "{0}/Profile/{1}/?components=CharacterActivities".format(platform, memID, charID), headers=my_header)
        # j = t.json()
        # print(t)

        # User if offline for now, can let them update later
        # if j["ErrorStatus"] != "Success":
        #     print("offline!")

        # print(j["Response"])

        # for x in j["Response"]["characterActivities"]:
        #     print(j["Response"]["characterActivities"][x])


        self.RPC = Presence(RPC_CLIENT_ID)
        self.start()
        
    def start(self):
        self.RPC.connect()

    def getCurrentActivity(self):
        # print("current activity")
        # data = ["details", "state", "Location - sublocation", "gender class - Season Pass level x"]
        data = ["Nessus Orbit - Raid", "fucking up calus", "Nessus Orbit - Raid", "Awoken Female - Season level 69"]

        j = self.getActivitiesJSON()

        data = self.getLatestActivity(j)

        return data

    def getLatestActivity(self, injson):

        # logic to find most recent activity from activities
        # stub to use first result

        # print(injson['Response'][])

        timestamps = {}
        tempjson = injson['Response']["characterActivities"]["data"]
        # print(tempjson["currentActivityHash"])
        for x in tempjson:
            timestamps[x] = tempjson[x]['dateActivityStarted']

        # for x in timestamps:
        #     print(timestamps[x])

        # print(timestamps)

        # ENDED HERE: trying to find the current activity has to then translate into the name of activity

        activity_hash = tempjson[max(timestamps, key=lambda key: timestamps[key])]
        # current_mode_type = activity_hash["currentActivityModeType"]
        
        print(activity_hash)
        # print(self.activity_hashes[current_mode_type])

        dataToReturn = [
            # self.activity_hashes[activity_hash]['name'],
            "name",
            # self.activity_hashes[current_mode_type],
            "description",
            "ta",
            "ab",
            "ba",
        ]

        # print(tempjson[dataToReturn[0]])
        # for x in tempjson[dataToReturn[0]]:
        #     print(x)

        # print(injson['Response']["characterActivities"]["data"])

    


        return dataToReturn

    def getActivitiesJSON(self):
        t = requests.get(BASE_URL + "{0}/Profile/{1}/?components=CharacterActivities".format(platform, memID, charID), headers=my_header)
        j = t.json()
        return j


    def update(self):
        # print("updating")
        details = self.getCurrentActivity()
        self.updatePresence(details)

    def updatePresence(self, details):
        self.RPC.update(
        details=details[0],
        state=details[1],
        start=time.time(),
        large_text=details[2],
        large_image=self.getLargeImage(details),
        small_text=details[3],
        small_image=self.getSmallImage(details),
        # join="join me",
        match="match test",
        )

    def getSmallImage(self, data):
        return "cockatiel_tank"

    def getLargeImage(self, data):
        return "cockatiel_german_officer"




    def test(self):
        t = requests.get(
            BASE_URL + ""
        )