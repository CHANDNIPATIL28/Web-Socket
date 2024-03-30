import asyncio
from fastapi import FastAPI, WebSocket
from fastapi.staticfiles import StaticFiles
from starlette.responses import FileResponse
import websockets

app = FastAPI()

# Serve static files, mainly for index.html
app.mount("/static", StaticFiles(directory="static"), name="static")


# Root endpoint serving the index.html
@app.get("/")
async def get():
    return FileResponse('static/index.html')

# Utility function to relay messages from the client to the WebSocket server
async def relay_client_to_server(websocket_client: WebSocket, websocket_server):
    try:
        while True:
            message = await websocket_client.receive_text()
            await websocket_server.send(message)
    except Exception as e:
        print(f"Error relaying client to server: {e}")

# Utility function to relay messages from the WebSocket server to the client
async def relay_server_to_client(websocket_client: WebSocket, websocket_server):
    try:
        while True:
            message = await websocket_server.recv()
            await websocket_client.send_text(message)
    except Exception as e:
        print(f"Error relaying server to client: {e}")

# WebSocket endpoint
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    async with websockets.connect('ws://localhost:6789') as websocket_server:
        await asyncio.gather(
            relay_client_to_server(websocket, websocket_server),
            relay_server_to_client(websocket, websocket_server),
        )