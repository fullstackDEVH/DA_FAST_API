from fastapi import HTTPException
from sqlalchemy.orm import Session, joinedload, contains_eager
from sqlalchemy import desc
from ..schemas.room import CreateRoom, UpdateRoom, TYPE_ROOM_ID

from ..database import Room, MembersRoom, Message
import uuid


class RoomService:
    def __init__(self, db: Session):
        self.db = db

    async def create_room(self, room_data: CreateRoom):
        room_create = Room(id=str(uuid.uuid4()), name=room_data.name, key=room_data.key)

        members = []
        for user_id in room_data.users_id:
            apartment_tag = MembersRoom(
                id=str(uuid.uuid4()), room_id=room_create.id, user_id=user_id
            )
            members.append(apartment_tag)

        room_create.members = members

        self.db.add(room_create)
        self.db.commit()
        self.db.refresh(room_create)
        return room_create

    async def get_room_users(self, sender_id: str, receiver_id: str):
        room_query = (
            self.db.query(Room)
            .join(MembersRoom, MembersRoom.room_id == Room.id)
            .filter(
                Room.id.in_(
                    self.db.query(Room.id)
                    .join(MembersRoom, MembersRoom.room_id == Room.id)
                    .filter(MembersRoom.user_id == sender_id)
                )
            )
            .filter(
                Room.id.in_(
                    self.db.query(Room.id)
                    .join(MembersRoom, MembersRoom.room_id == Room.id)
                    .filter(MembersRoom.user_id == receiver_id)
                )
            )
        )
        existing_room = room_query.first()

        return existing_room

    async def get_room_by_id(self, room_id: str):
        return self.db.query(Room).filter(Room.id == room_id).first()

    async def get_messages_in_room(self, type_query: TYPE_ROOM_ID, id: str):
        if type_query == "ROOM_ID":
            found_room = await self.get_room_by_id(id)

            if found_room is None:
                raise HTTPException(status_code=404, detail="room not found")

            room_data = (
                self.db.query(Room)
                .join(Room.messages)
                .filter(Room.id == id)
                .options(
                    contains_eager(Room.messages).options(contains_eager(Message.user))
                )
                # .order_by(desc(Message.created_at))
                .all()
            )

            messages = []
            for room_data in room_data:
                for message in room_data.messages:
                    messages.append(message)

            return messages

        elif type_query == "USER_ID":
            return (
                self.db.query(Room)
                .join(MembersRoom)
                .filter(MembersRoom.user_id == id)
                .options(joinedload(Room.members).options(joinedload(MembersRoom.user)))
                .all()
            )

    async def update_room(self, room_id: str, room_data: UpdateRoom):
        db_message = await self.get_room_by_id(room_id)

        if not db_message:
            raise HTTPException(status_code=404, detail="room not found")

        for key, value in room_data.model_dump(exclude_unset=True).items():
            setattr(db_message, key, value)

        self.db.commit()
        self.db.refresh(db_message)

        return db_message

    async def delete_room(self, room_id: str):
        db_message = self.db.query(Room).filter(Room.id == room_id).first()
        if db_message:
            self.db.delete(db_message)
            self.db.commit()
        return db_message
