import asyncio 
import json
import random
import websockets

# Global state
state = {chr(i + 65): random.randint(1000, 9999) for i in range(26)} #65 to 90 ascii code for capital A to Z
subscriptions = {chr(i + 65): set() for i in range(26)} #client id will be added after client subscribes and removed after unsubcribe 

# Notify subscribers with the current state
async def notify_subscribers(letter): #concurrent task
    if subscriptions[letter]: #checking for connections for the letter
        disconnected_websockets = set()
        message = json.dumps({letter: state[letter]}) #
        for websocket in subscriptions[letter]:
            try:
                await websocket.send(message)
            except websockets.exceptions.ConnectionClosed:
                disconnected_websockets.add(websocket)

        # Remove disconnected websockets
        for websocket in disconnected_websockets:
            subscriptions[letter].discard(websocket)
           

# Update state function
async def update_state():
    while True: #till server is on
        for letter in state: #all 26 letters,updated synchronously
            state[letter] = random.randint(1000, 9999)
            await notify_subscribers(letter) 
        await asyncio.sleep(1)  # Update every 10 seconds
        
# WebSocket handler
async def handler(websocket, path):
    global subscriptions, connections
    # Add the websocket connection to a global set of connections
    connections.add(websocket)
    try:
        async for message in websocket:#whenever a client clicks on button it will send a message to server
            data = json.loads(message)
            action = data['action']
            letter = data['letter'].upper()
            if action == 'subscribe' and letter in subscriptions:
                subscriptions[letter].add(websocket)
                await notify_subscribers(letter)#immediately sends notification/msg
            elif action == 'unsubscribe' and letter in subscriptions:
                if letter in subscriptions and websocket in subscriptions[letter]:
                    subscriptions[letter].remove(websocket)
                else:
                    new_message = json.dumps({letter: "You need to subscribe before un-subscribing"})
                    await websocket.send(new_message)
                    print(f"Client is not subscribed to {letter}")
    except websockets.exceptions.ConnectionClosed:
        print(f"WebSocket connection with {websocket.remote_address} closed.")
    finally:
        # Remove the websocket connection from all subscription sets
        for letter, subs in subscriptions.items():#key-value,connection close karna hai to websocket ko bhi hatana hai from their respective letters
            subs.discard(websocket)
        # Remove from the global set of connections
        connections.discard(websocket)
        
        

start_server = websockets.serve(handler, "localhost", 6789)

asyncio.get_event_loop().run_until_complete(start_server)#event loop starts
asyncio.ensure_future(update_state())  # Start the state update loop
asyncio.get_event_loop().run_forever()