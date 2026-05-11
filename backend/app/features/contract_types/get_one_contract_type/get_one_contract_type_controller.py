"""Get One Contract Type Controller - HTTP endpoint for retrieving a single contract type"""

from fastapi import APIRouter, Depends, Path
from sqlalchemy.orm import Session

from ....database import get_db
from ..shared.contract_type_dto import ContractTypeResponse
from .get_one_contract_type_usecase import GetOneContractTypeUseCase

router = APIRouter()


@router.get(
    "/{contract_type_id}",
    response_model=ContractTypeResponse,
    summary="Get a contract type by ID",
    description="Retrieve a specific contract type by its unique identifier.",
    responses={
        200: {"description": "Contract type retrieved successfully"},
        404: {"description": "Contract type not found"},
    }
)
def get_one_contract_type(
    contract_type_id: int = Path(..., gt=0, description="The ID of the contract type to retrieve"),
    db: Session = Depends(get_db)
):
    """
    Get a specific contract type by ID
    
    - **contract_type_id**: Unique identifier of the contract type
    """
    use_case = GetOneContractTypeUseCase(db)
    return use_case.execute(contract_type_id)
