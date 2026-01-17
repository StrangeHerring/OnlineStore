from fastapi import status, APIRouter, Depends, Header
from fastapi.responses import JSONResponse
from fastapi.security import HTTPBearer
from fastapi.security.http import HTTPAuthorizationCredentials
from fastapi.security.oauth2 import OAuth2PasswordRequestForm

from infrastructure.repositories.postgresql.auth import PostgreSQLAuthRepository
from usecase.login.abstract import AbstractLoginUseCase
from usecase.signup.abstract import AbstractSignupUseCase
from usecase.refresh_token.abstract import AbstractRefreshTokenUseCase

from .dependencies import login_use_case, signup_use_case, refresh_token_use_case
from .models import UserBase, UserOut, Signup

router = APIRouter(tags=["Auth"], prefix="/auth")

@router.post("/login")
async def login(
        credentials: OAuth2PasswordRequestForm = Depends(),
        usecase: AbstractLoginUseCase = Depends(login_use_case),):
    auth = await usecase.execute(credentials)
    return JSONResponse(status_code=status.HTTP_200_OK, content=auth.model_dump())

@router.post("/signup", response_model=UserOut)
async def signup(payload: Signup, usecase: AbstractSignupUseCase = Depends(signup_use_case)):
    await usecase.execute(payload)
    return JSONResponse(status_code=status.HTTP_200_OK)

@router.post("/refresh")
async def refresh_access_token(
        refresh_token: str = Header(),
        usecase: AbstractRefreshTokenUseCase = Depends(refresh_token_use_case)):
    token = await usecase.execute(refresh_token)
    return JSONResponse(status_code=status.HTTP_200_OK, content=token.model_dump())