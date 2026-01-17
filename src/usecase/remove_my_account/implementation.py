from .abstract import AbstractRemoveMyAccountUseCase


class PostgreSQLRemoveMyAccountUseCase(AbstractRemoveMyAccountUseCase):
    def __init__(self, uow):
        self._uow = uow

    async def execute(self, token):
        async with self._uow as uow_:
            user = await uow_.repository.remove_my_account(token)

        return user