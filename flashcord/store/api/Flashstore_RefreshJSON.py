import json
import os

Final_JSON = {
    "modules": "none",
    "plugins": "none",
    "themes": "none"
}

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
    for cycle in range (3):
        AddonArray = []
        for sub_cycle in range (len(UserFolders)):
            CurrentUser = UserFolders[sub_cycle]
            AddonFolders = ls(f"{AddonType[cycle]}\\{CurrentUser}")
            Addons = RemoveSuffix(AddonFolders)
            if Addons != "none":
                AddonArray.append({CurrentUser: Addons})
        if AddonArray != "none":
            Final_JSON[AddonType[cycle]]=AddonArray
    with open('data.json', 'w') as JSON_File:
        JSON_File.write(json.dumps(Final_JSON, indent = 1))