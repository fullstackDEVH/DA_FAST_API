from fastapi import HTTPException
from sqlalchemy.orm import Session, joinedload
from ..schemas.room import CreateRoom, UpdateRoom

from ..database import Room
import uuid


class RoomService:
    def __init__(self, db: Session):
        self.db = db

    async def create_room(self, room_data: CreateRoom):
        room_create = Room(id=str(uuid.uuid4()), **room_data.model_dump())
        self.db.add(room_create)
        self.db.commit()
        self.db.refresh(room_create)
        return room_create

    async def get_room_by_id(self, room_id: str):
        return self.db.query(Room).filter(Room.id == room_id).first()

    async def get_messages_in_room(self, room_id: str):
        found_room = await self.get_room_by_id(room_id)

        if found_room is None:
            raise HTTPException(status_code=404, detail="room not found")

        return (
            self.db.query(Room)
            .filter(Room.id == room_id)
            .options(joinedload(Room.messages))
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
