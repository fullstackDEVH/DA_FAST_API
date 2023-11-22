from fastapi import status, UploadFile, HTTPException
from sqlalchemy.orm import Session, joinedload
from ..database import (
    Apartment,
    ApartmentTag,
    Tag,
    Amenity,
    apartment_amenity,
    ApartmentImage,
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
        apartments = (
            self.db.query(Apartment).options(joinedload(Apartment.images)).all()
        )
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
        apartment = (
            self.db.query(Apartment)
            .filter_by(id=apartment_id)
            .options(
                joinedload(Apartment.comments),
                joinedload(Apartment.images),
                joinedload(Apartment.apartment_contract),  # Lấy thông tin hợp đồng
                joinedload(Apartment.apartment_tags).joinedload(
                    ApartmentTag.tag
                ),  # Lấy thông tin các thẻ và tên thẻ
                joinedload(Apartment.amenities),  # Lấy thông tin về tiện nghi
            )
            .first()
        )

        total_rating = 0

        if len(apartment.comments) > 0:
            for comment in apartment.comments:
                total_rating += (
                    comment.rate_location
                    + comment.rate_interior
                    + comment.rate_amenities
                    + comment.rate_price
                ) / 5

            total_rating = round(total_rating / len(apartment.comments), 1)

        apartment.comments.clear()
        apartment.total_rating = total_rating

        return apartment

    async def create_apartment(self, apartment: ApartmentCreateSchte):
        apartment_create = Apartment(
            id=str(uuid.uuid4()),
            name=apartment.name,
            desc=apartment.desc,
            price_per_day=apartment.price_per_day,
            num_bedrooms=apartment.num_bedrooms,
            num_living_rooms=apartment.num_living_rooms,
            num_bathrooms=apartment.num_bathrooms,
            num_toilets=apartment.num_toilets,
            total_people=apartment.total_people,
            rate=apartment.rate,
            address=apartment.address,
        )

        apartment_tags = []

        for tag_id in apartment.tag_ids[0].split(","):
            apartment_tag = ApartmentTag(
                id=str(uuid.uuid4()), apartment_id=apartment_create.id, tag_id=tag_id
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
        self.db.refresh(apartment_create)

        return apartment_create

    async def upload_images(self, apartment_id: str, images: list[UploadFile]):
        try:
            uploaded_images = await upload_files(
                folder_name=f"data/banner/apartments/{apartment_id}",
                allowed_image_types={"image/png", "image/jpeg"},
                files=images,
                endpoint=f"apartments/{apartment_id}/banner",
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
            .join(Apartment.apartment_tags)  # Joins để lấy các căn hộ có tagId cụ thể
            .filter(ApartmentTag.tag_id == tag_id)
            .options(joinedload(Apartment.images))
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
        apartmentQuery = self.db.query(Apartment)
        found_apartment = (
            apartmentQuery.filter(Apartment.id == apartment_id)
            .options(joinedload(Apartment.images))
            .first()
        )

        if not found_apartment:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Apartment not found!!"
            )

        total_imgs = len(found_apartment.images)
        if total_imgs > 0:
            for index, image in enumerate(found_apartment.images):
                delete_file_upload(f"data/banner/apartments/{apartment_id}", str(index))

        self.db.delete(found_apartment)
        self.db.commit()
        return {"message": f"Xoá phòng: {apartment_id} thành công."}
