import asyncio
import websockets
import json

async def test_ws():
    uri = "ws://localhost:8000/ws"  # your WebSocket URL
    async with websockets.connect(uri) as websocket:
        join_message = {
            "type": "join",
            "user": "Harry"
        }
        update_message = {
          "type": "update",
          "user": "Harry",
          "slot": 5,
          "value": True
        }
        await websocket.send(json.dumps(join_message))
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
    print(message)
    print(json.loads(message))


if __name__ == "__main__":
    # asyncio.run(test_ws())
    hello()
