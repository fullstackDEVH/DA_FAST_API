from pydantic import BaseModel
from datetime import datetime
from enum import Enum


class CreateContractSchema(BaseModel):
    content: str
    start_date: datetime
    end_date: datetime
    apartment_id: str
    user_id: str


class UpdateContractSchema(BaseModel):
    content: str | None = None
    start_date: datetime | None = None
    end_date: datetime | None = None
    apartment_id: str | None = None
    user_id: str | None = None


class TYPE_CONTRACT_ID(str, Enum):
    USER_ID = "USER_ID"
    APARTMENT_ID = "APARTMENT_ID"
