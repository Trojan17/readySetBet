"""
WebSocket connection manager for real-time communication
"""
from typing import Dict, List, Set
from fastapi import WebSocket
import json
import asyncio


class ConnectionManager:
    """Manages WebSocket connections for game sessions"""

    def __init__(self):
        # session_id -> set of WebSocket connections
        self.active_connections: Dict[str, Set[WebSocket]] = {}
        # websocket -> (session_id, player_name, player_token)
        self.connection_info: Dict[WebSocket, tuple] = {}

    async def connect(self, websocket: WebSocket, session_id: str, player_name: str, player_token: str):
        """Connect a player to a session"""
        await websocket.accept()

        if session_id not in self.active_connections:
            self.active_connections[session_id] = set()

        self.active_connections[session_id].add(websocket)
        self.connection_info[websocket] = (session_id, player_name, player_token)

    def disconnect(self, websocket: WebSocket):
        """Disconnect a player"""
        if websocket in self.connection_info:
            session_id, player_name, player_token = self.connection_info[websocket]

            if session_id in self.active_connections:
                self.active_connections[session_id].discard(websocket)

                # Clean up empty session
                if not self.active_connections[session_id]:
                    del self.active_connections[session_id]

            del self.connection_info[websocket]

    async def send_personal_message(self, message: dict, websocket: WebSocket):
        """Send message to specific connection"""
        try:
            await websocket.send_json(message)
        except Exception as e:
            print(f"Error sending personal message: {e}")

    async def broadcast_to_session(self, session_id: str, message: dict, exclude: WebSocket = None):
        """Broadcast message to all players in a session"""
        if session_id not in self.active_connections:
            return

        disconnected = []
        for connection in self.active_connections[session_id]:
            if connection == exclude:
                continue
            try:
                await connection.send_json(message)
            except Exception as e:
                print(f"Error broadcasting to session: {e}")
                disconnected.append(connection)

        # Clean up disconnected clients
        for conn in disconnected:
            self.disconnect(conn)

    def get_session_connections(self, session_id: str) -> int:
        """Get number of active connections in a session"""
        if session_id in self.active_connections:
            return len(self.active_connections[session_id])
        return 0

    def get_connection_info(self, websocket: WebSocket) -> tuple:
        """Get (session_id, player_name, player_token) for a connection"""
        return self.connection_info.get(websocket, (None, None, None))
