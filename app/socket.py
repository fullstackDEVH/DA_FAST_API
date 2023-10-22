from fastapi import WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
from fastapi import APIRouter
from typing import List, Dict
from starlette.websockets import WebSocketState

router = APIRouter()


class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []
        self.connection_user_ids: Dict[WebSocket, int] = {}

    async def connect(self, websocket: WebSocket, user_id: int):
        await websocket.accept()
        self.active_connections.append(websocket)
        self.connection_user_ids[websocket] = user_id

    def get_websocket_by_user_id(self, user_id: int) -> WebSocket:
        for connection, connection_user_id in self.connection_user_ids.items():
            if connection_user_id == user_id:
                return connection
        return None

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)
        del self.connection_user_ids[websocket]

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)

    async def send_message_to_clients(self, message: str, client_ids: List[int]):
        for connection in self.active_connections:
            if int(connection.query_params["client_id"]) in client_ids:
                await connection.send_text(message)


manager = ConnectionManager()


@router.websocket("/ws/private/{recipient_id}")
async def private_websocket(websocket: WebSocket, recipient_id: int):
    user_id = websocket.query_params.get("client_id")
    print(f"user_id : {user_id}")

    websocket.ap

    await manager.connect(websocket, recipient_id)

    try:
        while True:
            data = await websocket.receive_text()
            await manager.send_personal_message(
                f"You to recipient {recipient_id}: {data}", websocket
            )
            await manager.send_personal_message(
                f"From user #{user_id}: {data}",
                manager.get_websocket_by_user_id(recipient_id),
            )
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        await manager.broadcast(f"User #{user_id} left the chat")
