from fastapi import APIRouter, Depends, status, Path
from ..database import get_db
from sqlalchemy.orm import Session
from ..schemas.apartmentComment import (
    ApartmentCommentCreateSchema,
    ApartmentCommentUpdateSchema,
)
from ..services.apartmentCommentService import ApartmentCommentService
from ..helpers.response import make_response_object
import logging


logging.basicConfig(level=logging.INFO)

logger = logging.getLogger(__name__)

router = APIRouter()


def get_apartment_comment_service(db: Session = Depends(get_db)):
    return ApartmentCommentService(db)


@router.get("/{apartment_id}", status_code=status.HTTP_200_OK)
async def get_comments_by_apartment_id(
    apartment_id: str,
    apartmentCommentService: ApartmentCommentService = Depends(
        get_apartment_comment_service
    ),
):
    response = await apartmentCommentService.get_comments_by_apartment_id(apartment_id)
    return make_response_object(response)


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_comment(
    apartment_comment: ApartmentCommentCreateSchema,
    apartmentCommentService: ApartmentCommentService = Depends(
        get_apartment_comment_service
    ),
):
    response = await apartmentCommentService.create_comment(apartment_comment)
    return make_response_object(response)


@router.patch("/{comment_id}", status_code=status.HTTP_200_OK)
async def update_tag_by_id(
    apartment_comment: ApartmentCommentUpdateSchema,
    comment_id: str = Path(title="The ID of the item to get"),
    apartmentCommentService: ApartmentCommentService = Depends(
        get_apartment_comment_service
    ),
):
    response = await apartmentCommentService.update_comment(
        comment_id, apartment_comment
    )
    return make_response_object(response)


@router.delete("/{comment_id}", status_code=status.HTTP_200_OK)
async def delete_tag_by_id(
    comment_id: str = Path(title="The ID of the item to get"),
    apartmentCommentService: ApartmentCommentService = Depends(
        get_apartment_comment_service
    ),
):
    response = await apartmentCommentService.delete_comment(comment_id)
    return make_response_object(response)
