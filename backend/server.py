# whenwhere backend:
# tech: fastapi+ websockets
# Receives and updates in-memory data store real-time at fast speeds
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
import json
import sys


app = FastAPI()


# CORS connection allowances
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# In-memory store and list of connection
store = {}
connections = []


html = """
<!DOCTYPE html>
<html>
    <head>
        <title>WhenWhere</title>
        <style>
        body {
            font-size: 18px;
            font-family: Arial, sans-serif;
        }
        input[type="text"] {
            width: 500px;
            height: 40px;
            font-size: 18px;
            padding: 5px 10px;
        }
        button {
            height: 40px;
            font-size: 18px;
            padding: 0 15px;
        }
        ul#messages {
            list-style-type: none;
            padding: 0;
        }
        ul#messages li {
            margin-bottom: 10px;
        }
    </style>
    </head>
    <body>
        <h1>WhenWhere</h1>
        <h2>Your ID: <span id="ws-id"></span></h2>
        <form action="" onsubmit="sendMessage(event)">
            <input type="text" id="messageText" autocomplete="off"/>
            <button>Send</button>
        </form>
        <ul id='messages'>
        </ul>
        <script>
            var client_id = Date.now()
            document.querySelector("#ws-id").textContent = client_id;
            var ws = new WebSocket(`ws://localhost:8000/ws/${client_id}`);
            ws.onmessage = function(event) {
                var messages = document.getElementById('messages')
                var message = document.createElement('li')
                var content = document.createTextNode(event.data)
                message.appendChild(content)
                messages.appendChild(message)
            };
            function sendMessage(event) {
                var input = document.getElementById("messageText")
                ws.send(input.value)
                input.value = ''
                event.preventDefault()
            }
        </script>
    </body>
</html>
"""


class ConnectionManager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)


manager = ConnectionManager()


@app.get("/")
async def hello():
    return HTMLResponse(html)


@app.websocket("/ws/{user_id}")
async def whenwhere(websocket: WebSocket, user_id: int):
    await manager.connect(websocket)
    print("New websocket connection created: ", websocket)

    try:
        while True:
            message = await websocket.receive_text()
            print(message, type(message))
            data = json.loads(message)
            print(data, type(data))
            message_type =  data["type"]
            print("Received message: ", data)

            # new user
            if message_type == "join":
                print("Received join request")
                username = data["user"]
                if username not in store:
                    store[username] = [False] * 24
 
            # user data updates
            elif message_type == "update":
                print("Received update request")
                username = data["user"]
                slot = data["slot"]
                value = data["value"]
                if username in store:
                    store[username][slot] = value
 
            # TODO: elif disconnect
     
            # compute common free time
            # TODO: Inspect this
            if store:
                common_free_time = [all(users[hour] for users in store.values()) for hour in range(24)]
            else:
                common_free_time = [False] * 24
 
            # broadcast updated store
            payload = {
                "type": "state",
                "users": list(store.keys()),
                "availability": store,
                "commonFree": common_free_time
            }
            print("Broadcasting payload: ", payload)
            await manager.broadcast(json.dumps(payload))

    except WebSocketDisconnect:
        print("Closing websocket connection: ", websocket)
        manager.disconnect(websocket)



