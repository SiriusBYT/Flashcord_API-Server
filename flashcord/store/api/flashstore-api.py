import socket
import time
import _thread

def FlashStore_API():
    # Server Information
    ServerAddress = socket.gethostname()
    ServerPort = 1407
    PacketSize = 1024
    API_Socket = socket.socket()
    API_Version = "2"
    DebugMode = True
    MaxTimeoutCount = 10
    MaxIdleCount = 1000000
    RetryDelay = 1

    def FillRequest(RemoteClient, RequestData, ClientAddress):
        Sending(RemoteClient)
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
                    if DebugMode == True: print(f"TIMEOUT: {TimeoutCount}/{MaxTimeoutCount} Couldn't get new data from {ClientAddress}")
                    TimeoutCount+=1
                    time.sleep(RetryDelay)
            else:
                if DebugMode == True: print(f"TIMEOUT: {TimeoutCount}/{MaxTimeoutCount} Couldn't get new data from {ClientAddress}")
                TimeoutCount+=1
                time.sleep(RetryDelay)
                
    def isPreciseRequest(API_Request):
        isPreciseRequest = True
        try:
            DummyVar = API_Request[2]
        except:
            isPreciseRequest = False
        return isPreciseRequest

    def API_Deliverer(RemoteClient, ClientAddress):
        RemoteClient_Response = RemoteClient.recv(PacketSize).decode()
        if RemoteClient_Response != API_Version:
            print(f'[Flashstore API // Server] {ClientAddress} Requested API Version: {RemoteClient_Response}. [INVALID_API-VERSION]')
            InvalidVersion(RemoteClient)
            RemoteClient.close()
        else:
            print(f'[Flashstore API // Server] {ClientAddress} Requested API Version: {RemoteClient_Response}. [OK]')
            OK(RemoteClient)
        TimeoutCount = 0
        IdleCount = 0
        while True:
            try:
                RemoteClient_Response = RemoteClient.recv(PacketSize).decode()
            except:
                if DebugMode == True: print(f"TIMEOUT: {TimeoutCount}/{MaxTimeoutCount} Couldn't get new data from {ClientAddress}")
                TimeoutCount+=1
                time.sleep(RetryDelay)

            if TimeoutCount == MaxTimeoutCount:
                print(f'[Flashstore API // Server] {ClientAddress} timed out.')
                break
            elif IdleCount == MaxIdleCount:
                print(f'[Flashstore API // Server] {ClientAddress} idled for too long..')
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
                            if API_Request[1] == "MODULES":  
                                if isPreciseRequest(API_Request) == True:
                                    if API_Request[2].lower() in PluginData:
                                        FillRequest(RemoteClient, ModuleData[ModuleData.index(API_Request[2].lower()) + 1], ClientAddress)
                                    else:
                                        NotFound(RemoteClient)
                                else:
                                    FillRequest(RemoteClient, str(ModuleData), ClientAddress)

                            elif API_Request[1] == "PLUGINS":
                                if isPreciseRequest(API_Request) == True:
                                    if API_Request[2].lower() in PluginData:
                                        FillRequest(RemoteClient, PluginData[PluginData.index(API_Request[2].lower()) + 1], ClientAddress)
                                    else:
                                        NotFound(RemoteClient)
                                else:
                                    FillRequest(RemoteClient, str(PluginData), ClientAddress)
                                    
                            elif API_Request[1] == "USERS":
                                FillRequest(RemoteClient, str(UserData), ClientAddress)
                            else:
                                NotFound(RemoteClient)
                    else:
                        NotFound(RemoteClient)
        if DebugMode == True: print(f'Reached end of loop.')
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
    def InvalidVersion(RemoteClient):
        RemoteClient.send(str.encode('INVALID_API-VERSION'))
        RemoteClient.close()
    
    def OK(RemoteClient):
        RemoteClient.send(str.encode('OK'))

    def NotFound(RemoteClient):
        RemoteClient.send(str.encode('NOT_FOUND'))
        RemoteClient.close()

    def Done(RemoteClient):
        RemoteClient.send(str.encode('DONE'))
        RemoteClient.close()

    def Sending(RemoteClient):
        RemoteClient.send(str.encode('SENDING'))

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

