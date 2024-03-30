# WebSocket Server and Client Interface

This repository contains a WebSocket server (`webserver.py`) and a FastAPI application (`main.py`) that serves a WebSocket client interface (`index.html`). The WebSocket server maintains a dynamic state, represented by random numbers associated with each letter of the alphabet, and notifies subscribed clients of updates. The FastAPI application serves as an intermediary, facilitating communication between the client interface and the WebSocket server.

## webserver.py

`webserver.py` is an asyncio-based WebSocket server that:

- Maintains a global state with a random number assigned to each letter of the alphabet.
- Allows WebSocket clients to subscribe or unsubscribe to updates for specific letters.
- Periodically updates the state and notifies subscribed clients.

### Key Functions:

- `notify_subscribers(letter)`: Notifies all subscribers of updates to the specified letter.
- `update_state()`: Periodically updates the state and triggers notifications to subscribers.
- `handler(websocket, path)`: Manages incoming WebSocket connections and messages.

## main.py

`main.py` is a FastAPI application that:

- Serves static files and an `index.html` client interface.
- Establishes WebSocket connections to both the client and `webserver.py`, relaying messages between them.

### Key Endpoints:

- `/`: Serves the main client interface (`index.html`).
- `/ws`: Establishes a WebSocket connection with the client and relays messages to/from the WebSocket server.

## index.html

The client interface allows users to:

- Subscribe or unsubscribe to updates for each letter.
- View real-time updates from the WebSocket server displayed on the interface.

## Installation

To set up this project, clone the repository and install the necessary dependencies:

```bash
git clone https://github.com/CHANDNIPATIL28/Web-Socket.git
cd Web-Socket
pip install -r requirements.txt
```

## Usage

Start the WebSocket server:

```bash
python webserver.py
```

In a separate terminal, launch the FastAPI application:

```bash
uvicorn main:app --reload
```

Access the client interface at `http://localhost:8000`.



