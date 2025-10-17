# echo server with asyncio websockets
import asyncio
import websockets
import sys


members = set()

async def chat(websocket):
    print("New member: ", websocket)
    members.add(websocket)
    try:
        async for message in websocket:
            print("Received message: ", message)
            # broadcast message to all members
            print("Current members: ", members)
            for member in members:
                if member != websocket:
                    await member.send(message)
    except websockets.exceptions.ConnectionClosed:
        pass
    finally:
        print("Removing member: ", websocket)
        members.remove(websocket)


async def main():
    server = await websockets.serve(chat, "localhost", 8080)
    await server.serve_forever()


if __name__ == "__main__":
    try:
        print("Starting server (exit on Ctrl-C)...")
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nExiting the server on Ctrl-C")
        sys.exit()

