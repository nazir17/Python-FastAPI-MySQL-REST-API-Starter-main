import asyncio
import websockets
import json

WS_URL = "ws://localhost:8000/api/ws/chat/7"

async def chat_client():
    async with websockets.connect(WS_URL) as websocket:
        print("Connected! Type 'exit' to quit.")
        while True:
            message = input("Enter message: ")
            if message.lower() == "exit":
                break

            receiver_id = int(input("Enter receiver_id: "))
            order_id = int(input("Enter order_id: "))
            is_agent = input("Are you agent? (true/false): ").lower() == "true"

            payload = {
                "receiver_id": receiver_id,
                "order_id": order_id,
                "message": message,
                "is_agent": is_agent
            }

            await websocket.send(json.dumps(payload))

            
            response = await websocket.recv()
            print("Received:", json.loads(response))

asyncio.run(chat_client())
