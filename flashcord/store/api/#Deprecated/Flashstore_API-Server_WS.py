import asyncio
import websockets
from Flashstore_Client import *

async def Translate(websocket):
    print(f"Connection from {websocket}")
    async for message in websocket:
        API_Result = FlashClient_API_Request(message)
        await websocket.send(str(API_Result))

async def main():
    async with websockets.serve(Translate, "localhost", 1407):
        await asyncio.Future()  # run forever

asyncio.run(main())