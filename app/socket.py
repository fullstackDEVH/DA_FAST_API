from fastapi import WebSocket, WebSocketDisconnect
from fastapi import APIRouter
from typing import List, Dict

router = APIRouter()


class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []
        self.connection_user_ids: Dict[WebSocket, str] = {}

    async def connect(self, websocket: WebSocket, sender_id: str):
        await websocket.accept()

        self.active_connections.append(websocket)
        self.connection_user_ids[websocket] = sender_id

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)
        del self.connection_user_ids[websocket]

    def get_websocket_by_user_id(self, user_id: str) -> WebSocket:
        for websocket, sender_id in self.connection_user_ids.items():
            if sender_id == user_id:
                return websocket
        return None

    async def send_personal_message(self, message: dict, websocket: WebSocket):
        await websocket.send_json(message)

    # send all
    async def broadcast(self, message: dict):
        for websocket in self.active_connections:
            await websocket.send_json(message)

    # async def send_message_to_clients(self, message: str, client_ids: List[int]):
    #     for connection in self.active_connections:
    #         if int(connection.query_params["client_id"]) in client_ids:
    #             await connection.send_text(message)


manager = ConnectionManager()

class CreateMessageSocket:
    def __init__(self, sender_id, receiver_id, avatar, text):
        self.sender_id = sender_id
        self.receiver_id = receiver_id
        self.avatar = avatar
        self.text = text


@router.websocket("/ws/private/{sender_id}")
async def private_websocket(websocket: WebSocket, sender_id: str):
    await manager.connect(websocket, sender_id)

    try:
        while True:
            data = await websocket.receive_json()
            tag_create = CreateMessageSocket(**data)
            receiver_id = tag_create.receiver_id
            print(f"receiver_id : {receiver_id}")
            print(f"sender_id : {sender_id}")

            await manager.send_personal_message(
                data,
                manager.get_websocket_by_user_id(user_id=receiver_id),
            )


    except WebSocketDisconnect:
        manager.disconnect(websocket)

