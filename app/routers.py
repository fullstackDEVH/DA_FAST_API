from fastapi import APIRouter

from .enpoints import (
    apartment,
    notication,
    user,
    contract,
    tag,
    amenity,
    apartmentComment,
    statistical,
    room,
    message,
)
from .socket import router as socket_router


router = APIRouter()

router.include_router(user.router, prefix="/users", tags=["users"])
router.include_router(apartment.router, prefix="/apartments", tags=["apartments"])
router.include_router(tag.router, prefix="/tags", tags=["tags"])
router.include_router(contract.router, prefix="/contracts", tags=["contracts"])
router.include_router(amenity.router, prefix="/amenities", tags=["amenities"])
router.include_router(
    apartmentComment.router, prefix="/apartmentComment", tags=["apartmentComment"]
)
router.include_router(statistical.router, prefix="/statisticals", tags=["statisticals"])

router.include_router(
    notication.router, prefix="/notifications", tags=["notifications"]
)

router.include_router(message.router, prefix="/messages", tags=["messages"])

router.include_router(room.router, prefix="/rooms", tags=["rooms"])
