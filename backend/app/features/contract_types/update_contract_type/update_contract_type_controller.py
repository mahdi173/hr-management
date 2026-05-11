"""Update Contract Type Controller - HTTP endpoint for updating contract types"""

from fastapi import APIRouter, Depends, Path
from sqlalchemy.orm import Session

from ....database import get_db
from ..shared.contract_type_dto import ContractTypeUpdate, ContractTypeResponse
from .update_contract_type_usecase import UpdateContractTypeUseCase

router = APIRouter()


@router.put(
    "/{contract_type_id}",
    response_model=ContractTypeResponse,
    summary="Update a contract type",
    description="Update an existing contract type. All fields are optional.",
    responses={
        200: {"description": "Contract type updated successfully"},
        404: {"description": "Contract type not found"},
        400: {"description": "Invalid input or contract type name already exists"},
    }
)
def update_contract_type(
    contract_type_data: ContractTypeUpdate,
    contract_type_id: int = Path(..., gt=0, description="The ID of the contract type to update"),
    db: Session = Depends(get_db)
):
    """
    Update an existing contract type
    
    - **contract_type_id**: Unique identifier of the contract type to update
    - **name**: Optional new name for the contract type
    - **description**: Optional new description
    - **weekly_hours**: Optional new default weekly hours
    - **max_weekly_hours**: Optional new maximum weekly hours
    - **is_active**: Optional new active status
    """
    use_case = UpdateContractTypeUseCase(db)
    return use_case.execute(contract_type_id, contract_type_data)
