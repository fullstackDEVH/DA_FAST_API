from fastapi import APIRouter, Depends, status, Path
from ..database import get_db
from sqlalchemy.orm import Session
from ..schemas.message import CreateMessage, UpdateMessage
from ..helpers.oauth2 import JWTBearer
from ..services.messageService import MessageService
from ..helpers.response import make_response_object
import logging


logging.basicConfig(level=logging.INFO)

logger = logging.getLogger(__name__)

router = APIRouter()


def get_messages_service(db: Session = Depends(get_db)):
    return MessageService(db)


@router.get("/", status_code=status.HTTP_200_OK, response_model=CreateMessage)
async def get_message(
    message_id: str,
    messsageService: MessageService = Depends(get_messages_service),
):
    response = await messsageService.get_message_by_id(message_id)
    return make_response_object(response)


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=CreateMessage)
async def create_message(
    message_data: CreateMessage,
    messsageService: MessageService = Depends(get_messages_service),
):
    response = await messsageService.create_message(message_data)
    return make_response_object(response)


@router.patch(
    "/{message_id}", status_code=status.HTTP_200_OK, response_model=CreateMessage
)
async def update_message(
    message_data: UpdateMessage,
    message_id: str = Path(title="The ID of the item to get"),
    messsageService: MessageService = Depends(get_messages_service),
):
    response = await messsageService.update_message(message_id, message_data)
    return make_response_object(response)


@router.delete("/{message_id}", status_code=status.HTTP_200_OK)
async def delete_message(
    message_id: str = Path(title="The ID of the item to get"),
    messsageService: MessageService = Depends(get_messages_service),
):
    response = await messsageService.delete_message(message_id)
    return make_response_object(response)
