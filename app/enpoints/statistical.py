from fastapi import APIRouter, Depends, status, Path
from ..database import get_db
from sqlalchemy.orm import Session
from ..services.statisticalService import Statistical
import logging

logging.basicConfig(level=logging.INFO)

logger = logging.getLogger(__name__)

router = APIRouter()


def get_statistical_service(db: Session = Depends(get_db)):
    return Statistical(db)


@router.get('/common/admin')
async def get_statistical_admin(statistical_service : Statistical = Depends(get_statistical_service)) :
    response = await statistical_service.statistical_admin()
    return response


@router.get('/chart/admin')
async def get_statistical_admin(statistical_service : Statistical = Depends(get_statistical_service)) :
    response = await statistical_service.get_chart_admin()
    return response