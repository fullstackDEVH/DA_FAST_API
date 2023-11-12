from fastapi import status, UploadFile, HTTPException
from sqlalchemy.orm import Session, joinedload
from ..database import (
    Apartment,
    ApartmentTag,
    Tag,
    Amenity,
    apartment_amenity,
    ApartmentImage,
)
from ..schemas.apartment import (
    ApartmentSchema,
    ApartmentUpdateSchema,
    ApartmentCreateSchte,
)
from ..helpers.upload import delete_file_upload, upload_files
from typing import List
import uuid
import logging


logging.basicConfig(level=logging.INFO)

logger = logging.getLogger(__name__)


class ApartmentService:
    def __init__(self, db: Session):
        self.db = db

    async def gets_all(self):
        apartments = self.db.query(Apartment).all()
        return apartments

    async def get_apartment_by_apartment_id(
        self, apartment_id: str | None = None
    ) -> ApartmentSchema:
        apartmentQuery = self.db.query(Apartment)
        found_apartment = apartmentQuery.filter(Apartment.id == apartment_id).first()

        return found_apartment

    async def get_apartment_by_id(
        self, apartment_id: str | None = None
    ) -> ApartmentSchema:
        found_apartment = (
            self.db.query(Apartment).filter(Apartment.id == apartment_id).first()
        )
        apartment = (
            self.db.query(Apartment)
            .filter_by(id=apartment_id)
            .options(
                joinedload(Apartment.apartment_contract),  # Lấy thông tin hợp đồng
                joinedload(Apartment.apartment_tags).joinedload(
                    ApartmentTag.tag
                ),  # Lấy thông tin các thẻ và tên thẻ
                joinedload(Apartment.amenities),  # Lấy thông tin về tiện nghi
            )
            .first()
        )

        # Kiểm tra xem căn hộ có tồn tại không
        if apartment is not None:
            # In ra thông tin của căn hộ
            print("Tên căn hộ:", apartment.name)
            print("Mô tả:", apartment.desc)
            print("Hợp đồng:", apartment.apartment_contract)
            print(
                "Thẻ:",
                [apartment_tag.tag.name for apartment_tag in apartment.apartment_tags],
            )
            print("Tiện nghi:", [amenity.name for amenity in apartment.amenities])
        else:
            print("Căn hộ không tồn tại")

        # tags_in_apartment = [
        #     apartment_tag.tag.name for apartment_tag in found_apartment.apartment_tags
        # ]

        return found_apartment

    async def create_apartment(self, apartment: ApartmentCreateSchte):
        apartment_create = Apartment(
            id=uuid.uuid4(),
            name=apartment.name,
            desc=apartment.desc,
            price_per_day=apartment.price_per_day,
            num_bedrooms=apartment.num_bedrooms,
            num_living_rooms=apartment.num_living_rooms,
            num_bathrooms=apartment.num_bathrooms,
            num_toilets=apartment.num_toilets,
            total_people=apartment.total_people,
            rate=apartment.rate,
        )

        apartment_tags = []

        for tag_id in apartment.tag_ids[0].split(","):
            apartment_tag = ApartmentTag(
                id=uuid.uuid4(), apartment_id=apartment_create.id, tag_id=tag_id
            )
            apartment_tags.append(apartment_tag)

        apartment_create.apartment_tags = apartment_tags

        amenities = []
        for amenity_id in apartment.amenities[0].split(","):
            amenity = self.db.query(Amenity).filter(Amenity.id == amenity_id).first()
            if amenity:
                amenities.append(amenity)

        apartment_create.amenities = amenities

        self.db.add(apartment_create)
        self.db.commit()

        return apartment_create

    async def upload_images(self, apartment_id: str, images: list[UploadFile]):
        try:
            uploaded_images = await upload_files(
                folder_name=f"data/banner/apartment/{apartment_id}",
                allowed_image_types={"image/png", "image/jpeg"},
                files=images,
            )

            for image_path in uploaded_images:
                db_image = ApartmentImage(
                    id=str(uuid.uuid4()),
                    apartment_id=apartment_id,
                    image_url=image_path,
                )
                self.db.add(db_image)

            self.db.commit()

            return "Update success"

        except Exception as e:
            # Log the error or handle it as appropriate for your application
            logging.error(f"An error occurred during image upload: {e}")

            # Rollback the database transaction in case of an error
            self.db.rollback()

            # Return an error message or raise the exception if needed
            return f"Error: {e}"

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

    async def gets_apartment_by_tag_id(self, tag_id: str | None):
        apartments_with_tag = (
            self.db.query(Apartment)
            .join(Apartment.apartment_tags)
            .join(ApartmentTag.tag)
            .filter(Tag.id == tag_id)
            .all()
        )

        return apartments_with_tag

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

    async def delete(self, apartment_id: str):
        found_apartment_query = await self.get_apartment_by_apartment_id(apartment_id)

        if not found_apartment_query:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Apartment not found!!"
            )

        delete_file_upload("data/banner/apartment", apartment_id)

        self.db.delete(found_apartment_query)
        self.db.commit()
        return {"message": f"Xoá phòng: {apartment_id} thành công."}
