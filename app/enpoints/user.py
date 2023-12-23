from fastapi import APIRouter, Depends, status, UploadFile, File
from ..database import get_db
from sqlalchemy.orm import Session
from ..schemas.user import (
    UserCreateSchema,
    UserLoginSchema,
    UserUpdateSchema,
    UserChangePasswordSchema,
)
from ..helpers.oauth2 import JWTBearer
from ..services.userService import UserService
from ..helpers.response import make_response_object
from fastapi.responses import FileResponse
import logging
import os


logging.basicConfig(level=logging.INFO)

logger = logging.getLogger(__name__)

router = APIRouter()


def get_user_service(db: Session = Depends(get_db)):
    return UserService(db)


@router.get("/verify-active/user", status_code=status.HTTP_200_OK)
async def user_verify_active(
    email: str, verify_code: str, userService: UserService = Depends(get_user_service)
):
    print(email)
    await userService.active_user(email=email, verify_code=verify_code)
    return {"message": "Create user success!!"}


@router.get("/all", status_code=status.HTTP_200_OK)
async def get_users(
    page: int = None,
    email: str = None,
    userService: UserService = Depends(get_user_service),
    # access_token=Depends(JWTBearer()),
):
    kwargs = {"email": email, "page": page}
    response = await userService.gets(**kwargs)
    return response


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


@router.get("/{user_id}/avatar")
async def get_file(user_id: str):
    # Đường dẫn đến tệp ảnh
    folder_users_avatar = os.path.join("data/avatar/users")
    path_avatar = os.path.join(folder_users_avatar, user_id)

    if not os.path.exists(path_avatar):
        return {"message": "File not found"}

    return FileResponse(path_avatar)


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


@router.patch("/update_avatar/{user_id}", status_code=status.HTTP_200_OK)
async def update_avatar(
    user_id: str,
    avatar: UploadFile = File(...),
    userService: UserService = Depends(get_user_service),
):
    response = await userService.update_avatar(user_id=user_id, avatar=avatar)
    return make_response_object(response)


@router.patch("/update_user/{user_id}", status_code=status.HTTP_200_OK)
async def update_user(
    user_id: str,
    user_update: UserUpdateSchema,
    userService: UserService = Depends(get_user_service),
):
    response = await userService.update_user(user_id=user_id, user_update=user_update)
    return make_response_object(response)


@router.patch("/update_user/{user_id}", status_code=status.HTTP_200_OK)
async def update_user(
    user_id: str,
    user_update: UserUpdateSchema,
    userService: UserService = Depends(get_user_service),
):
    response = await userService.update_user(user_id=user_id, user_update=user_update)
    return make_response_object(response)


@router.delete("/", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
    email: str,
    user_id: str,
    userService: UserService = Depends(get_user_service),
):
    response = await userService.delete_user(email, user_id)
    return make_response_object(response)


@router.put("/change-password", status_code=status.HTTP_200_OK)
async def delete_user(
    data: UserChangePasswordSchema,
    userService: UserService = Depends(get_user_service),
):
    response = await userService.change_password(
        email=data.email, password=data.password
    )
    return make_response_object(response)
