from .abstract import AbstractGetMyInfoUseCase


class PostgreSQLGetMyInfoUseCase(AbstractGetMyInfoUseCase):
    def __init__(self, uow):
        self._uow = uow

    async def execute(self, token):
        async with self._uow as uow_:
            user = await uow_.repository.get_my_info(token)

        return user