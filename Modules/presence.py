from pypresence import Presence
from enum import Enum
import time
from datetime import datetime
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

class raceTypes(Enum):
    Human = 0
    Awoken = 1
    Exo = 2
    Unknown = 3

class genderTypes(Enum):
    Male = 0
    Female = 1
    Unknown = 2

class classTypes(Enum):
    Titan = 0
    Hunter = 1
    Warlock = 2
    Unknown = 3

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
        
        # tt = requests.get("http://bungie.net" + self.manifest["Response"]["jsonWorldComponentContentPaths"]["en"]).json()

        # print(self.manifest["Response"]["jsonWorldComponentContentPaths"]["en"])
        # with open('t.json', 'w') as out:
        #     json.dump(self.manifest["Response"], out)

        self.activity_hashes = requests.get("http://bungie.net" + self.manifest["Response"]["jsonWorldComponentContentPaths"]["en"]["DestinyActivityDefinition"]).json()
        # self.mode_type = requests.get("http://bungie.net" + self.manifest["Response"]["jsonWorldComponentContentPaths"]["en"]["DestinyActivityModeTypeDefinition"]).json()
        self.place_hashes = requests.get("http://bungie.net" + self.manifest["Response"]["jsonWorldComponentContentPaths"]["en"]["DestinyPlaceDefinition"]).json()
        self.destin_hashes = requests.get("http://bungie.net" + self.manifest["Response"]["jsonWorldComponentContentPaths"]["en"]["DestinyDestinationDefinition"]).json()
        self.activity_type_hashes = requests.get("http://bungie.net" + self.manifest["Response"]["jsonWorldComponentContentPaths"]["en"]["DestinyActivityTypeDefinition"]).json()

        # print(self.place_hashes)

        with open('destinations.json', 'w') as out:
            json.dump(self.destin_hashes, out)

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

    def doUpdate(self):
        print("updating information...")

    def getCurrentActivity(self):
        # print("current activity")
        # data = ["details", "state", "Location - sublocation", "gender class - Season Pass level x"]
        data = ["Nessus Orbit - Raid", "fucking up calus", "Nessus Orbit - Raid", "Awoken Female - Season level 69"]

        j = self.getActivitiesJSON()

        data = self.getLatestActivity(j)

        return data

    def getLatestActivity(self, injson):

        # Get the currently played character
        self.getCurrentCharacter()

        act = "null"
        act_type = "null"
        pl_act = "null"
        pl_act_hash = "null"

        destination = "null"
        place = "null"

        timestamps = {}
        tempjson = injson['Response']["characterActivities"]["data"]

        for x in tempjson:
            timestamps[x] = tempjson[x]['dateActivityStarted']

        # currentjson = tempjson[max(timestamps, key=lambda key: timestamps[key])]

        currentjson = json.load(open("testdata/europaexplore.json",))

        # with open('t.json', 'w') as out:
        #     json.dump(currentjson, out)

        activity_hash = currentjson["currentActivityHash"]

        # If it is a playlist activity, this will not be null
        playlist_activity_hash = None
        
        try:
            playlist_activity_hash = currentjson["currentPlaylistActivityHash"]
        except:
            pass
        
        # activity_hash = tempjson["currentActivityModeHash"]

        # What does this do?
        current_mode_hash = currentjson["currentActivityModeHash"]

        # Playlist activity (nullable)
        current_mode_type = None
        try:
            current_mode_type = currentjson["currentActivityModeType"]
        except:
            pass

        if current_mode_type:
            print("epic")

        print("activity hash = " + str(activity_hash))
        print("current mode hash = " + str(current_mode_hash))
        print("current mode type = " + str(current_mode_type))
        print("playlist activity hash = " + str(playlist_activity_hash))

        for x in self.activity_type_hashes:
            if str(x) == str(current_mode_hash):
                # print("match on type!")
                # print(self.activity_type_hashes[x]['displayProperties']['name'])
                act_type = self.activity_type_hashes[x]['displayProperties']['name']


        for x in self.activity_hashes:
            if str(x) == str(activity_hash):
                # print("match on activity!")
                # print(self.activity_hashes[x]['displayProperties']['name'])
                theHash = self.activity_hashes[x]
                act = theHash['displayProperties']['name']
                destination = theHash['destinationHash']
                place = theHash['placeHash']

        for x in self.activity_hashes:
            if str(x) == str(playlist_activity_hash):
                # print("match on playlist activity hash!")
                # print(self.activity_hashes[x]['displayProperties']['name'])
                # pl_act = self.activity_hashes[x]['displayProperties']['name']
                theHash = self.activity_hashes[x]
                pl_act = theHash['displayProperties']['name']
                destination = str(theHash['destinationHash'])
                place = str(theHash['placeHash'])

        # print(modeTypes(current_mode_type).name)
        pl_act_hash = str(modeTypes(current_mode_type).name)

        # for x in self.mode_type:
        #     if str(x) == str(current_mode_type):
        #         print("match on current mode type!")
        #         print(self.mode_type[x]['displayProperties']['name'])

        # print(self.activity_type_hashes[current_mode_hash]['name'])
        # print(self.activity_hashes[current_mode_type])

        # print(activity_hash)
        # print(self.activity_hashes[activity_hash])

        print("act = " + str(act))
        print("act_type = " + str(act_type))
        print("pl_act = " + str(pl_act))
        print("pl_act_hash = " + str(pl_act_hash))

        # data = ["details", "state", "Location - sublocation", "gender class - Season Pass level x"]
        
        if pl_act_hash != "NULL":
            data1 = str(pl_act_hash)
        elif act_type == "null" or act_type == "":
            data1 = "Orbit"
        else:
            data1 = str(act_type)
        
        data2 = ""
        # We do some stuff here with last wish because of a presumably unimplemented prestige mode.
        if act.startswith("Last Wish"):
            data2 = "Last Wish"
        elif act == "null" or act == "":
            data2 = "In Orbit"
        else:
            data2 = act
            # print("ACT IS: " + act)
        # if playlist activity do other stuff
        data3 = "33"
        data4 = "44"
        # The number of players in the fireteam/total fireteam size
        data5 = "4"
        data6 = "6"
        # The time the activity started
        data7 = time.time()
        if "dateActivityStarted" in currentjson:
            date = currentjson["dateActivityStarted"]
            data7 = datetime_zero_to_local(datetime.strptime(date, "%Y-%m-%dT%H:%M:%SZ")).timestamp()
            print(data7)

        if(str(act) == "Deep Stone Crypt"):
            data1 = "Raid"

        # get location and sublocation here

        if data2 == "In Orbit" or place == "null" or destination == "null":
            data3 = "Patrolling Space"
        else:
            loc = self.place_hashes[place]['displayProperties']['name']
            subloc = self.destin_hashes[destination]['displayProperties']['name']
            print("LOCATION: " + loc + " SUBLOCATION: " + subloc)
            if loc == subloc:
                data3 = loc
            else:
                data3 = loc + " - " + subloc
        
        self.getAccountLevel()

        data4 = self.currentRace + " " + self.currentGender + " " + self.currentClass + " - " + "Season Pass Level " + str(self.level)

        dataToReturn = [
            # str(act),  # State
            # str(act_type),      # Details
            # "act",
            # "act_type",
            data1,
            data2,
            # "large image",
            # "small image",
            data3,
            data4,
            # maybe have some fireteam size info here?
            data5,
            data6,
            data7,
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

    def getAccountLevel(self):
        t = requests.get(BASE_URL + "{0}/Profile/{1}/?components=202".format(platform, memID, charID), headers=my_header)

        # self.accjson = t.json()
        # with open('progression.json', 'w') as out:
            # json.dump(self.accjson["Response"], out)

        temp = t.json()["Response"]["characterProgressions"]["data"]["{}".format(self.currentCharacter)]["progressions"]
        # Should implement self.getCurrentSeason to grab current season's hash
        currentSeasonInfo = temp["477676543"]#["2098519537"]
        # for x in currentSeasonInfo:
        #     print(x)

        self.level = currentSeasonInfo["level"]
        # for x in temp["progressions"]:
        #     print(x)
        
        # self.level = -1

    def getCurrentCharacter(self):
        t = requests.get(BASE_URL + "{0}/Profile/{1}/?components=200".format(platform, memID, charID), headers=my_header)
        temp = t.json()["Response"]["characters"]["data"]
        
        # Find most recent "datelastplayed" for current player
        timestamps = {}

        for x in temp:
            timestamps[x] = temp[x]["dateLastPlayed"]
        
        # chracter id to be used later
        self.currentCharacter = max(timestamps, key=lambda key: timestamps[key])
        currentCharacterJSON = temp[self.currentCharacter]

        # These will have to be changed to xHash if multiple languages supported.
        self.currentRace = raceTypes(currentCharacterJSON["raceType"]).name
        self.currentGender = genderTypes(currentCharacterJSON["genderType"]).name
        self.currentClass = classTypes(currentCharacterJSON["classType"]).name
        # print(currentCharacterJSON)


        # self.accjson = t.json()
        # with open('acc.json', 'w') as out:
        #     json.dump(t.json()["Response"], out)
        



    def update(self):
        # print("updating")
        details = self.getCurrentActivity()
        self.updatePresence(details)

    def updatePresence(self, details):
        self.RPC.update(
        details=details[0],
        state=details[1],
        # start=time.time(),
        start=int(details[6]),
        large_text=details[2],
        large_image=self.getLargeImage(details[2]),
        small_text=details[3],
        small_image=self.getSmallImage(details[3]),
        # party_id="00",  # can't initiate a join
        party_size=[int(details[4]),int(details[5])],
        # join="",
        # match="match test",
        )

    def getSmallImage(self, data):
        return "cockatiel_tank"

    def getLargeImage(self, data):
        return "cockatiel_german_officer"




    def test(self):
        print("test")

def datetime_zero_to_local(zero_datetime):
    now = time.time()
    offset = datetime.fromtimestamp(now) - datetime.utcfromtimestamp(now)
    return zero_datetime + offset