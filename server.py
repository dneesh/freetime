# echo server with asyncio websockets
import asyncio
import websockets


async def echo(websocket):
    async for message in websocket:
        print(message)
        await websocket.send(message)


async def main():
    server = await websockets.serve(echo, "localhost", 8080)
    await server.serve_forever()


if __name__ == "__main__":
    asyncio.run(main())

