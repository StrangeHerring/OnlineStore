from api.v1.cart.models import CartCreate
from .abstract import AbstractCreateCartUseCase
from fastapi.security import HTTPAuthorizationCredentials


class PostgreSQLCreateCartUseCase(AbstractCreateCartUseCase):
    def __init__(self, uow):
        self._uow = uow

    async def execute(self, schema: CartCreate, credentials: HTTPAuthorizationCredentials):
        async with self._uow as uow_:
            cart = await uow_.repository.create_cart(credentials, schema)

        return cart