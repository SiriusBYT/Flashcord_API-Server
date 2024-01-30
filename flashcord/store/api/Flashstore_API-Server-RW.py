# Server Modules
import socket # API's Native Language 
import websockets # API's Translated Language

# Multi-threading modules
import asyncio # Required for WebSockets
import _thread # Required for multi-client raw socket clients.
import threading # Required for WebSockets

# Miscellaneous Modules
import time # Required for logs
import json # Server Data is in JSON format
import os # Required for KeyboardInterrupt (DEBUG)
import sys # Required for KeyboardInterrupt (DEBUG)

# Flashstore Scripts
from Flashstore_RefreshJSON import *

"""
EXTERNAL DEPENDENCIES TO INSTALL:
- WebSockets
"""

ASCII_Banner = " ▄▄▄▄▄▄▄ ▄▄▄     ▄▄▄▄▄▄ ▄▄▄▄▄▄▄ ▄▄   ▄▄ ▄▄▄▄▄▄▄ ▄▄▄▄▄▄▄ ▄▄▄▄▄▄▄ ▄▄▄▄▄▄   ▄▄▄▄▄▄▄    ▄▄▄▄▄▄▄ ▄▄▄▄▄▄▄ ▄▄▄ \n\
█       █   █   █      █       █  █ █  █       █       █       █   ▄  █ █       █  █       █       █   █ \n\
█    ▄▄▄█   █   █  ▄   █  ▄▄▄▄▄█  █▄█  █  ▄▄▄▄▄█▄     ▄█   ▄   █  █ █ █ █    ▄▄▄█  █   ▄   █    ▄  █   █ \n\
█   █▄▄▄█   █   █ █▄█  █ █▄▄▄▄▄█       █ █▄▄▄▄▄  █   █ █  █ █  █   █▄▄█▄█   █▄▄▄   █  █▄█  █   █▄█ █   █ \n\
█    ▄▄▄█   █▄▄▄█      █▄▄▄▄▄  █   ▄   █▄▄▄▄▄  █ █   █ █  █▄█  █    ▄▄  █    ▄▄▄█  █       █    ▄▄▄█   █ \n\
█   █   █       █  ▄   █▄▄▄▄▄█ █  █ █  █▄▄▄▄▄█ █ █   █ █       █   █  █ █   █▄▄▄   █   ▄   █   █   █   █ \n\
█▄▄▄█   █▄▄▄▄▄▄▄█▄█ █▄▄█▄▄▄▄▄▄▄█▄▄█ █▄▄█▄▄▄▄▄▄▄█ █▄▄▄█ █▄▄▄▄▄▄▄█▄▄▄█  █▄█▄▄▄▄▄▄▄█  █▄▄█ █▄▄█▄▄▄█   █▄▄▄█ \
"
"""
Very important almighty Flashstore API Banner
Legends say that removing this banner will cause the world to explode.
"""

# Server Information
Server_Address = socket.gethostname()
Server_Port = 1407
Server_Version = "r240129"
Server_API_Version = 3.0
API_Socket = socket.socket()
Packet_Size = 1024
DebugMode = False

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
    Time,Data = GetTime()
    LogFile = f"logs/{Data}.log"
    PrintLog = f"[{Time}] {Log}"
    FileLog = f'{PrintLog}\n'
    with open(LogFile, "a", encoding="utf=8") as LogFile:
        LogFile.write(FileLog)
        if isDebugMessage == True and DebugMode == True: print(PrintLog)
        elif isDebugMessage == False: print(PrintLog)

# Server Data Loader & Debug Display
def Display_Data():
    WriteLog(f'SYSTEM: Server Data: {Data_Server}',True)
    WriteLog(f'SYSTEM: Module Data: {Data_Modules}',False)
    WriteLog(f'SYSTEM: Plugin Data: {Data_Plugins}',False)
    WriteLog(f'SYSTEM: Theme Data: {Data_Themes}',False)
    WriteLog(f'SYSTEM: User Data: {Data_Users}',False)
def GetServerData():
    global Data_Modules,Data_Plugins,Data_Themes,Data_Users,Data_Server
    WriteLog(f'SYSTEM: Refreshing JSON...',False)
    RefreshJSON()
    WriteLog(f'SYSTEM: Loading JSON...',False)
    with open('data.json', 'r', encoding='utf-8') as Data_File:
        Data_Server = json.load(Data_File)
        Data_Modules = Data_Server["modules"]
        Data_Plugins = Data_Server["plugins"]
        Data_Themes = Data_Server["themes"]
        Data_Users = Data_Server["users"]
    Display_Data()
    return Data_Modules,Data_Plugins,Data_Themes,Data_Users,Data_Server



# Server Handlers
def WebSocket_Server():
    async def Websocket_Handler(websocket):
        Address = websocket.remote_address
        Client_Address = str(Address[0])+":"+str(Address[1])
        WriteLog(f'SUCCESS: New WebSocket connection from "{Client_Address}".',False)
        await Application_Programming_Interface(websocket,Client_Address,True)
    async def Websocket_Listener():
        WriteLog(f'INFO: Initiated WebSocket Translation Layer.',False)
        async with websockets.serve(Websocket_Handler, "localhost", 1407):
            await asyncio.Future()
    asyncio.run(Websocket_Listener())

def Socket_Server():
    def Socket_Handler(Connection_Socket):
        Address = Connection_Socket.accept()
        Client_Address = str(Address[0])+":"+str(Address[1])
        WriteLog(f"CONNECTION: {Client_Address} [SUCCESS]",True)
        try: _thread.start_new_thread(Application_Programming_Interface, (Connection_Socket, Client_Address, False))
        except Exception as ErrorInfo: WriteLog(f'DROPPED: {Client_Address}. \n[TRACEBACK]\n{ErrorInfo}\n',True)
    try: API_Socket.bind((Server_Address, Server_Port))
    except socket.error as ErrorInfo: WriteLog(f"CRITICAL ERROR: Failed to bind the server's address! \n[TRACEBACK]\n{ErrorInfo}\n",False)
    WriteLog(f'SYSTEM: Initiated Socket Server.',False)
    API_Socket.listen()
    while True: Socket_Handler(API_Socket)

# WARNING: Async hell. Why? Because WebSockets are fucking ass and complain & errors out if you don't await the .recv()
async def Application_Programming_Interface(Client,Client_Address,isWebSocket):
    # Key Handling Functions
    async def Close_Connection(): WriteLog(f"CLOSING: {Client_Address}.", False); await Client.close()
    async def ReceiveData():
        try:
            if isWebSocket == True: Response = await Client.recv()
            else: Response = await Client.recv(Packet_Size).decode()
        except: WriteLog(f"TIMED OUT: {Client_Address}.", False); await Close_Connection(); return
        return Response
    async def Send(Packet):
        if isWebSocket == True: await Client.send(Packet)
        else: await Client.send(Packet).encode()
        
    # Status Codes
        # General Codes
    async def Code_OK(): WriteLog(f'[OK] -> {Client_Address}', True); await Send("OK")
        # Client Error Codes
    async def Code_Client_Invalid_Version(): WriteLog(f'["INVALID_VERSION"] -> {Client_Address}', True); await Send("INVALID_VERSION"); await Close_Connection()
    async def Code_Client_Outdated(): WriteLog(f'["OUTDATED_VERSION"] -> {Client_Address}', True); await Send("OUTDATED_VERSION"); await Close_Connection()
        # Server Error Codes
    async def Code_Server_Outdated(): WriteLog(f'["OUTDATED_SERVER"] -> {Client_Address}', True); await Send("OUTDATED_SERVER")

    # Important Handling Functions
    async def CheckVersion():
        Client_Data = await ReceiveData()
        try: Client_Version = float(Client_Data)
        except: WriteLog(f'API Version Check // ERROR: {Client_Address} Invalid "{Client_Data}" API Version!', False); await Code_Client_Invalid_Version(); return
        if Client_Version == Server_API_Version: WriteLog(f'API Version Check // OK: {Client_Address}@API_"{Client_Data}"', False); await Code_OK(); return True
        elif Client_Version > Server_API_Version: WriteLog(f'API Version Check // WARNING: {Client_Address}@API_"{Client_Data}" is newer.', False); await Code_Server_Outdated(); return True
        elif Client_Version < Server_API_Version: WriteLog(f'API Version Check // ERROR: {Client_Address}@API_"{Client_Data}" is outdated!', False); await Code_Client_Outdated(); return False


    # Server Logic
    shouldProceed = await CheckVersion()
    if shouldProceed == True:
        Client_Request = await ReceiveData()
        if Client_Request != None:
            Client_Request = Client_Request.split("/")
            print(f"wow it worked {Client_Request}")
        else:
            WriteLog(f"ERROR: {Client_Address} didn't send new data.", False)
            await Close_Connection()
            return
    else: return

# Glorious.
def SplashBanner():
    Flood(16)
    print(ASCII_Banner)
    print(f"{Server_Address}:{Server_Port}@API_{Server_API_Version}/{Server_Version} // Debug: {DebugMode} - Packet Size: {Packet_Size}b\n")

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
    SplashBanner()
    WriteLog(f'SYSTEM: Initializing server...',False)

    # Retrieve server data
    Data_Modules,Data_Plugins,Data_Themes,Data_Users,Data_Server = GetServerData()
    WebSocket_Thread = threading.Thread(target=WebSocket_Server); WebSocket_Thread.start()
    Socket_Thread = threading.Thread(target=Socket_Server); Socket_Thread.start()
    WriteLog(f'SYSTEM: Server initialized.',False)
    try: 
        # Server Routine after Server Execution
        while True: 
            time.sleep(1)
            # There would be more code here, but right now I'm lazy.
    except KeyboardInterrupt:
        try: sys.exit(130)
        except SystemExit: os._exit(130)

# Spark
if __name__== '__main__': Bootstrap()
else: print("The fuck you doing m8? This isn't a module!")