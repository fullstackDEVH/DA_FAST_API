from fastapi import APIRouter

from .enpoints import apartment, notication, user, contract, tag, amenity
from .socket import router as socket_router


router = APIRouter()

router.include_router(user.router, prefix="/users", tags=["users"])
router.include_router(apartment.router, prefix="/apartments", tags=["apartments"])
router.include_router(tag.router, prefix="/tags", tags=["tags"])
router.include_router(contract.router, prefix="/contracts", tags=["contracts"])

router.include_router(
    notication.router, prefix="/notifications", tags=["notifications"]
)
router.include_router(amenity.router, prefix="/amenities", tags=["amenities"])
# router.include_router(socket_router, prefix="/sockets", tags=["sockets"])
