from fastapi import APIRouter, Depends, status
from fastapi.security import HTTPBearer
from fastapi.responses import JSONResponse
from api.v1.account.models import AccountOut, AccountUpdate
from fastapi.security import HTTPBearer
from api.v1.security import auth_scheme
from fastapi.security.http import HTTPAuthorizationCredentials

from usecase.get_my_info.abstract import AbstractGetMyInfoUseCase
from usecase.edit_my_info.abstract import AbstractEditMyInfoUseCase
from usecase.remove_my_account.abstract import AbstractRemoveMyAccountUseCase

from .dependencies import get_my_info_use_case, edit_my_info_use_case, remove_my_account_use_case


router = APIRouter(tags=["Account"], prefix="/me")
auth_scheme = HTTPBearer()


@router.get("/", response_model=AccountOut)
async def get_account(
    token: HTTPAuthorizationCredentials = Depends(auth_scheme),
    usecase: AbstractGetMyInfoUseCase = Depends(get_my_info_use_case),
) -> AccountOut:
    content = await usecase.execute(token)
    return JSONResponse(status_code=status.HTTP_200_OK, content=content.model_dump())

@router.put("/", response_model=AccountOut)
async def edit_my_info(
    updated_user: AccountUpdate,
    token: HTTPAuthorizationCredentials = Depends(auth_scheme), 
    usecase: AbstractEditMyInfoUseCase = Depends(edit_my_info_use_case)):
    await usecase.execute(token, updated_user)
    return JSONResponse(status_code=status.HTTP_200_OK)


@router.delete("/")
async def remove_my_account(
    token: HTTPAuthorizationCredentials = Depends(auth_scheme), 
    usecase: AbstractRemoveMyAccountUseCase = Depends(remove_my_account_use_case)):
    await usecase.execute(token)
    return JSONResponse(status_code=status.HTTP_204_NO_CONTENT)
