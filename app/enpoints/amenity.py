from fastapi import APIRouter, Depends, status, Path
from ..database import get_db
from sqlalchemy.orm import Session
from ..schemas.amenity import AmenityCreate
from ..helpers.oauth2 import JWTBearer
from ..services.amenityService import AmenityService
from ..helpers.response import make_response_object
import logging


logging.basicConfig(level=logging.INFO)

logger = logging.getLogger(__name__)

router = APIRouter()


def get_amenity_service(db: Session = Depends(get_db)):
    return AmenityService(db)


@router.get("/", status_code=status.HTTP_200_OK, response_model=AmenityCreate)
async def get_amenity(
    amenity_id: str,
    amenityService: AmenityService = Depends(get_amenity_service),
):
    response = await amenityService.get_amenity(amenity_id)
    return make_response_object(response)


@router.get("/all", status_code=status.HTTP_200_OK)
async def get_amenities(
    amenityService: AmenityService = Depends(get_amenity_service),
):
    response = await amenityService.get_amenitys()
    return make_response_object(response)


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_amenity(
    amenity: AmenityCreate,
    amenityService: AmenityService = Depends(get_amenity_service),
):
    response = await amenityService.create_amenity(amenity)
    return make_response_object(response)


@router.patch(
    "/{amenity_id}", status_code=status.HTTP_200_OK, response_model=AmenityCreate
)
async def update_amenity_by_id(
    amenity: AmenityCreate,
    amenity_id: str = Path(title="The ID of the item to get"),
    amenityService: AmenityService = Depends(get_amenity_service),
):
    response = await amenityService.update_amenity(amenity_id, amenity)
    return make_response_object(response)


@router.delete("/{amenity_id}", status_code=status.HTTP_200_OK)
async def delete_amenity_by_id(
    amenity_id: str = Path(title="The ID of the item to get"),
    amenityService: AmenityService = Depends(get_amenity_service),
):
    response = await amenityService.delete_amenity(amenity_id)
    return make_response_object(response)
