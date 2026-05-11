"""Contract Types Feature Package"""

from fastapi import APIRouter

from .create_contract_type import router as create_contract_type_router
from .get_all_contract_types import router as get_all_contract_types_router
from .get_one_contract_type import router as get_one_contract_type_router
from .update_contract_type import router as update_contract_type_router

router = APIRouter(prefix="/contract-types", tags=["Contract Types"])

router.include_router(create_contract_type_router)
router.include_router(get_all_contract_types_router)
router.include_router(get_one_contract_type_router)
router.include_router(update_contract_type_router)
