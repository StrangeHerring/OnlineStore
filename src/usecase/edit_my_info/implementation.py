from .abstract import AbstractEditMyInfoUseCase

from api.v1.account.models import AccountUpdate


class PostgreSQLEditMyInfoUseCase(AbstractEditMyInfoUseCase):
    def __init__(self, uow):
        self._uow = uow

    async def execute(self, token, schema: AccountUpdate):
        async with self._uow as uow_:
            user = await uow_.repository.edit_my_info(token, schema)

        return user