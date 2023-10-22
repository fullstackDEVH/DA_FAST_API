from fastapi import status, UploadFile, HTTPException
from sqlalchemy.orm import Session
from ..database import Apartment
from ..schemas.apartment import ApartmentSchema, ApartmentUpdateSchema
from ..helpers.upload import upload_file, delete_file_upload
import uuid
import logging


logging.basicConfig(level=logging.INFO)

logger = logging.getLogger(__name__)


class ApartmentService:
    def __init__(self, db: Session):
        self.db = db

    async def get_apartment_by_room(
        self, userId: str | None = None, room: int | None = None
    ) -> ApartmentSchema:
        apartmentQuery = self.db.query(Apartment)
        found_apartment = apartmentQuery.filter(Apartment.room == room).first()

        return found_apartment

    async def create_apartment(
        self, name: str, desc: str, room: str, image: UploadFile
    ):
        found_apartment = await self.get_apartment_by_room(userId=None, room=room)

        if found_apartment:
            raise HTTPException(status_code=400, detail="Apartment is exist!!")

        banner_apartment = upload_file(
            folder_name="data/banner/apartment",
            endpoint_path=room,
            allowed_image_types={"image/png", "image/jpeg"},
            file_upload=image,
        )

        apartment_create = self.db.add(
            Apartment(
                id=uuid.uuid4(),
                name=name,
                desc=desc,
                room=room,
                img_room=banner_apartment,
            )
        )

        self.db.commit()
        return apartment_create

    async def get(self, access_token: str, username: str | None):
        if username:
            found_user = (
                self.db.query(Apartment).filter(Apartment.username == username).first()
            )
        else:
            user_id = self.get_user_in_access_token(access_token)
            found_user = (
                self.db.query(Apartment).filter(Apartment.id == user_id).first()
            )
        return found_user

    async def gets(self):
        apartments = self.db.query(Apartment).all()
        return apartments

    async def update(self, apartment_id: str, apartment: ApartmentUpdateSchema):
        found_apartment = (
            self.db.query(Apartment).filter(Apartment.id == apartment_id).first()
        )

        if not found_apartment:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Apartment not found !!!"
            )

        apartment_update = apartment.model_dump(exclude_unset=True)

        for key, value in apartment_update.items():
            setattr(found_apartment, key, value)

        self.db.add(found_apartment)
        self.db.commit()
        self.db.refresh(found_apartment)

        return found_apartment

    async def delete(self, room: str):
        found_apartment_query = await self.get_apartment_by_room(room=room)

        if not found_apartment_query:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Apartment not found!!"
            )

        delete_file_upload("data/banner/apartment", room)

        self.db.delete(found_apartment_query)
        self.db.commit()
        return {"message": f"Xoá phòng: {room} thành công."}
