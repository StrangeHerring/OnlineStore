from .abstract import AbstractRefreshTokenUseCase


class PostgreSQLRefreshTokenUseCase(AbstractRefreshTokenUseCase):
    def __init__(self, uow):
        self._uow = uow

    async def execute(self, token):
        async with self._uow as uow_:
            refresh_token = await uow_.repository.get_refresh_token(token)

        return refresh_token