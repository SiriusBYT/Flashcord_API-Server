import socket
import time
import _thread

def FlashStore_API():
    # Server Information
    ServerAddress = socket.gethostname()
    ServerPort = 1407
    PacketSize = 1024
    API_Socket = socket.socket()
    DebugMode = True
    API_Version = "2"

    def API_Deliverer(RemoteClient):
        RemoteClient_Response = RemoteClient.recv(PacketSize).decode()
        if RemoteClient_Response != API_Version:
            print(f'[Flashstore API // Server] Requested API Version: {RemoteClient_Response}. [INVALID_API-VERSION]')
            InvalidVersion(RemoteClient)
            RemoteClient.close()
        else:
            print(f'[Flashstore API // Server] Requested API Version: {RemoteClient_Response}. [OK]')
            OK(RemoteClient)
        while True:
            RemoteClient_Response = RemoteClient.recv(PacketSize).decode()
            if RemoteClient_Response == "":
                if DebugMode == True: print("Client didn't send new data.")
            else:
                print(f'[Flashstore API // Server] Received Code: {RemoteClient_Response}.')
        print(f'[Flashstore API // Server] Reached end of loop.')
        RemoteClient.close()

    def IncomingConnection(Connection_Socket):
        Client, Address = Connection_Socket.accept()
        print(f'[Flashstore API] NOTICE: Incoming connection from {Address[0]}:{Address[1]}.')
        ClientAddress = str(Address[0])+str(Address[1])
        _thread.start_new_thread(API_Deliverer, (Client, ))

    # Status Codes
    def InvalidVersion(RemoteClient):
        RemoteClient.send(str.encode('INVALID_API-VERSION'))
        RemoteClient.close()
    
    def OK(RemoteClient):
        RemoteClient.send(str.encode('OK'))

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

