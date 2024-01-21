import socket

Exit = False
Code_HELLO = "HELLO"
Code_OK = "OK"
Code_CLOSE = "CLOSE"

ClientAddress = "127.0.0.1"  
ClientPort = 1407 
ErrorLevel = 0

def FlashstoreAPI_Request(API_Request):
    try:
        API_Data = []
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as api:
            api.connect((ClientAddress, ClientPort))
            api.send(Code_HELLO.encode())
            isConnectionOpened = True
            isReceivingData = False
            while isConnectionOpened == True:
                data = api.recv(1024).decode()
                if isReceivingData == False:
                    if data == "OK":
                        print(f'[Flashstore Client] Server sent back "{data}".')
                        api.send(API_Request.encode())
                    elif data == "CLOSE":
                        print(f'[Flashstore Client] Server sent back "{data}", terminating the connection!')
                        isConnectionOpened = False
                        api.close()
                        return API_Data
                    elif data == "DATA":
                        print('[Flashstore Client] Attempting to now receive data from the server.')
                        isReceivingData = True
                    else:
                        print('[Flashstore Client] ERROR: "', data, '"is not a known response!')
                        isConnectionOpened = False
                        api.close()
                        return API_Data
                else:
                    if data == "SENT":
                        isReceivingData = False
                        print('[Flashstore Client] Data fully received.')
                        api.send(Code_OK.encode())
                    else:
                        print(f'[Flashstore Client] Received Request with data as: "{data}".')
                        API_Data = data

    except Exception as ErrorInfo: 
        print("[Flashstore Client] Error Level increased by 1 because of", ErrorInfo, ".")
        ErrorLevel+=1
        if ErrorLevel >= 3:
            Exit = True
            print("[Flashstore Client] Exited due to too many errors!")
    print("[Flashstore Client] Function Ended.")

#                                                                    Get     What       By User    Module/plugin Name
print("[Flashstore Client] Retrieved Data:", FlashstoreAPI_Request("GET MODULES SIRIUSBYT"))
print("[Flashstore Client] Retrieved Data:", FlashstoreAPI_Request("GET PLUGINS SIRIUSBYT"))
print("[Flashstore Client] Retrieved Data:", FlashstoreAPI_Request("GET MODULES"))
print("[Flashstore Client] Retrieved Data:", FlashstoreAPI_Request("GET PLUGINS"))
print("[Flashstore Client] Retrieved Data:", FlashstoreAPI_Request("GET USERS"))