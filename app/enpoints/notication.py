from fastapi import APIRouter, Depends
from ..database import get_db
from sqlalchemy.orm import Session

router = APIRouter()


@router.get("/")
async def get_notifications():
    # notifications = db.query(Notification).all()
    return {"notifications": ""}
