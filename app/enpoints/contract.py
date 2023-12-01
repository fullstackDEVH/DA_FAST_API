from fastapi import APIRouter, Depends, status, Path
from ..database import get_db
from sqlalchemy.orm import Session
from ..schemas.contract import (
    CreateContractSchema,
    TYPE_CONTRACT_ID,
    UpdateContractSchema,
)
from ..helpers.oauth2 import JWTBearer
from ..services.contractService import ContractService
from ..helpers.response import make_response_object
import logging


logging.basicConfig(level=logging.INFO)

logger = logging.getLogger(__name__)

router = APIRouter()


def get_contract_service(db: Session = Depends(get_db)):
    return ContractService(db)


@router.get("/", status_code=status.HTTP_200_OK)
async def get_contract(
    type_id: TYPE_CONTRACT_ID,
    id: str,
    contractService: ContractService = Depends(get_contract_service),
):
    response = await contractService.get_contract_by_id(type_id, id)
    return make_response_object(response)


@router.get("/latest", status_code=status.HTTP_200_OK)
async def get_contract(
    contractService: ContractService = Depends(get_contract_service),
):
    response = await contractService.get_contract_latest()
    return make_response_object(response)

@router.get("/apartment/{apartment_id}", status_code=status.HTTP_200_OK)
async def get_contract_apartment(
    apartment_id : str,
    contractService: ContractService = Depends(get_contract_service),
):
    response = await contractService.get_contract_apartment(apartment_id)
    return make_response_object(response)


@router.get("/all", status_code=status.HTTP_200_OK)
async def get_contracts(
    contractService: ContractService = Depends(get_contract_service),
):
    response = await contractService.get_contracts()
    return make_response_object(response)


@router.get("/information", status_code=status.HTTP_200_OK)
async def get_contract_information(
    contract_id: str,
    contractService: ContractService = Depends(get_contract_service),
):
    response = await contractService.get_contract_user_and_apartment(id=contract_id)
    return make_response_object(response)


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_contract(
    contract: CreateContractSchema,
    contractService: ContractService = Depends(get_contract_service),
):
    response = await contractService.create(contract)
    return response


@router.patch("/{contract_id}", status_code=status.HTTP_200_OK)
async def update_contract_by_id(
    contract: UpdateContractSchema,
    contract_id: str = Path(title="The ID of the item to get"),
    contractService: ContractService = Depends(get_contract_service),
):
    response = await contractService.update(contract_id, contract)
    return make_response_object(response)


@router.delete("/{contract_id}", status_code=status.HTTP_200_OK)
async def delete_contract_by_id(
    contract_id: str = Path(title="The ID of the item to get"),
    contractService: ContractService = Depends(get_contract_service),
):
    response = await contractService.delete(contract_id=contract_id)
    return make_response_object(response)
