import socket
import time
import _thread
import asyncio
import websockets
import threading

# Server Information
ServerAddress = socket.gethostname()
ServerPort = 1407
ServerVersion = "r240129"
PacketSize = 1024
API_Socket = socket.socket()
API_Version = 2.02
DebugMode = True

# Logging System
def GetLogTime():
    LogTime = time.localtime()
    LogTime_String = f"{LogTime.tm_hour:02d}:{LogTime.tm_min:02d}:{LogTime.tm_sec:02d} - {LogTime.tm_mday:02d}/{LogTime.tm_mon:02d}/{LogTime.tm_year}"
    return LogTime_String
def WriteToLog(Log,isDebugMessage):
    LogTime = GetLogTime()
    LogFile = "api.log"
    FullLog = f"[{LogTime} // FsAPI Server] {Log}"
    FullLogToFile = f'{FullLog}\n'
    with open(LogFile, "a", encoding="utf=8") as LogFile:
        LogFile.write(FullLogToFile)
        if isDebugMessage == True and DebugMode == True: print(FullLog)
        elif isDebugMessage == False: print(FullLog)

# Server Data Loader
def GetServerData(GetWhat):
    if GetWhat == "Modules":
        with open('modules.dat', 'r', encoding='utf-8') as Data_File:
            Data = Data_File.read().replace(" ", "").replace(":", "\n").split("\n")
            return Data
    elif GetWhat == "Plugins":
        with open('plugins.dat', 'r', encoding='utf-8') as Data_File:
            Data = Data_File.read().replace(" ", "").replace(":", "\n").split("\n")
            return Data
    elif GetWhat == "Users":
        with open('users.dat', 'r', encoding='utf-8') as Data_File:
            Data = Data_File.read().replace(" ", "").replace(":", "\n").split("\n")
            return Data

# Status Codes
    # API Connection
def ServerOutdated(RemoteClient, ClientAddress):
    try: RemoteClient.send(str.encode('SERVER-OUTDATED_API-VERSION'))
    except socket.timeout:
        LogString = f'INFO: {ClientAddress} timed out before we told them our API Version is outdated!'
        WriteToLog(LogString,False)
        RemoteClient.close()

def ClientOutdated(RemoteClient, ClientAddress):
    try: RemoteClient.send(str.encode('CLIENT-OUTDATED_API-VERSION'))
    except socket.timeout:
        LogString = f'INFO: {ClientAddress} timed out before we told them their API Version is outdated!'
        WriteToLog(LogString,False)
    RemoteClient.close()

def InvalidVersion(RemoteClient, ClientAddress):
    try: RemoteClient.send(str.encode('INVALID_API-VERSION'))
    except socket.timeout:
        LogString = f'INFO: {ClientAddress} timed out before we told them their API Version is invalid!'
        WriteToLog(LogString,False)
    RemoteClient.close()

def OK(RemoteClient, ClientAddress):
    try: RemoteClient.send(str.encode('OK'))
    except socket.timeout:
        LogString = f'INFO: {ClientAddress} timed out before we told them everything was okay!'
        WriteToLog(LogString,False)
        RemoteClient.close()

    # Closing Status Codes
        # Arguments Error
def MissingArguments(RemoteClient, API_Request, ClientAddress):
    LogString = f'WARNING: {ClientAddress} sent out request "{API_Request}" but it is missing arguments!'
    WriteToLog(LogString,False)
    try: RemoteClient.send(str.encode('MISSING_ARGUMENTS'))
    except:
        LogString = f'WARNING: {ClientAddress} timed out while telling that their "{API_Request}" request is missing arguments!'
        WriteToLog(LogString,False)
    RemoteClient.close()

def InvalidArguments(RemoteClient, API_Request, ClientAddress):
    LogString = f'WARNING: {ClientAddress} sent out invalid request "{API_Request}"!'
    WriteToLog(LogString,False)
    try: RemoteClient.send(str.encode('INVALID_ARGUMENTS'))
    except:
        LogString = f'WARNING: {ClientAddress} timed out while telling that their "{API_Request}" request was invalid!'
        WriteToLog(LogString,False)
    RemoteClient.close()

        # Request Errors
def NotFound(RemoteClient, API_Request, ClientAddress):
    LogString = f'WARNING: {ClientAddress} sent out request "{API_Request}" but the result could not be found!'
    WriteToLog(LogString,False)
    try: RemoteClient.send(str.encode('NOT_FOUND'))
    except socket.timeout:
        LogString = f'WARNING: {ClientAddress} timed out while telling that the result to their "{API_Request}" request could not be found!'
        WriteToLog(LogString,False)
    RemoteClient.close()

    # Miscellaneous Codes
def Sending(RemoteClient, ClientAddress):
    try: RemoteClient.send(str.encode('SENDING'))
    except socket.timeout:
        LogString = f'INFO: {ClientAddress} timed out before we told them we were ready to send data!'
        WriteToLog(LogString,False)
        RemoteClient.close()

def UnknownError(RemoteClient, ClientAddress):
    try: RemoteClient.send(str.encode('UNKNOWN_ERROR'))
    except socket.timeout:
        LogString = f'INFO: {ClientAddress} timed out before we told them an unknown error occurred!'
        WriteToLog(LogString,False)
    RemoteClient.close()

# API Arguments Checkers
def isPreciseRequest(API_Request):
    isPreciseRequest = True
    try: DummyVar = API_Request[2]
    except:
        isPreciseRequest = False
    return isPreciseRequest

def isMissingArgument(API_Request):
    isMissingArgument = False
    try: DummyVar = API_Request[1]
    except:
        isMissingArgument = True
    return isMissingArgument


def FlashStore_API():
    LogString = f'INFO: Initializing server on {ServerAddress}:{ServerPort}, running Flashstore API Version {API_Version} and Flashstore API Server version {ServerVersion}.'
    WriteToLog(LogString,False)

    # Server Initialization
    ModuleData = GetServerData("Modules")
    PluginData = GetServerData("Plugins")
    UserData = GetServerData("Users")
    LogString = f'INFO: Loading "{ModuleData}" as Module Data.'
    WriteToLog(LogString,False)
    LogString = f'INFO: Loading "{PluginData}" as Plugin Data.'
    WriteToLog(LogString,False)
    LogString = f'INFO: Loading "{UserData}" as User Data.'
    WriteToLog(LogString,False)

    def FillRequest(RemoteClient, RequestData, ClientAddress):
        try:
            Sending(RemoteClient, ClientAddress)
        except Exception as ErrorInfo:
            LogString = f"ERROR: Unknown Error while full-filling request.\n[ERROR TRACEBACK]\n{ErrorInfo}\n"
            WriteToLog(LogString,False)
        while True:
            try:
                RemoteClient_Response = RemoteClient.recv(PacketSize).decode()
            except socket.timeout:
                LogString = f"WARNING: {ClientAddress} timed out while full-filling request."
                WriteToLog(LogString,False)
                break
            if RemoteClient_Response == "READY":
                try:
                    LogString = f'INFO: Sending "{RequestData}" to {ClientAddress}.'
                    WriteToLog(LogString,False)
                    RemoteClient.send(str.encode(RequestData))
                    break
                except socket.timeout:
                    LogString = f"WARNING: {ClientAddress} timed out while full-filling request despite them being ready."
                    WriteToLog(LogString,False)

        LogString = f"INFO: Reached the end of the Fill-Request loop for {ClientAddress}."
        WriteToLog(LogString,True)
        RemoteClient.close()
    async def ReceiveData():
        if isWebSocket == False: RemoteClient_Response = RemoteClient.recv(PacketSize).decode()
        else: RemoteClient_Response = await RemoteClient.recv()
        return RemoteClient_Response
    
    def API_Version_Checker(RemoteClient, ClientAddress, isWebSocket):
        RemoteClient_Response = ReceiveData(RemoteClient,ClientAddress,isWebSocket)
        try:
            Client_API = float(RemoteClient_Response)
        except:
            LogString = f'[ERROR] {ClientAddress} requested invalid API Version "{RemoteClient_Response}"!'
            WriteToLog(LogString,False)
            InvalidVersion(RemoteClient, ClientAddress)
            return "QUIT"

        if Client_API == API_Version:
            LogString = f'[OK] {ClientAddress} requested API Version "{RemoteClient_Response}"'
            WriteToLog(LogString,False)
            OK(RemoteClient, ClientAddress)
        elif Client_API > API_Version:
            LogString = f'[WARNING] {ClientAddress} requested API Version "{RemoteClient_Response}", but the API Version running is {API_Version}!'
            WriteToLog(LogString,False)
            ServerOutdated(RemoteClient, ClientAddress)
        else:
            LogString = f'[ERROR] {ClientAddress} requested outdated API Version "{RemoteClient_Response}", but the API Version running is {API_Version}!'
            WriteToLog(LogString,False)
            ClientOutdated(RemoteClient, ClientAddress)
        return "PROCEED"
        
    def API_Deliverer(RemoteClient, ClientAddress):
        VersionCheck = API_Version_Checker(RemoteClient, ClientAddress)
        if VersionCheck == "QUIT": return
        while True:
            try:
                RemoteClient_Response = RemoteClient.recv(PacketSize).decode()
            except socket.timeout:
                LogString = f"WARNING: {ClientAddress} timed out while attempting to receive their request."
                WriteToLog(LogString,False)
                break
            LogString = f'[INFO] {ClientAddress} requested "{RemoteClient_Response}".'
            WriteToLog(LogString,False)
            API_Request = RemoteClient_Response.replace("/"," ").split()
            if API_Request[0] == "GET":
                    if isMissingArgument(API_Request) == False:
                        if API_Request[1] == "MODULES":  
                            if isPreciseRequest(API_Request) == True:
                                try:
                                    FillRequest(RemoteClient, ModuleData[ModuleData.index(API_Request[2].lower()) + 1], ClientAddress)
                                    break
                                except:
                                    NotFound(RemoteClient, str(API_Request), ClientAddress)
                                    break
                            else:
                                FillRequest(RemoteClient, str(ModuleData), ClientAddress)
                                break

                        elif API_Request[1] == "PLUGINS":
                            if isPreciseRequest(API_Request) == True:
                                try:
                                    FillRequest(RemoteClient, PluginData[PluginData.index(API_Request[2].lower()) + 1], ClientAddress)
                                    break
                                except:
                                    NotFound(RemoteClient, str(API_Request), ClientAddress)
                                    break
                            else:
                                FillRequest(RemoteClient, str(PluginData), ClientAddress)
                                break
                                
                        elif API_Request[1] == "USERS":
                            FillRequest(RemoteClient, str(UserData), ClientAddress)
                            break
                        else:
                            InvalidArguments(RemoteClient, str(API_Request), ClientAddress)
                            break
                    else:
                        MissingArguments(RemoteClient, str(API_Request), ClientAddress)
                        break
            else:
                InvalidArguments(RemoteClient, str(API_Request), ClientAddress)
                break
        LogString = f"INFO: Reached the end of the API Deliverer loop for {ClientAddress}."
        WriteToLog(LogString,True)
        RemoteClient.close()

    def IncomingConnection(Connection_Socket):
        Client, Address = Connection_Socket.accept()
        ClientAddress = str(Address[0])+":"+str(Address[1])
        LogString = f"SUCCESS: Incoming connection from {ClientAddress}."
        WriteToLog(LogString,True)
        try:
            _thread.start_new_thread(API_Deliverer, (Client,ClientAddress))
        except Exception as ErrorInfo:
            LogString = f'INFO: Giving up delivering the request for {ClientAddress}. \n[ERROR TRACEBACK]\n{ErrorInfo}\n'
            WriteToLog(LogString,True)

    # Websocket Translation Layer
    def WebSocket_Server():
        async def TransferLayer(websocket):
            Client, Address = websocket.remote_address
            ClientAddress = str(Client)+":"+str(Address)
            LogString = f'SUCCESS: New WebSocket connection from "{ClientAddress}".'
            WriteToLog(LogString,False)
            #async for message in websocket:
            VersionCheck = await API_Version_Checker(websocket, ClientAddress, "True")
            if VersionCheck == "QUIT": return
            API_Result = FillRequest(message)
            await websocket.send(str(API_Result))

        async def TranslationLayer():
            LogString = f'INFO: Initiated WebSocket Translation Layer.'
            WriteToLog(LogString,False)
            async with websockets.serve(TransferLayer, "localhost", 1407):
                await asyncio.Future()

        asyncio.run(TranslationLayer())

    WebSocketThread = threading.Thread(target=WebSocket_Server)
    WebSocketThread.start()

    try:
        API_Socket.bind((ServerAddress, ServerPort))
    except socket.error as ErrorInfo:
        LogString = f"ERROR: Failed to bind the server's address! \n[ERROR TRACEBACK]\n{ErrorInfo}\n"
        WriteToLog(LogString,False)
    LogString = f'INFO: Initiated Socket Server.'
    WriteToLog(LogString,False)
    API_Socket.listen()
          
    while True:
        IncomingConnection(API_Socket)

FlashStore_API()

