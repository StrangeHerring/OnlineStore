from fastapi import status, APIRouter, Depends
from fastapi.responses import JSONResponse
from fastapi.security import HTTPBearer
from fastapi.security.http import HTTPAuthorizationCredentials

from infrastructure.repositories.postgresql.cart import PostgreSQLCartRepository
from usecase.create_cart.abstract import AbstractCreateCartUseCase

from .dependencies import create_cart_use_case
from .models import CartCreate, CartBase, CartUpdate

router = APIRouter(tags=["Carts"],prefix='/carts')

auth_scheme = HTTPBearer(scheme_name="Bearer")


@router.post("", response_model=CartBase)
async def create_cart(
    payload: CartCreate,
    token: HTTPAuthorizationCredentials = Depends(auth_scheme),
    usecase: AbstractCreateCartUseCase = Depends(create_cart_use_case)
) -> JSONResponse:
    cart = await usecase.execute(payload, token)
    return JSONResponse(status_code=status.HTTP_201_CREATED, content=cart.model_dump())

@router.get("/{cart_id}", response_model=CartBase)
async def get_cart(
    cart_id: int,
    token: HTTPAuthorizationCredentials = Depends(auth_scheme),
    repo: PostgreSQLCartRepository = Depends(),
) -> JSONResponse:
    content = repo.get_cart(token, cart_id)
    return JSONResponse(status_code=status.HTTP_200_OK, content=content.model_dump())

@router.get("/", response_model=list[CartBase])
async def list_Carts(
    limit: int = 10,
    offset: int = 0,
    token: HTTPAuthorizationCredentials = Depends(auth_scheme),
    repo: PostgreSQLCartRepository = Depends(),
) -> JSONResponse:
    content = repo.list_carts(token, limit, offset)
    return JSONResponse(status_code=status.HTTP_200_OK, content=[cart.model_dump() for cart in content])

@router.put("/{cart_id}", response_model=CartUpdate)
async def update_cart(
    cart_id: int,
    payload: CartUpdate,
    token: HTTPAuthorizationCredentials = Depends(auth_scheme),
    repo: PostgreSQLCartRepository = Depends(),
) -> JSONResponse:
    repo.update_cart(token, cart_id, payload)
    return JSONResponse(status_code=status.HTTP_200_OK)

@router.delete("/{cart_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_cart(
    cart_id: int,
    token: HTTPAuthorizationCredentials = Depends(auth_scheme),
    repo: PostgreSQLCartRepository = Depends(),
) -> JSONResponse:
    repo.delete_cart(token, cart_id)
    return JSONResponse(status_code=status.HTTP_204_NO_CONTENT)