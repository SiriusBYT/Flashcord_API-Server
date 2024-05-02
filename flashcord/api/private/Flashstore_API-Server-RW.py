# Server Modules
import socket # API's Native Language 
import websockets # API's Translated Language
import ssl # Required for WebSockets BS

# Multi-threading modules
import asyncio # Required for WebSockets
import _thread # Required for multi-client raw socket clients.
import threading # Required for WebSockets

# Miscellaneous Modules
import time # Required for logs
import json # Server Data is in JSON format
import os # Required for KeyboardInterrupt (DEBUG)
import sys # Required for KeyboardInterrupt (DEBUG)
import random # Required for Splash Text requests

# Flashstore Scripts
from Flashstore_RefreshJSON import *

"""
EXTERNAL DEPENDENCIES TO INSTALL:
- WebSockets
"""

ASCII_Banner = "░█▀▀░█░░░█▀█░█▀▀░█░█░█▀▀░█▀█░█▀▄░█▀▄░░░█▀█░█▀█░▀█▀░░░█▀▀░█▀▀░█▀▄░█░█░█▀▀░█▀▄\n\
░█▀▀░█░░░█▀█░▀▀█░█▀█░█░░░█░█░█▀▄░█░█░░░█▀█░█▀▀░░█░░░░▀▀█░█▀▀░█▀▄░▀▄▀░█▀▀░█▀▄\n\
░▀░░░▀▀▀░▀░▀░▀▀▀░▀░▀░▀▀▀░▀▀▀░▀░▀░▀▀░░░░▀░▀░▀░░░▀▀▀░░░▀▀▀░▀▀▀░▀░▀░░▀░░▀▀▀░▀░▀"

"""
Very important almighty Flashstore API Banner
Legends say that removing this banner will cause the world to explode.
"""

# Server Information
Server_Address = socket.gethostname()
Port_RawSocket = 1407
Port_WebSocket = 443
Server_Version = "r240502"
Server_API_Version = 3.2
Server_API_MinimumVersion = 3.0
API_Socket = socket.socket()
Packet_Size = 8192
Debug_Mode = False
Active_Connections = []
Routine_Sleep = 3600

SSL_Cert = "/System/SirioCloudcerts/FlashcordAPI.pem"
SSL_Key = "/System/SirioCloudcerts/FlashcordAPI.key"
SSL_Options = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
SSL_Options.load_cert_chain(SSL_Cert, keyfile=SSL_Key)

# This is useless and is only used once but hey, you never know if you gonna need this useless piece of shit. I swear I'm not a function hoarder.
def Flood(Lines):
    for cycle in range (Lines+1): print("\n")

# Logging System + Getting current time and date in preferred format
def GetTime():
    CTime = time.localtime()
    Time = f"{CTime.tm_hour:02d}:{CTime.tm_min:02d}:{CTime.tm_sec:02d}"
    Date = f"{CTime.tm_mday:02d}-{CTime.tm_mon:02d}-{CTime.tm_year}"
    return Time,Date
def WriteLog(Log,isDebugMessage):
    Time,Date = GetTime()
    LogFile = f"logs/{Date}.log"
    PrintLog = f"[{Time}] {Log}"
    FileLog = f'{PrintLog}\n'
    with open(LogFile, "a", encoding="utf=8") as LogFile:
        LogFile.write(FileLog)
        if isDebugMessage == True and Debug_Mode == True: print(PrintLog)
        elif isDebugMessage == False: print(PrintLog)


# Server Data Loader & Debug Display
def Display_Data():
    WriteLog(f'SYSTEM: Server Data: {Data_Server}',True)
    WriteLog(f'SYSTEM: Module Data: {Data_Modules}',False)
    WriteLog(f'SYSTEM: Plugin Data: {Data_Plugins}',False)
    WriteLog(f'SYSTEM: Theme Data: {Data_Themes}',False)
    WriteLog(f'SYSTEM: User Data: {Data_Users}',False)
    WriteLog(f'SYSTEM: Banned IPs Data: {Data_Banned}',False)
    WriteLog(f'SYSTEM: Splash Text Data: {Data_SplashText}',False)
def GetServerData():
    global Data_Modules,Data_Plugins,Data_Themes,Data_Users,Data_Server,Data_Banned,Data_SplashText,Data_Views,Data_Install
    WriteLog(f'SYSTEM: Refreshing JSON...',False)
    RefreshJSON()
    WriteLog(f'SYSTEM: Loading JSON...',False)
    with open('data.json', 'r', encoding='utf-8') as Data_File:
        Data_Server = json.load(Data_File)
        Data_Modules = Data_Server["modules"]
        Data_Plugins = Data_Server["plugins"]
        Data_Themes = Data_Server["themes"]
        Data_Users = Data_Server["users"]
    with open('banned.dat', 'r', encoding='utf-8') as Banned_File: Data_Banned = Banned_File.read().split("\n")
    with open('splash-text.dat', 'r', encoding='utf-8') as Splash_File:
        Data_SplashText = Splash_File.read().split("\n")
        for line in range (len(Data_SplashText)): Data_SplashText[line] = Data_SplashText[line].replace("[N]","\n")
    Display_Data()
    return Data_Modules,Data_Plugins,Data_Themes,Data_Users,Data_Server,Data_Banned,Data_SplashText


# Server Handlers
def WebSocket_Server():
    async def Websocket_Handler(websocket):
        Address = websocket.remote_address
        Client_Address = str(Address[0])+":"+str(Address[1])
        WriteLog(f'CONNECTION: WebSocket "{Client_Address}".',False)
        await Application_Programming_Interface(websocket,Client_Address,True)
    async def Websocket_Listener():
        WriteLog(f'INFO: Initiated WebSocket Translation Layer.',False)
        async with websockets.serve(Websocket_Handler, "0.0.0.0", Port_WebSocket, ssl=SSL_Options):
            await asyncio.Future()
    asyncio.run(Websocket_Listener())

def Socket_Server():
    async def Socket_Handler(Connection_Socket):
        Client_Socket, Address = Connection_Socket.accept()
        Client_Address = str(Address[0])+":"+str(Address[1])
        WriteLog(f"CONNECTION: {Client_Address} [SUCCESS]",False)
        try: await Application_Programming_Interface(Client_Socket, Client_Address, False)
        except Exception as ErrorInfo: WriteLog(f'DROPPED: {Client_Address}. \n[TRACEBACK]\n{ErrorInfo}\n',True)
    def Socket_Asyncer(Connection_Socket):
        asyncio.run(Socket_Handler(Connection_Socket))
    try: API_Socket.bind((Server_Address, Port_RawSocket))
    except socket.error as ErrorInfo: WriteLog(f"CRITICAL ERROR: Failed to bind the server's address! \n[TRACEBACK]\n{ErrorInfo}\n",False)
    WriteLog(f'SYSTEM: Initiated Socket Server.',False)
    API_Socket.listen()
    while True: Asyncer = threading.Thread(target=Socket_Asyncer(API_Socket)); Asyncer.start()

def ArrayIndexExists(Array,Index):
    try: DummyVar = Array[Index]; return True
    except: return False


# WARNING: Async hell. Why? Because WebSockets are fucking ass and copy plain & errors out if you don't await the .recv()
async def Application_Programming_Interface(Client,Client_Address,isWebSocket):
    # Key Handling Functions
    async def Close_Connection(): 
        #Client_IP = Client_Address.split(); Active_Connections = Active_Connections.remove(Client_IP[0])
        WriteLog(f"CLOSING: {Client_Address}.", False)
        if isWebSocket == True: await Client.close()
        else: Client.close()
    async def Mono_Connection():
        Client_IP = Client_Address.split(":"); Client_IP =  Client_IP[0]
        if Client_IP in Active_Connections: await Code_Already_Connected(); return False
        else: Active_Connections.append(Client_IP)
    async def Receive_Data():
        try:
            if isWebSocket == True: Response = await Client.recv()
            else: Response = (Client.recv(Packet_Size)).decode()
            return Response
        except: WriteLog(f"TIMED OUT: {Client_Address}.", False); await Close_Connection(); return
    async def Send(Packet):
        if isWebSocket == True: await Client.send(str(Packet))
        else: Client.send(str(Packet).encode())
    async def Ban_Check():
        Client_IP = Client_Address.split(":"); Client_IP = Client_IP[0]
        if Client_IP in Data_Banned: await Code_API_Banned(); return True

    # Status Codes
        # General Codes
    async def Code_OK(): WriteLog(f'[OK] -> {Client_Address}', True); await Send("OK")
        # Client Error Codes
            # API Version Codes
    async def Code_Client_Invalid_Version(): WriteLog(f'["INVALID_VERSION"] -> {Client_Address}', True); await Send("INVALID_VERSION"); await Close_Connection()
    async def Code_Client_Outdated(): WriteLog(f'["OUTDATED_VERSION"] -> {Client_Address}', True); await Send("OUTDATED_VERSION"); await Close_Connection()
            # API Request Codes
    async def Code_Not_Found(): WriteLog(f'NOT_FOUND: {Client_Request} from {Client_Address}', False); await Send("NOT_FOUND")
    async def Code_Already_Done(): WriteLog(f'ALREADY_DONE: {Client_Request} from {Client_Address}', False); await Send("ALREADY_DONE")
    async def Code_Invalid_Request(): WriteLog(f'INVALID_REQUEST: {Client_Request} from {Client_Address}', False); await Send("INVALID_REQUEST")
    async def Code_Missing_Arguments(): WriteLog(f'MISSING_ARGUMENTS: {Client_Request} from {Client_Address}', False); await Send("MISSING_ARGUMENTS")
            # Other Codes
    async def Code_Already_Connected(): WriteLog(f'ALREADY_CONNECTED: {Client_Address}', False); await Send("ALREADY_CONNECTED"); await Close_Connection();
    async def Code_API_Banned(): WriteLog(f'API_BANNED: {Client_Address}', False); await Send("API_BANNED")
        # Server Error Codes
    async def Code_Server_Outdated(): WriteLog(f'["OUTDATED_SERVER"] -> {Client_Address}', True); await Send("OUTDATED_SERVER")

    # Important Handling Functions
    async def CheckVersion():
        if await Ban_Check() == True: return False
        #if await Mono_Connection() == False: return False
        Client_Data = await Receive_Data()
        try: Client_Version = float(Client_Data)
        except: WriteLog(f'API Version Check // ERROR: {Client_Address} Invalid "{Client_Data}" API Version!', False); await Code_Client_Invalid_Version(); return False
        if Client_Version == Server_API_Version: WriteLog(f'API Version Check // [OK] {Client_Address}@API_{Client_Data}', False); await Code_OK(); return True
        elif Client_Version > Server_API_MinimumVersion: WriteLog(f'API Version Check // [WARNING] {Client_Address}@API_{Client_Data} is older but still accepted.', False); await Code_Server_Outdated(); return True
        elif Client_Version < Server_API_MinimumVersion: WriteLog(f'API Version Check // [ERROR] {Client_Address}@API_{Client_Data} is outdated!', False); await Code_Client_Outdated(); return False
    async def SearchNSend(Selected_Data, Selected_User):
        cycle = 0
        for cycle in range (len(Selected_Data)):
            if Selected_User in Selected_Data[cycle]: await Send(Selected_Data[cycle][Selected_User]); return cycle
        return None
    async def HotJSON_Write_ViewInst(CheckWhichFile):
        with open(CheckWhichFile, "r", encoding="utf-8") as File: HotJSON = json.load(File)
        if Client_Request[2] in HotJSON:
            Client_IP = Client_Address.split(":"); Client_IP = Client_IP[0]
            if Client_IP in HotJSON[Client_Request[2]]: WriteLog(f'[ERROR] IP Address {Client_IP} is already in {Client_Request[2]} of {CheckWhichFile}!', False);  await Code_Already_Done()
            else: 
                with open(CheckWhichFile, "w", encoding="utf-8") as File:
                    TempArray = HotJSON[Client_Request[2]]; TempArray.append(Client_IP)
                    HotJSON[Client_Request[2]] = TempArray; File.write(json.dumps(HotJSON, indent = 1))
                    WriteLog(f'[SUCCESS] Added IP Address {Client_IP} for {Client_Request[2]} in {CheckWhichFile}.', False); await Code_OK()
        else: await Code_Not_Found()
    async def HotJSON_Read_ViewInst(CheckWhichFile):
        with open(CheckWhichFile, "r", encoding="utf-8") as File: HotJSON = json.load(File)
        if Client_Request[2] in HotJSON: XCount = len(HotJSON[Client_Request[2]]); WriteLog(f'[SUCCESS] "{XCount}" -> {Client_Address}.', False); await Send(XCount)
        else: await Code_Not_Found()
    async def HotJSON_AllData(CheckWhichFile):
        TempDict = {}
        with open(CheckWhichFile, "r", encoding="utf-8") as File: HotJSON = json.load(File)
        for cycle in HotJSON: TempDict[cycle] = len(HotJSON[cycle])
        WriteLog(f'[SUCCESS] "{CheckWhichFile} (IP-less)" -> {Client_Address}.', False); await Send(TempDict)
    async def RepluggedProxy(GetWhat):
        WriteLog(f"Parsing Replugged {GetWhat}...", True)
        if GetWhat == "Plugins": Replugged_URL = "https://replugged.dev/api/store/list/plugin?page=1&items=100"
        else: Replugged_URL = "https://replugged.dev/api/store/list/theme?page=1&items=100"
        API = urllib.request.Request(
            Replugged_URL, 
            data=None, 
            headers={'User-Agent': f'Flashcord-API_CORS-Proxy/{Server_API_Version}'}
        )
        API_Result = json.load(urllib.request.urlopen(API))
        WriteLog(f'[SUCCESS] "[REPLUGGED API // {GetWhat}]" -> {Client_Address}', False); await Send(str(API_Result))
    # Server Logic (if statement hell // r240201 Update: I forgot switch statements existed lol, this is much better.)
    if await CheckVersion() == True:
        Client_Request = (await Receive_Data()).split("/")
        if Client_Request != None:
            WriteLog(f'REQUEST: {Client_Request} from {Client_Address}.', False)
            if Client_Request != ['']:
                match Client_Request[0]:
                    case "GET":
                        if ArrayIndexExists(Client_Request, 1) == True:
                            match Client_Request[1]:
                                case "MODULES":
                                    if ArrayIndexExists(Client_Request, 2) == True:
                                        Search_Result = await SearchNSend(Data_Modules, Client_Request[2].lower())
                                        if Search_Result != None: WriteLog(f'[SUCCESS] "Data_Modules[{Search_Result}][{Client_Request[2]}]" -> {Client_Address}.', False)
                                        else: await Code_Not_Found()
                                    else: WriteLog(f'[SUCCESS] "Data_Modules" -> {Client_Address}.', False); await Send(Data_Modules)
                                case "PLUGINS":
                                    if ArrayIndexExists(Client_Request, 2) == True:
                                        Search_Result = await SearchNSend(Data_Plugins, Client_Request[2].lower())
                                        if Search_Result != None: WriteLog(f'[SUCCESS] "Data_Plugins[{Search_Result}][{Client_Request[2]}]" -> {Client_Address}.', False)
                                        else: await Code_Not_Found()
                                    else: WriteLog(f'[SUCCESS] "Data_Plugins" -> {Client_Address}.', False); await Send(Data_Plugins)
                                case "THEMES":
                                    if ArrayIndexExists(Client_Request, 2) == True:
                                        Search_Result = await SearchNSend(Data_Themes, Client_Request[2].lower())
                                        if Search_Result != None: WriteLog(f'[SUCCESS] "Data_Themes[{Search_Result}][{Client_Request[2]}]" -> {Client_Address}.', False)
                                        else: await Code_Not_Found()
                                    else: WriteLog(f'[SUCCESS] "Data_Themes" -> {Client_Address}.', False); await Send(Data_Themes)
                                case "VIEWS":
                                    if ArrayIndexExists(Client_Request, 2) == True: await HotJSON_Read_ViewInst("views.json")
                                    else: await HotJSON_AllData("views.json")
                                case "INSTALLS":
                                    if ArrayIndexExists(Client_Request, 2) == True: await HotJSON_Read_ViewInst("installs.json")
                                    else: await HotJSON_AllData("installs.json")
                                case "USERS": WriteLog(f'[SUCCESS] "Data_Users" -> {Client_Address}.', False); await Send(Data_Users)
                                case "SERVER_VERSION": WriteLog(f'[SUCCESS] "Server_Version" -> {Client_Address}.', False); await Send(Server_Version)
                                case "API_VERSION": WriteLog(f'[SUCCESS] "Server_API_Version" -> {Client_Address}.', False); await Send(Server_API_Version)
                                case "SPLASH_TEXT":
                                    Selected_Splash = Data_SplashText[random.randint(0,len(Data_SplashText) - 1)]
                                    WriteLog(f'[SUCCESS] "{Selected_Splash}" -> {Client_Address}.', False); await Send(Selected_Splash)
                                case "REPLUGGED":
                                    if ArrayIndexExists(Client_Request, 2) == True:
                                        match Client_Request[2]:
                                            case "PLUGINS": await RepluggedProxy("Plugins")
                                            case "THEMES": await RepluggedProxy("Themes")
                                            case _: await Code_Invalid_Request()
                                    else: await Code_Missing_Arguments()
                                case _: await Code_Invalid_Request()
                        else: WriteLog(f'[SUCCESS] "Data_Server" -> {Client_Address}', False); await Send(Data_Server)
                    case "ADD_STAT":
                        if ArrayIndexExists(Client_Request, 1) == True:
                            match Client_Request[1]:
                                case "VIEWS":
                                    if ArrayIndexExists(Client_Request, 2) == True: await HotJSON_Write_ViewInst("views.json")
                                    else: await Code_Missing_Arguments()
                                case "INSTALLS":
                                    if ArrayIndexExists(Client_Request, 2) == True: await HotJSON_Write_ViewInst("installs.json")
                                    else: await Code_Missing_Arguments()
                                case _: await Code_Invalid_Request()
                        else: await Code_Missing_Arguments()
                    case _: await Code_Invalid_Request()
            else: WriteLog(f"[ERROR] {Client_Address} sent an empty request!", False)
        else: WriteLog(f"[ERROR] {Client_Address} didn't send new data.", False)
    await Close_Connection()
    return

# Glorious.
def SplashBanner():
    Flood(16)
    print(ASCII_Banner)
    WriteLog(f"{Server_Address}:{Port_RawSocket}@API_{Server_API_Version}-{Server_API_MinimumVersion}/{Server_Version} // Debug: {Debug_Mode} - Packet Size: {Packet_Size}b\n", False)

"""

- "Hey Sirius, what happens when you start the Flashstore API?"

...

It starts with
one thing
I don't know why,
it doesn't even matter how hard you try
keep that in mind I designed this rhyme to explain in due time that [all I know]
Time is a valuable thing,
watch it fly by as the pendulum swings,
the clock ticks life away,
it's so unreal.
Didn't look out below,
watch the time go out the window,
didn't even know,
I wasted all that time just to [watch you [go]]
Even though I tried,
it all fell apart.
What it eventually means to me,
will be a memory
of a time [I tried so hard.]
And got so far,
but in the end,
it doesn't even matter...

Okay I'm going insane. That's all I remember of the song, go fuck yourself.
Go add the rest of the lyrics yourself.

"""
def Bootstrap():
    global Active_Connections
    SplashBanner()
    WriteLog(f'SYSTEM: Initializing server...',False)

    # Retrieve server data
    Data_Modules,Data_Plugins,Data_Themes,Data_Users,Data_Server,Data_Banned,Data_SplashText = GetServerData()
    WebSocket_Thread = threading.Thread(target=WebSocket_Server); WebSocket_Thread.start()
    Socket_Thread = threading.Thread(target=Socket_Server); Socket_Thread.start()
    WriteLog(f'SYSTEM: Server initialized.',False)
    try: # Post-Execution Routine
        while True: 
            WriteLog(f'SYSTEM: Routine sleeping for now {Routine_Sleep} seconds.', False)
            time.sleep(Routine_Sleep)
            # There would be more code here, but right now I'm lazy.
            WriteLog(f'SYSTEM: Executing Routine.', False)
            Data_Modules,Data_Plugins,Data_Themes,Data_Users,Data_Server,Data_Banned,Data_SplashText = GetServerData()
    except KeyboardInterrupt:
        try: sys.exit(130)
        except SystemExit: os._exit(130)

# Spark
if __name__== '__main__': Bootstrap()
else: print("The fuck you doing m8? This isn't a module!")

