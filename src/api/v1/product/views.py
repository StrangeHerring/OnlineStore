from fastapi import status, APIRouter, Depends
from fastapi.responses import JSONResponse
from fastapi.security import HTTPBearer

from infrastructure.repositories.postgresql.product import PostgreSQLProductRepository
from usecase.create_product.abstract import AbstractCreateProductUseCase

from .dependencies import create_product_use_case
from .models import ProductCreate, ProductBase, ProductUpdate

router = APIRouter(tags=["Products"],prefix='/products')

auth_scheme = HTTPBearer(scheme_name="Bearer")


@router.post("", response_model=ProductBase)
async def create_product(
    payload: ProductCreate,
    usecase: AbstractCreateProductUseCase = Depends(create_product_use_case)
) -> JSONResponse:
    product = await usecase.execute(payload)
    return JSONResponse(status_code=status.HTTP_201_CREATED, content=product.model_dump())

@router.get("/{product_id}", response_model=ProductBase)
async def get_product(
    product_id: int,
    repo: PostgreSQLProductRepository = Depends(),
) -> JSONResponse:
    content = repo.get_product(product_id)
    return JSONResponse(status_code=status.HTTP_200_OK, content=content.model_dump())

@router.get("/", response_model=list[ProductBase])
async def list_products(
    limit: int = 10,
    offset: int = 0,
    repo: PostgreSQLProductRepository = Depends(),
) -> JSONResponse:
    content = repo.list_products(limit, offset)
    return JSONResponse(status_code=status.HTTP_200_OK, content=[product.model_dump() for product in content])

@router.put("/{product_id}", response_model=ProductUpdate)
async def update_product(
    product_id: int,
    payload: ProductUpdate,
    repo: PostgreSQLProductRepository = Depends(),
) -> JSONResponse:
    repo.update_product(product_id, payload)
    return JSONResponse(status_code=status.HTTP_200_OK)

@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_product(
    product_id: int,
    repo: PostgreSQLProductRepository = Depends(),
) -> JSONResponse:
    repo.delete_product(product_id)
    return JSONResponse(status_code=status.HTTP_204_NO_CONTENT)