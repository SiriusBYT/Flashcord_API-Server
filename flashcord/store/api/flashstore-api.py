import socket
import time

Exit = False
Code_HELLO = "HELLO".encode()
Code_OK = "OK".encode()
Code_CLOSE = "CLOSE".encode()
Code_NOTFOUND = "404".encode()
Code_SENDING = "DATA".encode()
Code_SENT = "SENT".encode()

api = socket.socket()

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
print(f'[Flashstore API] Loaded "{ModuleData}" as Module Data')
print(f'[Flashstore API] Loaded "{PluginData}" as Plugin Data')
print(f'[Flashstore API] Loaded "{UserData}" as User Data')


def FlashstoreAPI():
    def SendData(RequestedData):
        isDataSent = False
        while isDataSent == False:
            conn.send(Code_SENDING)
            print(f'[Flashstore API] Sending {RequestedData} to {addr}.')
            conn.send(str(RequestedData).encode())
            time.sleep(0.1)
            conn.send(Code_SENT)
            data = conn.recv(1024).decode()
            if data == "OK":
                isDataSent = True
            else:
                api.close()
        conn.send(Code_CLOSE)
    
    print("[Flashstore API] Listening for API requests.")
    api.listen()
    conn, addr = api.accept()
    while Exit != True:
        print(f"[Flashstore API] Connection received by {addr}")
        while True:
            data = conn.recv(1024).decode()
            if not data:
                break
            print(f'[Flashstore API] {addr} sent "{data}".')
            if data == "HELLO":
                conn.send(Code_OK)
                data = conn.recv(1024).decode()
                if not data:
                    break
                print(f'[Flashstore API] {addr} sent "{data}".')
                API_Request = data.split()
                for RequestStep in API_Request:
                    if API_Request[0] == "GET":
                        if API_Request[1] == "MODULES":
                            try: 
                                if API_Request[2].lower() in ModuleData:
                                    SendData(ModuleData[ModuleData.index(API_Request[2].lower()) + 1])
                            except IndexError:
                                SendData(ModuleData)
                        elif API_Request[1] == "PLUGINS":
                            try: 
                                if API_Request[2].lower() in PluginData:
                                    SendData(PluginData[PluginData.index(API_Request[2].lower()) + 1])
                            except IndexError:
                                SendData(PluginData)
                        else:
                            conn.send(Code_NOTFOUND)
                            conn.send(Code_CLOSE)
            conn.send(Code_CLOSE)
        conn.close()

def bindServer():
    ServerAddress = "127.0.0.1"
    ServerPort = 1407
    api.bind((ServerAddress, ServerPort))

bindServer()

while Exit != True:
    try:
        FlashstoreAPI()
    except Exception as ErrorInfo:
        print(f"[Flashstore API] WARNING: Server errored out with code {ErrorInfo} !")
        FlashstoreAPI()