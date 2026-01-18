from dependency_injector.containers import DeclarativeContainer
from dependency_injector.providers import Singleton, Factory

from infrastructure.databases.postgresql.session_manager import DatabaseSessionManager
from infrastructure.repositories.postgresql.user import PostgreSQLUserUnitOfWork
from infrastructure.repositories.postgresql.product import PostgreSQLProductUnitOfWork
from infrastructure.repositories.postgresql.category import PostgreSQLCategoryUnitOfWork
from infrastructure.repositories.postgresql.cart import PostgreSQLCartUnitOfWork
from infrastructure.repositories.postgresql.auth import PostgreSQLAuthUnitOfWork
from infrastructure.repositories.postgresql.account import PostgreSQLAccountUnitOfWork



class Container(DeclarativeContainer):
    session_manager = Singleton(DatabaseSessionManager)

    user_uow_factory = Factory(PostgreSQLUserUnitOfWork)
    product_uow_factory = Factory(PostgreSQLProductUnitOfWork)
    category_uow_factory = Factory(PostgreSQLCategoryUnitOfWork)
    cart_uow_factory = Factory(PostgreSQLCartUnitOfWork)
    auth_uow_factory = Factory(PostgreSQLAuthUnitOfWork)
    account_uow_factory = Factory(PostgreSQLAccountUnitOfWork)