from fastapi import status, APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from fastapi.security import HTTPBearer

from infrastructure.repositories.postgresql.user import PostgreSQLUserRepository
from infrastructure.repositories.postgresql.user.exceptions import UserIsExist
from usecase.create_user.abstract import AbstractCreateUserUseCase

from .dependencies import create_user_use_case
from .models import UserCreate, UserBase, UserUpdate

router = APIRouter(tags=["Users"],prefix='/users')

auth_scheme = HTTPBearer(scheme_name="Bearer")


@router.post("", response_model=UserBase)
async def create_user(
    payload: UserCreate,
    usecase: AbstractCreateUserUseCase = Depends(create_user_use_case)
) -> JSONResponse:
    try:
        user = await usecase.execute(payload)
    except UserIsExist as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))
    return JSONResponse(status_code=status.HTTP_201_CREATED, content=user.model_dump())

@router.get("/{user_id}", response_model=UserBase)
async def get_user(
    user_id: int,
    repo: PostgreSQLUserRepository = Depends(),
) -> JSONResponse:
    content = repo.get_user(user_id)
    return JSONResponse(status_code=status.HTTP_200_OK, content=content.model_dump())

@router.get("/", response_model=list[UserBase])
async def list_users(
    limit: int = 10,
    offset: int = 0,
    repo: PostgreSQLUserRepository = Depends(),
) -> JSONResponse:
    content = repo.list_users(limit, offset)
    return JSONResponse(status_code=status.HTTP_200_OK, content=[user.model_dump() for user in content])

@router.put("/{user_id}", response_model=UserUpdate)
async def update_user(
    user_id: int,
    payload: UserUpdate,
    repo: PostgreSQLUserRepository = Depends(),
) -> JSONResponse:
    repo.update_user(user_id, payload)
    return JSONResponse(status_code=status.HTTP_200_OK)

@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
    user_id: int,
    repo: PostgreSQLUserRepository = Depends(),
) -> JSONResponse:
    repo.delete_user(user_id)
    return JSONResponse(status_code=status.HTTP_204_NO_CONTENT)