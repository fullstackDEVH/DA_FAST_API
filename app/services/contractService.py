from fastapi import HTTPException, status
from sqlalchemy.orm import Session, joinedload
from ..schemas.contract import (
    CreateContractSchema,
    TYPE_CONTRACT_ID,
    UpdateContractSchema,
)
from ..database import Contract, User, Apartment
from enum import Enum
import uuid
from sqlalchemy import desc


class TYPE_CONTRACT_ID(str, Enum):
    USER_ID = "USER_ID"
    APARTMENT_ID = "APARTMENT_ID"
    CONTRACT_ID = "CONTRACT_ID"


class ContractService:
    def __init__(self, db: Session):
        self.db = db

    async def get_contract_user_and_apartment(self, id: str):
        # Sử dụng SQLAlchemy để thực hiện truy vấn, kết nối Contract, User và Apartment
        result = (
            self.db.query(Contract, User, Apartment)
            .join(User, User.id == Contract.user_id)
            .join(Apartment, Apartment.id == Contract.apartment_id)
            .filter(Contract.id == id)
            .first()
        )
        if not result:
            return {"contract": None, "user": None, "apartment": None}

        contract, user, apartment = result
        return {"contract": contract, "owner": user, "apartment": apartment}

    async def get_contracts(self):
        return (
            self.db.query(Contract)
            .order_by(desc(Contract.created_at))
            .options(
                joinedload(Contract.user),
                joinedload(Contract.apartment).options(joinedload(Apartment.images)),
            )
            .all()
        )

    async def get_contract_latest(self):
        return (
            self.db.query(Contract)
            .order_by(desc(Contract.created_at))
            .limit(6)
            .options(
                joinedload(Contract.user),
                joinedload(Contract.apartment).options(joinedload(Apartment.images)),
            )
            .all()
        )

    async def get_contract_by_id(self, type_id: TYPE_CONTRACT_ID, id: str):
        if type_id == TYPE_CONTRACT_ID.USER_ID:
            return (
                self.db.query(Contract)
                .filter(Contract.user_id == id)
                .options(joinedload(Contract.apartment).joinedload(Apartment.images))
                .all()
            )
        elif type_id == TYPE_CONTRACT_ID.APARTMENT_ID:
            return self.db.query(Contract).filter(Contract.apartment_id == id).first()

        return self.db.query(Contract).filter(Contract.id == id).first()

    async def create(self, contract: CreateContractSchema):
        found_contract = (
            self.db.query(Contract)
            .filter(
                Contract.apartment_id == contract.apartment_id,
                Contract.user_id == contract.user_id,
            )
            .first()
        )

        if found_contract:
            raise HTTPException(status_code=400, detail="Contract is exist !!")

        contract_create = Contract(
            id=str(uuid.uuid4()),
            content=contract.content,
            start_date=contract.start_date,
            end_date=contract.end_date,
            apartment_id=contract.apartment_id,
            user_id=contract.user_id,
            total_amount=contract.total_amount,
            num_of_people=contract.num_of_people,
        )
        self.db.add(contract_create)
        self.db.commit()
        self.db.refresh(contract_create)

        return contract_create

    async def update(self, contract_id: str, contract: UpdateContractSchema):
        found_contract = await self.get_contract_by_id(
            type_id=TYPE_CONTRACT_ID.CONTRACT_ID, id=contract_id
        )

        if not found_contract:
            raise HTTPException(status_code=404, detail="Contract not found")

        contract_data = contract.model_dump(exclude_unset=True)

        for key, value in contract_data.items():
            setattr(found_contract, key, value)

        self.db.add(found_contract)
        self.db.commit()
        self.db.refresh(found_contract)

        return found_contract

    async def delete(self, contract_id: str):
        found_contract_query = await self.get_contract_by_id(
            type_id=TYPE_CONTRACT_ID.CONTRACT_ID, id=contract_id
        )

        if not found_contract_query:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="contract not found!!"
            )

        self.db.delete(found_contract_query)
        self.db.commit()

        return {"message": f"Xoá hợp đồng thành công."}
