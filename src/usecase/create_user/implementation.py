from api.v1.user.models import UserCreate
from .abstract import AbstractCreateUserUseCase


class PostgreSQLCreateUserUseCase(AbstractCreateUserUseCase):
    def __init__(self, uow):
        self._uow = uow

    async def execute(self, schema: UserCreate):
        async with self._uow as uow_:
            user = await uow_.repository.create_user(schema)

        return user