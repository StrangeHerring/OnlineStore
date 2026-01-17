from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from infrastructure.databases.postgresql.session import get_async_session
from infrastructure.di.injection import build_auth_unit_of_work
from infrastructure.repositories.postgresql.auth import PostgreSQLAuthUnitOfWork

from usecase.login.implementation import PostgreSQLLoginUseCase
from usecase.signup.implementation import PostgreSQLSignupUseCase
from usecase.refresh_token.implementation import PostgreSQLRefreshTokenUseCase

def get_auth_unit_of_work(
    session: AsyncSession = Depends(get_async_session),
) -> PostgreSQLAuthUnitOfWork:
    return build_auth_unit_of_work(session)


def login_use_case(
    session: AsyncSession = Depends(get_async_session),
):
    uow = build_auth_unit_of_work(session)
    return PostgreSQLLoginUseCase(uow=uow)

def signup_use_case(
    session: AsyncSession = Depends(get_async_session),
):
    uow = build_auth_unit_of_work(session)
    return PostgreSQLSignupUseCase(uow=uow)

def refresh_token_use_case(
    session: AsyncSession = Depends(get_async_session),
):
    uow = build_auth_unit_of_work(session)
    return PostgreSQLRefreshTokenUseCase(uow=uow)