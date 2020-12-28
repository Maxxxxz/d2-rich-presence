from pypresence import Presence
from enum import Enum
import time
from datetime import datetime
import requests
import json
import operator
import threading

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

# ["details", "state", "Location - sublocation", "gender class - Season Pass level x"]
# ["Nessus Orbit - Raid", "fucking up calus", "Nessus Orbit - Raid", "Awoken Female - Season level 69"]
        # self.RPC.update(
        # details=details[0],
        # state=details[1],
        # # start=time.time(),
        # start=int(details[6]),
        # large_text=details[2],
        # large_image=self.getLargeImage(details[2]),
        # small_text=details[3],
        # small_image=self.getSmallImage(details[3]),
        # # party_id="00",  # can't initiate a join
        # party_size=[int(details[4]),int(details[5])],
        # # join="",
        # # match="match test",
        # )


class RichPresenceState:
    # A Rich Presence State
    #
    # Here is a map between the information here and
    # What Discord requires for a Rich Presence
    # 
    # Discord ------------- D2 Rich Presence
    #  state                .
    #  details              .
    #  start timestamp      .
    #  large image text     .
    #  small image text     .
    #  party id             (any number to enable "x of y")
    #  party size           .
    #  party max            .

    def __init__(self):
        # Universal Information
        self.LocalizedTimeStarted = time.time()     # Must be a number
        self.Platform = "PC" # Default PC, don't display PC.
        self.Level = 0
        
        # Raw information
        self.details = "null"
        self.state = "null"
        self.start = 0

        # Extrapolated Information
        self.large_text = "Location - sublocation"
        self.small_text = "gender class - Season pass level x"
        self.large_image = "cockatiel_tank"
        self.small_image = "cockatiel_german_officer"

        # Basic Activity Information
        self.ActivityName = "null"
        # self.Activity
        self.Location = "null"
        self.SubLocation = "null"

        # Character info
        self.Race = "null"
        self.Gender = "null"
        self.Class = "null"

        # Extra info (Control, Supremacy, Clash, etc.)
        self.Mode = "null"

        # Fireteam Size Limits (MUST be numbers; Fireteam size is ALWAYS at least 1)
        self.FireteamSize = 1
        self.FireteamMaxSize = 3
    
    def extrapolate(self):
        if self.details == "IronBannerControl":
            self.details = "Iron Banner"
            # self.Location = self.details
            self.SubLocation = self.ActivityName
        
        
        if self.Location == self.SubLocation:
            self.large_text = "{0}".format(self.Location)
        else:
            self.large_text = "{0} - {1}".format(self.Location, self.SubLocation)

        self.small_text = "{0} {1} {2} - Season Pass Level {3}".format(self.Gender, self.Race, self.Class, self.Level)

        if self.Platform != "PC":
            self.small_text = "(" + self.Platform + ") " + self.small_text


        # Change FireteamMaxSize based on activity; further change based on crucible mode
        # in orbit, max is 12 for private crucible
        if(self.Mode == "Control" or
           self.Mode == "IronBannerControl" or
           self.Mode == "Raid"
           ):
            self.FireteamMaxSize = 6
        else:
            self.FireteamMaxSize = 3

    def output(self):
        print("LocalizedTimeStarted = {}".format(self.LocalizedTimeStarted))
        print("Level = {}".format(self.Level))
        print("details = {}".format(self.details))
        print("state = {}".format(self.state))
        print("start = {}".format(self.start))
        print("large_text = {}".format(self.large_text))
        print("small_text = {}".format(self.small_text))
        print("large_image = {}".format(self.large_image))
        print("small_image = {}".format(self.small_image))
        print("ActivityName = {}".format(self.ActivityName))
        print("Location = {}".format(self.Location))
        print("SubLocation = {}".format(self.SubLocation))
        print("Race = {}".format(self.Race))
        print("Gender = {}".format(self.Gender))
        print("Class = {}".format(self.Class))
        print("Mode = {}".format(self.Mode))
        print("FireteamSize = {}".format(self.FireteamSize))
        print("FireteamMaxSize = {}".format(self.FireteamMaxSize))

class D2Presence:
    def __init__(self):
        print("init presence")
        self.state = RichPresenceState()
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
        # self.season_definition = requests.get("http://bungie.net" + self.manifest["Response"]["jsonWorldComponentContentPaths"]["en"]["DestinySeasonDefinition"]).json()
        self.season_pass_definition = requests.get("http://bungie.net" + self.manifest["Response"]["jsonWorldComponentContentPaths"]["en"]["DestinySeasonPassDefinition"]).json()

        # print(self.season_pass_definition)

        # for x in self.season_definition:
        #     print(x)
        # print(self.season_definition)

        # print(self.place_hashes)

        # with open('destinations.json', 'w') as out:
        #     json.dump(self.destin_hashes, out)

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
        self.updateThread = threading.Thread(target=self.doUpdate, name="Updater")
        self.updateThread.daemon = True # Set to true to stop after program exits
        self.start()
        
    def printPresence(self):
        self.state.output()

    def start(self):
        self.RPC.connect()

    def startUpdate(self):
        print("updating information...")
        # if valid user
        self.updateThread.start()


    def getCurrentActivity(self):
        # print("current activity")
        # data = ["details", "state", "Location - sublocation", "gender class - Season Pass level x"]
        data = ["Nessus Orbit - Raid", "fucking up calus", "Nessus Orbit - Raid", "Awoken Female - Season level 69"]

        j = self.getActivitiesJSON()

        # data = self.getLatestActivity(j)
        self.getLatestActivity(j)
        
        return 0

    def getLatestActivity(self, injson):

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

        currentjson = tempjson[max(timestamps, key=lambda key: timestamps[key])]

        # currentjson = json.load(open("testdata/raid.json",))

        # with open('t.json', 'w') as out:
            # json.dump(currentjson, out)

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
        
        # this is so fuckign stupid is there something else I can do
        if pl_act_hash != "NULL":
            data1 = str(pl_act_hash)
        elif act_type == "null" or act_type == "":
            data1 = "Orbit"
        else:
            data1 = str(act_type)
        

        if pl_act_hash == "IronBannerControl":
            self.state.ActivityName = str(act)
        else:
            self.state.ActivityName = data1

        self.state.Mode = pl_act_hash

        data2 = ""
        # We do some stuff here with last wish because of a presumably unimplemented prestige mode.
        if act.startswith("Last Wish"):
            data2 = "Last Wish"
        elif act == "null" or act == "":
            data2 = "In Orbit"
        else:
            data2 = act
            # print("ACT IS: " + act)

        # self.state.

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
            self.state.start = data7
            print(data7)

        if(str(act) == "Deep Stone Crypt"):
            data1 = "Raid"
            self.state.Mode = "Raid"

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
            
            self.state.Location = loc
            self.state.SubLocation = subloc
        
        self.getAccountLevel()


        self.state.details = data1
        self.state.state = data2

        # data4 = self.state.Race + " " + self.state.Gender + " " + self.state.Class + " - " + "Season Pass Level " + str(self.level)

        # dataToReturn = [
        #     # str(act),  # State
        #     # str(act_type),      # Details
        #     # "act",
        #     # "act_type",
        #     data1,
        #     data2,
        #     # "large image",
        #     # "small image",
        #     data3,
        #     data4,
        #     # maybe have some fireteam size info here?
        #     data5,
        #     data6,
        #     data7,
        # ]

        # print(tempjson[dataToReturn[0]])
        # for x in tempjson[dataToReturn[0]]:
        #     print(x)

        # print(injson['Response']["characterActivities"]["data"])

    


        # return dataToReturn

    def getActivitiesJSON(self):
        # t = requests.get(BASE_URL + "{0}/Profile/{1}/?components=CharacterActivities".format(platform, memID, charID), headers=my_header)
        t = requests.get(BASE_URL + "{0}/Profile/{1}/?components=204".format(platform, memID, charID), headers=my_header)
        j = t.json()
        return j

    def getAccountLevel(self):
        t = requests.get(BASE_URL + "{0}/Profile/{1}/?components=202".format(platform, memID, charID), headers=my_header)

        # self.accjson = t.json()
        # with open('progression.json', 'w') as out:
        #     json.dump(self.accjson["Response"], out)
        
        temp = t.json()["Response"]["characterProgressions"]["data"]["{}".format(self.currentCharacter)]["progressions"]

        currentSeasonHash, currentSeasonPrestigeHash = self.getCurrentSeasonHashes()

        normal = temp[currentSeasonHash]["level"]
        prestige = temp[currentSeasonPrestigeHash]["level"]

        self.state.Level = int(normal) + int(prestige)

    def getCurrentSeasonHashes(self):

        seasonHash = list(self.season_pass_definition.keys())[-1]

        # print(seasonHash)

        normal = self.season_pass_definition[str(seasonHash)]["rewardProgressionHash"]
        prestige = self.season_pass_definition[str(seasonHash)]["prestigeProgressionHash"]

        return str(normal), str(prestige)

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
        self.state.Race = raceTypes(currentCharacterJSON["raceType"]).name
        self.state.Gender = genderTypes(currentCharacterJSON["genderType"]).name
        self.state.Class = classTypes(currentCharacterJSON["classType"]).name
        # print(currentCharacterJSON)


        # self.accjson = t.json()
        # with open('acc.json', 'w') as out:
        #     json.dump(t.json()["Response"], out)

        return 0
        

    def doUpdate(self):
        starttime = time.time()
        success = True
        while success:
            success = self.update()
            time.sleep(15.0 - ((time.time() - starttime) % 15.0))

    def update(self):
        # print("updating")
        # details = self.getCurrentActivity()

        useDefault = False

        # On fail, attempt 2 more times to get info, else set presence to default
        # functions return 0 if successful
        # else it does not return, keeping res = None

        # Get the currently played character

        loops = 0

        if not useDefault:
            res = None
            while res is None and loops < 3:
                try:
                    res = self.getCurrentCharacter()
                except:
                    print("failed!")
                    loops = loops + 1

        # if failed 3 times, set useDefault to True
        if loops == 3:
            useDefault = True

        loops = 0

        if not useDefault:
            res = None
            while res is None and loops < 3:
                try:
                    res = self.getCurrentActivity()
                except:
                    print("failed!")
                    loops = loops + 1
        
            # if failed 3 times, set useDefault to True
            if loops == 3:
                useDefault = True

        # res = self.getCurrentActivity()

        # self.updatePresence(details)
        


        # true -> default stuff
        # false -> actual presence
        self.updatePresence(useDefault)
        return True

    # def updatePresence(self, details):
    #     self.RPC.update(
    #     details=details[0],
    #     state=details[1],
    #     # start=time.time(),
    #     start=int(details[6]),
    #     large_text=details[2],
    #     large_image=self.getLargeImage(details[2]),
    #     small_text=details[3],
    #     small_image=self.getSmallImage(details[3]),
    #     # party_id="00",  # can't initiate a join
    #     party_size=[int(details[4]),int(details[5])],
    #     # join="",
    #     # match="match test",
    #     )

    def updatePresence(self, doDefault):
        
        if not doDefault:
            self.state.extrapolate()
            self.RPC.update(
            details=self.state.details,
            state=self.state.state,
            # start=time.time(),
            start=int(self.state.start),
            large_text=self.state.large_text,
            # large_image=self.getLargeImage(self.state.large_text),
            large_image=self.state.large_image,
            small_text=self.state.small_text,
            small_image=self.state.small_image,
            # small_image=self.getSmallImage(self.state.small_text),
            # party_id="00",  # can't initiate a join
            party_size=[int(self.state.FireteamSize),int(self.state.FireteamMaxSize)],
            # join="",
            # match="match test",
            )
        else:
            print("Using Default!")
            self.RPC.update(
            details="Orbit",
            state="Patrolling Space",
            start=time.time(),
            large_text="orbit",
            large_image="default",
            small_text=self.state.small_text,
            small_image="default",
            # party_size=[0,0],
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