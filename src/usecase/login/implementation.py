from .abstract import AbstractLoginUseCase
from fastapi.security import OAuth2PasswordRequestForm


class PostgreSQLLoginUseCase(AbstractLoginUseCase):
    def __init__(self, uow):
        self._uow = uow

    async def execute(self, credentials: OAuth2PasswordRequestForm):
        async with self._uow as uow_:
            auth = await uow_.repository.login(credentials)

        return auth