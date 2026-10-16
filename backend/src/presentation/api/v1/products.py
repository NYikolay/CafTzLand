from typing import Annotated

from fastapi import APIRouter, Depends

from application.products.list_products import ListProducts
from domain.products import Product
from presentation.api.v1.schemas import ProductOut
from presentation.dependencies import get_list_products

router = APIRouter(tags=["products"])


@router.get("/products", response_model=list[ProductOut])
async def list_products(
    use_case: Annotated[ListProducts, Depends(get_list_products)],
) -> list[Product]:
    return await use_case()
