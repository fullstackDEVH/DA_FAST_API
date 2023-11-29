from fastapi import APIRouter, Depends, status, Path
from ..database import get_db
from sqlalchemy.orm import Session
from ..schemas.room import CreateRoom, UpdateRoom, TYPE_ROOM_ID
from ..services.roomService import RoomService
from ..helpers.response import make_response_object
import logging


logging.basicConfig(level=logging.INFO)

logger = logging.getLogger(__name__)

router = APIRouter()


def get_rooms_service(db: Session = Depends(get_db)):
    return RoomService(db)


@router.get("/users", status_code=status.HTTP_200_OK)
async def get_room_users(
    sender_id: str,
    receiver_id: str,
    roomService: RoomService = Depends(get_rooms_service),
):
    response = await roomService.get_room_users(
        sender_id=sender_id, receiver_id=receiver_id
    )
    return make_response_object(response)


@router.get("/", status_code=status.HTTP_200_OK)
async def get_messages_in_room(
    id: str,
    type_query: TYPE_ROOM_ID,
    roomService: RoomService = Depends(get_rooms_service),
):
    response = await roomService.get_messages_in_room(type_query=type_query, id=id)
    return make_response_object(response)


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_message(
    room_data: CreateRoom,
    roomService: RoomService = Depends(get_rooms_service),
):
    response = await roomService.create_room(room_data)
    return make_response_object(response)


@router.patch("/{room_id}", status_code=status.HTTP_200_OK)
async def update_message(
    room_data: UpdateRoom,
    room_id: str = Path(title="The ID of the item to get"),
    roomService: RoomService = Depends(get_rooms_service),
):
    response = await roomService.update_room(room_id, room_data)
    return make_response_object(response)


@router.delete("/{room_id}", status_code=status.HTTP_200_OK)
async def delete_message(
    room_id: str = Path(title="The ID of the item to get"),
    roomService: RoomService = Depends(get_rooms_service),
):
    response = await roomService.delete_room(room_id)
    return make_response_object(response)
