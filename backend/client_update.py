import asyncio
import websockets
import json

async def test_ws():
    uri = "ws://localhost:8000/ws"  # your WebSocket URL
    async with websockets.connect(uri) as websocket:
        update_message = {
          "type": "update",
          "user": "Harry",
          "slot": 5,
          "value": True
        }
        await websocket.send(json.dumps(update_message))
        response = await websocket.recv()
        print("Received:", response)

def hello():
    message = '''
    {
      "type": "update",
      "user": "Harry",
      "slot": 5,
      "value": True
    }
    '''
    message = '{"type": "update", "user": "Harry", "slot": 5, "value": true}'
    # json.loads converts the string into a Python dictionary
    print(json.loads(message))


if __name__ == "__main__":
    asyncio.run(test_ws())
