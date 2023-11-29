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

    async def gets_all(self, **argsKwg):
        amenities = argsKwg.get("amenities")
        city = argsKwg.get("city")
        lowest_price = argsKwg.get("lowest_price")
        hightest_price = argsKwg.get("hightest_price")
        apartment_type = argsKwg.get("apartment_type")

        filters = []

        if lowest_price is not None and hightest_price is not None:
            filters.append(
                Apartment.price_per_day.between(lowest_price, hightest_price)
            )

        if city:
            filters.append(Apartment.city == city)

        if apartment_type:
            filters.append(Apartment.apartment_type == apartment_type)

        if amenities and "" not in amenities and len(amenities) > 0:
            print(amenities)
            filters.append(Apartment.amenities.any(Amenity.name.in_(amenities)))

        apartments = (
            self.db.query(Apartment)
            .filter(*filters)
            .options(
                joinedload(Apartment.images),
                joinedload(Apartment.comments),
            )
            .all()
        )

        for apartment in apartments:
            if len(apartment.comments) < 1:
                apartment.total_rating = 0
            else:
                total_rating_in_comment = 0
                for comment in apartment.comments:
                    total_rating_in_comment += (
                        comment.rate_location
                        + comment.rate_interior
                        + comment.rate_amenities
                        + comment.rate_price
                    ) / 5

                apartment.total_rating = round(
                    (total_rating_in_comment / len(apartment.comments)), 1
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
                joinedload(Apartment.owner),
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
                comment.total_rating = total_rating

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
            total_people=apartment.total_people,
            address=apartment.address,
            city=apartment.city,
            apartment_type=apartment.apartment_type,
            user_id=apartment.user_id,
        )

        apartment_tags = []

        for tag_id in apartment.tag_ids:
            apartment_tag = ApartmentTag(
                id=str(uuid.uuid4()), apartment_id=apartment_create.id, tag_id=tag_id
            )
            apartment_tags.append(apartment_tag)

        apartment_create.apartment_tags = apartment_tags

        amenities = []
        for amenity_id in apartment.amenities:
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

    async def gets_apartment_by_tag_id(self, tag_id: str | None, **argsKw):
        amenities = argsKw.get("amenities")
        city = argsKw.get("city")
        lowest_price = argsKw.get("lowest_price")
        hightest_price = argsKw.get("hightest_price")
        apartment_type = argsKw.get("apartment_type")

        filters = []

        filters.append(ApartmentTag.tag_id == tag_id)

        if lowest_price and hightest_price:
            filters.append(
                Apartment.price_per_day.between(lowest_price, hightest_price)
            )

        if city:
            filters.append(Apartment.city == city)

        if apartment_type:
            filters.append(Apartment.apartment_type == apartment_type)

        if amenities:
            filters.append(Apartment.amenities.any(Amenity.name.in_(amenities)))

        apartments_with_tag = (
            self.db.query(Apartment)
            .join(Apartment.apartment_tags)  # Joins để lấy các căn hộ có tagId cụ thể
            .filter(*filters)
            .options(joinedload(Apartment.images), joinedload(Apartment.comments))
            .all()
        )

        for apartment in apartments_with_tag:
            total_rating_in_comment = 0

            if len(apartment.comments) < 1:
                apartment.total_rating = 0
            else:
                for comment in apartment.comments:
                    total_rating_in_comment += (
                        comment.rate_location
                        + comment.rate_interior
                        + comment.rate_amenities
                        + comment.rate_price
                    ) / 5

                apartment.total_rating = round(
                    total_rating_in_comment / len(apartment.comments), 1
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
