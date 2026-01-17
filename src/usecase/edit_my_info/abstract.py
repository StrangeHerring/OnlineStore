from abc import ABC, abstractmethod

from api.v1.account.models import AccountUpdate


class AbstractEditMyInfoUseCase(ABC):
    @abstractmethod
    async def execute(self, token, schema: AccountUpdate):
        ...