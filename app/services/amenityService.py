from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from ..schemas.amenity import AmenityCreate

from ..database import Amenity, Apartment
from enum import Enum
import uuid


class AmenityService:
    def __init__(self, db: Session):
        self.db = db

    async def create_amenity(self, amenity: AmenityCreate):
        amenity_create = Amenity(
            id=str(uuid.uuid4()), name=amenity.name, desc=amenity.desc
        )
        self.db.add(amenity_create)
        self.db.commit()
        self.db.refresh(amenity_create)
        return amenity_create

    async def get_amenity(self, amenity_id: str):
        return self.db.query(Amenity).filter(Amenity.id == amenity_id).first()

    async def get_amenitys_by_apartment_id(self, apartment_id: str):
        apartment = (
            self.db.query(Apartment).filter(Apartment.id == apartment_id).first()
        )

        # Lấy danh sách các tag trong apartment
        tags_in_apartment = [
            apartment_tag.tag.name for apartment_tag in apartment.apartment_tags
        ]

        return tags_in_apartment

    async def get_amenitys(self):
        return self.db.query(Amenity).all()

    async def update_amenity(self, amenity_id: str, amenity: AmenityCreate):
        db_tag = await self.get_tag(amenity_id)

        if not db_tag:
            raise HTTPException(status_code=404, detail="tag not found")

        for key, value in db_tag.model_dump().items():
            setattr(db_tag, key, value)
        self.db.commit()
        self.db.refresh(db_tag)

        return db_tag

    async def delete_amenity(self, amenity_id: str):
        db_tag = self.db.query(Amenity).filter(Amenity.id == amenity_id).first()
        if db_tag:
            self.db.delete(db_tag)
            self.db.commit()
        return db_tag
