from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from infrastructure.databases.postgresql.session import get_async_session
from infrastructure.di.injection import build_account_unit_of_work
from infrastructure.repositories.postgresql.account import PostgreSQLAccountUnitOfWork

from usecase.get_my_info.implementation import PostgreSQLGetMyInfoUseCase
from usecase.edit_my_info.implementation import PostgreSQLEditMyInfoUseCase
from usecase.remove_my_account.implementation import PostgreSQLRemoveMyAccountUseCase

def get_account_unit_of_work(
    session: AsyncSession = Depends(get_async_session),
) -> PostgreSQLAccountUnitOfWork:
    return build_account_unit_of_work(session)

def get_my_info_use_case(
    session: AsyncSession = Depends(get_async_session),
):
    uow = build_account_unit_of_work(session)
    return PostgreSQLGetMyInfoUseCase(uow=uow)

def edit_my_info_use_case(
    session: AsyncSession = Depends(get_async_session),
):
    uow = build_account_unit_of_work(session)
    return PostgreSQLEditMyInfoUseCase(uow=uow)

def remove_my_account_use_case(
    session: AsyncSession = Depends(get_async_session),
):
    uow = build_account_unit_of_work(session)
    return PostgreSQLRemoveMyAccountUseCase(uow=uow)