from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from infrastructure.databases.postgresql.session import get_async_session
from infrastructure.di.injection import build_cart_unit_of_work
from infrastructure.repositories.postgresql.cart import PostgreSQLCartUnitOfWork

from usecase.create_cart.implementation import PostgreSQLCreateCartUseCase

def get_cart_unit_of_work(
    session: AsyncSession = Depends(get_async_session),
) -> PostgreSQLCartUnitOfWork:
    return build_cart_unit_of_work(session)


def create_cart_use_case(
    session: AsyncSession = Depends(get_async_session),
):
    uow = build_cart_unit_of_work(session)
    return PostgreSQLCreateCartUseCase(uow=uow)