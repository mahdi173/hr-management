"""Create Contract Type Controller - HTTP endpoint for creating contract types"""

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from ....database import get_db
from ..shared.contract_type_dto import ContractTypeCreate, ContractTypeResponse
from .create_contract_type_usecase import CreateContractTypeUseCase

router = APIRouter()


@router.post(
    "/",
    response_model=ContractTypeResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new contract type",
    description="Create a new contract type with the provided data. Contract type names must be unique.",
    responses={
        201: {"description": "Contract type created successfully"},
        400: {"description": "Invalid input or contract type name already exists"},
    }
)
def create_contract_type(
    contract_type_data: ContractTypeCreate,
    db: Session = Depends(get_db)
):
    """
    Create a new contract type
    
    - **name**: Unique name for the contract type (e.g., "CDI", "CDD")
    - **description**: Optional description of the contract type
    - **weekly_hours**: Default weekly hours (must be > 0 and <= 168)
    - **max_weekly_hours**: Optional maximum weekly hours allowed
    - **is_active**: Whether the contract type is active (default: true)
    """
    use_case = CreateContractTypeUseCase(db)
    return use_case.execute(contract_type_data)
