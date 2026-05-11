"""Get All Contract Types Controller - HTTP endpoint for listing contract types"""

from typing import List
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from ....database import get_db
from ..shared.contract_type_dto import ContractTypeResponse
from .get_all_contract_types_usecase import GetAllContractTypesUseCase

router = APIRouter()


@router.get(
    "/",
    response_model=List[ContractTypeResponse],
    summary="Get all contract types",
    description="Retrieve a list of contract types with optional pagination and filtering.",
    responses={
        200: {"description": "List of contract types retrieved successfully"},
    }
)
def get_all_contract_types(
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(100, ge=1, le=1000, description="Maximum number of records to return"),
    active_only: bool = Query(False, description="Filter to show only active contract types"),
    db: Session = Depends(get_db)
):
    """
    Get all contract types
    
    - **skip**: Number of records to skip (for pagination)
    - **limit**: Maximum number of records to return (default: 100, max: 1000)
    - **active_only**: If true, returns only active contract types
    """
    use_case = GetAllContractTypesUseCase(db)
    return use_case.execute(skip=skip, limit=limit, active_only=active_only)
