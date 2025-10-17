# When's everyone free?
A real-time broadcasting system that makes it easy to find free time for a group.


## Assumptions
The below boundaries are set up beforehand:
- Time can be selected only for a single day.
- Time slots are fixed to 1 hour.
- localhost is the single session.


# Technologies and Architecture

## Architecture
```yaml
Frontend (React, TailwindCSS)
         |
   Native WebSocket (realtime)
         |
Backend (FastAPI + fastapi.websockets)
         |
   In-memory store

```

## Frontend State
```js
{
  users: ["Harry", "Ron", "Hermione"],
  availability: {
    Aneesh: [true, false, true, ...],  // 24 booleans
    Priya:  [false, false, true, ...],
    Rohit:  [true, true, false, ...]
  },
  commonFree: [false, false, true, ...]  // derived from above
}

```

## UI View
TODO

## State transfers

### Backend
1. **Structure**
- `/ws`: WebSocket endpoint
- Store times in-memory (Python dict data structure)
```
state = {
    "Harry": [False]*24,
    "Hermione": [False]*24,
}
```

2. **WebSocket events**
| Event        | Action                                           |
| ------------ | ------------------------------------------------ |
| `join`       | Add new user to `state` with all False           |
| `update`     | Update that user’s slot(s)                       |
| `disconnect` | Optionally remove user                           |
| (All)        | Broadcast updated state to all connected clients |

3. WebSocket message transfers

```
// Client → Server
{
  "type": "update",
  "user": "Harry",
  "slot": 5,
  "value": true
}

// Server → All Clients
{
  "type": "state",
  "users": ["Harry", "Ron", "Hermione"],
  "availability": {
    "Harry": [true, false, ...],
    "Ron": [true, true, ...]
    "Hermione": [true, false, ...]
  },
  "commonFree": [true, false, ...]
}
```


# Prerequisites
- Python <= 3.6
- pip (python package installer)
- npm

# Setup
Setup a virtual environment
```sh
python -m venv venv
source venv/bin/activate

pip install -r requirements.txt
```

Run everything in the same virtual environment

Start the server:
> python3 server.py

Start the client in a different terminal:
> python3 client.py

