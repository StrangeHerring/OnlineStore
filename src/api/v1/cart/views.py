from fastapi import status, APIRouter, Depends, Cookie
from typing import Optional
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
    usecase: AbstractCreateCartUseCase = Depends(create_cart_use_case),
    cart_cookie: Optional[str] = Cookie(default=None, alias='cart'),
) -> JSONResponse:
    cart = await usecase.execute(payload, token, cart_cookie)
    # if user.is_guest():
    #     JSONResponse.set_cookie(
    #         key='cart',
    #         value=cart.model_dump(),
    #         max_age=30 * 24 * 3600,
    #         httponly=True,
    #         samesite="lax"
    #     )
    #     return JSONResponse(status_code=status.HTTP_201_CREATED)
    return JSONResponse(status_code=status.HTTP_201_CREATED, content=cart.model_dump())

@router.get("/{cart_id}", response_model=CartBase)
async def get_cart(
    cart_id: int,
    token: HTTPAuthorizationCredentials = Depends(auth_scheme),
    repo: PostgreSQLCartRepository = Depends(),
    cart_cookie: Optional[str] = Cookie(default=None, alias='cart'),
) -> JSONResponse:
    content = repo.get_cart(token, cart_id, cart_cookie)
    # if user.is_guest():
    #     JSONResponse.set_cookie(
    #         key='cart',
    #         value=content.model_dump(),
    #         max_age=30 * 24 * 3600,
    #         httponly=True,
    #         samesite="lax"
    #     )
    return JSONResponse(status_code=status.HTTP_200_OK, content=content.model_dump())

@router.get("/", response_model=list[CartBase])
async def list_сarts(
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
    cart_cookie: Optional[str] = Cookie(default=None, alias='cart'),
) -> JSONResponse:
    repo.update_cart(token, cart_id, payload, cart_cookie)  
    # if user.is_guest():
    #     JSONResponse.set_cookie(
    #         key='cart',
    #         value=content.model_dump(),
    #         max_age=30 * 24 * 3600,
    #         httponly=True,
    #         samesite="lax"
    #     )
    return JSONResponse(status_code=status.HTTP_200_OK)

@router.delete("/{cart_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_cart(
    cart_id: int,
    token: HTTPAuthorizationCredentials = Depends(auth_scheme),
    repo: PostgreSQLCartRepository = Depends(),
) -> JSONResponse:
    repo.delete_cart(token, cart_id)
    return JSONResponse(status_code=status.HTTP_204_NO_CONTENT)