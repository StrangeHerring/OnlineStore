from sqlalchemy.ext.asyncio import AsyncSession

from container import Container
from infrastructure.repositories.postgresql.user import PostgreSQLUserUnitOfWork
from infrastructure.repositories.postgresql.product import PostgreSQLProductUnitOfWork
from infrastructure.repositories.postgresql.category import PostgreSQLCategoryUnitOfWork
from infrastructure.repositories.postgresql.cart import PostgreSQLCartUnitOfWork


def build_user_unit_of_work(
    session: AsyncSession,
) -> PostgreSQLUserUnitOfWork:
    return Container.user_uow_factory(session=session)

def build_product_unit_of_work(
    session: AsyncSession,
) -> PostgreSQLProductUnitOfWork:
    return Container.product_uow_factory(session=session)

def build_category_unit_of_work(
    session: AsyncSession,
) -> PostgreSQLCategoryUnitOfWork:
    return Container.category_uow_factory(session=session)

def build_cart_unit_of_work(
    session: AsyncSession,
) -> PostgreSQLCartUnitOfWork:
    return Container.cart_uow_factory(session=session)