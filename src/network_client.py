"""
Network client for Ready Set Bet multiplayer
Handles WebSocket communication with server
"""
import asyncio
import json
import threading
from typing import Optional, Callable, Dict
import websockets
import requests
from datetime import datetime


class NetworkClient:
    """Handles client-server communication via WebSocket"""

    def __init__(self, server_url: str = "ws://localhost:8000"):
        self.server_url = server_url
        self.http_url = server_url.replace("ws://", "http://").replace("wss://", "https://")
        self.websocket: Optional[websockets.WebSocketClientProtocol] = None
        self.session_id: Optional[str] = None
        self.player_token: Optional[str] = None
        self.player_name: Optional[str] = None
        self.is_connected: bool = False

        # Callbacks for different message types
        self.callbacks: Dict[str, Callable] = {}

        # Threading
        self.loop: Optional[asyncio.AbstractEventLoop] = None
        self.thread: Optional[threading.Thread] = None

    def create_session(self) -> Optional[str]:
        """
        Create a new game session on the server
        Returns session_id or None
        """
        try:
            response = requests.post(f"{self.http_url}/api/sessions/create", timeout=5)
            if response.status_code == 200:
                data = response.json()
                return data.get("session_id")
        except Exception as e:
            print(f"Error creating session: {e}")
        return None

    def join_session(self, session_id: str, player_name: str) -> bool:
        """
        Join an existing session
        Returns True if successful
        """
        try:
            response = requests.post(
                f"{self.http_url}/api/sessions/{session_id}/join",
                params={"player_name": player_name},
                timeout=5
            )
            if response.status_code == 200:
                data = response.json()
                self.session_id = data["session_id"]
                self.player_token = data["player_token"]
                self.player_name = data["player_name"]
                return True
        except Exception as e:
            print(f"Error joining session: {e}")
        return False

    def reconnect(self, player_token: str) -> bool:
        """
        Reconnect using saved player token
        Returns True if successful
        """
        try:
            response = requests.post(
                f"{self.http_url}/api/players/reconnect",
                params={"player_token": player_token},
                timeout=5
            )
            if response.status_code == 200:
                data = response.json()
                self.session_id = data["session_id"]
                self.player_token = data["player_token"]
                self.player_name = data["player_name"]
                return True
        except Exception as e:
            print(f"Error reconnecting: {e}")
        return False

    def start_connection(self):
        """Start WebSocket connection in background thread"""
        if self.thread and self.thread.is_alive():
            return

        self.thread = threading.Thread(target=self._run_async_loop, daemon=True)
        self.thread.start()

    def _run_async_loop(self):
        """Run asyncio event loop in thread"""
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)
        self.loop.run_until_complete(self._connect_and_listen())

    async def _connect_and_listen(self):
        """Connect to WebSocket and listen for messages"""
        if not self.session_id or not self.player_token:
            print("Cannot connect: missing session_id or player_token")
            return

        ws_url = f"{self.server_url}/ws/{self.session_id}/{self.player_token}"

        try:
            async with websockets.connect(ws_url) as websocket:
                self.websocket = websocket
                self.is_connected = True
                print(f"✅ Connected to session {self.session_id}")

                # Trigger connection callback
                if "connected" in self.callbacks:
                    self.callbacks["connected"]()

                # Listen for messages
                async for message in websocket:
                    data = json.loads(message)
                    await self._handle_message(data)

        except websockets.exceptions.ConnectionClosed:
            print("❌ Connection closed")
            self.is_connected = False
            if "disconnected" in self.callbacks:
                self.callbacks["disconnected"]()
        except Exception as e:
            print(f"❌ Connection error: {e}")
            self.is_connected = False

    async def _handle_message(self, message: dict):
        """Handle incoming messages from server"""
        msg_type = message.get("type")

        if msg_type in self.callbacks:
            # Call registered callback
            callback = self.callbacks[msg_type]
            if asyncio.iscoroutinefunction(callback):
                await callback(message)
            else:
                callback(message)

    def register_callback(self, message_type: str, callback: Callable):
        """Register a callback for a message type"""
        self.callbacks[message_type] = callback

    def send_message(self, message: dict):
        """Send a message to the server"""
        if not self.is_connected or not self.websocket:
            print("Cannot send message: not connected")
            return

        if self.loop:
            asyncio.run_coroutine_threadsafe(
                self.websocket.send(json.dumps(message)),
                self.loop
            )

    def place_bet(self, bet_data: dict):
        """Send place_bet message"""
        self.send_message({
            "type": "place_bet",
            "data": bet_data
        })

    def remove_bet(self, spot_key: str):
        """Send remove_bet message"""
        self.send_message({
            "type": "remove_bet",
            "spot_key": spot_key
        })

    def start_race(self):
        """Send start_race message"""
        self.send_message({"type": "start_race"})

    def end_race(self, results: dict):
        """Send end_race message"""
        self.send_message({
            "type": "end_race",
            "data": results
        })

    def next_race(self):
        """Send next_race message"""
        self.send_message({"type": "next_race"})

    def request_state(self):
        """Request full state sync from server"""
        self.send_message({"type": "request_state"})

    def disconnect(self):
        """Close connection"""
        self.is_connected = False
        if self.websocket:
            if self.loop:
                asyncio.run_coroutine_threadsafe(self.websocket.close(), self.loop)
