# client using asyncio websockets
import asyncio
import websockets
import sys


async def hello():
    async with websockets.connect("ws://localhost:8080") as websocket:
        while True:
            try:
                message = input("Enter message: ")
            except EOFError:
                print("User entered Ctrl-D while typing")
                sys.exit()
            await websocket.send(message)
            response = await websocket.recv()
            print("Response: ", response)


if __name__ == "__main__":
    try:
        print("Starting client (exit on Ctrl-C)...")
        asyncio.run(hello())
    except KeyboardInterrupt:
        print("\nExiting client on Ctrl-C")
        sys.exit()
