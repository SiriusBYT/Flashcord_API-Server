import socket
import time
import _thread

def FlashStore_API():
    # Server Information
    ServerAddress = socket.gethostname()
    ServerPort = 1407
    PacketSize = 1024
    API_Socket = socket.socket()
    API_Version = 2.01
    DebugMode = True
    MaxTimeoutCount = 3
    MaxIdleCount = 3
    RetryDelay = 5

    def FillRequest(RemoteClient, RequestData, ClientAddress):
        try:
            Sending(RemoteClient)
        except Exception as ErrorInfo:
            print(f'[Flashstore API // Server] An unknown error occurred while full-filling request. "{ErrorInfo}"')
        TimeoutCount = 0
        while True:
            RemoteClient_Response = RemoteClient.recv(PacketSize).decode()
            if TimeoutCount == MaxTimeoutCount:
                print(f'[Flashstore API // Server] {ClientAddress} timed out.')
                break
            elif RemoteClient_Response == "READY":
                try:
                    print(f'[Flashstore API // Server] Sending to {ClientAddress} the data "{RequestData}".')
                    RemoteClient.send(str.encode(RequestData))
                    Done(RemoteClient)
                    break
                except:
                    if DebugMode == True: print(f"[Flashstore API // Server] WARNING: TIMEOUT({TimeoutCount}/{MaxTimeoutCount}) // Couldn't get new data from {ClientAddress}")
                    TimeoutCount+=1
                    time.sleep(RetryDelay)
            else:
                if DebugMode == True: print(f"[Flashstore API // Server] WARNING: TIMEOUT({TimeoutCount}/{MaxTimeoutCount}) // Couldn't get new data from {ClientAddress}")
                TimeoutCount+=1
                time.sleep(RetryDelay)
        if DebugMode == True: print(f'[Flashstore API // Server] NOTICE: FillRequest Reached end of loop.')
        RemoteClient.close()

    def isPreciseRequest(API_Request):
        isPreciseRequest = True
        try:
            DummyVar = API_Request[2]
        except:
            isPreciseRequest = False
        return isPreciseRequest
    
    def isMissingArgument(API_Request):
        isMissingArgument = False
        try:
            DummyVar = API_Request[1]
        except:
            isMissingArgument = True
        return isMissingArgument
    
    def API_Deliverer(RemoteClient, ClientAddress):
        RemoteClient_Response = RemoteClient.recv(PacketSize).decode()
        if float(RemoteClient_Response) < API_Version:
            print(f'[Flashstore API // Server] {ClientAddress} Requested API Version: {RemoteClient_Response}. [INVALID_API-VERSION]')
            InvalidVersion(RemoteClient)
        else:
            if float(RemoteClient_Response) == API_Version:
                print(f'[Flashstore API // Server] {ClientAddress} Requested API Version: {RemoteClient_Response}. [OK]')
                OK(RemoteClient)
            else:
                print(f'[Flashstore API // Server] {ClientAddress} Requested API Version: {RemoteClient_Response}. [SERVER-OUTDATED_API-VERSION]')
                ServerOutdated(RemoteClient)
        TimeoutCount = 0
        IdleCount = 0
        while True:
            try:
                RemoteClient_Response = RemoteClient.recv(PacketSize).decode()
            except:
                if DebugMode == True: print(f"[Flashstore API // Server] WARNING: TIMEOUT({TimeoutCount}/{MaxTimeoutCount}) // Couldn't get new data from {ClientAddress}")
                TimeoutCount+=1
                time.sleep(RetryDelay)

            if TimeoutCount == MaxTimeoutCount:
                print(f'[Flashstore API // Server] INFO: {ClientAddress} timed out.')
                break
            elif IdleCount == MaxIdleCount:
                print(f'[Flashstore API // Server] WARNING: {ClientAddress} idled for too long..')
                break
            else:
                if RemoteClient_Response == "":
                    if DebugMode == True: print(f"IDLE: {IdleCount}/{MaxIdleCount} Didn't get new data from {ClientAddress}")
                    IdleCount+=1
                    time.sleep(RetryDelay)
                else:
                    print(f'[Flashstore API // Server] Received Request: "{RemoteClient_Response}".')
                    API_Request = RemoteClient_Response.replace("/"," ").split()
                    if API_Request[0] == "GET":
                            if isMissingArgument(API_Request) == False:
                                if API_Request[1] == "MODULES":  
                                    print(isPreciseRequest(API_Request))
                                    print(API_Request[2])
                                    if isPreciseRequest(API_Request) == True:
                                        try:
                                            FillRequest(RemoteClient, ModuleData[ModuleData.index(API_Request[2].lower()) + 1], ClientAddress)
                                        except:
                                            NotFound(RemoteClient)
                                    else:
                                        FillRequest(RemoteClient, str(ModuleData), ClientAddress)

                                elif API_Request[1] == "PLUGINS":
                                    if isPreciseRequest(API_Request) == True:
                                        try:
                                            FillRequest(RemoteClient, PluginData[PluginData.index(API_Request[2].lower()) + 1], ClientAddress)
                                        except:
                                            NotFound(RemoteClient)
                                    else:
                                        FillRequest(RemoteClient, str(PluginData), ClientAddress)
                                        
                                elif API_Request[1] == "USERS":
                                    FillRequest(RemoteClient, str(UserData), ClientAddress)
                                else:
                                    InvalidArguments(RemoteClient)
                            else:
                                MissingArguments(RemoteClient)
                    else:
                        InvalidArguments(RemoteClient)
        if DebugMode == True: print(f'[Flashstore API // Server] WARNING: API_Deliverer Reached end of loop.')
        RemoteClient.close()

    def IncomingConnection(Connection_Socket):
        Client, Address = Connection_Socket.accept()
        print(f'[Flashstore API] NOTICE: Incoming connection from {Address[0]}:{Address[1]}.')
        ClientAddress = str(Address[0])+":"+str(Address[1])
        try:
            _thread.start_new_thread(API_Deliverer, (Client,ClientAddress))
        except:
            print(f'[Flashstore API // Server] Giving up {ClientAddress}.')

    # Status Codes
    def Sending(RemoteClient):
        RemoteClient.send(str.encode('SENDING'))
    def ServerOutdated(RemoteClient):
        RemoteClient.send(str.encode('SERVER-OUTDATED_API-VERSION'))
    def OK(RemoteClient):
        RemoteClient.send(str.encode('OK'))

    def InvalidVersion(RemoteClient):
        try:
            RemoteClient.send(str.encode('INVALID_API-VERSION'))
        except:
            print(f'[Flashstore API // Server] NOTICE: Failed to send that the client has an invalid version.')
        RemoteClient.close()
    def NotFound(RemoteClient):
        try:
            RemoteClient.send(str.encode('NOT_FOUND'))
        except:
            print(f'[Flashstore API // Server] NOTICE: Failed to send to the client that the request could not be found.')
        RemoteClient.close()
    def Done(RemoteClient):
        try:
            RemoteClient.send(str.encode('DONE'))
        except:
            print(f'[Flashstore API // Server] NOTICE: Failed to send to the client that we are done.')
        RemoteClient.close()
    def InvalidArguments(RemoteClient):
        try:
            RemoteClient.send(str.encode('INVALID_ARGUMENTS'))
        except:
            print(f'[Flashstore API // Server] NOTICE: Failed to send that the client has invalid arguments.')
        RemoteClient.close()
    def MissingArguments(RemoteClient):
        try:
            RemoteClient.send(str.encode('MISSING_ARGUMENTS'))
        except:
            print(f'[Flashstore API // Server] NOTICE: Failed to send that the client is missing arguments.')
        RemoteClient.close()
    def UnknownError(RemoteClient):
        try:
            RemoteClient.send(str.encode('UNKNOWN_ERROR'))
        except:
            print(f'[Flashstore API // Server] NOTICE: Failed to send to the client that an unknown error occurred.')
        RemoteClient.close()

    print(f'[Flashstore API] INFO: Initializing Server...\n')
    
    # Server Initialization
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
    ModuleData = GetServerData("Modules")
    PluginData = GetServerData("Plugins")
    UserData = GetServerData("Users")
    print(f'[Flashstore API] Loaded as Module Data: \n{ModuleData}.\n')
    print(f'[Flashstore API] Loaded as Plugin Data: \n{PluginData}.\n')
    print(f'[Flashstore API] Loaded as User Data: \n{UserData}.\n')

    try:
        API_Socket.bind((ServerAddress, ServerPort))
    except socket.error as ErrorInfo:
        print(f'[Flashstore API] Error binding the API: "{ErrorInfo}".')
    print(f'[Flashstore API] Listening on Port "{ServerPort}" on Address "{ServerAddress}"')
    API_Socket.listen()
          
    while True:
        IncomingConnection(API_Socket)


FlashStore_API()

