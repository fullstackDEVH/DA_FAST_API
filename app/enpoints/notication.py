from fastapi import APIRouter, Depends, status, Path
from ..database import get_db
from sqlalchemy.orm import Session
from ..schemas.tag import TagCreate
from ..helpers.oauth2 import JWTBearer
from ..services.tagService import TagService
from ..helpers.response import make_response_object
import logging


logging.basicConfig(level=logging.INFO)

logger = logging.getLogger(__name__)

router = APIRouter()


def get_tags_service(db: Session = Depends(get_db)):
    return TagService(db)


@router.get("/", status_code=status.HTTP_200_OK, response_model=TagCreate)
async def get_tag(
    tag_id: str,
    tagsService: TagService = Depends(get_tags_service),
):
    response = await tagsService.get_tag(tag_id)
    return make_response_object(response)


@router.get("/all", status_code=status.HTTP_200_OK)
async def get_tags(
    tagsService: TagService = Depends(get_tags_service),
):
    response = await tagsService.get_tags()
    return make_response_object(response)


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=TagCreate)
async def create_tag(
    contract: TagCreate,
    tagsService: TagService = Depends(get_tags_service),
):
    response = await tagsService.create(contract)
    return make_response_object(response)


@router.patch(
    "/{contract_id}", status_code=status.HTTP_200_OK, response_model=TagCreate
)
async def update_tag_by_id(
    tag: TagCreate,
    tag_id: str = Path(title="The ID of the item to get"),
    tagsService: TagService = Depends(get_tags_service),
):
    response = await tagsService.update_tag(tag_id, tag)
    return make_response_object(response)


@router.delete("/{tag_id}", status_code=status.HTTP_200_OK)
async def delete_tag_by_id(
    tag_id: str = Path(title="The ID of the item to get"),
    tagsService: TagService = Depends(get_tags_service),
):
    response = await tagsService.delete_tag(tag_id)
    return make_response_object(response)
