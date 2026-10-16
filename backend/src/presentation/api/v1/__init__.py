from fastapi import APIRouter

from presentation.api.v1 import leads, products

router = APIRouter(prefix="/api/v1")
router.include_router(leads.router)
router.include_router(products.router)
