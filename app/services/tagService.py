from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from ..schemas.tag import TagCreate

from ..database import Tag, Apartment
from enum import Enum
import uuid


class TagService:
    def __init__(self, db: Session):
        self.db = db

    async def create_tag(self, tag: TagCreate):
        tag_create = Tag(id=str(uuid.uuid4()), name=tag.name, desc=tag.desc)
        self.db.add(tag_create)
        self.db.commit()
        self.db.refresh(tag_create)
        return tag_create

    async def get_tag(self, tag_id: str):
        return self.db.query(Tag).filter(Tag.id == tag_id).first()

    async def get_tags_by_apartment_id(self, apartment_id : str):
        apartment = (
            self.db.query(Apartment)
            .filter(Apartment.id == apartment_id)
            .first()
        )

        # Lấy danh sách các tag trong apartment
        tags_in_apartment = [
            apartment_tag.tag.name for apartment_tag in apartment.apartment_tags
        ]

        return tags_in_apartment

    async def get_tags(self):
        return self.db.query(Tag).all()

    async def update_tag(self, tag_id: str, tag: TagCreate):
        db_tag = await self.get_tag(tag_id)

        if not db_tag:
            raise HTTPException(status_code=404, detail="tag not found")

        for key, value in tag.model_dump().items():
            setattr(db_tag, key, value)
        self.db.commit()
        self.db.refresh(db_tag)

        return db_tag

    async def delete_tag(self, tag_id: str):
        db_tag = self.db.query(Tag).filter(Tag.id == tag_id).first()
        if db_tag:
            self.db.delete(db_tag)
            self.db.commit()
        return db_tag
