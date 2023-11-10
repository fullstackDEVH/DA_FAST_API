from fastapi import APIRouter, Depends, status
from ..database import get_db
from sqlalchemy.orm import Session
from ..schemas.user import UserCreateSchema, UserLoginSchema
from ..helpers.oauth2 import JWTBearer
from ..services.userService import UserService
from ..helpers.response import make_response_object
import logging


logging.basicConfig(level=logging.INFO)

logger = logging.getLogger(__name__)

router = APIRouter()


def get_user_service(db: Session = Depends(get_db)):
    return UserService(db)


@router.get("/all", status_code=status.HTTP_200_OK)
async def get_users(
    username: str | None = None,
    userService: UserService = Depends(get_user_service),
    access_token=Depends(JWTBearer()),
):
    response = await userService.gets()
    return make_response_object(response)


@router.get("/", status_code=status.HTTP_200_OK)
async def get_user(
    username: str | None = None,
    userService: UserService = Depends(get_user_service),
    access_token=Depends(JWTBearer()),
):
    response = await userService.get(access_token, username)
    return make_response_object(response)


@router.get("/{user_id}", status_code=status.HTTP_200_OK)
async def get_user(
    user_id: str | None = None,
    userService: UserService = Depends(get_user_service),
    # access_token=Depends(JWTBearer()),
):
    response = await userService.get_user_by_id(user_id)
    return make_response_object(response)


@router.post("/login", status_code=status.HTTP_200_OK)
async def login(
    user_create: UserLoginSchema, userService: UserService = Depends(get_user_service)
):
    response = await userService.user_login(user_obj=user_create)
    return make_response_object(response)


@router.post("/sign_up", status_code=status.HTTP_201_CREATED)
async def create_user(
    user_create: UserCreateSchema, userService: UserService = Depends(get_user_service)
):
    await userService.user_sign_up(user_obj=user_create)
    return {"message": "Create user success!!"}


@router.post("/refresh_token", status_code=status.HTTP_200_OK)
async def refresh_token(
    access_token=Depends(JWTBearer()),
    userService: UserService = Depends(get_user_service),
):
    response = await userService.user_refresh_token(access_token)
    return make_response_object(response)


@router.post("/verify_code", status_code=status.HTTP_200_OK)
async def verify_user_by_code():
    return make_response_object({"data": "scu"})


@router.delete("/", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
    email: str,
    user_id: str,
    userService: UserService = Depends(get_user_service),
):
    response = await userService.delete_user(email, user_id)
    return make_response_object(response)
