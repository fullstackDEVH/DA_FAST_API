from fastapi import WebSocket, WebSocketDisconnect
from fastapi import APIRouter
from typing import List, Dict

router = APIRouter()


class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []
        self.connection_user_ids: Dict[WebSocket, Dict[str, str]] = {}

    async def connect(self, websocket: WebSocket, sender_id: str, room_name: str):
        await websocket.accept()
        self.active_connections.append(websocket)
        self.connection_user_ids[websocket] = {
            "user_id": sender_id,
            "room_name": room_name,
        }

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)
        del self.connection_user_ids[websocket]

    def get_websocket_by_user_id(self, user_id: str, room_name: str) -> WebSocket:
        for websocket, data in self.connection_user_ids.items():
            if data["user_id"] == user_id and data["room_name"] == room_name:
                print(f'room_name : {room_name}')
                print(f'receiver : {user_id}')

                return websocket
        return None

    async def send_personal_message(self, message: dict, websocket: WebSocket):
        await websocket.send_json(message)

    async def broadcast(self, message: dict):
        for websocket in self.active_connections:
            await websocket.send_json(message)

    # async def send_message_to_clients(self, message: str, client_ids: List[int]):
    #     for connection in self.active_connections:
    #         if int(connection.query_params["client_id"]) in client_ids:
    #             await connection.send_text(message)


manager = ConnectionManager()


@router.websocket("/ws/private/{sender_id}/{receiver_id}/{room_name}")
async def private_websocket(
    websocket: WebSocket, sender_id: str, receiver_id: str, room_name: str
):
    await manager.connect(websocket, sender_id, room_name)

    try:
        while True:
            data = await websocket.receive_json()
            print(f"data : {data}")
            await manager.send_personal_message(
                data,
                manager.get_websocket_by_user_id(
                    user_id=receiver_id, room_name=room_name
                ),
            )
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        # await manager.broadcast(f"User # left the chat")
