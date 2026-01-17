from api.v1.auth.models import Signup
from .abstract import AbstractSignupUseCase


class PostgreSQLSignupUseCase(AbstractSignupUseCase):
    def __init__(self, uow):
        self._uow = uow

    async def execute(self, schema: Signup):
        async with self._uow as uow_:
            auth = await uow_.repository.signup(schema)

        return auth