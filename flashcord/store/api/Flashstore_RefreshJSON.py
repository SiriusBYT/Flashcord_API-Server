import urllib.request
import json
import os

Final_JSON = {
    "modules": "none",
    "plugins": "none",
    "themes": "none",
    "users": "none"
}

Other_JSON = {}

def Replugged_API(GetWhat):
    if GetWhat == "Plugins": Replugged_API = "https://replugged.dev/api/store/list/plugin?page=1&items=100"
    else: Replugged_API = "https://replugged.dev/api/store/list/theme?page=1&items=100"
    API = urllib.request.Request(
        Replugged_API, 
        data=None, 
        headers={'User-Agent': 'Flashcord-RefreshJSON/r240203'}
    )
    API_Result = json.load(urllib.request.urlopen(API))
    API_ResultKey = API_Result["results"]

    Addon_IDs = []
    for cycle in range (len(API_ResultKey)):
        Addon = ""
        Addon = API_ResultKey[cycle]
        Addon_IDs.append(Addon["id"])
    return Addon_IDs

def ls(Folder):
    Path = os.getcwd() + "\\" + Folder
    Path = Path.replace("\\api","")
    try: return next(os.walk(Path))[1]
    except: return "none"

def FolderUnduper(Folders):
    UndupedFolders = []
    for cycle in range (len(Folders)):
        if Folders[cycle] in UndupedFolders or Folders[cycle] == []: continue
        else: UndupedFolders.append(Folders[cycle])
    return UndupedFolders

def GetUserFolders():
    return FolderUnduper((ls("modules") + ls("plugins") + ls("themes")))

def RemoveSuffix(AddonFolders):
    if AddonFolders != "none":
        for cycle in range (len(AddonFolders)):
            AddonFolders[cycle] = AddonFolders[cycle].replace("-files","")
    return AddonFolders
    
def RefreshJSON():
    UserFolders = GetUserFolders()
    AddonType = ["modules","plugins","themes"]
    FlashcordIDs = PluginIDs = ThemeIDs = Addon_IDs = []
    for cycle in range (3):
        AddonArray = []
        for sub_cycle in range (len(UserFolders)):
            CurrentUser = UserFolders[sub_cycle]
            AddonFolders = ls(f"{AddonType[cycle]}\\{CurrentUser}")
            Addons = RemoveSuffix(AddonFolders)
            if Addons != "none":
                AddonArray.append({CurrentUser: Addons})
                FlashcordIDs.append(Addons)
        Final_JSON[AddonType[cycle]]=AddonArray
    Final_JSON["users"]=UserFolders
    with open('data.json', 'w') as JSON_File:
        JSON_File.write(json.dumps(Final_JSON, indent = 1))
    PluginIDs = Replugged_API("Plugins")
    ThemeIDs = Replugged_API("Themes")
    Addon_IDs = FlashcordIDs + PluginIDs + ThemeIDs
    Addon_IDs = str(Addon_IDs)
    Addon_IDs = Addon_IDs.replace("[","").replace("]","").replace("'","").replace('"','').replace(" ","").split(",")
    Addon_IDs.sort()
    def ViewInstallJSON(doWhat):
        if doWhat == "views": WhatFile = "views.json"
        else: WhatFile = "installs.json"
        with open(WhatFile, 'r') as File: File_JSON = json.load(File)
        if File_JSON == "":
            with open(WhatFile, 'w') as File: File.write("{}")
        with open(WhatFile, 'w') as File:
            for cycle in range (len(Addon_IDs)):
                if Addon_IDs[cycle] not in File_JSON: File_JSON[Addon_IDs[cycle]] = []
            File.write(json.dumps(File_JSON, indent = 1))
    ViewInstallJSON("views")
    ViewInstallJSON("plugins")
    
RefreshJSON()