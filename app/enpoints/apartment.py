from fastapi import APIRouter, Depends, status, UploadFile, Form, File, Path, Query
from typing import Annotated, List
from ..database import get_db, Apartment
from pydantic import BaseModel, UUID4
from sqlalchemy.orm import Session
from ..schemas.apartment import (
    ApartmentUpdateSchema,
    ApartmentCreateSchte,
    ApartmentType,
    ApartmentCity,
)
from ..helpers.oauth2 import JWTBearer
from ..services.apartmentService import ApartmentService
from ..services import userService
from ..helpers.response import make_response_object
from ..helpers.oauth2 import get_user_in_access_token
from fastapi.responses import FileResponse
import logging
import os

logging.basicConfig(level=logging.INFO)

logger = logging.getLogger(__name__)


router = APIRouter()


def get_apartment_service(db: Session = Depends(get_db)):
    return ApartmentService(db)


@router.get("/all", status_code=status.HTTP_200_OK)
async def get_apartments(
    name: str = None,
    page: int = None,
    is_approved: bool = None,
    apartmentService: ApartmentService = Depends(get_apartment_service),
):
    args = {"name": name, "page": page, "is_approved": is_approved}
    response = await apartmentService.gets_all(**args)
    return response


@router.get("/", status_code=status.HTTP_200_OK)
async def get_apartment_detail_by_id(
    apartment_id: str | None = None,
    apartmentService: ApartmentService = Depends(get_apartment_service),
):
    response = await apartmentService.get_apartment_by_apartment_id(apartment_id)
    return make_response_object(response)


@router.get("/tag", status_code=status.HTTP_200_OK)
async def gets_apartment_by_tag_id(
    tag_id: str = None,
    city: ApartmentCity = None,
    lowest_price: int = None,
    hightest_price: int = None,
    apartment_type: ApartmentType = None,
    amenities: list = Query(
        None, title="Amenity Names", description="List of amenity names"
    ),
    is_approved: bool = None,
    apartmentService: ApartmentService = Depends(get_apartment_service),
):
    argsKwg = {
        "city": city,
        "lowest_price": lowest_price,
        "hightest_price": hightest_price,
        "apartment_type": apartment_type,
        "amenities": amenities,
        "is_approved": is_approved,
    }

    if tag_id is not None:
        response = await apartmentService.gets_apartment_by_tag_id(
            tag_id=tag_id, **argsKwg
        )
    else:
        response = await apartmentService.gets_all(**argsKwg)

    return response


@router.get("/{apartment_id}/apartment", status_code=status.HTTP_200_OK)
async def get_apartment_by_id(
    apartment_id: str | None = None,
    apartmentService: ApartmentService = Depends(get_apartment_service),
):
    response = await apartmentService.get_apartment_by_id(apartment_id)
    return make_response_object(response)


@router.get("/{apartment_id}/banner/{index}")
async def get_file(apartment_id: str, index: int):
    # Đường dẫn đến tệp ảnh
    folder_banner_apartment = os.path.join("data/banner/apartments")
    path_banner_apartment = os.path.join(folder_banner_apartment, apartment_id)
    endpoint_banner_apartment = os.path.join(path_banner_apartment, str(index))

    print(f"path_banner_apartment : {endpoint_banner_apartment}")

    if not os.path.exists(endpoint_banner_apartment):
        return {"message": "File not found"}

    return FileResponse(endpoint_banner_apartment)


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_apartment(
    apartment: ApartmentCreateSchte = Depends(),
    apartmentService: ApartmentService = Depends(get_apartment_service),
    access_token=Depends(JWTBearer()),
):
    user_id = get_user_in_access_token(access_token)
    response = await apartmentService.create_apartment(apartment, user_id=user_id)
    return response


@router.patch("/upload/{apartment_id}", status_code=status.HTTP_201_CREATED)
async def upload_images_apartment(
    apartment_id: str,
    images: list[UploadFile] = File(...),
    apartmentService: ApartmentService = Depends(get_apartment_service),
):
    response = await apartmentService.upload_images(apartment_id, images)
    return make_response_object(response)


@router.patch("/{apartment_id}", status_code=status.HTTP_200_OK)
async def update_apartment(
    apartment_id: Annotated[str, Path(title="The ID apartment to get")],
    apartment: ApartmentUpdateSchema,
    apartmentService: ApartmentService = Depends(get_apartment_service),
):
    response = await apartmentService.update(apartment_id, apartment)
    return make_response_object(response)


@router.delete("/{apartment_id}")
async def delete_apartment(
    apartment_id: str | None,
    apartmentService: ApartmentService = Depends(get_apartment_service),
):
    response = await apartmentService.delete(apartment_id)
    return make_response_object(response)
