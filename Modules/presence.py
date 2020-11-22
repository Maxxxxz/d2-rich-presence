from pypresence import Presence
from enum import Enum
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


class modeTypes(Enum):
    NULL = None
    NONE = 0
    Story = 2
    Strike = 3
    Raid = 4
    AllPvP = 5
    Patrol = 6
    AllPvE = 7
    Reserved9 = 9
    Control = 10
    Reserved11 = 11
    Clash = 12
    Reserved13 = 13
    CrimsonDoubles = 15
    Nightfall = 16
    HeroicNightfall = 17
    AllStrikes = 18
    IronBanner = 19
    Reserved20 = 20
    Reserved21 = 21
    Reserved22 = 22
    Reserved24 = 24
    AllMayhem = 25
    Reserved26 = 26
    Reserved27 = 27
    Reserved28 = 28
    Reserved29 = 29
    Reserved30 = 30
    Supremacy = 31
    PrivateMatchesAll = 32
    Survival = 37
    Countdown = 38
    TrialsOfTheNine = 39
    Social = 40
    TrialsCountdown = 41
    TrialsSurvival = 42
    IronBannerControl = 43
    IronBannerClash = 44
    IronBannerSupremacy = 45
    ScoredNightfall = 46
    ScoredHeroicNightfall = 47
    Rumble = 48
    AllDoubles = 49
    Doubles = 50
    PrivateMatchesClash = 51
    PrivateMatchesControl = 52
    PrivateMatchesSupremacy = 53
    PrivateMatchesCountdown = 54
    PrivateMatchesSurvival = 55
    PrivateMatchesMayhem = 56
    PrivateMatchesRumble = 57
    HeroicAdventure = 58
    Showdown = 59
    Lockdown = 60
    Scorched = 61
    ScorchedTeam = 62
    Gambit = 63
    AllPvECompetitive = 64
    Breakthrough = 65
    BlackArmoryRun = 66
    Salvage = 67
    IronBannerSalvage = 68
    PvPCompetitive = 69
    PvPQuickplay = 70
    ClashQuickplay = 71
    ClashCompetitive = 72
    ControlQuickplay = 73
    ControlCompetitive = 74
    GambitPrime = 75
    Reckoning = 76
    Menagerie = 77
    VexOffensive = 78
    NightmareHunt = 79
    Elimination = 80
    Momentum = 81
    Dungeon = 82
    Sundial = 83
    TrialsOfOsiris = 84

class D2Presence:
    def __init__(self):
        print("init presence")

        man = requests.get(BASE_URL + "Manifest/")
        self.manifest = man.json()
        # print(j1["Response"]["jsonWorldComponentContentPaths"]['en']['DestinyActivityDefinition'])
        # hashes = requests.get("http://bungie.net" + self.manifest["Response"]["jsonWorldComponentContentPaths"]['en'])
        # for x in j1["Response"]:
        #     print(x)
        # print(j1["Response"]["jsonWorldComponentContentPaths"]["en"]['DestinyDestinationDefinition'])
        # self.hashes = hashes.json()
        self.activity_hashes = requests.get("http://bungie.net" + self.manifest["Response"]["jsonWorldComponentContentPaths"]["en"]["DestinyActivityDefinition"]).json()
        self.destin_hashes = requests.get("http://bungie.net" + self.manifest["Response"]["jsonWorldComponentContentPaths"]["en"]["DestinyPlaceDefinition"]).json()
        self.activity_type_hashes = requests.get("http://bungie.net" + self.manifest["Response"]["jsonWorldComponentContentPaths"]["en"]["DestinyActivityTypeDefinition"]).json()

        # for x in self.activity_hashes:
        #     print(x)

        # destin_hashes = requests.get("http://bungie.net" + self.manifest["Response"]["jsonWorldComponentContentPaths"]["en"]['DestinyDestinationDefinition'])
        # self.dest_hashes = destin_hashes.json()
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

        act = "null"
        act_type = "null"

        # todo
        # get place hash
        # get destination hash
        # change how rich presence is done with playlist activities

        timestamps = {}
        tempjson = injson['Response']["characterActivities"]["data"]
        # print(tempjson["currentActivityHash"])
        for x in tempjson:
            timestamps[x] = tempjson[x]['dateActivityStarted']

        # for x in timestamps:
        #     print(timestamps[x])

        # print(timestamps)

        # ENDED HERE: trying to find the current activity has to then translate into the name of activity

        # for x in tempjson:
        #     print(x)

        currentjson = tempjson[max(timestamps, key=lambda key: timestamps[key])]

        activity_hash = currentjson["currentActivityHash"]
        
        # activity_hash = tempjson["currentActivityModeHash"]
        current_mode_hash = currentjson["currentActivityModeHash"]
        current_mode_type = currentjson["currentActivityModeType"]

        print(activity_hash)
        print(current_mode_hash)
        print(current_mode_type)

        for x in self.activity_type_hashes:
            if str(x) == str(current_mode_hash):
                print("match on type!")
                # print(self.activity_type_hashes[x]['displayProperties']['name'])
                act_type = self.activity_type_hashes[x]['displayProperties']['name']


        for x in self.activity_hashes:
            if str(x) == str(activity_hash):
                print("match on activity!")
                # print(self.activity_hashes[x]['displayProperties']['name'])
                act = self.activity_hashes[x]['displayProperties']['name']

        # for x in self.:
        #     if str(x) == str(activity_hash):
        #         print("match!")
        #         print(self.activity_hashes[x]['displayProperties']['name'])

        # print(self.activity_type_hashes[current_mode_hash]['name'])
        # print(self.activity_hashes[current_mode_type])

        # print(activity_hash)
        # print(self.activity_hashes[activity_hash])

        dataToReturn = [
            act,  # State
            act_type,      # Details
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
        # t = requests.get(BASE_URL + "{0}/Profile/{1}/?components=CharacterActivities".format(platform, memID, charID), headers=my_header)
        t = requests.get(BASE_URL + "{0}/Profile/{1}/?components=204".format(platform, memID, charID), headers=my_header)
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