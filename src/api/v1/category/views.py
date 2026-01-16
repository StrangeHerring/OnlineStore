from fastapi import status, APIRouter, Depends
from fastapi.responses import JSONResponse
from fastapi.security import HTTPBearer

from infrastructure.repositories.postgresql.category import PostgreSQLCategoryRepository
from usecase.create_category.abstract import AbstractCreateCategoryUseCase

from .dependencies import create_category_use_case
from .models import CategoryCreate, CategoryBase, CategoryUpdate

router = APIRouter(tags=["Categories"],prefix='/categories')

auth_scheme = HTTPBearer(scheme_name="Bearer")


@router.post("", response_model=CategoryBase)
async def create_category(
    payload: CategoryCreate,
    usecase: AbstractCreateCategoryUseCase = Depends(create_category_use_case)
) -> JSONResponse:
    category = await usecase.execute(payload)
    return JSONResponse(status_code=status.HTTP_201_CREATED, content=category.model_dump())

@router.get("/{category_id}", response_model=CategoryBase)
async def get_category(
    category_id: int,
    repo: PostgreSQLCategoryRepository = Depends(),
) -> JSONResponse:
    content = repo.get_category(category_id)
    return JSONResponse(status_code=status.HTTP_200_OK, content=content.model_dump())

@router.get("/", response_model=list[CategoryBase])
async def list_Categories(
    limit: int = 10,
    offset: int = 0,
    repo: PostgreSQLCategoryRepository = Depends(),
) -> JSONResponse:
    content = repo.list_categories(limit, offset)
    return JSONResponse(status_code=status.HTTP_200_OK, content=[category.model_dump() for category in content])

@router.put("/{category_id}", response_model=CategoryUpdate)
async def update_category(
    category_id: int,
    payload: CategoryUpdate,
    repo: PostgreSQLCategoryRepository = Depends(),
) -> JSONResponse:
    repo.update_category(category_id, payload)
    return JSONResponse(status_code=status.HTTP_200_OK)

@router.delete("/{category_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_category(
    category_id: int,
    repo: PostgreSQLCategoryRepository = Depends(),
) -> JSONResponse:
    repo.delete_category(category_id)
    return JSONResponse(status_code=status.HTTP_204_NO_CONTENT)