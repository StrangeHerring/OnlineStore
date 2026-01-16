from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from infrastructure.databases.postgresql.session import get_async_session
from infrastructure.di.injection import build_product_unit_of_work
from infrastructure.repositories.postgresql.product import PostgreSQLProductUnitOfWork

from usecase.create_product.implementation import PostgreSQLCreateProductUseCase

def get_product_unit_of_work(
    session: AsyncSession = Depends(get_async_session),
) -> PostgreSQLProductUnitOfWork:
    return build_product_unit_of_work(session)


def create_product_use_case(
    session: AsyncSession = Depends(get_async_session),
):
    uow = build_product_unit_of_work(session)
    return PostgreSQLCreateProductUseCase(uow=uow)