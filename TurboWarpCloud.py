# turbowarpcloud.py

import asyncio
import websockets
import json

class TurboWarpCloudClient:
    def __init__(self, username: str, project_id: str):
        self.username = username
        self.project_id = str(project_id)
        self.websocket = None

    async def connect(self):
        uri = "wss://clouddata.turbowarp.org"
        self.websocket = await websockets.connect(uri)
        handshake = {
            "method": "handshake",
            "user": self.username,
            "project_id": self.project_id
        }
        await self.websocket.send(json.dumps(handshake))
        print(f"[INFO] Connected as {self.username} to project {self.project_id}")

    async def set_variable(self, variable_name: str, value):
        if not self.websocket:
            raise Exception("WebSocket is not connected.")
        message = {
            "method": "set",
            "name": variable_name,
            "value": str(value)
        }
        await self.websocket.send(json.dumps(message))
        print(f"[SUCCESS] Set '{variable_name}' to '{value}'")

    async def listen(self):
        if not self.websocket:
            raise Exception("WebSocket is not connected.")
        print("[INFO] Listening for cloud updates...")
        try:
            while True:
                message = await self.websocket.recv()
                print("[EVENT]", message)
        except websockets.exceptions.ConnectionClosed:
            print("[INFO] WebSocket connection closed.")

    async def close(self):
        if self.websocket:
            await self.websocket.close()
            print("[INFO] WebSocket closed.")
