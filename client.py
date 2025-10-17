# client using asyncio websockets
import asyncio
import websockets


async def hello():
    async with websockets.connect("ws://localhost:8080") as websocket:
        while True:
            message = input("Enter message: ")
            await websocket.send(message)
            response = await websocket.recv()
            print("Response: ", message)


if __name__ == "__main__":
    asyncio.run(hello())

