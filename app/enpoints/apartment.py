from fastapi import APIRouter, Depends, status, UploadFile, Form, File, Path
from typing import Annotated
from ..database import get_db, Apartment
from sqlalchemy.orm import Session
from ..schemas.apartment import ApartmentUpdateSchema
from ..helpers.oauth2 import JWTBearer
from ..services.apartmentService import ApartmentService
from ..helpers.response import make_response_object
from fastapi.responses import FileResponse
import logging
import os

logging.basicConfig(level=logging.INFO)

logger = logging.getLogger(__name__)


router = APIRouter()


def get_apartment_service(db: Session = Depends(get_db)):
    return ApartmentService(db)


@router.get("/", status_code=status.HTTP_200_OK)
async def get_apartment_by_room(
    room: str | None = None,
    userId: str | None = None,
    apartmentService: ApartmentService = Depends(get_apartment_service),
):
    response = await apartmentService.get_apartment_by_room(userId, room)
    return make_response_object(response)


@router.get("/all", status_code=status.HTTP_200_OK)
async def get_apartments(
    apartmentService: ApartmentService = Depends(get_apartment_service),
):
    response = await apartmentService.gets()
    return make_response_object(response)


@router.get("/{room}/banner")
async def get_file(room: str):
    # Đường dẫn đến tệp ảnh
    folder_banner_apartment = os.path.join("data/banner/apartment")
    path_banner_apartment = os.path.join(folder_banner_apartment, room)

    if not os.path.exists(path_banner_apartment):
        return {"message": "File not found"}

    return FileResponse(path_banner_apartment)


@router.post("/", status_code=status.HTTP_201_CREATED)
async def get_apartment_by_room(
    name: Annotated[str, Form()],
    desc: Annotated[str, Form()],
    room: Annotated[str, Form()],
    image: UploadFile = File(...),
    apartmentService: ApartmentService = Depends(get_apartment_service),
):
    response = await apartmentService.create_apartment(name, desc, room, image)
    return make_response_object(response)


@router.patch("/{apartment_id}", status_code=status.HTTP_200_OK)
async def update_apartment(
    apartment_id :  Annotated[str, Path(title="The ID apartment to get")],
    apartment : ApartmentUpdateSchema,
    apartmentService: ApartmentService = Depends(get_apartment_service),
):
    response = await apartmentService.update(apartment_id, apartment)
    return make_response_object(response)


@router.delete("/{room}")
async def delete_apartment(
    room: str | None,
    apartmentService: ApartmentService = Depends(get_apartment_service),
):
    response = await apartmentService.delete(room)
    return make_response_object(response)
