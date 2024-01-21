import socket
import time 

def FlashClient_API_Request():

    print(f'[Flashstore API // Client] INFO: Attempting to communicate with the FlashStore API...')
    # Server Information
    ServerAddress = socket.gethostname()
    ServerPort = 1407
    PacketSize = 1024
    RemoteServer = socket.socket()
    DebugMode = False
    API_Version = "2"
    try:
        RemoteServer.connect((ServerAddress, ServerPort))
    except socket.error as ErrorInfo:
        print(f'[Flashstore API // Client] Error connecting to the FlashStore API: "{ErrorInfo}".')
    print(f'[Flashstore API // Client] Successfully connected to {ServerAddress}:{ServerPort}.')
    print(f'[Flashstore API // Client] Sent that we are requesting to use version v{API_Version} of the API.')
    RemoteServer.send(str.encode(API_Version))
    while True:
        RemoteServer_Response = RemoteServer.recv(PacketSize).decode()
        if RemoteServer_Response == "":
            if DebugMode == True: print("Server didn't send new data.")
        else:
            print(f'[Flashstore API // Client] Received Code: {RemoteServer_Response}.')

FlashClient_API_Request()