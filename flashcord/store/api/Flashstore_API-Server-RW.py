import socket # API's Native Language 
import websockets # API's Translated Language
import time
import asyncio
import _thread
import threading
import json

"""
Very important almighty Flashstore API Banner
Legends say that removing this banner will cause the world to explode.
"""
ASCII_Banner = " ▄▄▄▄▄▄▄ ▄▄▄     ▄▄▄▄▄▄ ▄▄▄▄▄▄▄ ▄▄   ▄▄ ▄▄▄▄▄▄▄ ▄▄▄▄▄▄▄ ▄▄▄▄▄▄▄ ▄▄▄▄▄▄   ▄▄▄▄▄▄▄    ▄▄▄▄▄▄▄ ▄▄▄▄▄▄▄ ▄▄▄ \n\
█       █   █   █      █       █  █ █  █       █       █       █   ▄  █ █       █  █       █       █   █ \n\
█    ▄▄▄█   █   █  ▄   █  ▄▄▄▄▄█  █▄█  █  ▄▄▄▄▄█▄     ▄█   ▄   █  █ █ █ █    ▄▄▄█  █   ▄   █    ▄  █   █ \n\
█   █▄▄▄█   █   █ █▄█  █ █▄▄▄▄▄█       █ █▄▄▄▄▄  █   █ █  █ █  █   █▄▄█▄█   █▄▄▄   █  █▄█  █   █▄█ █   █ \n\
█    ▄▄▄█   █▄▄▄█      █▄▄▄▄▄  █   ▄   █▄▄▄▄▄  █ █   █ █  █▄█  █    ▄▄  █    ▄▄▄█  █       █    ▄▄▄█   █ \n\
█   █   █       █  ▄   █▄▄▄▄▄█ █  █ █  █▄▄▄▄▄█ █ █   █ █       █   █  █ █   █▄▄▄   █   ▄   █   █   █   █ \n\
█▄▄▄█   █▄▄▄▄▄▄▄█▄█ █▄▄█▄▄▄▄▄▄▄█▄▄█ █▄▄█▄▄▄▄▄▄▄█ █▄▄▄█ █▄▄▄▄▄▄▄█▄▄▄█  █▄█▄▄▄▄▄▄▄█  █▄▄█ █▄▄█▄▄▄█   █▄▄▄█ \
"
# Server Information
ServerAddress = socket.gethostname()
ServerPort = 1407
ServerVersion = "r240129"
PacketSize = 1024
API_Socket = socket.socket()
API_Version = 3.0
DebugMode = True

# This is useless and is only used once but hey, you never know if you gonna need this useless piece of shit. I swear I'm not a function hoarder.
def Flood(Lines):
    Flood = ""
    for cycle in range (Lines+1):
        Flood = Flood + "\n"
    return Flood

# Logging System + Getting current time and date in prefered format
def GetTime():
    CTime = time.localtime()
    Time = f"{CTime.tm_hour:02d}:{CTime.tm_min:02d}:{CTime.tm_sec:02d} - {CTime.tm_mday:02d}/{CTime.tm_mon:02d}"
    Date = f"{CTime.tm_mday:02d}-{CTime.tm_mon:02d}-{CTime.tm_year}"
    return Time,Date
def WriteLog(Log,isDebugMessage):
    Time,Data = GetTime()
    LogFile = f"logs/{Data}.log"
    PrintLog = f"[{Time}] {Log}"
    FileLog = f'{PrintLog}\n'
    with open(LogFile, "a", encoding="utf=8") as LogFile:
        LogFile.write(FileLog)
        if isDebugMessage == True and DebugMode == True: print(PrintLog)
        elif isDebugMessage == False: print(PrintLog)

# Server Data Loader
def GetServerData():
    with open('data/modules.dat', 'r', encoding='utf-8') as Data_File:
        ModuleData = Data_File.read().replace(" ", "").replace(":", "\n").split("\n")
    with open('data/plugins.dat', 'r', encoding='utf-8') as Data_File:
        PluginData = Data_File.read().replace(" ", "").replace(":", "\n").split("\n")
    with open('data/users.dat', 'r', encoding='utf-8') as Data_File:
        UserData = Data_File.read().replace(" ", "").replace(":", "\n").split("\n")
    return ModuleData,PluginData,UserData

def Bootstrap():
    print(Flood(16))
    print(ASCII_Banner)
    print(f"{ServerAddress}:{ServerPort}@API_{API_Version}/{ServerVersion} // Debug: {DebugMode} - Packet Size: {PacketSize}b\n")
    WriteLog(f'Initializing server...',False)
    ModuleData,PluginData,UserData = GetServerData()
    WriteLog(f'[INFO] Module Data: {ModuleData}',False)
    WriteLog(f'[INFO] Plugin Data: {PluginData}',False)
    WriteLog(f'[INFO] User Data: {UserData}',False)

Bootstrap()