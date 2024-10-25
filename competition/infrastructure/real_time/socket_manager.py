import json
from collections import defaultdict
from typing import Dict, List, Any

import redis
from fastapi import WebSocket

class ConnectionManager:
    def __init__(self):
        self.active_connections: Dict[int, Dict[WebSocket, str]] = {}
        self.competition_data: Dict[int, Dict[str, Any]] = {}

    def get_competition_data(self, competition_id: int):
        if competition_id not in self.competition_data:
            self.competition_data[competition_id] = {
                "participant_progress": defaultdict(dict),
                "responses_count": defaultdict(int),
            }
        return self.competition_data[competition_id]
    async def connect(self, websocket: WebSocket, username: str, competition_id: int):
        if competition_id not in self.active_connections:
            self.active_connections[competition_id] = {}
        self.active_connections[competition_id][websocket] = username
        await self.broadcast_users(competition_id)

    async def disconnect(self, websocket: WebSocket, competition_id: int):
        if competition_id in self.active_connections and websocket in self.active_connections[competition_id]:
            del self.active_connections[competition_id][websocket]
            if not self.active_connections[competition_id]:
                del self.active_connections[competition_id]  # Clean up if no more connections
            await self.broadcast_users(competition_id)
            print(f"WebSocket disconnected from competition {competition_id}")

    async def send_personal_message(self, message: str, websocket: WebSocket):
        if websocket in self.active_connections:
            await websocket.send_text(message)

    async def broadcast(self, message: str, competition_id: int):
        if competition_id in self.active_connections:
            # Crear una lista de conexiones que están activas
            connections_to_remove = []
            for connection in list(self.active_connections[competition_id].keys()):
                try:
                    await connection.send_text(message)
                except Exception as e:
                    print(f"Error sending message to {connection}: {e}")
                    # Agregar a la lista de conexiones a remover en caso de error
                    connections_to_remove.append(connection)

            # Remover las conexiones cerradas o problemáticas
            for connection in connections_to_remove:
                await self.disconnect(connection, competition_id)

    async def send_message_to_user(self, message: str, username: str, competition_id: int):
        if competition_id in self.active_connections:
            for websocket, user in self.active_connections[competition_id].items():
                if user == username:
                    await websocket.send_text(message)

    async def broadcast_users(self, competition_id: int):
        if competition_id in self.active_connections:
            users_list = list(self.active_connections[competition_id].values())
            users_message = {"type": "users_update", "users": users_list}
            await self.broadcast(json.dumps(users_message), competition_id)

